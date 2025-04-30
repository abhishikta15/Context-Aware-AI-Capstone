# Teacher Assistant Chatbot (TeaBot)

An AI-powered teaching assistant that helps educators analyze classroom situations, detect student emotions, and receive actionable teaching recommendations.

## Features

- 🤖 ChatGPT-like interface built with Streamlit
- 🎯 Emotion detection from text using HuggingFace models
- 💡 Multiple AI options:
  - Local LLM integration using llama-cpp-python
  - Cloud-based integration using Google Gemini API
- 📱 Mobile-friendly chat UI
- 🔄 Fallback mode when no AI model is available
- 📚 Evidence-based teaching recommendations

## Installation

1. Clone this repository:
```bash
git clone https://github.com/sujalraunak/teabot.git
cd teabot
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

   ### Option B: Gemini API
   - Install the Google GenAI package: `pip install google-genai`
   - Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Configure the API key through the application interface

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Configure your preferred AI option:
   - For local LLM: Select and load a model from the dropdown
   - For Gemini API: Enter your API key and select a model variant

4. Start chatting! You can:
   - Describe classroom situations
   - Ask for teaching advice
   - Get emotional insights about students
   - Receive actionable recommendations

## Using Without AI Models

If you don't have a local LLM model or Gemini API key, the application will run in "fallback mode":
- Emotion detection will still work
- Responses will be based on predefined templates in `data/fallback_responses.json`
- You can customize these responses by editing the JSON file

For instructions on running without AI models, see [RUNNING_SIMPLIFIED.md](docs/RUNNING_SIMPLIFIED.md).

## Documentation

- [RUNNING.md](docs/RUNNING.md) - Detailed setup and running instructions
- [RUNNING_SIMPLIFIED.md](docs/RUNNING_SIMPLIFIED.md) - Running without AI models
- [CODEBASE.md](docs/CODEBASE.md) - Overview of codebase structure
- [GEMINI.md](docs/GEMINI.md) - Guide for using Gemini API integration
- [CHANGELOG.md](CHANGELOG.md) - Version history and changes

## Project Structure

```
teabot/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── README.md               # Project overview
├── CHANGELOG.md            # Version history
├── models/                 # Directory for GGML/GGUF models
├── docs/                   # Documentation
│   ├── CODEBASE.md         # Codebase documentation
│   ├── GEMINI.md           # Gemini API guide
│   ├── RUNNING.md          # Setup instructions
│   └── RUNNING_SIMPLIFIED.md # Simplified instructions
├── src/                    # Source code directory
│   ├── emotion_detector.py    # Emotion detection module
│   ├── response_generator.py  # LLM interface and response generation
│   ├── prompt_templates.py    # Structured prompts for AI models
│   ├── gemini_integration.py  # Gemini API integration
│   └── utils.py               # Helper functions
└── data/
    └── fallback_responses.json  # Predefined responses for fallback mode
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 