"""
Main application file containing the Streamlit UI, Cyber Aurora theme, 
and unified Session State management.
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
# PAGE CONFIGURATION & CSS
# ==========================================
st.set_page_config(
    page_title="AI Multiverse - Memory Vault",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cyber Aurora Custom Theme
st.markdown("""
<style>
    /* Main Backgrounds */
    .stApp { background-color: #0B1020 !important; }
    [data-testid="stSidebar"] { background-color: #12182B !important; border-right: 1px solid #1A2138; }
    
    /* Typography & Colors */
    h1, h2, h3, p, span, div { color: #E2E8F0 !important; }
    .primary-text { color: #7C5CFF !important; }
    .secondary-text { color: #38BDF8 !important; }
    .accent-text { color: #22D3EE !important; }
    
    /* Glassmorphism Chat & Cards */
    .stChatInputContainer { background-color: #12182B !important; border-color: #7C5CFF !important; }
    [data-testid="stChatMessage"] { background-color: #1A2138 !important; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] { color: #22D3EE !important; font-size: 1.5rem !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #38BDF8 !important; font-size: 0.9rem !important; }
    
    /* Layout Adjustments */
    .block-container { padding-top: 2rem !important; max-width: 90% !important; }
    header, footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
# Single unified conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Metrics for the latest interaction
if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "time": 0.0, "chars": 0, "words": 0, "tokens": 0
    }

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.markdown("<h2 class='primary-text'>🌌 AI Multiverse</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8B949E !important;'>Memory Vault Edition</p>", unsafe_allow_html=True)
    st.divider()

    # Persona Settings
    st.markdown("### Settings")
    selected_persona = st.selectbox("Active Persona", options=list(PERSONAS.keys()))
    temperature = st.slider("Creativity (Temp)", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max Output Tokens", 256, 8192, 2048, 256)
    
    st.divider()
    
    # Session Management
    st.markdown("### Session Controls")
    if st.button("🗑️ Clear Memory Vault", use_container_width=True):
        st.session_state.messages = []
        st.session_state.metrics = {"time": 0.0, "chars": 0, "words": 0, "tokens": 0}
        st.rerun()

    # Export Tools
    st.markdown("### Export Conversation")
    c1, c2, c3 = st.columns(3)
    has_history = len(st.session_state.messages) > 0
    with c1:
        st.download_button("TXT", data=export_chat_txt(st.session_state.messages), file_name="vault_export.txt", mime="text/plain", disabled=not has_history)
    with c2:
        st.download_button("MD", data=export_chat_md(st.session_state.messages), file_name="vault_export.md", mime="text/markdown", disabled=not has_history)
    with c3:
        st.download_button("JSON", data=export_chat_json(st.session_state.messages), file_name="vault_export.json", mime="application/json", disabled=not has_history)

    st.divider()
    st.markdown("<small style='color: #4B5563 !important;'>Assignment 3: MirAI AI Builder Internship</small>", unsafe_allow_html=True)

# ==========================================
# MAIN PANEL
# ==========================================
st.markdown("<h1 class='primary-text' style='text-align: center; margin-bottom: 0;'>AI Multiverse</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='secondary-text' style='text-align: center; margin-top: 0; margin-bottom: 2rem;'>Memory Vault</h3>", unsafe_allow_html=True)

# Metrics Dashboard
m1, m2, m3, m4, m5 = st.columns(5)
metrics = st.session_state.metrics
m1.metric("Response Time", f"{metrics['time']:.2f}s")
m2.metric("Characters", metrics['chars'])
m3.metric("Words", metrics['words'])
m4.metric("Est. Tokens", metrics['tokens'])
m5.metric("Total Messages", len(st.session_state.messages))

st.markdown("<br>", unsafe_allow_html=True)

# Chat Area (Fixed height container for seamless UX)
chat_container = st.container(height=450, border=False)

with chat_container:
    # Render unified memory
    for message in st.session_state.messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# ==========================================
# CHAT INPUT & PROCESSING
# ==========================================
if prompt := st.chat_input(f"Message the {selected_persona}..."):
    
    # Render user prompt instantly
    with chat_container:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
            
    # Append to memory vault
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Process AI Response
    with chat_container:
        with st.chat_message("assistant", avatar="🤖"):
            start_time = time.time()
            
            # The spinner provides visual feedback before the stream starts yielding
            with st.spinner("Processing in Memory Vault..."):
                stream = generate_chat_stream(
                    prompt=prompt,
                    history=st.session_state.messages[:-1], # Send history excluding current prompt
                    system_instruction=PERSONAS[selected_persona],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
            # Streamlit natively handles the generator mapping to UI
            full_response = st.write_stream(stream)
            
            end_time = time.time()
            
    # Save response to memory and update metrics
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    st.session_state.metrics = {
        "time": end_time - start_time,
        "chars": count_characters(full_response),
        "words": count_words(full_response),
        "tokens": estimate_tokens(full_response)
    }
    
    # Force rerun to update top metrics panel immediately
    st.rerun()