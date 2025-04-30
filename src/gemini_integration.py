"""
Gemini API integration for TeaBot.
This module provides a wrapper for Google's Gemini API to serve as an alternative to local LLM models.
Includes support for both text and image inputs.
"""

import os
import base64
import requests
import time
import random
from typing import List, Dict, Any, Optional, Union, BinaryIO
from src.prompt_templates import PromptTemplates

class GeminiGenerator:
    """
    A response generator that uses Google's Gemini API to generate responses.
    Supports text and image inputs.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini API client.
        
        Args:
            api_key (str, optional): The Gemini API key. If not provided, will try to load from environment variables.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = None
        self.genai = None
        self.model_name = "gemini-2.0-flash"  # Default model, can be updated
        self.is_available = False
        self.supports_image = False
        self.max_retries = 3
        self.base_retry_delay = 2  # Base delay in seconds
        
        try:
            from google import genai
            self.genai = genai
            if self.api_key:
                self.client = genai.Client(api_key=self.api_key)
                self.is_available = True
                # Check if model supports image input - 2.0-flash, 2.0-pro, and 1.5-flash/pro all support images
                self.supports_image = "-flash" in self.model_name or "-pro" in self.model_name
                print(f"Successfully initialized Gemini API with model: {self.model_name}")
            else:
                print("No Gemini API key provided. Please set the API key to use this feature.")
        except ImportError:
            print("Google GenAI package not found. Install it with: pip install google-genai")
    
    def set_api_key(self, api_key: str) -> bool:
        """
        Set or update the Gemini API key.
        
        Args:
            api_key (str): The Gemini API key
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.genai:
                from google import genai
                self.genai = genai
            
            self.api_key = api_key
            self.client = self.genai.Client(api_key=api_key)
            self.is_available = True
            self.supports_image = "-flash" in self.model_name or "-pro" in self.model_name
            print(f"Successfully set Gemini API key")
            return True
        except ImportError:
            print("Google GenAI package not found. Install it with: pip install google-genai")
            return False
        except Exception as e:
            print(f"Error setting Gemini API key: {e}")
            self.is_available = False
            return False
    
    def set_model(self, model_name: str) -> bool:
        """
        Set the Gemini model to use.
        
        Args:
            model_name (str): Name of the Gemini model (e.g., "gemini-2.0-flash", "gemini-2.0-pro")
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_available or not self.client:
            print("Gemini API not initialized. Set API key first.")
            return False
            
        try:
            self.model_name = model_name
            # Check if model supports image input
            self.supports_image = "-flash" in model_name or "-pro" in model_name
            print(f"Set Gemini model to: {model_name}")
            print(f"Image support: {'Enabled' if self.supports_image else 'Disabled'}")
            return True
        except Exception as e:
            print(f"Error setting Gemini model: {e}")
            return False
    
    def _execute_with_retry(self, func, *args, **kwargs):
        """
        Execute a function with retry logic for handling API overloads.
        
        Args:
            func: Function to execute
            args: Positional arguments to pass to the function
            kwargs: Keyword arguments to pass to the function
            
        Returns:
            The result of the function call
        
        Raises:
            Exception: If all retries fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                error_message = str(e).lower()
                
                # Check if this is a retryable error
                if any(x in error_message for x in ["overloaded", "unavailable", "503", "429", "quota"]):
                    # Calculate exponential backoff with jitter
                    delay = self.base_retry_delay * (2 ** attempt) + random.uniform(0, 1)
                    print(f"API overloaded, retrying in {delay:.2f} seconds (attempt {attempt+1}/{self.max_retries})")
                    time.sleep(delay)
                else:
                    # Non-retryable error
                    raise e
        
        # If we get here, all retries failed
        error_msg = f"Failed after {self.max_retries} attempts. Last error: {str(last_exception)}"
        print(error_msg)
        return f"I apologize, but I'm having trouble connecting to the Gemini API. The service appears to be overloaded at the moment. Please try again in a few minutes. Error details: {str(last_exception)}"
    
    def generate_response(
        self,
        prompt: str,
        emotions: List[tuple],
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        image_data: Optional[bytes] = None,
        image_mime_type: Optional[str] = None,
        max_tokens: int = 512
    ) -> str:
        """
        Generate a response using the Gemini API.
        
        Args:
            prompt (str): The input prompt
            emotions (List[tuple]): List of (emotion, score) tuples from emotion detection
            conversation_history (List[Dict]): Previous messages in the conversation
            image_data (bytes, optional): Image data if providing an image input
            image_mime_type (str, optional): MIME type of the image (e.g., 'image/jpeg')
            max_tokens (int): Maximum number of tokens to generate (may not be directly supported by Gemini)
            
        Returns:
            str: Generated response
        """
        if not self.is_available or not self.client:
            print("Gemini API not initialized. Cannot generate response.")
            return "I'm unable to generate a response because the Gemini API is not configured. Please set an API key."
        
        try:
            # Format the prompt using templates
            formatted_prompt = PromptTemplates.format_teaching_prompt(
                user_input=prompt,
                detected_emotions=emotions,
                conversation_history=conversation_history
            )
            
            # Check if image is provided and model supports images
            if image_data and self.supports_image:
                # Create content list with image and text
                try:
                    from google.genai import types
                    
                    # Create image part from bytes
                    image_part = types.Part.from_bytes(
                        data=image_data,
                        mime_type=image_mime_type or "image/jpeg"
                    )
                    
                    # Generate content using Gemini API with image using retry mechanism
                    def generate_content_with_image():
                        return self.client.models.generate_content(
                            model=self.model_name,
                            contents=[image_part, formatted_prompt]
                        )
                    
                    response = self._execute_with_retry(generate_content_with_image)
                except Exception as e:
                    print(f"Error processing image: {e}")
                    # Fall back to text-only
                    def generate_text_only():
                        return self.client.models.generate_content(
                            model=self.model_name, 
                            contents=formatted_prompt
                        )
                    
                    response = self._execute_with_retry(generate_text_only)
            else:
                # Generate text-only content using retry mechanism
                def generate_text_only():
                    return self.client.models.generate_content(
                        model=self.model_name, 
                        contents=formatted_prompt
                    )
                
                response = self._execute_with_retry(generate_text_only)
            
            # Check if response is a string (error message from retry mechanism)
            if isinstance(response, str):
                return response
            
            # Extract the response text
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates') and response.candidates:
                return response.candidates[0].content.parts[0].text
            else:
                return "I received your question but had trouble generating a response. Please try again."
                
        except Exception as e:
            print(f"Error generating response with Gemini API: {e}")
            return f"I encountered an error while generating a response: {str(e)}"
            
    def upload_image_file(self, file_path: str) -> Optional[Any]:
        """
        Upload an image file to Gemini API for later use.
        
        Args:
            file_path (str): Path to the image file
            
        Returns:
            Any: File reference object from Gemini API or None if failed
        """
        if not self.is_available or not self.client:
            print("Gemini API not initialized. Cannot upload file.")
            return None
        
        if not self.supports_image:
            print(f"Current model ({self.model_name}) does not support images.")
            return None
            
        try:
            # Upload file using Files API with retry
            def upload_file():
                return self.client.files.upload(file=file_path)
                
            uploaded_file = self._execute_with_retry(upload_file)
            
            if isinstance(uploaded_file, str):  # Error message from retry
                print(uploaded_file)
                return None
                
            print(f"Successfully uploaded file: {os.path.basename(file_path)}")
            return uploaded_file
        except Exception as e:
            print(f"Error uploading image file: {e}")
            return None
    
    def detect_objects_in_image(
        self, 
        image_data: bytes, 
        image_mime_type: str = "image/jpeg"
    ) -> str:
        """
        Detect objects in an image and return bounding box information.
        Uses NLP patterns to describe relationships between objects.
        
        Args:
            image_data (bytes): Image data
            image_mime_type (str): MIME type of the image
            
        Returns:
            str: Generated object detection response with bounding boxes
        """
        if not self.is_available or not self.client:
            return "Gemini API not initialized. Cannot analyze image."
            
        if not self.supports_image:
            return f"Current model ({self.model_name}) does not support images."
            
        try:
            from google.genai import types
            
            # Create object detection prompt with NLP emphasis
            prompt = """
            Detect all prominent objects in this classroom scene.
            For each object detected:
            1. Provide a label that's relevant to education
            2. Include bounding box coordinates [ymin, xmin, ymax, xmax] normalized to 0-1000
            3. Describe how this object relates to the learning process using sensory-based language (visual, auditory, kinesthetic)
            4. Suggest how teachers can use this object to anchor positive learning states
            
            Format the response as a clear list with sensory-rich descriptions.
            """
            
            # Create image part
            image_part = types.Part.from_bytes(
                data=image_data,
                mime_type=image_mime_type
            )
            
            # Generate content with retry
            def generate_object_detection():
                return self.client.models.generate_content(
                    model=self.model_name,
                    contents=[image_part, prompt]
                )
            
            response = self._execute_with_retry(generate_object_detection)
            
            # Check if response is a string (error message from retry mechanism)
            if isinstance(response, str):
                return response
            
            # Return the object detection results
            if hasattr(response, 'text'):
                return response.text
            else:
                return "I couldn't analyze the image properly. Please try again with a clearer image."
                
        except Exception as e:
            print(f"Error detecting objects in image: {e}")
            return f"I encountered an error while analyzing the image: {str(e)}"
    
    def analyze_student_work(
        self, 
        image_data: bytes, 
        grade_level: str,
        subject: str,
        image_mime_type: str = "image/jpeg"
    ) -> str:
        """
        Analyze student work from an image and provide educational feedback
        with NLP patterns for positive reframing and sensory-based language.
        
        Args:
            image_data (bytes): Image data of student work
            grade_level (str): Grade level of the student (e.g., "3rd grade")
            subject (str): Subject of the work (e.g., "math", "writing")
            image_mime_type (str): MIME type of the image
            
        Returns:
            str: Generated analysis and feedback
        """
        if not self.is_available or not self.client:
            return "Gemini API not initialized. Cannot analyze image."
            
        if not self.supports_image:
            return f"Current model ({self.model_name}) does not support images."
            
        try:
            from google.genai import types
            
            # Create student work analysis prompt with NLP focus
            prompt = f"""
            This is a sample of student work from a {grade_level} student in {subject}.
            
            Please analyze this work using a neuro-linguistic approach:
            
            1. POSITIVE FRAMING:
               - Identify 3 specific strengths using "I notice..." statements
               - Use present tense, positive language that anchors success
            
            2. SENSORY-RICH FEEDBACK:
               - Visual: What do you see that shows understanding?
               - Auditory: How might the student describe their thinking?
               - Kinesthetic: What process or approach did the student use?
            
            3. FUTURE PACING:
               - Suggest 2-3 specific next steps using "When you..." language
               - Create a connection between current work and future success
            
            4. REFRAMING CHALLENGES:
               - Transform any errors into learning opportunities
               - Use "You're in the process of..." rather than corrective language
            
            Be specific, supportive, and use language patterns that build confidence and capability.
            Focus on the student's developmental journey rather than just assessment.
            """
            
            # Create image part
            image_part = types.Part.from_bytes(
                data=image_data,
                mime_type=image_mime_type
            )
            
            # Generate content with retry
            def generate_student_work_analysis():
                return self.client.models.generate_content(
                    model=self.model_name,
                    contents=[image_part, prompt]
                )
            
            response = self._execute_with_retry(generate_student_work_analysis)
            
            # Check if response is a string (error message from retry mechanism)
            if isinstance(response, str):
                return response
            
            # Return the analysis results
            if hasattr(response, 'text'):
                return response.text
            else:
                return "I couldn't analyze the student work properly. Please try again with a clearer image."
                
        except Exception as e:
            print(f"Error analyzing student work: {e}")
            return f"I encountered an error while analyzing the student work: {str(e)}"
    
    def analyze_classroom_setup(
        self, 
        image_data: bytes, 
        image_mime_type: str = "image/jpeg"
    ) -> str:
        """
        Analyze classroom setup from an image and provide recommendations
        with NLP patterning for spatial anchoring and state management.
        
        Args:
            image_data (bytes): Image data of classroom setup
            image_mime_type (str): MIME type of the image
            
        Returns:
            str: Generated analysis and recommendations
        """
        if not self.is_available or not self.client:
            return "Gemini API not initialized. Cannot analyze image."
            
        if not self.supports_image:
            return f"Current model ({self.model_name}) does not support images."
            
        try:
            from google.genai import types
            
            # Create classroom setup analysis prompt with NLP emphasis
            prompt = """
            This is an image of a classroom setup.
            
            Please analyze this learning environment using neuro-linguistic principles:
            
            1. SPATIAL ANCHORING:
               - Identify 3-4 locations that can anchor specific learning states
               - Describe how each space could be associated with particular emotions or activities
               - Suggest how to enhance these anchors through sensory elements
            
            2. REPRESENTATIONAL SYSTEMS:
               - Visual elements: How the space appeals to visual learners
               - Auditory elements: Sound considerations and verbal learning opportunities
               - Kinesthetic elements: Movement possibilities and tactile experiences
            
            3. STATE MANAGEMENT:
               - How the environment supports different emotional/learning states
               - Transitions between high-energy and focused attention states
               - Elements that provide safety, curiosity, and engagement
            
            4. LANGUAGE PATTERNS:
               - Suggest specific language/signage to reinforce positive states
               - Frame recommendations using presuppositions of success
               - Include "as you..." and "when you..." language patterns
            
            Frame your analysis as constructive possibilities that empower the teacher rather than criticisms.
            Focus on small changes that can create significant state shifts for optimal learning.
            """
            
            # Create image part
            image_part = types.Part.from_bytes(
                data=image_data,
                mime_type=image_mime_type
            )
            
            # Generate content with retry
            def generate_classroom_analysis():
                return self.client.models.generate_content(
                    model=self.model_name,
                    contents=[image_part, prompt]
                )
            
            response = self._execute_with_retry(generate_classroom_analysis)
            
            # Check if response is a string (error message from retry mechanism)
            if isinstance(response, str):
                return response
            
            # Return the analysis results
            if hasattr(response, 'text'):
                return response.text
            else:
                return "I couldn't analyze the classroom setup properly. Please try again with a clearer image."
                
        except Exception as e:
            print(f"Error analyzing classroom setup: {e}")
            return f"I encountered an error while analyzing the classroom setup: {str(e)}" 