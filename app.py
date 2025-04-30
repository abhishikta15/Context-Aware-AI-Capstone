import streamlit as st
import os
from src.emotion_detector import EmotionDetector
from src.response_generator import ResponseGenerator
from src.utils import process_uploaded_image, resize_image_if_needed, compress_image_for_api, image_to_base64

# Try to import Gemini integration
try:
    from src.gemini_integration import GeminiGenerator
    gemini_available = True
except ImportError:
    gemini_available = False

# Page configuration
st.set_page_config(
    page_title="Teacher Assistant Bot",
    page_icon="🤖",
    layout="wide"
)

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "emotion_detector" not in st.session_state:
    st.session_state.emotion_detector = EmotionDetector()
if "response_generator" not in st.session_state:
    st.session_state.response_generator = ResponseGenerator()
if "gemini_generator" not in st.session_state and gemini_available:
    st.session_state.gemini_generator = GeminiGenerator()
if "active_generator" not in st.session_state:
    st.session_state.active_generator = "fallback"  # Options: "fallback", "llm", "gemini"
if "enable_image_input" not in st.session_state:
    st.session_state.enable_image_input = False
if "last_uploaded_image" not in st.session_state:
    st.session_state.last_uploaded_image = None
if "last_image_mime_type" not in st.session_state:
    st.session_state.last_image_mime_type = None
if "current_analysis_type" not in st.session_state:
    st.session_state.current_analysis_type = "general"  # Options: "general", "student_work", "classroom"
if "api_error" not in st.session_state:
    st.session_state.api_error = None
if "active_chat_tab" not in st.session_state:
    st.session_state.active_chat_tab = "Teaching Advice"  # Default tab

# Custom CSS
st.markdown("""
<style>
    .stChat {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .user-message {
        background-color: #e6f3ff;
        text-align: right;
    }
    .assistant-message {
        background-color: #f0f2f6;
    }
    .emotion-label {
        font-size: 0.8em;
        color: #666;
        margin-top: 5px;
    }
    .stButton button {
        width: 100%;
    }
    .api-key-input input {
        background-color: #f9f9f9;
    }
    .uploaded-image {
        max-width: 100%;
        max-height: 300px;
        border-radius: 8px;
        margin: 10px 0;
        border: 1px solid #ddd;
    }
    .image-controls {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    .image-caption {
        font-size: 0.8em;
        color: #666;
        margin-top: 5px;
        font-style: italic;
    }
    .analysis-type-card {
        background-color: #2c3035;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #4CAF50;
    }
    .analysis-type-card h4 {
        margin-top: 0;
        color: #4CAF50;
    }
    .analysis-type-card p {
        font-size: 0.9em;
        margin-bottom: 10px;
        color: #e0e0e0;
    }
    .analysis-type-card ul {
        color: #e0e0e0;
    }
    .tab-content {
        padding: 20px 10px;
        border: 1px solid #e0e0e0;
        border-radius: 0 0 10px 10px;
    }
    .error-message {
        background-color: #ffebee;
        color: #c62828;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #c62828;
    }
    .tab-success {
        border-bottom: 3px solid #4CAF50 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        background-color: #2c3035;
        color: #e0e0e0 !important;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for model selection and information
with st.sidebar:
    st.title("ℹ️ Configuration")
    
    # Model type selection
    st.header("Model Selection")
    model_type = st.radio(
        "Select model type:",
        options=["Local LLM", "Gemini API"] if gemini_available else ["Local LLM"],
        help="Choose between running a local LLM model or using Google's Gemini API"
    )
    
    if model_type == "Local LLM":
        # Local LLM section
        st.subheader("Local LLM Model Selection")
        
        # Check for existing models
        model_files = []
        if os.path.exists("models"):
            for file in os.listdir("models"):
                if file.endswith((".gguf", ".ggml", ".bin")):
                    model_files.append(file)
        
        # Display model selection options
        if model_files:
            selected_model = st.selectbox(
                "Select a model:",
                options=model_files,
                help="Select a GGUF or GGML model to use for generating responses"
            )
            
            if st.button("Load Selected Model"):
                with st.spinner("Loading model... This may take a moment"):
                    model_path = os.path.join("models", selected_model)
                    if st.session_state.response_generator.set_model(model_path):
                        st.session_state.active_generator = "llm"
                        st.success(f"Successfully loaded model: {selected_model}")
                    else:
                        st.error("Failed to load model. Check logs for details.")
        
        # Model upload
        st.subheader("Upload New Model")
        uploaded_file = st.file_uploader("Choose a GGUF/GGML model file", type=["gguf", "ggml", "bin"])
        
        if uploaded_file is not None:
            with st.spinner("Uploading model... This may take a moment"):
                # Save the uploaded model
                model_path = os.path.join("models", uploaded_file.name)
                with open(model_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"Model uploaded: {uploaded_file.name}")
                
                # Option to load the uploaded model
                if st.button("Load Uploaded Model"):
                    if st.session_state.response_generator.set_model(model_path):
                        st.session_state.active_generator = "llm"
                        st.success(f"Successfully loaded model: {uploaded_file.name}")
                    else:
                        st.error("Failed to load model. Check logs for details.")
    
    elif model_type == "Gemini API":
        # Gemini API section
        st.subheader("Gemini API Configuration")
        
        # API key input
        gemini_api_key = st.text_input(
            "Enter Gemini API Key",
            type="password",
            help="Get your API key from Google AI Studio",
            key="gemini_api_key_input"
        )
        
        if st.button("Set API Key"):
            if gemini_api_key:
                with st.spinner("Setting up Gemini API..."):
                    if st.session_state.gemini_generator.set_api_key(gemini_api_key):
                        st.session_state.active_generator = "gemini"
                        st.success("Gemini API configured successfully!")
                    else:
                        st.error("Failed to configure Gemini API. Check logs for details.")
            else:
                st.warning("Please enter an API key")
        
        # Model selection for Gemini
        gemini_model_options = ["gemini-2.0-flash", "gemini-2.0-pro", "gemini-2.0-ultra"]
        selected_gemini_model = st.selectbox(
            "Select Gemini model",
            options=gemini_model_options,
            help="Choose the Gemini model to use. Flash is fastest, Ultra is highest quality."
        )
        
        if st.button("Set Gemini Model"):
            if st.session_state.gemini_generator.is_available:
                if st.session_state.gemini_generator.set_model(selected_gemini_model):
                    st.success(f"Gemini model set to: {selected_gemini_model}")
                else:
                    st.error("Failed to set Gemini model")
            else:
                st.warning("Please set your API key first")
                
        # Image input toggle (only available for Gemini API)
        st.subheader("Image Analysis Settings")
        
        enable_image = st.checkbox(
            "Enable image analysis", 
            value=st.session_state.enable_image_input,
            help="Allow uploading images for analysis by Gemini"
        )
        
        if enable_image != st.session_state.enable_image_input:
            st.session_state.enable_image_input = enable_image
            st.rerun()
    
    # Status display
    st.header("Current Status")
    if st.session_state.active_generator == "llm" and st.session_state.response_generator.llm:
        st.success("✅ Local LLM is loaded and active")
        st.info(f"Model: {os.path.basename(st.session_state.response_generator.model_path)}")
    elif st.session_state.active_generator == "gemini" and gemini_available and st.session_state.gemini_generator.is_available:
        st.success("✅ Gemini API is configured and active")
        st.info(f"Model: {st.session_state.gemini_generator.model_name}")
        if st.session_state.enable_image_input and st.session_state.gemini_generator.supports_image:
            st.success("✅ Image analysis is enabled")
        elif st.session_state.enable_image_input and not st.session_state.gemini_generator.supports_image:
            st.warning("⚠️ Current model doesn't support image analysis")
    else:
        st.warning("⚠️ Using fallback mode (no LLM)")
        st.info("Responses are based on predefined templates and emotion detection only.")
    
    # Information about the application
    st.header("About")
    st.markdown("""
    ### Features
    - Emotion detection from text
    - Teaching advice based on detected emotions
    - LLM integration for personalized responses
    - Gemini API support for cloud-based responses
    - Image analysis for classroom scenes and student work
    - Mobile-friendly interface
    
    ### Usage Tips
    - Be specific about classroom situations
    - Mention student behaviors and age groups
    - Ask for specific strategies or approaches
    - Upload images of classroom setups or student work for analysis
    """)
    
    # Example queries
    st.subheader("Example Queries")
    examples = [
        "My students seem disengaged during math lessons. What can I do?",
        "A student is showing signs of anxiety before tests. How can I help?",
        "The class becomes very excited and hard to manage after lunch. Any advice?",
        "Some students are struggling with group work. What strategies would you recommend?"
    ]
    
    for example in examples:
        if st.button(f"📝 {example[:40]}...", key=example):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": example})
            
            # Detect emotions
            emotions = st.session_state.emotion_detector.detect_emotions(example)
            
            # Generate response based on active generator
            if st.session_state.active_generator == "gemini" and gemini_available and st.session_state.gemini_generator.is_available:
                response = st.session_state.gemini_generator.generate_response(
                    prompt=example,
                    emotions=emotions,
                    conversation_history=st.session_state.messages[:-1]
                )
            elif st.session_state.active_generator == "llm" and st.session_state.response_generator.llm:
                response = st.session_state.response_generator.generate_response(
                    prompt=example,
                    emotions=emotions,
                    conversation_history=st.session_state.messages[:-1]
                )
            else:
                response = st.session_state.response_generator.generate_response(
                    prompt=example,
                    emotions=emotions,
                    conversation_history=st.session_state.messages[:-1]
                )
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "emotions": emotions
            })
            
            # Rerun to update the display
            st.rerun()

# Main chat interface
st.title("👩‍🏫 Emotion Aware AI For Teachers Using NLP")
st.markdown("""
Applying Neuro Linguistic Programming and leveraging LLMs the system will analyze student emotions and provide actionable recommendations.
""")

# Display API error if present
if st.session_state.api_error:
    st.markdown(f"""
    <div class="error-message">
        <strong>API Error:</strong> {st.session_state.api_error}
        <p>The Gemini API might be experiencing high demand. Please try again in a few moments or switch to a different model.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Clear error button
    if st.button("Clear Error Message"):
        st.session_state.api_error = None
        st.rerun()

# Replace tabs with a single chat container
st.markdown("""
<div style="background-color: #1e2126; border-radius: 10px; padding: 15px; margin-bottom: 20px; border: 1px solid #4CAF50;">
    <h3 style="color: #4CAF50; margin: 0 0 10px 0;">Built by Abhishikta Datta (10345) & Shreyashi Shankar (10273) from SRM UNIVERSITY AP</h3>
    <p style="color: #e0e0e0; font-size: 0.9em;">Get personalized teaching advice, student work analysis, and classroom environment insights with NLP-enhanced feedback.</p>
</div>
""", unsafe_allow_html=True)

# Helper function to get the analysis types 
def get_analysis_types():
    return [
        {"id": "teaching", "name": "General Teaching Analysis", 
         "description": "Get personalized teaching strategies with embedded NLP patterns that help create positive learning states."},
        {"id": "student_work", "name": "Student Work Analysis", 
         "description": "Upload images of student work to receive NLP-enhanced feedback with positive framing and future-paced language."},
        {"id": "classroom", "name": "Classroom Environment Analysis", 
         "description": "Analyze classroom layouts for spatial anchoring and representational system optimization."}
    ]

# Image upload section - Only show if Gemini API is active and image analysis is enabled
image_uploaded = False
if (st.session_state.enable_image_input and 
    st.session_state.active_generator == "gemini" and 
    gemini_available and 
    st.session_state.gemini_generator.is_available and
    st.session_state.gemini_generator.supports_image):
    
    # Create a container with a distinctive style for the image upload section
    with st.container():
        st.markdown("""
        <div style="background-color: #1e2126; border-radius: 10px; padding: 10px; margin-bottom: 20px; border: 1px solid #4CAF50;">
            <h3 style="color: #4CAF50; margin: 0 0 10px 0;">Image Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        
        image_col1, image_col2 = st.columns([3, 2])
        
        with image_col1:
            # Image upload
            uploaded_image = st.file_uploader(
                "Upload an image for NLP-enhanced analysis",
                type=["png", "jpg", "jpeg", "webp"],
                help="Upload an image of a classroom, student work, or teaching materials"
            )
            
            if uploaded_image is not None:
                # Process the image
                image_bytes, mime_type, error = process_uploaded_image(uploaded_image)
                
                if error:
                    st.error(error)
                else:
                    # Display the image
                    st.image(image_bytes, caption="Uploaded image", use_column_width=True)
                    
                    # Display file info for debugging
                    file_size_kb = len(image_bytes) / 1024
                    st.info(f"Image info: {mime_type}, {file_size_kb:.1f} KB")
                    
                    # Store image in session state
                    st.session_state.last_uploaded_image = image_bytes
                    st.session_state.last_image_mime_type = mime_type
                    image_uploaded = True
        
        with image_col2:
            # If no image is uploaded yet, show tips
            if not image_uploaded:
                with st.expander("Image Analysis Tips", expanded=True):
                    st.markdown("""
                    - **JPEG** format works best
                    - Keep images **under 1MB**
                    - Use **clear, well-lit** images
                    - Try **Flash model** for reliability
                    - Each analysis type offers specialized insights
                    """)
            # If image is uploaded, show analysis controls
            else:
                st.markdown("<h4 style='color: #4CAF50;'>Analysis Settings</h4>", unsafe_allow_html=True)
                
                # Let user select analysis type directly
                analysis_types = get_analysis_types()
                analysis_options = [t["name"] for t in analysis_types]
                
                selected_analysis = st.selectbox(
                    "Select analysis type:",
                    options=analysis_options,
                    index=0
                )
                
                # Find the selected analysis type
                for a_type in analysis_types:
                    if a_type["name"] == selected_analysis:
                        st.session_state.current_analysis_type = a_type["id"]
                        st.markdown(f"""
                        <div style="background-color: #2c3035; border-radius: 6px; padding: 10px; margin: 10px 0; border-left: 3px solid #4CAF50;">
                            <p style="color: #e0e0e0; margin: 0;">{a_type["description"]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        break
                
                # Show specific controls based on the analysis type
                if st.session_state.current_analysis_type == "student_work":
                    # Additional fields for student work assessment
                    col1, col2 = st.columns(2)
                    with col1:
                        grade_level = st.selectbox(
                            "Grade level:",
                            options=["Preschool", "Kindergarten", "1st grade", "2nd grade", "3rd grade", 
                                    "4th grade", "5th grade", "6th grade", "7th grade", "8th grade",
                                    "9th grade", "10th grade", "11th grade", "12th grade", "College"]
                        )
                    with col2:
                        subject = st.selectbox(
                            "Subject:",
                            options=["Math", "Science", "Language Arts", "Social Studies", 
                                    "Art", "Music", "Physical Education", "Foreign Language", "Other"]
                        )
                elif st.session_state.current_analysis_type == "classroom":
                    st.info("💡 Classroom analysis works best with clear images showing the entire layout.")
                else:  # teaching
                    st.info("💡 Teaching analysis provides general feedback on teaching materials and methods.")
                
                # Add analyze button
                analyze_button = st.button("Analyze Image", type="primary", use_container_width=True)
                
                if analyze_button:
                    try:
                        with st.spinner("Analyzing image with NLP perspective..."):
                            # Log the process for debugging
                            print(f"Starting analysis of {uploaded_image.name}, type: {st.session_state.current_analysis_type}")
                            
                            # Compress the image for API
                            processed_image = compress_image_for_api(resize_image_if_needed(image_bytes))
                            print(f"Image processed and compressed from {len(image_bytes)} to {len(processed_image)} bytes")
                            
                            # Create a status container to show progress
                            status_container = st.empty()
                            
                            # Determine which analysis to run
                            if st.session_state.current_analysis_type == "student_work":
                                status_container.info("Analyzing student work...")
                                response = st.session_state.gemini_generator.analyze_student_work(
                                    image_data=processed_image,
                                    grade_level=grade_level,
                                    subject=subject,
                                    image_mime_type=mime_type
                                )
                                prompt = f"Please analyze this {subject} work from a {grade_level} student with NLP perspective."
                                analysis_type = "student_work"
                            elif st.session_state.current_analysis_type == "classroom":
                                # Special handling for classroom analysis which seems to have issues
                                status_container.info("Analyzing classroom environment...")
                                
                                try:
                                    # Try with a more focused prompt that might work better with API limitations
                                    print("Attempting classroom environment analysis...")
                                    
                                    # First, try with a simplified prompt if full analysis fails
                                    response = st.session_state.gemini_generator.analyze_classroom_setup(
                                        image_data=processed_image,
                                        image_mime_type=mime_type
                                    )
                                    print("Classroom analysis completed successfully")
                                except Exception as classroom_error:
                                    # Fallback to generic image analysis if specialized method fails
                                    print(f"Error in classroom analysis: {str(classroom_error)}")
                                    status_container.warning("Using simplified classroom analysis due to API limitations.")
                                    
                                    # Try with the generic response generator as fallback
                                    response = st.session_state.gemini_generator.generate_response(
                                        prompt="Analyze this classroom environment with focus on spatial organization and learning zones",
                                        emotions=[],
                                        image_data=processed_image,
                                        image_mime_type=mime_type
                                    )
                                
                                prompt = "Please analyze this classroom setup with NLP spatial anchoring."
                                analysis_type = "classroom"
                            else:
                                status_container.info("Performing general teaching analysis...")
                                response = st.session_state.gemini_generator.generate_response(
                                    prompt="What can you tell me about this image from a teaching perspective?",
                                    emotions=[],
                                    image_data=processed_image,
                                    image_mime_type=mime_type
                                )
                                prompt = "What can you tell me about this teaching image using NLP patterns?"
                                analysis_type = "teaching"
                            
                            # Clear the status
                            status_container.empty()
                            
                            # Check if response contains an API error message
                            if "apologize" in response and ("API" in response or "overloaded" in response):
                                st.session_state.api_error = response
                                st.error("The Gemini API is currently overloaded. Please try again in a few moments.")
                            else:
                                # Add to message history
                                st.session_state.messages.append({
                                    "role": "user", 
                                    "content": prompt, 
                                    "image": image_bytes,
                                    "analysis_type": analysis_type
                                })
                                st.session_state.messages.append({
                                    "role": "assistant", 
                                    "content": response,
                                    "analysis_type": analysis_type
                                })
                            
                            # Clear image from session
                            st.session_state.last_uploaded_image = None
                            st.session_state.last_image_mime_type = None
                    
                    except Exception as e:
                        error_msg = str(e)
                        print(f"Error during image analysis: {error_msg}")
                        st.session_state.api_error = error_msg
                        
                        # Provide specific guidance based on the error
                        if "503" in error_msg or "overloaded" in error_msg:
                            st.error("🔄 The Gemini API is currently overloaded. Please try again in a few minutes.")
                        elif "429" in error_msg or "quota" in error_msg:
                            st.error("⚠️ API quota limit reached. Try again later or switch to a different API key.")
                        elif "image" in error_msg.lower():
                            st.error("🖼️ There was a problem processing your image. Try a smaller or different format image.")
                        else:
                            st.error(f"❌ An error occurred: {error_msg}. Try a different analysis type or image.")
                    
                    # Always rerun to update display
                    st.rerun()

# Unified message display - Replace the tab-specific message displays
st.markdown("""
<div style="background-color: #1e2126; border-radius: 10px; padding: 10px; margin: 20px 0; border: 1px solid #4CAF50;">
    <h3 style="color: #4CAF50; margin: 0 0 10px 0;">Conversation History</h3>
</div>
""", unsafe_allow_html=True)

# Display all chat messages in one section
has_messages = False
for message in st.session_state.messages:
    has_messages = True
    with st.container():
        # Add a badge indicating analysis type
        analysis_badge = ""
        if message.get("analysis_type") == "student_work":
            analysis_badge = '<span style="background-color: #3949ab; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; margin-left: 10px;">Student Work</span>'
        elif message.get("analysis_type") == "classroom":
            analysis_badge = '<span style="background-color: #43a047; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; margin-left: 10px;">Classroom</span>'
        else:
            analysis_badge = '<span style="background-color: #e65100; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; margin-left: 10px;">Teaching</span>'
            
        if message["role"] == "user":
            st.markdown(f"""
            <div style="background-color: #233142; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #e0e0e0;">You:</strong>
                    {analysis_badge}
                </div>
                <p style="color: #e0e0e0;">{message['content']}</p>
            </div>
            """, unsafe_allow_html=True)
            # Display image if included in the message
            if "image" in message and message["image"]:
                st.image(message["image"], caption="Uploaded image", use_column_width=True)
        else:
            st.markdown(f"""
            <div style="background-color: #1c3b27; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
                <strong style="color: #4CAF50;">Assistant:</strong>
                <p style="color: #e0e0e0;">{message['content']}</p>
            </div>
            """, unsafe_allow_html=True)
            if "emotions" in message:
                emotions_list = [
                    f"{emotion} ({score:.0%})"
                    for emotion, score in message["emotions"]
                    if score > 0.1
                ]
                if emotions_list:
                    emotions_text = ", ".join(emotions_list)
                    st.markdown(f"""
                    <div style="background-color: #2a2a2a; padding: 5px 10px; border-radius: 5px; display: inline-block; margin-bottom: 15px;">
                        <small style="color: #bbb;">Detected emotions: {emotions_text}</small>
                    </div>
                    """, unsafe_allow_html=True)

if not has_messages:
    st.markdown("""
    <div style="text-align: center; padding: 30px; color: #aaa; background-color: #2a2a2a; border-radius: 10px; margin: 30px 0;">
        <i>No conversation history yet. Start a conversation or upload an image for analysis.</i>
    </div>
    """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Set analysis type based on active tab
    if st.session_state.active_chat_tab == "Student Work Analysis":
        analysis_type = "student_work"
    elif st.session_state.active_chat_tab == "Classroom Environment":
        analysis_type = "classroom"
    else:
        analysis_type = "teaching"
    
    # Add user message to chat history
    if st.session_state.last_uploaded_image is not None:
        # If there's an image, include it in the message
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "image": st.session_state.last_uploaded_image,
            "analysis_type": analysis_type
        })
        
        # Get image data for processing
        image_data = st.session_state.last_uploaded_image
        image_mime_type = st.session_state.last_image_mime_type
        
        # Process image for API
        processed_image = compress_image_for_api(resize_image_if_needed(image_data))
        
        # Clear image from session after use
        st.session_state.last_uploaded_image = None
        st.session_state.last_image_mime_type = None
    else:
        # Regular text message
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "analysis_type": analysis_type
        })
        processed_image = None
        image_mime_type = None
    
    # Detect emotions
    emotions = st.session_state.emotion_detector.detect_emotions(prompt)
    
    # Generate response based on active generator
    try:
        if st.session_state.active_generator == "gemini" and gemini_available and st.session_state.gemini_generator.is_available:
            response = st.session_state.gemini_generator.generate_response(
                prompt=prompt,
                emotions=emotions,
                conversation_history=st.session_state.messages[:-1],  # Exclude the current message
                image_data=processed_image,
                image_mime_type=image_mime_type
            )
        elif st.session_state.active_generator == "llm" and st.session_state.response_generator.llm:
            response = st.session_state.response_generator.generate_response(
                prompt=prompt,
                emotions=emotions,
                conversation_history=st.session_state.messages[:-1]  # Exclude the current message
            )
        else:
            response = st.session_state.response_generator.generate_response(
                prompt=prompt,
                emotions=emotions,
                conversation_history=st.session_state.messages[:-1]  # Exclude the current message
            )
            
        # Check if response contains an API error message
        if "apologize" in response and ("API" in response or "overloaded" in response):
            st.session_state.api_error = response
            response = "I'm currently experiencing connectivity issues with the AI service. Please try again in a moment."
            
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "emotions": emotions,
            "analysis_type": analysis_type
        })
    
    except Exception as e:
        st.session_state.api_error = str(e)
    
    # Rerun to update the display
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
Made with ❤️ using Streamlit and open-source models. Supports local LLM, Gemini API, and NLP-enhanced image analysis.
""") 