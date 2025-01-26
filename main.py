# -*- coding: utf-8 -*-
# main chat interface for gemini models
# last updated: 2025-01-26 (maybe)

import google.generativeai as genai
# import dotenv - uncomment this line to use locally
import streamlit as st
import os
import time
import pyperclip
from datetime import datetime

# ----- config stuff -----
# dotenv.load_dotenv()  # load from .env file - uncomment this line to use locally

# check if api key exists
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("API key missing! Check .env file")
    st.stop()  # dont continue without key

genai.configure(api_key=GOOGLE_API_KEY)

# model names with emojis because why not
MODEL_DISPLAY_NAMES = {
    "gemini-1.5-flash-latest": "🚀 Gemini 1.5 Flash",
    "gemini-2.0-flash-exp": "🧪 Gemini 2.0 Flash (exp)",
    "gemini-2.0-flash-thinking-exp-1219": "🤔 Gemini 2.0 Thinking",
    "gemini-exp-1206": "🔬 1206 Experimental",
    "learnlm-1.5-pro-experimental": "📚 LearnLM Pro",
}

# reverse mapping for dropdown
AVAILABLE_MODELS = {v: k for k, v in MODEL_DISPLAY_NAMES.items()}

# ----- session state init -----
# messy but works
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "🚀 Gemini 1.5 Flash"

if "stop_requested" not in st.session_state:
    st.session_state.stop_requested = False

if "generating" not in st.session_state:
    st.session_state.generating = False

if "show_help" not in st.session_state:
    st.session_state.show_help = True

# ----- sidebar setup -----
with st.sidebar:
    st.header("🛠️ Control Panel")
    
    # model selection
    current_model = st.selectbox(
        "Select AI Model:",
        list(AVAILABLE_MODELS.keys()),
        index=0,
        help="Different models have different strengths"
    )
    
    # advanced settings
    st.subheader("⚙️ Tuning Parameters")
    temp = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1,
                    help="0 = strict, 1 = creative")
    top_k = st.slider("Top K", 1, 100, 40,
                     help="Number of candidates to consider")
    top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1,
                     help="Probability mass to consider")
    max_tokens = st.slider("Max Tokens", 100, 32000, 4096,
                          help="Maximum response length")
    
    # model instance with settings
    model = genai.GenerativeModel(
        model_name=AVAILABLE_MODELS[current_model],
        generation_config=genai.types.GenerationConfig(
            temperature=temp,
            top_k=top_k,
            top_p=top_p,
            max_output_tokens=max_tokens,
        )
    )
    
    # clear history button
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.session_state.show_help = True
        st.toast("Chat history cleared!", icon="⚠️")
    
    # model info
    with st.expander("ℹ️ Model Info"):
        st.markdown("""
            - **Flash 1.5**: General purpose
            - **Flash 2.0**: Better responses
            - **Thinking 2.0**: Better reasoning
            - **1206 Exp**: Advance model for maths and science
            - **LearnLM**: Educational focus
        """)
    
    st.markdown("---")
    st.markdown("**⚠️ Warning:**\n- Outputs may be inaccurate\n- Don't share sensitive info")

# ----- main chat area -----
st.title("💬 AI Chat Interface")
st.caption("v1.3 | Sometimes gets confused")

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(
                f"📋 Copy ({msg['time']})",
                key=f"copy_{msg['time']}",
                help="Copy this response"
            ):
                pyperclip.copy(msg["content"])
                st.toast("Copied!", icon="✅")


# Handle new input
user_input = st.chat_input("Type your message here...")
if user_input:
    # Immediately add and display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.show_help = False
    
    # Generate response
    with st.chat_message("assistant"):
        response_box = st.empty()
        full_response = ""
        
        try:
            st.session_state.generating = True
            response = model.generate_content(user_input, stream=True)
            
            for chunk in response:
                if st.session_state.stop_requested:
                    break
                full_response += chunk.text
                response_box.markdown(full_response + "▌")
                time.sleep(0.02)
            
            response_box.markdown(full_response)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "time": datetime.now().strftime("%H:%M:%S")
            })
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            st.session_state.generating = False

# stop button during generation
if st.session_state.generating:
    if st.button("⏹️ Stop Generating", type="primary"):
        st.session_state.stop_requested = True
        st.toast("Stopping...", icon="⏳")

# help section when empty
if st.session_state.show_help and not st.session_state.messages:
    st.markdown("---")
    st.subheader("Getting Started Guide")
    
    cols = st.columns(2)
    with cols[0]:
        st.markdown("""
            **📌 Quick Tips:**
            - Change models for different tasks
            - Lower temp for factual answers
            - Higher temp for creative writing
            - Use stop button if stuck
        """)
    
    with cols[1]:
        st.markdown("""
            **🔧 Troubleshooting:**
            - Slow? Reduce max tokens
            - Errors? Check API key
            - Weird answers? Adjust temp
        """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using [Gemini API](https://ai.google.dev/) and [Streamlit](https://streamlit.io/)")

# debug section (hidden)
if os.getenv("DEBUG_MODE") == "True":
    st.sidebar.markdown("---")
    st.sidebar.write("**Debug Info:**")
    st.sidebar.json({
        "messages_count": len(st.session_state.messages),
        "current_model": st.session_state.selected_model,
        "last_update": datetime.now().isoformat()
    })