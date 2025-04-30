import json
import os
from typing import Optional, Dict, List, Any
import sys
import importlib.util

# Try to import PromptTemplates, but handle the case where it might not exist yet
try:
    from src.prompt_templates import PromptTemplates
except ImportError:
    # This will be created when the application runs
    PromptTemplates = None

class ResponseGenerator:
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the response generator with an optional LLM model.
        
        Args:
            model_path (str, optional): Path to the GGML/GGUF model file
        """
        self.llm = None
        self.model_path = model_path
        self.fallback_responses = self._load_fallback_responses()
        
        # Check if llama_cpp is available in the environment
        self.llama_cpp_available = importlib.util.find_spec("llama_cpp") is not None
        
        if not self.llama_cpp_available:
            print("llama-cpp-python is not installed. Running in fallback mode only.")
            return
            
        # Check if model path is provided and try to load the model
        if model_path and os.path.exists(model_path):
            self.set_model(model_path)
        else:
            print("Model not found. Using fallback mode: LLM features are disabled")

    def _load_fallback_responses(self) -> Dict:
        """Load fallback responses from JSON file."""
        try:
            with open("data/fallback_responses.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default fallback responses if file doesn't exist
            default_responses = {
                "engagement": [
                    "Try incorporating interactive activities like think-pair-share or group discussions to boost engagement.",
                    "Use real-world examples and connections to make the content more relevant and interesting.",
                    "Implement gamification elements or educational games to make learning more fun.",
                    "Break the lesson into smaller, manageable chunks with frequent check-ins.",
                    "Use multimedia resources like videos, images, or interactive simulations."
                ],
                "confusion": [
                    "Review prerequisite concepts and provide clear connections to prior knowledge.",
                    "Use visual aids, diagrams, or concept maps to explain complex topics.",
                    "Encourage students to ask questions and create a safe space for clarification.",
                    "Provide step-by-step explanations and worked examples.",
                    "Implement frequent formative assessments to identify misconceptions early."
                ],
                "frustration": [
                    "Break down complex tasks into smaller, manageable steps.",
                    "Offer additional support resources and scaffolding materials.",
                    "Provide positive reinforcement and celebrate small victories.",
                    "Create opportunities for peer support and collaborative learning.",
                    "Allow flexible deadlines or alternative assessment methods when appropriate."
                ],
                "anxiety": [
                    "Create a supportive and non-judgmental learning environment.",
                    "Teach stress management and test-taking strategies.",
                    "Provide clear expectations and rubrics for assignments.",
                    "Offer practice opportunities and mock assessments.",
                    "Consider alternative assessment formats that reduce pressure."
                ],
                "default": [
                    "Maintain clear and open communication with students about their needs.",
                    "Create a supportive and inclusive learning environment.",
                    "Use diverse teaching methods to accommodate different learning styles.",
                    "Regularly collect student feedback to adjust teaching strategies.",
                    "Focus on building positive relationships with students."
                ]
            }
            os.makedirs("data", exist_ok=True)
            with open("data/fallback_responses.json", "w") as f:
                json.dump(default_responses, f, indent=2)
            return default_responses

    def generate_response(
        self,
        prompt: str,
        emotions: List[tuple],
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        max_tokens: int = 512
    ) -> str:
        """
        Generate a response using either the LLM or fallback responses.
        
        Args:
            prompt (str): The input prompt
            emotions (List[tuple]): List of (emotion, score) tuples
            conversation_history (List[Dict]): Previous messages in the conversation
            max_tokens (int): Maximum number of tokens to generate
            
        Returns:
            str: Generated response
        """
        if self.llm and self.llama_cpp_available and PromptTemplates:
            try:
                # Format the prompt using templates
                formatted_prompt = PromptTemplates.format_teaching_prompt(
                    user_input=prompt,
                    detected_emotions=emotions,
                    conversation_history=conversation_history
                )
                
                # Generate response using the LLM
                completion = self.llm(
                    formatted_prompt,
                    max_tokens=max_tokens,
                    stop=["Teacher:", "\n\n"],
                    echo=False
                )
                
                # Extract and clean the response
                if isinstance(completion, dict) and "choices" in completion:
                    response = completion["choices"][0]["text"].strip()
                else:
                    response = completion.strip()
                
                return response
            except Exception as e:
                print(f"Error generating LLM response: {e}")
                # Fall back to static responses if LLM fails
                return self._get_fallback_response(emotions)
        else:
            # Use fallback responses if no LLM is available
            return self._get_fallback_response(emotions)

    def _get_fallback_response(self, emotions: List[tuple]) -> str:
        """
        Get a fallback response based on detected emotions.
        
        Args:
            emotions (List[tuple]): Detected emotions
            
        Returns:
            str: Fallback response
        """
        if not emotions:
            category = "default"
        else:
            # Map the primary emotion to a response category
            emotion_map = {
                "joy": "engagement",
                "surprise": "confusion",
                "anger": "frustration",
                "fear": "anxiety",
                "sadness": "frustration",
                "disgust": "engagement",
                "neutral": "default"
            }
            category = emotion_map.get(emotions[0][0], "default")
        
        responses = self.fallback_responses.get(category, self.fallback_responses["default"])
        return responses[hash(str(emotions)) % len(responses)]

    def set_model(self, model_path: str) -> bool:
        """
        Set or update the LLM model.
        
        Args:
            model_path (str): Path to the model file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.llama_cpp_available:
            print("llama-cpp-python is not installed. Running in fallback mode only.")
            return False
            
        try:
            # Import llama_cpp
            from llama_cpp import Llama
            
            # Verify model file exists
            if not os.path.exists(model_path):
                print(f"Model file not found at {model_path}")
                return False
            
            # Load the model
            self.llm = Llama(
                model_path=model_path,
                n_ctx=2048,            # Context window size
                n_parts=-1,            # Number of parts to split the model into (-1 means auto)
                seed=-1,               # Random seed (-1 means random)
                f16_kv=True,           # Use half-precision for key/value cache
                logits_all=False,      # Return logits for all tokens, not just the last token
                vocab_only=False,      # Only load the vocabulary, no weights
                use_mlock=False,       # Use mlock to keep model in memory
                embedding=False        # Return embeddings (not needed for chat)
            )
            
            self.model_path = model_path
            print(f"Successfully loaded model from {model_path}")
            return True
            
        except ImportError:
            print("llama-cpp-python is not installed. Install it with: pip install llama-cpp-python --prefer-binary")
            self.llama_cpp_available = False
            return False
        except Exception as e:
            print(f"Error loading model: {e}")
            self.llm = None
            return False 