# TeaBot Codebase Documentation

This document provides an overview of the Teacher Assistant Bot (TeaBot) codebase, explaining its structure, key components, and how they work together.

## Directory Structure

```
teabot/
├── app.py                  # Main Streamlit application entry point
├── requirements.txt        # Project dependencies
├── README.md               # Project overview
├── CHANGELOG.md            # Version history and changes
├── RUNNING.md              # Detailed setup and running instructions
├── models/                 # Directory for storing LLM models
├── docs/                   # Documentation directory
│   ├── CODEBASE.md         # This file - codebase documentation
│   ├── GEMINI.md           # Gemini API integration guide
│   ├── RUNNING.md          # Detailed setup instructions
│   └── RUNNING_SIMPLIFIED.md # Running without AI models
├── src/                    # Source code directory
│   ├── emotion_detector.py    # Emotion detection module
│   ├── response_generator.py  # LLM interface and response generation
│   ├── gemini_integration.py  # Gemini API integration
│   ├── prompt_templates.py    # Structured prompts for AI models
│   └── utils.py               # Helper functions
└── data/
    └── fallback_responses.json  # Predefined responses for fallback mode
```

## Core Components

### 1. Emotion Detector (`src/emotion_detector.py`)

This component uses a pre-trained Hugging Face transformer model to detect emotions in text input.

**Key Features:**
- Loads a distilled RoBERTa model specialized for emotion detection
- Analyzes text to identify emotions like joy, sadness, anger, fear, etc.
- Maps detected emotions to teaching-relevant interpretations
- Provides confidence scores for each emotion

**Usage Flow:**
1. Text is sent to the `detect_emotions()` method
2. The model processes the text and returns emotion predictions
3. Predictions are sorted by confidence score
4. The results can be further interpreted with `get_teaching_interpretation()`

### 2. Response Generator (`src/response_generator.py`)

This component manages local LLM integration and fallback responses.

**Key Features:**
- Loads and manages LLM models using llama-cpp-python
- Formats prompts using templates from `prompt_templates.py`
- Generates contextual responses based on user input and detected emotions
- Falls back to predefined responses when LLM is unavailable

**Operational Modes:**
- **LLM Mode**: Uses a loaded language model to generate custom responses
- **Fallback Mode**: Uses predefined templates categorized by emotion

### 3. Gemini Generator (`src/gemini_integration.py`)

This component integrates Google's Gemini API as an alternative to local LLMs.

**Key Features:**
- Connects to Google's Gemini API using API keys
- Supports multiple Gemini model variants (Flash, Pro, Ultra)
- Uses the same prompt templates for consistent response formatting
- Handles API authentication and error states gracefully

**Usage Flow:**
1. User provides a Gemini API key through the UI
2. The key is validated and a client connection is established
3. The user selects a Gemini model variant
4. Queries are formatted with prompt templates and sent to the API
5. Responses are processed and returned to the UI

### 4. Prompt Templates (`src/prompt_templates.py`)

Contains structured prompts to guide AI models' responses.

**Key Components:**
- System prompt that defines the bot's persona and capabilities
- Teaching prompt template that incorporates user input, emotions, and conversation history
- Emotion analysis prompt template for deeper emotional understanding

### 5. Utilities (`src/utils.py`)

Helper functions for common operations across the application.

**Key Functions:**
- Text cleaning and normalization
- Conversation history management (save/load)
- Model information extraction
- Keyword extraction for topic analysis

### 6. Main Application (`app.py`)

The Streamlit-based user interface and application controller.

**Key Features:**
- Chat interface with message history
- Model selection UI (Local LLM vs Gemini API)
- Emotion visualization
- Example queries for demo purposes
- API key management for Gemini integration

## Data Flow

1. User sends a message through the Streamlit interface
2. The message is processed by the Emotion Detector to identify emotional context
3. The message, emotions, and conversation history are passed to the active generator (Local LLM or Gemini API)
4. If a local LLM is active:
   - The prompt is formatted using templates from Prompt Templates
   - The LLM generates a contextual response
5. If Gemini API is active:
   - The prompt is formatted using the same templates
   - The request is sent to Google's Gemini API
   - The response is received and processed
6. If no AI model is available:
   - A predefined response is selected based on detected emotions
7. The response is displayed to the user along with detected emotions
8. The interaction is added to the conversation history

## Fallback Responses

The `data/fallback_responses.json` file contains predefined responses categorized by emotional states:
- **Engagement**: For situations where students appear disinterested
- **Confusion**: For situations where students are struggling to understand
- **Frustration**: For situations where students are experiencing difficulties
- **Anxiety**: For situations where students show signs of stress or worry
- **Default**: Generic teaching advice when no specific emotion is detected

## AI Model Options

### Local LLM Integration

The application supports any GGML or GGUF format model compatible with llama-cpp-python. The models can be:
- Loaded from the local file system
- Uploaded through the Streamlit interface
- Selected from previously uploaded models

Models are loaded with optimized parameters for the best balance of performance and resource usage on consumer hardware.

### Gemini API Integration

As an alternative to local models, the application can use Google's Gemini API:
- Requires an API key from Google AI Studio
- Supports multiple model variants (Flash, Pro, Ultra)
- Provides higher quality responses without local hardware requirements
- Includes a free tier sufficient for most educational use cases 