"""
Utility functions for the Teacher Assistant Bot application.
"""

import os
import json
import re
import io
import base64
from typing import Dict, List, Optional, Any, Tuple, Union
from PIL import Image

def clean_text(text: str) -> str:
    """
    Clean text input by removing extra whitespace and normalizing.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

def save_conversation_history(conversation: List[Dict[str, Any]], filepath: str) -> bool:
    """
    Save conversation history to a file.
    
    Args:
        conversation (List[Dict]): List of conversation messages
        filepath (str): Path to save the conversation
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving conversation: {e}")
        return False
        
def load_conversation_history(filepath: str) -> List[Dict[str, Any]]:
    """
    Load conversation history from a file.
    
    Args:
        filepath (str): Path to the conversation file
        
    Returns:
        List[Dict]: List of conversation messages
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading conversation: {e}")
        return []

def get_model_info(model_path: str) -> Dict[str, Any]:
    """
    Get information about a model file.
    
    Args:
        model_path (str): Path to the model file
        
    Returns:
        Dict: Model information including size, type, etc.
    """
    if not os.path.exists(model_path):
        return {"error": "Model not found"}
    
    try:
        size_bytes = os.path.getsize(model_path)
        size_mb = size_bytes / (1024 * 1024)
        
        model_info = {
            "filename": os.path.basename(model_path),
            "path": model_path,
            "size_bytes": size_bytes,
            "size_mb": round(size_mb, 2),
            "last_modified": os.path.getmtime(model_path)
        }
        
        # Try to determine model type from filename
        filename = os.path.basename(model_path).lower()
        if "llama" in filename:
            model_info["model_family"] = "LLaMA"
        elif "alpaca" in filename:
            model_info["model_family"] = "Alpaca"
        elif "mistral" in filename:
            model_info["model_family"] = "Mistral"
        elif "vicuna" in filename:
            model_info["model_family"] = "Vicuna"
        else:
            model_info["model_family"] = "Unknown"
            
        # Extract quantization info if available
        quant_patterns = ["q4_0", "q4_1", "q5_0", "q5_1", "q8_0", "f16"]
        for pattern in quant_patterns:
            if pattern in filename:
                model_info["quantization"] = pattern
                break
        
        return model_info
    except Exception as e:
        return {"error": str(e)}

def extract_keywords(text: str) -> List[str]:
    """
    Extract important keywords from text for topic analysis.
    
    Args:
        text (str): Input text
        
    Returns:
        List[str]: List of extracted keywords
    """
    # This is a simple keyword extraction
    # For a production app, consider using NLTK, spaCy, or a keyword extraction model
    
    # Convert to lowercase and tokenize
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove common stopwords
    stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
                'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 
                'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 
                'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
                'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 
                'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
                'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
                'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 
                'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
                'into', 'through', 'during', 'before', 'after', 'above', 'below', 
                'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 
                'under', 'again', 'further', 'then', 'once', 'here', 'there', 
                'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 
                'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 
                'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
                's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
    
    keywords = [word for word in words if word not in stopwords and len(word) > 3]
    
    # Count frequencies and return top keywords
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_keywords[:10]]

# Image handling utilities

def process_uploaded_image(uploaded_file) -> Tuple[Optional[bytes], Optional[str], Optional[str]]:
    """
    Process an uploaded image file from Streamlit.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Tuple: (image_bytes, mime_type, error_message)
    """
    if uploaded_file is None:
        return None, None, "No file uploaded"
    
    try:
        # Get file details
        file_name = uploaded_file.name
        file_type = uploaded_file.type
        
        # Check if file is an image
        if not file_type.startswith('image/'):
            return None, None, f"Uploaded file is not an image. Got: {file_type}"
        
        # Read file content
        image_bytes = uploaded_file.getvalue()
        
        # Validate image by opening it with PIL
        try:
            Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            return None, None, f"Invalid image format: {str(e)}"
        
        return image_bytes, file_type, None
    except Exception as e:
        return None, None, f"Error processing image: {str(e)}"

def resize_image_if_needed(image_bytes: bytes, max_size: int = 1024) -> bytes:
    """
    Resize an image if it's larger than max_size in either dimension.
    
    Args:
        image_bytes (bytes): Image data
        max_size (int): Maximum dimension size
        
    Returns:
        bytes: Resized image data
    """
    try:
        # Open image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Check if resize is needed
        width, height = img.size
        if width <= max_size and height <= max_size:
            return image_bytes
        
        # Calculate new dimensions while maintaining aspect ratio
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        
        # Resize image
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert back to bytes
        output = io.BytesIO()
        resized_img.save(output, format=img.format)
        
        return output.getvalue()
    except Exception as e:
        print(f"Error resizing image: {e}")
        # Return original image if resize fails
        return image_bytes

def compress_image_for_api(image_bytes: bytes, quality: int = 85) -> bytes:
    """
    Compress an image to reduce size for API calls.
    
    Args:
        image_bytes (bytes): Image data
        quality (int): JPEG quality (1-100)
        
    Returns:
        bytes: Compressed image data
    """
    try:
        # Open image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed (in case of RGBA or other formats)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save as JPEG with compression
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        
        return output.getvalue()
    except Exception as e:
        print(f"Error compressing image: {e}")
        # Return original image if compression fails
        return image_bytes

def image_to_base64(image_bytes: bytes) -> str:
    """
    Convert image bytes to base64 string for embedding in HTML.
    
    Args:
        image_bytes (bytes): Image data
        
    Returns:
        str: Base64 encoded image string
    """
    try:
        # Encode image to base64
        base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
        return base64_encoded
    except Exception as e:
        print(f"Error encoding image to base64: {e}")
        return ""

def get_image_mime_type(image_bytes: bytes) -> str:
    """
    Detect the MIME type of an image.
    
    Args:
        image_bytes (bytes): Image data
        
    Returns:
        str: MIME type of the image
    """
    try:
        # Open image with PIL
        img = Image.open(io.BytesIO(image_bytes))
        
        # Map format to MIME type
        format_to_mime = {
            'JPEG': 'image/jpeg',
            'PNG': 'image/png',
            'GIF': 'image/gif',
            'WEBP': 'image/webp',
            'BMP': 'image/bmp'
        }
        
        # Get format and return corresponding MIME type
        return format_to_mime.get(img.format, 'application/octet-stream')
    except Exception as e:
        print(f"Error detecting image MIME type: {e}")
        return 'application/octet-stream' 