# Changelog

All notable changes to the Teacher Assistant Bot (TeaBot) project will be documented in this file.

## [1.0.0] - 2023-06-15

### Added
- Initial release of Teacher Assistant Bot
- Streamlit-based chat interface with clean, modern design
- Emotion detection from text using HuggingFace transformer models
- Fallback response system using predefined educational advice templates
- Mobile-friendly UI with responsive design
- Example queries for quick testing

## [1.1.0] - 2023-07-20

### Added
- LLM integration using llama-cpp-python
- Model upload functionality through Streamlit interface
- Custom prompt templates for better teaching-focused responses
- Conversation history preservation for context-aware responses
- Utility functions for text processing and model management

### Changed
- Improved UI with status indicators for LLM availability
- Enhanced sidebar with model selection dropdown
- Updated example queries for better demonstration
- Better error handling for model loading failures

### Fixed
- Emotion detection accuracy improvements
- Fixed display issues on mobile devices
- Corrected fallback response categorization

## [1.2.0] - 2023-08-30

### Added
- Support for GGUF format models (newer format replacing GGML)
- Model information display in sidebar
- Conversation export/import functionality
- Keyword extraction for better topic understanding

### Changed
- Optimized LLM loading for faster startup
- Improved prompt templates for more relevant responses
- Updated UI with emotion detection confidence display
- Enhanced documentation with clearer usage instructions

### Fixed
- Memory usage optimizations
- Fixed model loading issues on Windows systems
- Improved error reporting for failed LLM calls

## [1.3.0] - 2023-10-15

### Added
- Google Gemini API integration as an alternative to local LLMs
- Model type selection in sidebar (Local LLM vs Gemini API)
- API key management interface
- Support for multiple Gemini model variants (Flash, Pro, Ultra)
- Documentation for Gemini API setup and usage

### Changed
- Updated requirements.txt with google-genai package
- Simplified running instructions for users without local models
- Modified response generation logic to support multiple generator types
- Enhanced error handling for API authentication issues

### Fixed
- Streamlit rerun method compatibility with newer versions
- Example queries not returning responses issue
- Improved error messages for connectivity problems 