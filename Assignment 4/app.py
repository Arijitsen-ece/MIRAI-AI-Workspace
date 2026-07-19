"""
Main application file strictly for UI rendering and state management.
Business logic is imported from supporting modules.
"""
import streamlit as st
import random
from prompt_library import ART_STYLES, MAGIC_ENHANCE_PROMPT, SURPRISE_PROMPTS
from image_api import build_image_url, fetch_image
from ui_utils import inject_custom_css, render_metrics

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)
inject_custom_css()

# ==========================================
# SESSION STATE MANAGEMENT
# ==========================================
if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "gen_count" not in st.session_state:
    st.session_state.gen_count = 0
if "last_style" not in st.session_state:
    st.session_state.last_style = "Realistic"

def set_surprise_prompt():
    """Callback to inject a random prompt into the text area."""
    st.session_state.prompt_text = random.choice(SURPRISE_PROMPTS)

# ==========================================
# SIDEBAR LAYOUT
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:0;'>🎨 AI Image Studio</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-top:0;'>Design studio interface</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### Image Settings")
    selected_style = st.selectbox("Art Style", options=list(ART_STYLES.keys()))
    
    width = st.slider("Width (px)", min_value=256, max_value=1920, value=1024, step=64)
    height = st.slider("Height (px)", min_value=256, max_value=1080, value=1024, step=64)
    
    st.divider()
    enhance = st.checkbox("✨ Magic Enhance", value=True)
    
    st.divider()
    st.markdown("<small style='color:#64748B;'>Assignment 4 - MirAI AI Builder Internship</small>", unsafe_allow_html=True)

# ==========================================
# MAIN PANEL LAYOUT
# ==========================================
st.markdown("<h1>Workspace</h1>", unsafe_allow_html=True)

# Fixed presentation split workspace column layout
left_col, right_col = st.columns([1, 1.2], gap="medium")

with left_col:
    st.markdown("<h3 style='margin-bottom:0;'>Prompt Engineering</h3>", unsafe_allow_html=True)
    
    user_prompt = st.text_area(
        "Describe your image in detail", 
        key="prompt_text",
        height=120,
        placeholder="A cinematic shot of a..."
    )
    
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        generate_clicked = st.button("🚀 Generate Image", use_container_width=True, type="primary")
    with btn_col2:
        st.button("🎲 Surprise Me", use_container_width=True, on_click=set_surprise_prompt, type="secondary")

    if generate_clicked:
        if not user_prompt.strip():
            st.warning("Please enter a prompt or use the Surprise Me button.")
        else:
            with st.spinner("Rendering image..."):
                target_url = build_image_url(
                    prompt=user_prompt,
                    style=selected_style,
                    width=width,
                    height=height,
                    enhance=enhance,
                    magic_prompt=MAGIC_ENHANCE_PROMPT,
                    style_prompts=ART_STYLES
                )
                
                success, image_data, message = fetch_image(target_url)
                
                if success:
                    st.session_state.image_bytes = image_data
                    st.session_state.gen_count += 1
                    st.session_state.last_style = selected_style
                else:
                    st.error(message)

with right_col:
    st.markdown("<h3 style='margin-bottom:0;'>Preview</h3>", unsafe_allow_html=True)
    
    # Controlled container size to enforce absolute window scaling constraints
    preview_container = st.container(height=360, border=True)
    with preview_container:
        if st.session_state.image_bytes:
            # FIXED: Changed use_column_width to use_container_width
            st.image(st.session_state.image_bytes, use_container_width=True)
        else:
            st.markdown(
                """
                <div style='display: flex; justify-content: center; align-items: center; height: 100%; color: #64748B;'>
                    Your generated image will appear here.
                </div>
                """, 
                unsafe_allow_html=True
            )
            
    if st.session_state.image_bytes:
        clean_style_name = st.session_state.last_style.replace(" ", "_")
        dynamic_filename = f"{clean_style_name}_image.png"
        
        st.download_button(
            label="💾 Download Image",
            data=st.session_state.image_bytes,
            file_name=dynamic_filename,
            mime="image/png",
            use_container_width=True
        )

# ==========================================
# METRICS PANEL
# ==========================================
st.divider()
render_metrics(
    width=width, 
    height=height, 
    style=selected_style, 
    enhance=enhance, 
    count=st.session_state.gen_count
)