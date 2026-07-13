"""
Main Streamlit UI application. No business logic, purely UI rendering and state management.
"""
import streamlit as st
import time
from prompts import PERSONAS
from utils import (
    estimate_tokens, count_words, count_characters, 
    export_chat_txt, export_chat_md, export_chat_json
)
from gemini_api import generate_chat_stream

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI Multiverse",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS (SaaS UI & No-Scroll Constraints)
# ==========================================
st.markdown("""
<style>
    /* Prevent main page scrolling and hide default padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 95% !important;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Glassmorphism Dark Theme Styling */
    [data-testid="stSidebar"] {
        background-color: #0E1117 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    .stChatInputContainer {
        padding-bottom: 10px !important;
    }

    /* Metric cards styling */
    [data-testid="stMetricValue"] {
        font-size: 1.2rem !important;
        color: #4CAF50;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        color: #A0AEC0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "current_persona" not in st.session_state:
    st.session_state.current_persona = list(PERSONAS.keys())[0]

# Initialize independent chat history for each persona
if "chats" not in st.session_state:
    st.session_state.chats = {persona: [] for persona in PERSONAS.keys()}

# Initialize independent metrics tracking for each persona
if "metrics" not in st.session_state:
    st.session_state.metrics = {
        persona: {"time": 0.0, "words": 0, "chars": 0, "tokens": 0} 
        for persona in PERSONAS.keys()
    }

# ==========================================
# SIDEBAR LAYOUT
# ==========================================
with st.sidebar:
    st.markdown("### 🌌 AI Multiverse")
    st.caption("Experience Conversations with Multiple AI Personalities")
    st.divider()

    # Persona Selection
    selected_persona = st.selectbox(
        "Choose your AI Universe:",
        options=list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.current_persona)
    )
    
    # Check if persona changed to update state correctly
    if selected_persona != st.session_state.current_persona:
        st.session_state.current_persona = selected_persona
        st.rerun()

    current_history = st.session_state.chats[selected_persona]

    # Model Parameters
    st.markdown("#### Settings")
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1, help="Higher values make output more random.")
    max_tokens = st.slider("Max Tokens", min_value=100, max_value=8192, value=2048, step=100, help="Maximum length of the AI's response.")
    
    st.divider()
    
    # Session Controls
    st.markdown(f"**Messages:** {len(current_history)}")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chats[selected_persona] = []
        st.session_state.metrics[selected_persona] = {"time": 0.0, "words": 0, "chars": 0, "tokens": 0}
        st.rerun()

    # Export functionality
    st.markdown("#### Export Chat")
    exp_col1, exp_col2, exp_col3 = st.columns(3)
    
    with exp_col1:
        st.download_button("TXT", data=export_chat_txt(current_history), file_name=f"{selected_persona}_chat.txt", mime="text/plain", use_container_width=True)
    with exp_col2:
        st.download_button("MD", data=export_chat_md(current_history), file_name=f"{selected_persona}_chat.md", mime="text/markdown", use_container_width=True)
    with exp_col3:
        st.download_button("JSON", data=export_chat_json(current_history), file_name=f"{selected_persona}_chat.json", mime="application/json", use_container_width=True)
        
    st.divider()
    st.caption("Built for MirAI School of Technology Internship.")

# ==========================================
# MAIN PAGE LAYOUT
# ==========================================
# Metrics row
m1, m2, m3, m4 = st.columns(4)
current_metrics = st.session_state.metrics[selected_persona]

m1.metric("Response Time", f"{current_metrics['time']:.2f}s")
m2.metric("Word Count", current_metrics['words'])
m3.metric("Characters", current_metrics['chars'])
m4.metric("Est. Tokens", current_metrics['tokens'])

# Chat Container - Fixed height to ensure it fits on 1366x768 without page scroll
chat_container = st.container(height=480, border=False)

# Render Chat History
with chat_container:
    for message in current_history:
        avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input(f"Talk to the {selected_persona}..."):
    
    # 1. Display User Message
    with chat_container:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
            
    # 2. Add User Message to History
    st.session_state.chats[selected_persona].append({"role": "user", "content": prompt})
    
    # 3. Generate AI Response
    with chat_container:
        with st.chat_message("assistant", avatar="🤖"):
            system_instruction = PERSONAS[selected_persona]
            
            # Record start time
            start_time = time.time()
            
            # Stream response
            stream = generate_chat_stream(
                prompt=prompt,
                history=st.session_state.chats[selected_persona][:-1], # Exclude current prompt from history
                system_instruction=system_instruction,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            full_response = st.write_stream(stream)
            
            # Record end time & calculate metrics
            end_time = time.time()
            
    # 4. Save AI Response and update metrics
    st.session_state.chats[selected_persona].append({"role": "assistant", "content": full_response})
    
    st.session_state.metrics[selected_persona] = {
        "time": end_time - start_time,
        "words": count_words(full_response),
        "chars": count_characters(full_response),
        "tokens": estimate_tokens(full_response)
    }
    
    # 5. Rerun to update metrics display at the top
    st.rerun()