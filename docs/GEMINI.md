# Using Gemini API with TeaBot

This guide explains how to set up and use Google's Gemini API with TeaBot for advanced AI-powered teaching assistance.

## Overview

TeaBot supports two AI options:
1. Local LLM (for those who want to run models on their own machine)
2. Gemini API (for cloud-based, high-quality responses with image analysis capabilities)

The Gemini API option provides access to Google's powerful AI models without requiring you to download large model files or have specialized hardware.

## Benefits of Using Gemini API

1. **No Large Downloads**: You don't need to download large model files (which can be 4-7GB+)
2. **Better Performance**: Responses are generated in Google's cloud, so you don't need a powerful local machine
3. **Higher Quality**: Access to Google's state-of-the-art models like Gemini-2.0-Ultra
4. **Faster Setup**: Just need an API key - no complex model installation or configuration
5. **Regular Updates**: Models are continuously improved on Google's side

## Getting Started with Gemini API

### 1. Get a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a Google account or sign in if you already have one
3. Click "Create API Key"
4. Copy your new API key (keep it secure, like a password)

### 2. Install Required Package

```bash
pip install google-genai
```

### 3. Configure TeaBot to Use Gemini

1. Start TeaBot with `streamlit run app.py`
2. In the sidebar, select "Gemini API" as the model type
3. Paste your API key in the field provided
4. Click "Set API Key"
5. Select a Gemini model variant:
   - **gemini-2.0-flash**: Fastest, good for most teaching applications
   - **gemini-2.0-pro**: Balanced speed and quality
   - **gemini-2.0-ultra**: Highest quality, most capable, but may be slower
6. Click "Set Gemini Model"

Once configured, you'll see a green checkmark and confirmation message indicating that Gemini API is active.

### 4. Using with TeaBot

Once configured, TeaBot will use Gemini API for all responses. You'll see a status indicator in the sidebar showing "Gemini API is configured and active".

You can use the chat interface exactly as before - all the emotion detection and conversation history features work the same, but responses will come from Gemini instead of a local model.

## Image Analysis Features

TeaBot uses Gemini's multimodal capabilities to analyze educational images. These features are only available when using the Gemini API option.

### Enabling Image Analysis

1. Make sure Gemini API is configured and active
2. Check the "Enable image analysis" box in the sidebar
3. You'll now see an image upload section in the main interface

### Types of Image Analysis

TeaBot offers three specialized NLP-enhanced image analysis options:

#### 1. General Teaching Analysis

Provides insights about any classroom-related image using sensory-based language. Best for:
- Teaching materials and resources
- Learning activities in progress
- Educational environments

This analysis includes NLP language patterns for building rapport and engagement with suggestions framed as presuppositions of success.

#### 2. Student Work NLP Assessment

Analyzes student work samples with a focus on growth-oriented developmental feedback. Features:
- Positive framing using "I notice..." statements that anchor success
- Sensory-rich feedback across visual, auditory, and kinesthetic systems
- Future pacing with "When you..." language to connect current work to future capability
- Transformational reframing that converts errors into learning opportunities

Perfect for assessment, grading assistance, and personalized feedback.

#### 3. Classroom Environment NLP Analysis

Examines classroom spaces through the lens of spatial anchoring and state management:
- Spatial anchoring that connects physical locations to learning states
- Representational system analysis across visual, auditory, and kinesthetic modalities
- State management strategies for different emotional/learning conditions
- Language pattern suggestions that reinforce positive states

Ideal for classroom setup, traffic flow improvement, and creating optimal learning environments.

## Handling Overloaded API States

The Gemini API occasionally experiences high demand, leading to temporary "overloaded" states. TeaBot implements several features to handle this:

- Automatic retry with exponential backoff when the API is overloaded
- Clear error messages when retries are unsuccessful
- Option to switch to a different Gemini model that might have more capacity

If you see an API overload message, simply wait a few minutes and try again, or switch to another model variant.

## API Usage and Costs

Google's Gemini API offers a free tier that is sufficient for typical educational usage:

- Free tier includes a generous number of requests per month
- No credit card required for the free tier
- Usage limits automatically reset each month

For the latest information on quotas and pricing, visit the [Google AI Studio documentation](https://ai.google.dev/pricing).

## Troubleshooting

Common issues and solutions:

- **"API not initialized"**: Make sure you've entered your API key and clicked "Set API Key"
- **"API overloaded"**: Wait a few minutes and try again, or switch to a different model variant
- **Image analysis not available**: Ensure you've enabled image analysis in the sidebar and are using a supported model (Flash or Pro)
- **Slow responses**: Try switching to the "Flash" model variant for faster results

If problems persist, check the [Google AI Status Dashboard](https://status.cloud.google.com/) for any ongoing service disruptions.

## Switching Between Models

You can easily switch between Gemini API and local LLM models by changing the model type in the sidebar. Your conversation history will be preserved, and you can compare the quality of responses between different models. 