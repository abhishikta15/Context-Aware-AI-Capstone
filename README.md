# Context Aware Teaching Assistant Powered by Neuro Linguistic Programming 

An AI-powered teaching assistant that combines Neuro-Linguistic Programming principles with emotion detection to provide educators with actionable teaching recommendations and advanced image analysis.

## Features

- 🧠 **Neuro-Linguistic Programming Integration**: Uses NLP techniques for more effective teaching advice
- 🎭 **Emotion Detection**: Analyzes student emotions from text using HuggingFace models
- 🖼️ **Image Analysis**: Powered by Gemini API to analyze:
  - Teaching materials and scenes
  - Student work with grade-specific feedback
  - Classroom environments with spatial anchoring insights
- 💡 **Multiple AI Options**:
  - Local LLM integration using llama-cpp-python
  - Cloud-based integration using Google Gemini API
- 🎯 **Specialized Analysis Types**:
  - Teaching advice with linguistic patterns and reframing techniques
  - Student work feedback with positive framing and future pacing
  - Classroom environment analysis with spatial anchoring
- 📱 **Responsive UI**: Mobile-friendly modern interface
- 🔄 **Fallback Mode**: Works even without AI models available

## Installation

1. Clone this repository:
```bash
git clone https://github.com/abhishikta15/Capstone-AP21110010345---Context-Aware-AI-teacher-assistant.git
cd
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Choose your AI option:

   ### Option A: Local LLM
   - Download a GGML/GGUF model from [TheBloke's Hugging Face profile](https://huggingface.co/TheBloke)
   - Place the model file in the `models` directory (created automatically)
   - Select the model through the application interface

   ### Option B: Gemini API (Recommended for Image Analysis)
   - Install the Google GenAI package: `pip install google-genai`
   - Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Configure the API key through the application interface
   - Enable image analysis in the sidebar for full capabilities

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Configure your preferred AI option:
   - For local LLM: Select and load a model from the dropdown
   - For Gemini API: Enter your API key and select a model variant (recommended for image analysis)

4. Using the interface:
   - Chat directly with the assistant for text-based teaching advice
   - Upload images for analysis with three specialized analysis types:
     - **General Teaching Analysis**: Get feedback on teaching materials and methods
     - **Student Work Analysis**: Get feedback on student assignments with grade-specific insights
     - **Classroom Environment Analysis**: Optimize classroom layouts with spatial anchoring techniques
   - View conversation history with visual indicators of analysis types

## Documentation

- [RUNNING.md](docs/RUNNING.md) - Detailed setup and running instructions
- [RUNNING_SIMPLIFIED.md](docs/RUNNING_SIMPLIFIED.md) - Running without AI models
- [CODEBASE.md](docs/CODEBASE.md) - Overview of codebase structure
- [GEMINI.md](docs/GEMINI.md) - Guide for using Gemini API integration
- [CHANGELOG.md](docs/CHANGELOG.md) - Version history and changes

## Project Structure

```
teabot/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── README.md               # Project overview
├── models/                 # Directory for GGML/GGUF models
├── docs/                   # Documentation
│   ├── CODEBASE.md         # Codebase documentation
│   ├── GEMINI.md           # Gemini API guide
│   ├── RUNNING.md          # Setup instructions
│   ├── RUNNING_SIMPLIFIED.md # Simplified instructions
│   └── CHANGELOG.md        # Version history
└── src/                    # Source code directory
    ├── emotion_detector.py    # Emotion detection module
    ├── response_generator.py  # LLM interface and response generation
    ├── prompt_templates.py    # Structured prompts for AI models
    ├── gemini_integration.py  # Gemini API integration with image analysis
    └── utils.py               # Helper functions for images and data handling
```

## Neuro-Linguistic Programming Features

The application incorporates several NLP principles to enhance teaching effectiveness:

1. **Linguistic Patterns**: Advice includes specific language patterns to build rapport and engagement
2. **Reframing Techniques**: Converts challenging situations into opportunities
3. **Future Pacing**: Connects current actions with desired future outcomes
4. **Sensory-Based Language**: Tailors language to visual, auditory, and kinesthetic learning styles
5. **Spatial Anchoring**: Analyzes classroom layouts to optimize learning states
6. **Transformational Feedback**: Converts errors into learning opportunities

## Image Analysis Capabilities

With Gemini API integration, the system can analyze images in three specialized modes:

1. **Teaching Material Analysis**: 
   - Evaluates instructional resources
   - Suggests improvements based on NLP principles
   - Identifies engagement opportunities

2. **Student Work Analysis**:
   - Provides grade-level appropriate feedback
   - Uses "I notice..." statements to anchor success
   - Frames feedback in future-paced language
   - Supports multiple subjects and grade levels

3. **Classroom Environment Analysis**:
   - Analyzes spatial organization
   - Suggests optimal learning zones
   - Provides state management strategies
   - Recommends environmental adjustments

## Built By

Abhishikta Datta (10345) & Shreyashi Shankar (10273) from SRM UNIVERSITY AP

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
