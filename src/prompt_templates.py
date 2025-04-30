"""
This module contains prompt templates for the Teacher Assistant Bot.
These templates structure the way queries are sent to the LLM to ensure consistent,
high-quality responses focused on educational assistance.
"""

from typing import List, Dict, Any, Optional

class PromptTemplates:
    """Contains templates for generating prompts for the LLM."""
    
    @staticmethod
    def get_system_prompt() -> str:
        """
        Returns the system prompt that defines the bot's persona and capabilities.
        
        Returns:
            str: The system prompt text
        """
        return """You are a helpful AI teaching assistant designed to support educators.
Your primary goals are to:
1. Help teachers analyze classroom situations
2. Identify potential emotional states of students based on descriptions
3. Provide evidence-based teaching strategies and recommendations
4. Offer practical, actionable advice that can be implemented in real classrooms

Respond in a supportive, professional tone. Focus on practical solutions rather than theoretical explanations.
Base your recommendations on established educational research and best practices.
When appropriate, organize your responses with bullet points for clarity.
Always consider the emotional needs of students and teachers in your responses."""

    @staticmethod
    def get_image_system_prompt() -> str:
        """
        Returns the system prompt for image analysis capabilities.
        
        Returns:
            str: The image analysis system prompt text
        """
        return """You are a helpful AI teaching assistant with image analysis capabilities designed to support educators.
Your primary goals are to:
1. Analyze classroom images to provide useful insights
2. Assess student work samples with constructive feedback
3. Evaluate classroom setups and learning environments
4. Provide evidence-based teaching strategies based on visual information

Respond in a supportive, professional tone. Focus on practical solutions rather than theoretical explanations.
Base your recommendations on established educational research and best practices.
When appropriate, organize your responses with bullet points for clarity.
Always consider the context and purpose of the shared image in your analysis."""

    @staticmethod
    def format_teaching_prompt(
        user_input: str, 
        detected_emotions: List[tuple],
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Formats a teaching-related prompt with emotion context for the LLM.
        
        Args:
            user_input (str): The teacher's query or description
            detected_emotions (List[tuple]): List of (emotion, score) tuples from emotion detection
            conversation_history (List[Dict]): Previous messages in the conversation
            
        Returns:
            str: Formatted prompt for the LLM
        """
        # Format emotion information
        emotion_context = ""
        if detected_emotions:
            relevant_emotions = [
                f"{emotion} ({score:.0%})"
                for emotion, score in detected_emotions
                if score > 0.1
            ]
            if relevant_emotions:
                emotion_context = f"Based on my analysis, these emotions may be present: {', '.join(relevant_emotions)}.\n\n"
        
        # Format conversation history if provided
        history_text = ""
        if conversation_history:
            history_text = "Conversation history:\n"
            for msg in conversation_history:
                role = "Teacher" if msg["role"] == "user" else "Assistant"
                history_text += f"{role}: {msg['content']}\n"
            history_text += "\n"
        
        # Build the complete prompt
        prompt = f"""{history_text}Teacher's situation: {user_input}

{emotion_context}Provide specific, actionable teaching strategies to address this situation. 
Focus on practical advice that can be implemented in a classroom setting.
Format your response in a clear, concise manner using bullet points where appropriate.
"""
        return prompt

    @staticmethod
    def format_emotion_analysis_prompt(user_input: str, detected_emotions: List[tuple]) -> str:
        """
        Creates a prompt specifically for analyzing student emotions from a teacher's description.
        
        Args:
            user_input (str): The teacher's description of student behavior
            detected_emotions (List[tuple]): List of (emotion, score) tuples from emotion detection
            
        Returns:
            str: Formatted prompt for emotion analysis
        """
        # Format emotion information
        emotion_context = ""
        if detected_emotions:
            relevant_emotions = [
                f"{emotion} ({score:.0%})"
                for emotion, score in detected_emotions
                if score > 0.1
            ]
            if relevant_emotions:
                emotion_context = f"Initial emotion analysis detected: {', '.join(relevant_emotions)}.\n\n"
        
        prompt = f"""Teacher's description: {user_input}

{emotion_context}Based on this description, analyze what emotions the students might be experiencing.
Consider both explicit emotional cues and implicit indicators in the teacher's description.
Explain how these emotions might be affecting student learning and engagement.
Suggest approaches for addressing these emotional needs in an educational context.
"""
        return prompt
        
    @staticmethod
    def format_general_image_analysis_prompt(user_input: str, image_present: bool) -> str:
        """
        Creates a prompt for general image analysis of classroom-related content.
        
        Args:
            user_input (str): The teacher's query or description
            image_present (bool): Whether an image is included with the prompt
            
        Returns:
            str: Formatted prompt for image analysis
        """
        if not image_present:
            return user_input
            
        prompt = f"""Teacher's request: {user_input}

Analyze the uploaded image providing the following:
1. A brief description of what you see in the image
2. Key educational elements or materials visible
3. Specific insights relevant to a classroom context
4. Practical advice or suggestions based on the visual information

Focus on providing actionable, evidence-based teaching recommendations related to what's visible in the image.
"""
        return prompt
        
    @staticmethod
    def format_student_work_analysis_prompt(user_input: str, image_present: bool) -> str:
        """
        Creates a prompt specifically for analyzing student work samples from images.
        
        Args:
            user_input (str): The teacher's query or description
            image_present (bool): Whether an image is included with the prompt
            
        Returns:
            str: Formatted prompt for student work analysis
        """
        if not image_present:
            return user_input
            
        prompt = f"""Teacher's request about student work: {user_input}

Analyze the uploaded student work sample providing the following:
1. Strengths demonstrated in this work (2-3 specific points)
2. Areas for growth or improvement (1-2 specific points)
3. Next steps for instruction based on this sample
4. Specific feedback that could be shared with the student

Consider developmental appropriateness and focus on growth-oriented, constructive feedback.
Be specific in your analysis, referencing particular elements visible in the work sample.
"""
        return prompt
        
    @staticmethod
    def format_classroom_setup_analysis_prompt(user_input: str, image_present: bool) -> str:
        """
        Creates a prompt specifically for analyzing classroom setup and learning environments.
        
        Args:
            user_input (str): The teacher's query or description
            image_present (bool): Whether an image is included with the prompt
            
        Returns:
            str: Formatted prompt for classroom environment analysis
        """
        if not image_present:
            return user_input
            
        prompt = f"""Teacher's request about classroom setup: {user_input}

Analyze the uploaded classroom environment providing the following:
1. Strengths of the current setup (3-4 positive aspects)
2. Potential enhancement opportunities (2-3 evidence-based suggestions)
3. Organization and flow considerations
4. How this environment might impact different types of learners

Consider factors such as:
- Seating arrangements and traffic flow
- Display of materials and student work
- Organization of teaching resources
- Lighting, color, and atmosphere
- Accessibility and inclusivity features

Provide practical, actionable recommendations that are feasible to implement.
"""
        return prompt 