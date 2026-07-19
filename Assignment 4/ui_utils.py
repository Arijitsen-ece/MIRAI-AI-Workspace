"""
Handles UI injection, CSS styling, and component rendering for a clean SaaS aesthetic.
"""
import streamlit as st

def inject_custom_css() -> None:
    """Injects a light modern theme while fully preventing scrolling and fixing element leaks."""
    st.markdown(
        """
        <style>
        /* Force root html/body viewport limits */
        html, body, [data-testid="stAppViewContainer"] {
            overflow: hidden !important;
            height: 100vh !important;
        }

        /* Base Backgrounds */
        .stApp { background-color: #F8FAFC !important; }
        [data-testid="stSidebar"] { 
            background-color: #FFFFFF !important; 
            border-right: 1px solid #E2E8F0 !important; 
        }
        
        /* HARD FIX: Remove the default Streamlit sidebar collapse button text leak */
        [data-testid="stSidebarCollapseButton"], 
        header, 
        footer, 
        .stAppDeployButton { 
            display: none !important; 
            visibility: hidden !important; 
        }
        
        /* Compact application container padding */
        .block-container { 
            padding-top: 0.75rem !important; 
            padding-bottom: 0rem !important; 
            max-width: 96% !important; 
        }
        
        /* Typography */
        h1, h2, h3, h4, p, span, label { color: #0F172A !important; font-family: 'Inter', sans-serif !important; }
        h1 { margin-bottom: 0.5rem !important; font-size: 1.75rem !important; }
        .stMarkdown p { color: #64748B !important; margin-bottom: 0.25rem !important; }
        
        /* Form Inputs & Sizing */
        .stTextInput > div > div > input, .stTextArea > div > textarea {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
            border-radius: 6px !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        }
        
        /* Tighten default element gaps */
        [data-testid="stVerticalBlock"] {
            gap: 0.5rem !important;
        }
        
        /* Standard Buttons (Generate, etc.) */
        .stButton > button {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            padding: 0.4rem 1rem !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
            transition: background-color 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #3B82F6 !important;
            color: #FFFFFF !important;
        }
        
        /* Outline variant for Surprise Button */
        [data-testid="stButton"] button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            border: 1px solid #E2E8F0 !important;
        }
        
        /* DOWNLOAD BUTTON STYLING (Emerald Green) */
        [data-testid="stDownloadButton"] button {
            background-color: #10B981 !important; 
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        }
        [data-testid="stDownloadButton"] button:hover {
            background-color: #059669 !important; 
            color: #FFFFFF !important;
        }
        
        /* Metric Cards Matrix Configuration */
        [data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            padding: 0.5rem 0.75rem !important;
            border-radius: 8px !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.01) !important;
        }
        [data-testid="stMetricValue"] { color: #2563EB !important; font-size: 1.15rem !important; font-weight: 700 !important; }
        [data-testid="stMetricLabel"] { color: #64748B !important; font-size: 0.75rem !important; font-weight: 500 !important; }
        </style>
        """, 
        unsafe_allow_html=True
    )

def render_metrics(width: int, height: int, style: str, enhance: bool, count: int) -> None:
    """Renders the generation metrics in a clean row."""
    st.markdown("<h4 style='margin-top:0.25rem; margin-bottom:0.25rem;'>Generation Details</h4>", unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Resolution", f"{width} × {height}")
    m2.metric("Art Style", style)
    m3.metric("Magic Enhance", "Active" if enhance else "Off")
    m4.metric("Engine", "Pollinations")
    m5.metric("Total Generations", count)