# Simplified Guide: Running TeaBot Without LLM

If you're having trouble installing the optional LLM component, you can still use TeaBot with its emotion detection and fallback response system. Here's how:

## Quick Start

1. **Install the required dependencies**:
   ```bash
   pip install streamlit transformers torch numpy pandas
   ```

2. **Run the application**:
   ```bash
   streamlit run app.py
   ```

That's it! The application will start and open in your browser, running in fallback mode.

## What Works in Fallback Mode

Even without an LLM, TeaBot can:
- Detect emotions in text using the HuggingFace transformer model
- Provide teaching advice based on detected emotions
- Maintain conversation history
- Display a clean, mobile-friendly chat interface

The only difference is that responses come from predefined templates rather than being dynamically generated.

## If You Want LLM Features Later

When you're ready to add LLM capabilities:

1. Install Visual Studio Build Tools with C++ development components
2. Install llama-cpp-python:
   ```bash
   pip install llama-cpp-python --prefer-binary
   ```
3. Download a GGUF model from Hugging Face
4. Place it in the models directory or upload it through the app
5. Select and load it in the app's sidebar

## Troubleshooting

- **"streamlit: command not found"**: Make sure you've installed streamlit correctly. Try running `python -m streamlit run app.py` instead.
- **Transformer model errors**: Check your internet connection, as the model may need to be downloaded the first time you run the app.

For more detailed instructions, see the full RUNNING.md file. 