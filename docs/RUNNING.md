# Running the Teacher Assistant Bot (TeaBot)

This guide provides detailed instructions for running the Teacher Assistant Bot on your local machine.

## Prerequisites

Before running the application, ensure you have:

1. **Python 3.8+** installed on your system
2. **Git** for cloning the repository
3. **5+ GB of disk space** if you plan to use a local LLM model

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sujalraunak/teabot.git
cd teabot
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to avoid package conflicts:

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Note: If you encounter issues with the `llama-cpp-python` installation, it's okay - you can still use the app in fallback mode or with Gemini API.

For GPU acceleration with local LLMs (if you have a compatible NVIDIA GPU):
```bash
pip uninstall -y llama-cpp-python
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --no-cache-dir
```

## AI Model Options

You have three options for running TeaBot:

1. **Using a Local LLM model**
2. **Using Google's Gemini API**
3. **Using fallback mode** (without any AI model)

### Option 1: Using a Local LLM Model

1. Download a GGUF format model from [TheBloke's Hugging Face profile](https://huggingface.co/TheBloke)
   - Recommended models:
     - [Llama-2-7B-Chat-GGUF](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF)
     - [Mistral-7B-Instruct-v0.2-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)

2. Choose the appropriate quantization for your system:
   - `Q4_K_M` variants are a good balance of quality and memory usage
   - `Q5_K_M` variants offer better quality with higher memory requirements
   - `Q2_K` variants are smallest but with reduced output quality

3. Create a `models` directory in the project root and place the downloaded model file there:
   ```bash
   mkdir -p models
   # Move your downloaded model file to the models directory
   ```

### Option 2: Using Google's Gemini API

1. Install the Google GenAI package:
   ```bash
   pip install google-genai
   ```

2. Get a Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create an account if needed
   - Generate an API key
   - Keep your API key secure

3. You'll enter this API key in the TeaBot interface when running the app.

### Option 3: Using Fallback Mode

If you don't want to use either AI option, you can run TeaBot in fallback mode:
- No additional setup required
- Uses predefined responses based on detected emotions
- Still provides useful teaching advice
- See [RUNNING_SIMPLIFIED.md](RUNNING_SIMPLIFIED.md) for more details

## Running the Application

### Start the Streamlit App

```bash
streamlit run app.py
```

This will start the application and open it in your default web browser (typically at http://localhost:8501).

### Configuring Your AI Option

#### For Local LLM:
1. In the sidebar, select "Local LLM" as the model type
2. Choose your downloaded model from the dropdown
3. Click "Load Selected Model" to activate it

#### For Gemini API:
1. In the sidebar, select "Gemini API" as the model type
2. Enter your API key in the input field
3. Click "Set API Key" to authenticate
4. Select a model variant (Flash, Pro, or Ultra)
5. Click "Set Gemini Model" to apply your selection

### Using the Application

1. **With a Local LLM or Gemini API**:
   - You'll see a green check mark and status message indicating which AI option is active
   - Enter your questions to get high-quality, personalized responses

2. **Without any AI model (fallback mode)**:
   - You'll see a warning message indicating you're in fallback mode
   - Responses will be based on predefined templates, but still useful

3. **Interacting with the bot**:
   - Type your questions or classroom situations in the chat input
   - Use the example queries in the sidebar for inspiration
   - The bot will analyze emotions and provide teaching advice

## Troubleshooting

### Common Issues

1. **Model loading fails**:
   - Ensure you have enough RAM for the model you're trying to load
   - Try a smaller quantized model if you're on a lower-end machine
   - Check that the model file is not corrupted

2. **Gemini API issues**:
   - Verify your API key is correct
   - Check your internet connection
   - Make sure your account has sufficient quota remaining

3. **Slow responses**:
   - LLM inference can be slow on CPU
   - Consider using GPU acceleration if available
   - Try a smaller model for faster responses
   - Switch to Gemini API for better performance on less powerful machines

4. **Package installation issues**:
   - Ensure you're using Python 3.8+
   - Try installing with `--prefer-binary` flag
   - Make sure you have the required compilers if building from source

### Getting Help

If you encounter any issues not covered here, please open an issue on the GitHub repository. 