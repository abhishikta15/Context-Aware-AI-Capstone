from transformers import pipeline
import torch
from typing import Dict, List, Tuple

class EmotionDetector:
    def __init__(self):
        """Initialize the emotion detection model."""
        self.model_name = "j-hartmann/emotion-english-distilroberta-base"
        try:
            self.classifier = pipeline(
                "text-classification",
                model=self.model_name,
                top_k=None
            )
        except Exception as e:
            print(f"Error loading emotion model: {e}")
            self.classifier = None

        # Mapping of emotions to teaching-relevant terms
        self.emotion_mapping = {
            'joy': 'engaged and enthusiastic',
            'sadness': 'discouraged or unmotivated',
            'anger': 'frustrated or challenged',
            'fear': 'anxious or uncertain',
            'surprise': 'curious or confused',
            'neutral': 'attentive or composed',
            'disgust': 'disengaged or resistant'
        }

    def detect_emotions(self, text: str) -> List[Tuple[str, float]]:
        """
        Detect emotions in the given text.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            List[Tuple[str, float]]: List of (emotion, score) tuples
        """
        if not self.classifier:
            return [("neutral", 1.0)]
        
        try:
            results = self.classifier(text)[0]
            # Sort by score in descending order
            emotions = [(item['label'], item['score']) for item in results]
            emotions.sort(key=lambda x: x[1], reverse=True)
            return emotions
        except Exception as e:
            print(f"Error detecting emotions: {e}")
            return [("neutral", 1.0)]

    def get_teaching_interpretation(self, emotions: List[Tuple[str, float]], threshold: float = 0.2) -> str:
        """
        Convert emotion detection results into teaching-relevant interpretations.
        
        Args:
            emotions (List[Tuple[str, float]]): List of (emotion, score) tuples
            threshold (float): Minimum score to consider an emotion relevant
            
        Returns:
            str: Teaching-relevant interpretation of the emotions
        """
        relevant_emotions = [
            (self.emotion_mapping.get(emotion, emotion), score)
            for emotion, score in emotions
            if score >= threshold
        ]
        
        if not relevant_emotions:
            return "The response appears neutral or unclear in emotional content."
        
        # Create a natural language interpretation
        if len(relevant_emotions) == 1:
            emotion, score = relevant_emotions[0]
            return f"The response primarily indicates a student who is {emotion}."
        else:
            emotion_str = ", ".join([
                f"{emotion} ({score:.0%})"
                for emotion, score in relevant_emotions[:-1]
            ])
            last_emotion, last_score = relevant_emotions[-1]
            return f"The response shows a mix of emotions: {emotion_str}, and {last_emotion} ({last_score:.0%})." 