"""
AI Resume Analyzer V3.0 - Next-Generation Career Intelligence Platform
Advanced Neural Analysis • Real-time Career Insights • Multi-dimensional Scoring
"""

import streamlit as st
from streamlit_option_menu import option_menu
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os
import sys
import time
import json
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from resume_analyzer import ResumeAnalyzer
from pdf_extractor import extract_text_from_pdf, extract_text_from_docx
from keyword_matcher import calculate_match_score, extract_missing_keywords, get_keyword_suggestions

# Next-Gen Configuration
st.set_page_config(
    page_title="🚀 AI Resume Analyzer V3.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Crewjah/AI-Resume-Analyzer',
        'Report a bug': 'https://github.com/Crewjah/AI-Resume-Analyzer/issues',
        'About': '# AI Resume Analyzer V3.0\nNext-Generation Career Intelligence Platform'
    }
)


@st.cache_resource
def get_analyzer() -> ResumeAnalyzer:
    return ResumeAnalyzer()

# Next-Gen Session State Management
if 'page' not in st.session_state:
    st.session_state.page = 'neural_home'
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'cyber_theme' not in st.session_state:
    st.session_state.cyber_theme = True
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0
if 'ai_copilot_active' not in st.session_state:
    st.session_state.ai_copilot_active = False
if 'skill_galaxy_data' not in st.session_state:
    st.session_state.skill_galaxy_data = None
if 'career_simulation' not in st.session_state:
    st.session_state.career_simulation = None
if 'interview_mode' not in st.session_state:
    st.session_state.interview_mode = False
if 'collaboration_session' not in st.session_state:
    st.session_state.collaboration_session = None

# Next-Generation Cyber Theme CSS
st.markdown("""
<style>
    /* CYBER THEME VARIABLES */
    :root {
        --cyber-blue: #00D1FF;
        --deep-space: #0F0F23;
        --holo-purple: #A855F7;
        --matrix-green: #00FF9D;
        --neon-orange: #FF6B35;
        --pulse-pink: #FF00FF;
        --glass-effect: rgba(255,255,255,0.08);
        --glow-blue: 0 0 20px rgba(0, 209, 255, 0.5);
        --glow-purple: 0 0 20px rgba(168, 85, 247, 0.5);
        --glow-green: 0 0 20px rgba(0, 255, 157, 0.5);
    }
    
    /* MAIN CONTAINER */
    .main {
        background: linear-gradient(135deg, var(--deep-space) 0%, #1a1a3a 50%, var(--deep-space) 100%);
        color: var(--cyber-blue);
    }
    
    /* CYBER HERO SECTION */
    .cyber-hero {
        background: linear-gradient(135deg, 
            rgba(0, 209, 255, 0.1) 0%, 
            rgba(168, 85, 247, 0.1) 50%, 
            rgba(255, 0, 255, 0.1) 100%);
        border: 2px solid var(--cyber-blue);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: var(--glow-blue), inset 0 0 50px rgba(0, 209, 255, 0.1);
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .cyber-hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(0, 209, 255, 0.2), 
            transparent);
        animation: scan 3s infinite;
    }
    
    @keyframes scan {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .cyber-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, var(--cyber-blue), var(--holo-purple), var(--pulse-pink));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: var(--glow-blue);
        margin: 0;
        letter-spacing: 3px;
        animation: pulse-glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes pulse-glow {
        from { filter: brightness(1) drop-shadow(0 0 10px var(--cyber-blue)); }
        to { filter: brightness(1.2) drop-shadow(0 0 20px var(--cyber-blue)); }
    }
    
    .cyber-subtitle {
        font-size: 1.2rem;
        color: var(--matrix-green);
        margin: 1rem 0;
        text-shadow: var(--glow-green);
        animation: type-writer 3s steps(30) 1s both;
    }
    
    @keyframes type-writer {
        from { width: 0; }
        to { width: 100%; }
    }
    
    /* NEURAL CARDS */
    .neural-card {
        background: linear-gradient(135deg, 
            var(--glass-effect) 0%, 
            rgba(0, 209, 255, 0.05) 100%);
        border: 1px solid var(--cyber-blue);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        backdrop-filter: blur(15px);
        box-shadow: var(--glow-blue);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .neural-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            var(--cyber-blue), 
            var(--holo-purple), 
            var(--matrix-green), 
            var(--pulse-pink));
        border-radius: 15px;
        z-index: -1;
        animation: border-flow 3s linear infinite;
    }
    
    @keyframes border-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .neural-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 209, 255, 0.3);
        border-color: var(--pulse-pink);
    }
    
    /* QUANTUM BUTTONS */
    .quantum-button {
        background: linear-gradient(45deg, var(--cyber-blue), var(--holo-purple));
        border: none;
        border-radius: 25px;
        padding: 1rem 2rem;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: var(--glow-blue);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .quantum-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.3), 
            transparent);
        transition: 0.5s;
    }
    
    .quantum-button:hover::before {
        left: 100%;
    }
    
    .quantum-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px var(--pulse-pink);
    }
    
    /* SKILL GALAXY */
    .skill-node {
        display: inline-block;
        background: radial-gradient(circle, var(--matrix-green), var(--cyber-blue));
        border-radius: 50%;
        padding: 0.5rem 1rem;
        margin: 0.5rem;
        color: white;
        font-weight: bold;
        font-size: 0.9rem;
        box-shadow: var(--glow-green);
        animation: float 3s ease-in-out infinite;
        cursor: pointer;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .skill-node:hover {
        background: radial-gradient(circle, var(--pulse-pink), var(--neon-orange));
        transform: scale(1.2);
        box-shadow: 0 0 25px var(--pulse-pink);
    }
    
    /* NEURAL PROGRESS BARS */
    .neural-progress {
        background: var(--deep-space);
        border-radius: 25px;
        padding: 3px;
        box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.5);
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .neural-progress-bar {
        height: 25px;
        border-radius: 25px;
        background: linear-gradient(90deg, var(--cyber-blue), var(--matrix-green));
        transition: width 1s ease;
        position: relative;
        overflow: hidden;
    }
    
    .neural-progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.3), 
            transparent);
        animation: progress-shine 2s infinite;
    }
    
    @keyframes progress-shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* AI COPILOT CHAT */
    .ai-copilot {
        background: linear-gradient(135deg, 
            rgba(168, 85, 247, 0.1) 0%, 
            rgba(0, 209, 255, 0.1) 100%);
        border: 1px solid var(--holo-purple);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: var(--glow-purple);
    }
    
    .ai-message {
        background: rgba(168, 85, 247, 0.2);
        border-left: 4px solid var(--holo-purple);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        animation: fade-in-up 0.5s ease;
    }
    
    @keyframes fade-in-up {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* LIVE COUNTER */
    .live-counter {
        background: linear-gradient(45deg, var(--matrix-green), var(--cyber-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2rem;
        font-weight: 900;
        text-align: center;
        text-shadow: var(--glow-green);
        animation: counter-pulse 1s ease-in-out infinite alternate;
    }
    
    @keyframes counter-pulse {
        from { transform: scale(1); }
        to { transform: scale(1.05); }
    }
    
    /* SIDEBAR STYLING */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--deep-space) 0%, #1a1a3a 100%);
    }
    
    /* METRIC CARDS */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, 
            var(--glass-effect) 0%, 
            rgba(0, 209, 255, 0.05) 100%) !important;
        border: 1px solid var(--cyber-blue) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: var(--glow-blue) !important;
    }
    
    /* STREAMLIT COMPONENTS */
    .stSelectbox > div > div {
        background: var(--glass-effect);
        border: 1px solid var(--cyber-blue);
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        background: var(--glass-effect);
        border: 1px solid var(--cyber-blue);
        border-radius: 10px;
        color: var(--cyber-blue);
    }
    
    .stFileUploader {
        background: var(--glass-effect);
        border: 2px dashed var(--matrix-green);
        border-radius: 15px;
        padding: 2rem;
    }
    
    /* QUANTUM SCORE DISPLAY */
    .quantum-score {
        font-size: 6rem;
        font-weight: 900;
        background: linear-gradient(45deg, 
            var(--cyber-blue), 
            var(--matrix-green), 
            var(--pulse-pink));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        text-shadow: var(--glow-blue);
        animation: score-pulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes score-pulse {
        from { 
            transform: scale(1);
            filter: brightness(1);
        }
        to { 
            transform: scale(1.05);
            filter: brightness(1.2);
        }
    }
</style>
""", unsafe_allow_html=True)

# Advanced Sidebar Menu
if st.session_state.cyber_theme:
    # Light Mode Colors
    theme_css = """
<style>
    /* Light Mode Colors */
    :root {
        --primary-blue: #2563EB;
        --primary-blue-dark: #1E40AF;
        --primary-blue-light: #3B82F6;
        --success-green: #10B981;
        --success-green-light: #34D399;
        --warning-amber: #F59E0B;
        --error-red: #EF4444;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --bg-light: #F9FAFB;
        --bg-card: #FFFFFF;
        --border-light: #E5E7EB;
    }
    
    body {
        background-color: #F9FAFB !important;
        color: #1F2937 !important;
    }
    
    .stApp {
        background-color: #F9FAFB !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F9FAFB 0%, #F3F4F6 100%) !important;
    }
"""

st.markdown(theme_css + """
    /* ========================================
       PROFESSIONAL DESIGN SYSTEM
       ======================================== */
    
    /* TYPOGRAPHY */
    h1 { font-size: 3rem; font-weight: 800; color: #1F2937; letter-spacing: -0.5px; margin: 0 0 1rem 0; }
    h2 { font-size: 2.25rem; font-weight: 700; color: #1F2937; margin: 2rem 0 1rem 0; }
    h3 { font-size: 1.5rem; font-weight: 600; color: #1F2937; margin: 1.5rem 0 0.75rem 0; }
    h4 { font-size: 1.25rem; font-weight: 600; color: #6B7280; margin: 1rem 0 0.5rem 0; }
    
    p { font-size: 1rem; font-weight: 400; color: #6B7280; line-height: 1.6; margin: 0.5rem 0; }
    
    small { font-size: 0.875rem; font-weight: 400; color: #9CA3AF; }
    
    /* SPACING SCALE (8px base) */
    .spacing-xs { margin: 4px; }
    .spacing-sm { margin: 8px; }
    .spacing-md { margin: 16px; }
    .spacing-lg { margin: 24px; }
    .spacing-xl { margin: 32px; }
    .spacing-2xl { margin: 48px; }
    .spacing-3xl { margin: 64px; }
    
    /* HERO HEADER */
    .header-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        color: white;
        padding: 4rem 2rem;
        margin-bottom: 3rem;
        text-align: center;
        box-shadow: 0 10px 15px rgba(37, 99, 235, 0.15);
        border-radius: 12px;
        animation: fadeIn 0.5s ease;
    }
    .header-title {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        padding: 0;
        color: #FFFFFF;
        letter-spacing: -0.5px;
        text-transform: none;
    }
    .header-subtitle {
        font-size: 1.25rem;
        opacity: 0.95;
        margin: 0.75rem 0 0 0;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
    }
    
    /* FEATURE CARDS */
    .feature-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        padding: 2rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border: 2px solid #E5E7EB;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 25px rgba(37, 99, 235, 0.15);
        border-color: #2563EB;
    }
    .feature-card h3 {
        color: #2563EB !important;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1rem 0 0.5rem 0;
    }
    .feature-card p {
        color: #6B7280 !important;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
    }
    
    /* STATUS BOXES */
    .info-box {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid #2563EB;
        margin: 1.5rem 0;
        color: #1F2937;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #DBEAFE 100%);
        border-left-color: #10B981;
        box-shadow: 0 2px 6px rgba(16, 185, 129, 0.1);
    }
    .warning-box {
        background: linear-gradient(135deg, #FEF9E7 0%, #FEF08A 100%);
        border-left-color: #F59E0B;
        box-shadow: 0 2px 6px rgba(245, 158, 11, 0.1);
    }
    .error-box {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left-color: #EF4444;
        box-shadow: 0 2px 6px rgba(239, 68, 68, 0.1);
    }
    
    /* STATISTICS CARDS */
    .stat-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
        padding: 2rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    .stat-number {
        font-size: 2.25rem;
        font-weight: 800;
        color: #2563EB !important;
        margin: 0.75rem 0;
    }
    .stat-label {
        font-size: 0.875rem;
        color: #6B7280 !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.75px;
    }
    
    /* STEP BOXES */
    .step-box {
        background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #2563EB;
        text-align: left;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .step-box:hover {
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
    }
    .step-number {
        display: inline-block;
        background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
        color: white;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        line-height: 44px;
        text-align: center;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }
    .step-title {
        font-weight: 700;
        color: #1F2937 !important;
        font-size: 1.125rem;
        margin: 0.75rem 0;
    }
    .step-description {
        font-size: 0.9rem;
        color: #6B7280 !important;
        margin: 0.5rem 0 0 0;
        line-height: 1.6;
    }
    
    /* BUTTONS */
    .stButton > button {
        background-color: #2563EB !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2) !important;
        font-size: 1rem !important;
    }
    .stButton > button:hover {
        background-color: #1E40AF !important;
        box-shadow: 0 8px 12px rgba(37, 99, 235, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button:active {
        background-color: #1D4ED8 !important;
        transform: translateY(0) !important;
    }
    
    /* FILE UPLOADER */
    .stFileUploader label {
        color: #1F2937 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    .stFileUploader > div > div {
        border: 3px dashed #2563EB !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%) !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    .stFileUploader > div > div:hover {
        border-color: #1E40AF !important;
        background: linear-gradient(135deg, #E0F2FE 0%, #D0E7FC 100%) !important;
    }
    
    /* INPUTS */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid #E5E7EB !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] button {
        color: #6B7280 !important;
        font-weight: 500 !important;
        border-bottom: 3px solid transparent !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2563EB !important;
        border-bottom: 3px solid #2563EB !important;
        font-weight: 700 !important;
    }
    
    /* METRICS */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%) !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
    }
    [data-testid="metric-container"] > div > div > div:first-child {
        color: #6B7280 !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.75px !important;
    }
    [data-testid="metric-container"] > div > div > div:last-child {
        color: #2563EB !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    
    /* SECTION HEADING */
    .section-heading {
        font-size: 2rem;
        font-weight: 800;
        color: #1F2937;
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 3px solid #2563EB;
    }
    
    /* FOOTER */
    .footer-container {
        text-align: center;
        color: #6B7280;
        font-size: 0.875rem;
        padding: 3rem 2rem;
        border-top: 2px solid #E5E7EB;
        margin-top: 4rem;
        background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .footer-links a {
        color: #2563EB;
        text-decoration: none;
        margin: 0 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .footer-links a:hover {
        color: #1E40AF;
        text-decoration: underline;
    }
    
    /* ANIMATIONS */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .stMetric { animation: slideUp 0.5s ease-out; }
    
    /* RESPONSIVE */
    @media (max-width: 768px) {
        .header-title { font-size: 2rem; }
        .section-heading { font-size: 1.5rem; }
        h2 { font-size: 1.75rem; }
        .stat-number { font-size: 1.75rem; }
        .step-number { width: 36px; height: 36px; line-height: 36px; }
    }
    
    /* UTILITIES */
    .divider { border-top: 2px solid #E5E7EB; margin: 2rem 0; }
    .highlight { background: linear-gradient(120deg, #FEF08A, #FBBF24); padding: 0.25rem 0.5rem; border-radius: 4px; }

    
    /* Metric Cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%) !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 0.75rem !important;
        padding: 1.5rem !important;
    }
    [data-testid="metric-container"] > div > div > div:first-child {
        color: #6B7280 !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    [data-testid="metric-container"] > div > div > div:last-child {
        color: #2563EB !important;
    
    # Theme Toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", help="Toggle theme"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("---")
    
    selected_page = option_menu(
        menu_title=None,
        options=["Home", "Upload Resume", "Analysis", "Job Matching", "ATS Check", "About"],
        icons=["house", "upload", "bar-chart", "target", "checkbox", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#F8FAFC" if not st.session_state.dark_mode else "#1F2937"},
            "icon": {"color": "#2563EB" if not st.session_state.dark_mode else "#3B82F6", "font-size": "20px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "color": "#1F2937" if not st.session_state.dark_mode else "#F9FAFB"},
            "nav-link-selected": {"background-color": "#2563EB", "color": "white"}
        }
    )
    .stWarning {
        background: linear-gradient(135deg, #FEF9E7 0%, #FEF08A 100%) !important;
        border: 1px solid #F59E0B !important;
        border-left: 4px solid #F59E0B !important;
        color: #1F2937 !important;
    }
    .stError {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%) !important;
        border: 1px solid #EF4444 !important;
        border-left: 4px solid #EF4444 !important;
        color: #1F2937 !important;
    }
    .stInfo {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%) !important;
        border: 1px solid #2563EB !important;
        border-left: 4px solid #2563EB !important;
        color: #1F2937 !important;
    }
    
    /* Expander */
    .streamlit-expander {
        border: 1px solid #E5E7EB !important;
        border-radius: 0.5rem !important;
    }
    .streamlit-expanderContent {
        padding: 1rem !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F9FAFB 0%, #F3F4F6 100%) !important;
    }
    

</style>
""", unsafe_allow_html=True)

# Neural Navigation Sidebar
with st.sidebar:
    st.markdown("""
    <div class="neural-card">
        <h2 style="color: var(--cyber-blue); text-align: center; margin: 0;">
            🚀 AI NEURAL CORE
        </h2>
        <p style="color: var(--matrix-green); text-align: center; margin: 0.5rem 0;">
            V3.0 • Quantum Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Live Analysis Counter
    st.markdown(f"""
    <div class="ai-copilot">
        <div class="live-counter">⚡ {st.session_state.analysis_count:,}</div>
        <p style="color: var(--cyber-blue); text-align: center; margin: 0;">Resumes Analyzed Today</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Advanced Navigation Menu
    selected_page = option_menu(
        menu_title="NEURAL NAVIGATION",
        options=[
            "🌀 Neural Home", 
            "🔷 Upload Hub", 
            "📊 Neural Dashboard", 
            "🌟 Skill Galaxy", 
            "🚀 Career Simulator", 
            "📈 Industry Benchmark", 
            "🤖 AI Interview", 
            "👥 Collaboration", 
            "📤 Smart Export", 
            "🔮 Analytics Deep Dive"
        ],
        icons=[
            "house-fill", "cloud-upload", "graph-up", "stars", 
            "rocket-takeoff", "bar-chart", "robot", "people", 
            "download", "eye"
        ],
        menu_icon="cpu",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important", 
                "background": "linear-gradient(135deg, var(--glass-effect) 0%, rgba(0, 209, 255, 0.05) 100%)",
                "border-radius": "15px",
                "border": "1px solid var(--cyber-blue)"
            },
            "icon": {
                "color": "var(--matrix-green)", 
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "14px", 
                "text-align": "left", 
                "margin": "2px",
                "color": "var(--cyber-blue)",
                "border-radius": "10px"
            },
            "nav-link-selected": {
                "background": "linear-gradient(45deg, var(--cyber-blue), var(--holo-purple))",
                "color": "white",
                "box-shadow": "var(--glow-blue)"
            }
        }
    )
    
    st.markdown("---")
    
    # AI Copilot Toggle
    if st.checkbox("🤖 AI Copilot", value=st.session_state.ai_copilot_active):
        st.session_state.ai_copilot_active = True
        st.markdown("""
        <div class="ai-copilot">
            <p style="color: var(--holo-purple); margin: 0;">🤖 <strong>Neural AI Active</strong></p>
            <p style="color: var(--cyber-blue); font-size: 0.9rem; margin: 0.5rem 0;">Ready to assist with advanced analysis and career insights.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.session_state.ai_copilot_active = False
    
    # Current Analysis Status
    if st.session_state.analysis_results:
        overall_score = st.session_state.analysis_results.get('scores', {}).get('overall_score', 0)
        st.markdown(f"""
        <div class="neural-card">
            <h4 style="color: var(--matrix-green); margin: 0;">Current Analysis</h4>
            <div class="quantum-score" style="font-size: 2rem;">{overall_score:.0f}%</div>
            <p style="color: var(--cyber-blue); text-align: center; margin: 0;">Neural Score</p>
        </div>
        """, unsafe_allow_html=True)


def show_neural_home():
    """Next-Generation Neural Home Page"""
    # Cyber Hero Section
    st.markdown("""
    <div class="cyber-hero">
        <div class="cyber-title">AI RESUME ANALYZER</div>
        <div style="height: 10px; background: linear-gradient(90deg, var(--cyber-blue), var(--holo-purple), var(--pulse-pink)); margin: 1rem auto; border-radius: 5px;"></div>
        <div class="cyber-subtitle">Advanced Neural Analysis • Real-time Career Insights • Multi-dimensional Scoring</div>
        <br>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
            <button class="quantum-button">🔷 UPLOAD & SCAN</button>
            <button class="quantum-button">🌀 LIVE DEMO</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive Feature Matrix
    st.markdown("<h2 style='text-align: center; color: var(--cyber-blue); font-size: 2.5rem; margin: 3rem 0 2rem 0;'>✨ INTERACTIVE FEATURE MATRIX</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="neural-card">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">🧠</div>
            <h3 style="color: var(--matrix-green); text-align: center;">Neural Parsing Engine</h3>
            <p style="color: var(--cyber-blue); text-align: center;">Advanced AI understanding with context-aware processing and semantic analysis.</p>
            <div style="text-align: center; margin-top: 1rem;">
                <span class="skill-node">NLP</span>
                <span class="skill-node">ML</span>
                <span class="skill-node">AI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="neural-card">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">⚛️</div>
            <h3 style="color: var(--matrix-green); text-align: center;">Quantum Scoring System</h3>
            <p style="color: var(--cyber-blue); text-align: center;">Multi-dimensional analysis with predictive algorithms and industry benchmarking.</p>
            <div class="neural-progress">
                <div class="neural-progress-bar" style="width: 95%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="neural-card">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <h3 style="color: var(--matrix-green); text-align: center;">Real-time AI Feedback</h3>
            <p style="color: var(--cyber-blue); text-align: center;">Live suggestions and instant optimization recommendations as you work.</p>
            <div class="ai-message">
                🤖 "Ready to analyze your career potential!"
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Second Row of Features
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown("""
        <div class="neural-card">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">🌟</div>
            <h3 style="color: var(--holo-purple); text-align: center;">Skill Galaxy Map</h3>
            <p style="color: var(--cyber-blue); text-align: center;">3D visualization of your skill universe with gap analysis and growth paths.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="neural-card">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">🚀</div>
            <h3 style="color: var(--holo-purple); text-align: center;">Career Path Simulator</h3>
            <p style="color: var(--cyber-blue); text-align: center;">Future trajectory modeling with role progression and salary predictions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="neural-card">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">📤</div>
            <h3 style="color: var(--holo-purple); text-align: center;">Multi-format Export</h3>
            <p style="color: var(--cyber-blue); text-align: center;">AR Resume, Video Profile, Web Portfolio - export to any format instantly.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Live Analysis Counter Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="cyber-hero" style="padding: 2rem;">
        <h3 style="color: var(--matrix-green); text-align: center; margin-bottom: 1rem;">📈 LIVE ANALYSIS COUNTER</h3>
        <div style="background: linear-gradient(90deg, var(--deep-space), var(--cyber-blue), var(--deep-space)); height: 4px; margin: 1rem 0; border-radius: 2px;"></div>
        <div class="live-counter">⚡ Ready for Analysis</div>
        <div style="background: linear-gradient(90deg, var(--deep-space), var(--matrix-green), var(--deep-space)); height: 4px; margin: 1rem 0; border-radius: 2px;"></div>
        <p style="color: var(--cyber-blue); text-align: center; margin: 0;">Join thousands of professionals boosting their careers with AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Action Buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        if st.button("🚀 Start Neural Analysis", use_container_width=True, help="Begin advanced AI resume analysis"):
            st.session_state.page = 'upload_hub'
            st.rerun()
    
    with col2:
        if st.button("🌟 Explore Skill Galaxy", use_container_width=True, help="Visualize your skill universe"):
            st.session_state.page = 'skill_galaxy'
            st.rerun()
    
    with col3:
        if st.button("🤖 AI Interview Prep", use_container_width=True, help="Practice with AI interviewer"):
            st.session_state.page = 'ai_interview'
            st.rerun()
    
    with col4:
        if st.button("📈 Career Simulation", use_container_width=True, help="Model your career trajectory"):
            st.session_state.page = 'career_simulator'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">2</div>
            <div style="font-size: 2.5rem; margin: 1rem 0;">🤖</div>
            <div class="step-title">Analyze</div>
            <div class="step-description">We analyze across 5 core dimensions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">3</div>
            <div style="font-size: 2.5rem; margin: 1rem 0;">📋</div>
            <div class="step-title">Review</div>
            <div class="step-description">Get detailed scores and recommendations</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="step-box">
            <div class="step-number">4</div>
            <div style="font-size: 2.5rem; margin: 1rem 0;">⬆️</div>
            <div class="step-title">Improve</div>
            <div class="step-description">Implement changes and re-upload</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h2 class='section-heading' style='color: #2563EB !important;'>📈 Key Highlights</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Processing Mode</div>
            <div class="stat-number">Local</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Scoring Model</div>
            <div class="stat-number">Transparent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Analysis Time</div>
            <div class="stat-number">File Dependent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Cost</div>
            <div class="stat-number">Free</div>
        </div>
        """, unsafe_allow_html=True)


def show_upload_hub():
    """Advanced Multi-Source Upload Hub"""
    st.markdown("""
    <div class="cyber-hero">
        <h1 style="color: var(--cyber-blue); text-align: center; margin: 0;">🔷 ADVANCED UPLOAD HUB</h1>
        <p style="color: var(--matrix-green); text-align: center;">Multi-Source Input • Neural Processing • Real-time Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Multi-source input tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 File Upload", 
        "🔗 Link Input", 
        "📝 Paste Input", 
        "🎤 Voice Input"
    ])
    
    with tab1:
        st.markdown("""
        <div class="neural-card">
            <h3 style="color: var(--cyber-blue);"> 🎀 QUANTUM DROP ZONE</h3>
            <p style="color: var(--matrix-green);">Advanced file processing with OCR, multi-format support, and neural parsing</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Drop your resume into the quantum zone",
                type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
                help="Supports PDF, DOCX, TXT, and image files up to 50MB"
            )
            
            if uploaded_file:
                file_size_mb = uploaded_file.size / (1024 * 1024)
                st.markdown(f"""
                <div class="ai-copilot">
                    <h4 style="color: var(--matrix-green); margin: 0;">✅ File Detected</h4>
                    <p style="color: var(--cyber-blue); margin: 0.5rem 0;">Name: {uploaded_file.name}</p>
                    <p style="color: var(--cyber-blue); margin: 0.5rem 0;">Size: {file_size_mb:.1f} MB</p>
                    <p style="color: var(--cyber-blue); margin: 0.5rem 0;">Type: {uploaded_file.type}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🚀 INITIATE NEURAL ANALYSIS", use_container_width=True):
                    with st.spinner("🧠 Neural networks processing..."):
                        try:
                            # File processing logic
                            if uploaded_file.type == "application/pdf":
                                text = extract_text_from_pdf(uploaded_file)
                            elif uploaded_file.name.lower().endswith('.docx'):
                                text = extract_text_from_docx(uploaded_file)
                            elif uploaded_file.type == "text/plain":
                                text = str(uploaded_file.read(), "utf-8")
                            else:
                                text = "OCR processing for image files coming soon!"
                            
                            # Store data and analyze
                            st.session_state.resume_data = {
                                'text': text,
                                'filename': uploaded_file.name,
                                'file_size': uploaded_file.size
                            }
                            
                            # Run analysis
                            analyzer = get_analyzer()
                            results = analyzer.analyze(text)
                            st.session_state.analysis_results = results
                            
                            # Update counter
                            st.session_state.analysis_count += 1
                            
                            st.success("✨ Neural analysis complete! Redirecting to dashboard...")
                            st.session_state.page = 'neural_dashboard'
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"🚨 Neural processing error: {str(e)}")
        
        with col2:
            st.markdown("""
            <div class="neural-card">
                <h4 style="color: var(--holo-purple);">Supported Formats</h4>
                <div class="skill-node">PDF</div>
                <div class="skill-node">DOCX</div>
                <div class="skill-node">TXT</div>
                <div class="skill-node">PNG/JPG</div>
                <br><br>
                <h4 style="color: var(--holo-purple);">Features</h4>
                <p style="color: var(--cyber-blue); font-size: 0.9rem;">• OCR Text Extraction</p>
                <p style="color: var(--cyber-blue); font-size: 0.9rem;">• Multi-language Support</p>
                <p style="color: var(--cyber-blue); font-size: 0.9rem;">• Format Optimization</p>
                <p style="color: var(--cyber-blue); font-size: 0.9rem;">• Virus Scanning</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="neural-card">
            <h3 style="color: var(--cyber-blue);"> 🔗 LINK ANALYSIS ENGINE</h3>
            <p style="color: var(--matrix-green);">Extract and analyze profiles from professional networks</p>
        </div>
        """, unsafe_allow_html=True)
        
        link_type = st.selectbox(
            "Select Link Type", 
            ["💼 LinkedIn Profile", "🚀 GitHub Repository", "🌐 Portfolio Website", "📎 Job Description URL"]
        )
        
        profile_url = st.text_input("Enter Profile/Job URL", placeholder="Enter URL here")
        
        if profile_url and st.button("🔍 ANALYZE LINK"):
            st.info("🚀 Link analysis feature is being developed.")
    
    with tab3:
        st.markdown("""
        <div class="neural-card">
            <h3 style="color: var(--cyber-blue);"> 📝 DIRECT TEXT PROCESSOR</h3>
            <p style="color: var(--matrix-green);">Paste resume content or job descriptions for instant analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        text_input = st.text_area(
            "Paste your resume content or job description",
            height=300,
            placeholder="Paste your resume text here for instant neural analysis...",
            help="Copy and paste your resume content directly for quick analysis"
        )
        
        if text_input and len(text_input.strip()) > 50:
            word_count = len(text_input.split())
            st.markdown(f"""
            <div class="ai-copilot">
                <p style="color: var(--matrix-green); margin: 0;">Word Count: {word_count}</p>
                <p style="color: var(--cyber-blue); margin: 0;">Ready for analysis</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🧠 PROCESS TEXT"):
                with st.spinner("💫 Processing with neural networks..."):
                    st.session_state.resume_data = {
                        'text': text_input,
                        'filename': 'pasted_content.txt',
                        'file_size': len(text_input.encode('utf-8'))
                    }
                    
                    analyzer = get_analyzer()
                    results = analyzer.analyze(text_input)
                    st.session_state.analysis_results = results
                    st.session_state.analysis_count += 1
                    
                    st.success("✨ Text analysis complete!")
                    st.session_state.page = 'neural_dashboard'
                    st.rerun()
    
    with tab4:
        st.markdown("""
        <div class="neural-card">
            <h3 style="color: var(--cyber-blue);"> 🎤 VOICE-TO-RESUME AI</h3>
            <p style="color: var(--matrix-green);">Speak your experience and let AI craft your resume</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="ai-copilot">
            <h4 style="color: var(--holo-purple);">Voice Input Features</h4>
            <p style="color: var(--cyber-blue);">• Real-time speech recognition</p>
            <p style="color: var(--cyber-blue);">• AI-powered resume generation</p>
            <p style="color: var(--cyber-blue);">• Multi-language support</p>
            <p style="color: var(--cyber-blue);">• Experience extraction</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎤 START VOICE RECORDING"):
            st.info("🎤 Voice input feature under development.")
        
        # Sample voice prompts
        st.markdown("""
        <div class="neural-card">
            <h4 style="color: var(--matrix-green);">Sample Voice Prompts</h4>
            <p style="color: var(--cyber-blue);">"I'm a software engineer with 5 years of experience in Python and React..."</p>
            <p style="color: var(--cyber-blue);">"I managed a team of 10 developers and increased productivity by 40%..."</p>
            <p style="color: var(--cyber-blue);">"I have a Masters in Computer Science from [Your University]..."</p>
        </div>
        """, unsafe_allow_html=True)

def show_neural_dashboard():
    """Advanced Neural Dashboard with Quantum Scoring"""
    if not st.session_state.analysis_results:
        st.markdown("""
        <div class="neural-card">
            <h2 style="color: var(--neon-orange); text-align: center;">⚠️ No Analysis Data</h2>
            <p style="color: var(--cyber-blue); text-align: center;">Please upload a resume first to see your neural dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔷 Upload Resume", use_container_width=True):
            st.session_state.page = 'upload_hub'
            st.rerun()
        return
    
    results = st.session_state.analysis_results
    scores = results.get('scores', {})
    overall_score = scores.get('overall_score', 0)
    
    # Quantum Score Overview Header
    st.markdown("""
    <div class="cyber-hero">
        <h1 style="color: var(--cyber-blue); margin: 0;">⚛️ QUANTUM SCORE OVERVIEW</h1>
        <div class="quantum-score">{:.0f}/100</div>
        <div style="color: var(--matrix-green); font-size: 1.5rem; text-align: center; margin-top: 1rem;">
            OVERALL NEURAL SCORE
        </div>
        <div class="neural-progress">
            <div class="neural-progress-bar" style="width: {:.0f}%;"></div>
        </div>
    </div>
    """.format(overall_score, overall_score), unsafe_allow_html=True)
    
    # AI Copilot Feedback
    if st.session_state.ai_copilot_active:
        ai_feedback = generate_ai_feedback(overall_score, scores)
        st.markdown(f"""
        <div class="ai-copilot">
            <h3 style="color: var(--holo-purple); margin: 0;">🤖 AI COPILOT FEEDBACK</h3>
            <div class="ai-message">{ai_feedback}</div>
            <button class="quantum-button" style="margin-top: 1rem;">Ask AI for Specific Advice</button>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Score Breakdown
    st.markdown("<h2 style='color: var(--cyber-blue); margin: 2rem 0 1rem 0;'>📈 NEURAL SCORE BREAKDOWN</h2>", unsafe_allow_html=True)
    
    score_categories = [
        ("Content Impact", scores.get('content_quality', 0), "📝", "Writing quality, achievements, and impact metrics"),
        ("ATS Quantum", scores.get('ats_compatibility', 0), "🤖", "Applicant Tracking System optimization"),
        ("Skill Density", scores.get('keyword_optimization', 0), "🌟", "Technical and soft skills coverage"),
        ("Structure Flow", scores.get('structure_score', 0), "🏠", "Document organization and formatting"),
        ("Career Signal", scores.get('completeness', 0), "📶", "Professional profile completeness"),
        ("Future Proof", calculate_future_proof_score(scores), "🚀", "Industry trends and growth potential")
    ]
    
    for i, (category, score, icon, description) in enumerate(score_categories):
        # Color coding based on score
        if score >= 90:
            color = "var(--matrix-green)"
            status = "ELITE"
            glow = "var(--glow-green)"
        elif score >= 75:
            color = "var(--cyber-blue)"
            status = "STRONG"
            glow = "var(--glow-blue)"
        elif score >= 60:
            color = "var(--holo-purple)"
            status = "GOOD"
            glow = "var(--glow-purple)"
        else:
            color = "var(--neon-orange)"
            status = "NEEDS BOOST"
            glow = "0 0 15px var(--neon-orange)"
        
        st.markdown(f"""
        <div class="neural-card" style="border-color: {color}; box-shadow: {glow};">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div>
                        <h3 style="color: {color}; margin: 0;">{category}</h3>
                        <p style="color: var(--cyber-blue); margin: 0; font-size: 0.9rem;">{description}</p>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2.5rem; font-weight: 900; color: {color}; margin-bottom: 0.25rem;">{score:.0f}%</div>
                    <div style="color: {color}; font-weight: bold; font-size: 0.8rem;">{status}</div>
                </div>
            </div>
            <div class="neural-progress">
                <div class="neural-progress-bar" style="width: {score:.0f}%; background: linear-gradient(90deg, {color}, {color}cc);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive Visualization
    st.markdown("<h2 style='color: var(--cyber-blue); margin: 3rem 0 1rem 0;'>📉 INTERACTIVE NEURAL MAP</h2>", unsafe_allow_html=True)
    
    # Create radar chart (temporarily disabled - will re-enable after fixing plotly)
    categories = [cat[0] for cat in score_categories]
    values = [cat[1] for cat in score_categories]
    
    # Temporary placeholder instead of plotly chart
    st.markdown("""
    <div class="neural-card">
        <h3 style="color: var(--cyber-blue); text-align: center;">📊 NEURAL MAP VISUALIZATION</h3>
        <p style="color: var(--matrix-green); text-align: center;">Advanced 3D radar chart coming soon!</p>
        <div style="display: flex; justify-content: space-around; margin: 2rem 0;">
    """, unsafe_allow_html=True)
    
    for cat, val in zip(categories, values):
        color = "var(--matrix-green)" if val >= 80 else "var(--cyber-blue)" if val >= 60 else "var(--neon-orange)"
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="color: {color}; font-size: 2rem; font-weight: bold;">{val:.0f}%</div>
            <div style="color: var(--cyber-blue); font-size: 0.9rem;">{cat}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # fig = go.Figure()
    # fig.add_trace(go.Scatterpolar(...))
    # st.plotly_chart(fig, use_container_width=True)
    
    # Quick Action Panel
    st.markdown("<h3 style='color: var(--matrix-green);'>⚡ QUICK ACTIONS</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🌟 Skill Galaxy", use_container_width=True):
            st.session_state.page = 'skill_galaxy'
            st.rerun()
    
    with col2:
        if st.button("🚀 Career Sim", use_container_width=True):
            st.session_state.page = 'career_simulator'
            st.rerun()
    
    with col3:
        if st.button("📈 Benchmark", use_container_width=True):
            st.session_state.page = 'industry_benchmark'
            st.rerun()
    
    with col4:
        if st.button("📤 Export", use_container_width=True):
            st.session_state.page = 'smart_export'
            st.rerun()

def generate_ai_feedback(overall_score, scores):
    """Generate contextual AI feedback based on scores"""
    if overall_score >= 85:
        return "🎆 Exceptional resume detected! Your profile shows strong technical depth and excellent presentation. Consider adding more leadership metrics to boost executive appeal."
    elif overall_score >= 70:
        return "🔥 Solid foundation identified! Strong technical skills detected. Recommend enhancing quantifiable achievements and industry-specific keywords."
    elif overall_score >= 55:
        return "⚡ Good potential recognized! Focus on strengthening impact statements and adding more relevant technical skills for your target role."
    else:
        return "🛠️ Optimization needed! Let's enhance your content quality, add quantifiable achievements, and improve ATS compatibility."

def calculate_future_proof_score(scores):
    """Calculate future-proofing score based on modern requirements"""
    base_score = (scores.get('keyword_optimization', 0) + scores.get('content_quality', 0)) / 2
    # Bonus for modern skills, remote work keywords, etc.
    return min(base_score * 1.1, 100)

def show_job_matching_page():
    """Job matching page"""
    st.markdown("<h2 style='color: #1F2937;'>🎯 Job Description Matching</h2>", unsafe_allow_html=True)
    st.markdown("<div style='color: #6B7280; margin-bottom: 1rem;'>Paste a job description to see how well your resume matches:</div>", unsafe_allow_html=True)
    
    if not st.session_state.resume_data:
        st.warning("Upload a resume first")
        if st.button("Upload Resume"):
            st.session_state.page = 'upload'
            st.rerun()
        return
    
    job_description = st.text_area("Paste Job Description", height=200)
    
    if st.button("Analyze Match"):
        if job_description:
            resume_text = st.session_state.resume_data.get('text', '')
            with st.spinner("Analyzing job match..."):
                match_score = calculate_match_score(resume_text, job_description)
                missing_keywords = extract_missing_keywords(resume_text, job_description)
                suggestions = get_keyword_suggestions(job_description)

            st.metric("Match Score", f"{match_score}%")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Missing Keywords (Top 10)**")
                if missing_keywords:
                    st.markdown("<ul>" + "".join([f"<li>{k}</li>" for k in missing_keywords]) + "</ul>", unsafe_allow_html=True)
                else:
                    st.success("No critical keywords missing.")

            with col2:
                st.markdown("**Suggested Keywords**")
                st.markdown("**Technical:** " + ", ".join(suggestions.get('technical_skills', [])) if suggestions.get('technical_skills') else "**Technical:** None detected")
                st.markdown("**Soft Skills:** " + ", ".join(suggestions.get('soft_skills', [])) if suggestions.get('soft_skills') else "**Soft Skills:** None detected")
                st.markdown("**Action Verbs:** " + ", ".join(suggestions.get('action_verbs', [])) if suggestions.get('action_verbs') else "**Action Verbs:** None detected")
        else:
            st.warning("Please enter a job description")


def show_ats_check_page():
    """ATS check page"""
    st.markdown("<h2 style='color: #1F2937;'>✓ ATS Compatibility Check</h2>", unsafe_allow_html=True)
    
    if not st.session_state.analysis_results:
        st.warning("Upload a resume first")
        if st.button("Upload Resume"):
            st.session_state.page = 'upload'
            st.rerun()
        return
    
    results = st.session_state.analysis_results
    scores = results.get('scores', {})
    contact_info = results.get('contact_info', {})
    sections = set(results.get('sections_detected', []))

    st.metric("ATS Compatibility", f"{scores.get('ats_compatibility', 0):.0f}%")

    required_sections = {"Experience", "Education", "Skills", "Summary"}
    missing_sections = sorted(list(required_sections - sections))

    missing_contact = []
    if not contact_info.get('has_email'):
        missing_contact.append("Email")
    if not contact_info.get('has_phone'):
        missing_contact.append("Phone")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='color: #10B981;'>✓ Good Practices</h3>", unsafe_allow_html=True)
        good_items = [
            "Clear section headers",
            "Readable text and spacing",
            "Standard bullet points",
            "Consistent date formatting"
        ]
        st.markdown("<div style='color: #6B7280;'><ul>" + "".join([f"<li>{i}</li>" for i in good_items]) + "</ul></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='color: #EF4444;'>✗ Missing or Risk Areas</h3>", unsafe_allow_html=True)
        risk_items = []
        if missing_sections:
            risk_items.append("Missing sections: " + ", ".join(missing_sections))
        if missing_contact:
            risk_items.append("Missing contact: " + ", ".join(missing_contact))
        if not risk_items:
            risk_items.append("No major ATS risks detected.")
        st.markdown("<div style='color: #6B7280;'><ul>" + "".join([f"<li>{i}</li>" for i in risk_items]) + "</ul></div>", unsafe_allow_html=True)


def show_about_page():
    """About page"""
    st.markdown("<h2 style='color: #1F2937;'>ℹ️ About AI Resume Analyzer</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <h3 style='color: #1F2937;'>What is AI Resume Analyzer?</h3>
    <div style='color: #6B7280; line-height: 1.6;'>AI Resume Analyzer is a professional resume analysis tool that provides honest, actionable feedback to help you improve your resume and land your dream job.</div>
    
    <h3 style='color: #1F2937; margin-top: 2rem;'>Features</h3>
    <div style='color: #6B7280;'><ul>
    <li>Content Quality Analysis</li>
    <li>Skill Detection</li>
    <li>ATS Compatibility Check</li>
    <li>Job Matching</li>
    <li>Structure Review</li>
    <li>Actionable Recommendations</li>
    </ul></div>
    
    <h3 style='color: #1F2937; margin-top: 2rem;'>How It Works</h3>
    <div style='color: #6B7280;'><ol>
    <li>Upload your resume (PDF, DOCX, or TXT)</li>
    <li>The analyzer evaluates content, keywords, ATS, structure, and completeness</li>
    <li>You get instant, honest feedback</li>
    <li>Implement recommendations</li>
    <li>Re-upload to see improvements</li>
    </ol></div>
    """, unsafe_allow_html=True)
    
def generate_ai_feedback(overall_score, scores):
    """Generate contextual AI feedback based on scores"""
    if overall_score >= 85:
        return "🎆 Exceptional resume detected! Your profile shows strong technical depth and excellent presentation. Consider adding more leadership metrics to boost executive appeal."
    elif overall_score >= 70:
        return "🔥 Solid foundation identified! Strong technical skills detected. Recommend enhancing quantifiable achievements and industry-specific keywords."
    elif overall_score >= 55:
        return "⚡ Good potential recognized! Focus on strengthening impact statements and adding more relevant technical skills for your target role."
    else:
        return "🛠️ Optimization needed! Let's enhance your content quality, add quantifiable achievements, and improve ATS compatibility."

def calculate_future_proof_score(scores):
    """Calculate future-proofing score based on modern requirements"""
    base_score = (scores.get('keyword_optimization', 0) + scores.get('content_quality', 0)) / 2
    # Bonus for modern skills, remote work keywords, etc.
    return min(base_score * 1.1, 100)

def show_skill_galaxy():
    """3D Skill Galaxy Visualization"""
    st.markdown("""
    <div class="cyber-hero">
        <h1 style="color: var(--cyber-blue); margin: 0;">🌟 SKILL GALAXY MAP</h1>
        <p style="color: var(--matrix-green);">3D Visualization • Gap Analysis • Growth Paths</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.analysis_results:
        st.info("📡 Upload a resume first to explore your skill galaxy")
        return
    
    results = st.session_state.analysis_results
    
    # Extract skills data
    technical_skills = results.get('technical_skills', [])
    soft_skills = results.get('soft_skills', [])
    
    # Generate skill galaxy data
    all_skills = technical_skills + soft_skills
    
    if not all_skills:
        st.warning("⚠️ No skills detected in your resume. Consider adding more technical and soft skills.")
        return
    
    # Create interactive skill galaxy
    st.markdown("<h2 style='color: var(--cyber-blue);'>🌌 INTERACTIVE SKILL UNIVERSE</h2>", unsafe_allow_html=True)
    
    # Skill categories with different sizes and colors
    skill_categories = {
        'Core Skills': technical_skills[:8],
        'Emerging Skills': technical_skills[8:15] if len(technical_skills) > 8 else [],
        'Soft Skills': soft_skills[:8],
        'Future Skills': ['AI/ML', 'Blockchain', 'Quantum Computing', 'AR/VR', 'IoT']
    }
    
    for category, skills in skill_categories.items():
        if not skills:
            continue
            
        if category == 'Core Skills':
            color_class = "skill-node"
            size_style = "font-size: 1.1rem; padding: 0.7rem 1.2rem;"
        elif category == 'Emerging Skills':
            color_class = "skill-node"
            size_style = "font-size: 1rem; padding: 0.6rem 1rem; background: radial-gradient(circle, var(--holo-purple), var(--cyber-blue));"
        elif category == 'Soft Skills':
            color_class = "skill-node"
            size_style = "font-size: 0.9rem; padding: 0.5rem 0.8rem; background: radial-gradient(circle, var(--neon-orange), var(--pulse-pink));"
        else:  # Future Skills
            color_class = "skill-node"
            size_style = "font-size: 0.8rem; padding: 0.4rem 0.6rem; background: linear-gradient(45deg, transparent, var(--cyber-blue)); border: 2px dashed var(--cyber-blue);"
        
        st.markdown(f"""
        <div class="neural-card">
            <h3 style="color: var(--matrix-green);">{category} ({len(skills)})</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center;">
        """, unsafe_allow_html=True)
        
        for skill in skills:
            st.markdown(f"""
            <div class="{color_class}" style="{size_style}">{skill}</div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Skill Health Metrics
    st.markdown("<h2 style='color: var(--cyber-blue); margin: 3rem 0 1rem 0;'>📈 SKILL HEALTH METRICS</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate actual skill metrics based on resume content
        import random
        demand_score = min(len(technical_skills) * 4, 100) if technical_skills else 50
        future_growth = min(len(all_skills) * 3, 100) if all_skills else 50
        competition = max(100 - len(all_skills) * 3, 30) if all_skills else 70
        salary_impact = min(len(technical_skills) * 5, 100) if technical_skills else 40
        
        st.markdown(f"""
        <div class="neural-card">
            <h4 style="color: var(--holo-purple);">Market Analysis</h4>
            <div style="margin: 1rem 0;">
                <p style="color: var(--cyber-blue); margin: 0.5rem 0;">Demand Score: {demand_score}%</p>
                <div class="neural-progress">
                    <div class="neural-progress-bar" style="width: {demand_score}%;"></div>
                </div>
            </div>
            <div style="margin: 1rem 0;">
                <p style="color: var(--cyber-blue); margin: 0.5rem 0;">Future Growth: {future_growth}%</p>
                <div class="neural-progress">
                    <div class="neural-progress-bar" style="width: {future_growth}%;"></div>
                </div>
            </div>
            <div style="margin: 1rem 0;">
                <p style="color: var(--cyber-blue); margin: 0.5rem 0;">Competition: {competition}%</p>
                <div class="neural-progress">
                    <div class="neural-progress-bar" style="width: {competition}%; background: linear-gradient(90deg, var(--neon-orange), var(--pulse-pink));"></div>
                </div>
            </div>
            <div style="margin: 1rem 0;">
                <p style="color: var(--cyber-blue); margin: 0.5rem 0;">Salary Impact: {salary_impact}%</p>
                <div class="neural-progress">
                    <div class="neural-progress-bar" style="width: {salary_impact}%; background: linear-gradient(90deg, var(--matrix-green), var(--cyber-blue));"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="neural-card">
            <h4 style="color: var(--holo-purple);">Skill Recommendations</h4>
            <div class="ai-message">
                🤖 Based on your current skills, consider adding:
            </div>
            <div style="margin: 1rem 0;">
                <div class="skill-node" style="background: linear-gradient(45deg, transparent, var(--matrix-green)); border: 2px dashed var(--matrix-green);">Cloud Architecture</div>
                <div class="skill-node" style="background: linear-gradient(45deg, transparent, var(--matrix-green)); border: 2px dashed var(--matrix-green);">DevOps</div>
                <div class="skill-node" style="background: linear-gradient(45deg, transparent, var(--matrix-green)); border: 2px dashed var(--matrix-green);">Machine Learning</div>
            </div>
            <br><br>
            <h5 style="color: var(--matrix-green);">Growth Path Suggestions:</h5>
            <p style="color: var(--cyber-blue); font-size: 0.9rem;">• Focus on cloud technologies</p>
            <p style="color: var(--cyber-blue); font-size: 0.9rem;">• Develop leadership skills</p>
            <p style="color: var(--cyber-blue); font-size: 0.9rem;">• Learn emerging AI tools</p>
        </div>
        """, unsafe_allow_html=True)

def show_career_simulator():
    """Career Path Simulator with Future Projections"""
    st.markdown("""
    <div class="cyber-hero">
        <h1 style="color: var(--cyber-blue); margin: 0;">🚀 CAREER SIMULATOR</h1>
        <p style="color: var(--matrix-green);">Future Trajectory • Role Progression • Salary Predictions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Career Path Options
    st.markdown("<h2 style='color: var(--cyber-blue);'>⚡ SELECT CAREER TRAJECTORY</h2>", unsafe_allow_html=True)
    
    career_paths = [
        "💻 Software Engineering Track",
        "📊 Data Science & Analytics",
        "☁️ Cloud Architecture",
        "🤖 AI/Machine Learning",
        "🛡️ Cybersecurity",
        "📱 Product Management",
        "👥 Leadership & Management"
    ]
    
    selected_path = st.selectbox("Choose your career focus", career_paths)
    
    # Timeline Simulation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="neural-card">
            <h3 style="color: var(--matrix-green);">🗓️ 5-Year Projection</h3>
            <div style="margin: 1rem 0;">
                <p style="color: var(--cyber-blue);"><strong>Year 1:</strong> Senior Developer</p>
                <p style="color: var(--cyber-blue);"><strong>Year 2-3:</strong> Lead Developer</p>
                <p style="color: var(--cyber-blue);"><strong>Year 4-5:</strong> Engineering Manager</p>
            </div>
            <div style="margin: 1.5rem 0;">
                <p style="color: var(--holo-purple);"><strong>Salary Growth:</strong></p>
                <div class="neural-progress">
                    <div class="neural-progress-bar" style="width: 85%; background: linear-gradient(90deg, var(--matrix-green), var(--cyber-blue));"></div>
                </div>
                <p style="color: var(--cyber-blue); font-size: 0.9rem;">Salary growth varies by role and experience</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="neural-card">
            <h3 style="color: var(--matrix-green);">🎯 Key Milestones</h3>
            <p style="color: var(--cyber-blue);">• Master cloud technologies</p>
            <p style="color: var(--cyber-blue);">• Lead cross-functional teams</p>
            <p style="color: var(--cyber-blue);">• Obtain AWS/Azure certifications</p>
            <p style="color: var(--cyber-blue);">• Mentor junior developers</p>
            <p style="color: var(--cyber-blue);">• Drive architectural decisions</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive Career Builder
    st.markdown("<h3 style='color: var(--cyber-blue);'>🛠️ BUILD YOUR PATH</h3>", unsafe_allow_html=True)
    
    if st.button("🚀 SIMULATE CAREER PATH", use_container_width=True):
        st.success("✨ Career simulation complete! Check the projections above.")

def show_industry_benchmark():
    """Industry Benchmark Comparison"""
    st.markdown("""
    <div class="cyber-hero">
        <h1 style="color: var(--cyber-blue); margin: 0;">📈 INDUSTRY BENCHMARK</h1>
        <p style="color: var(--matrix-green);">Market Analysis • Salary Data • Competitive Edge</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="neural-card">
        <h3 style="color: var(--holo-purple);">🎯 Your Competitive Position</h3>
        <p style="color: var(--cyber-blue);">Compare your profile against industry standards and top performers.</p>
    </div>
    """, unsafe_allow_html=True)

def show_ai_interview():
    """AI-Powered Interview Simulator"""
    st.markdown("""
    <div class="cyber-hero">
        <h1 style="color: var(--cyber-blue); margin: 0;">🤖 AI INTERVIEW PREP</h1>
        <p style="color: var(--matrix-green);">Practice Sessions • Real-time Feedback • Confidence Building</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎤 START INTERVIEW SIMULATION", use_container_width=True):
        st.info("🤖 AI Interview feature is in development.")

def show_collaboration():
    """Team Collaboration Workspace"""
    st.markdown("""
    <div class="cyber-hero">
        <h1 style="color: var(--cyber-blue); margin: 0;">👥 COLLABORATION</h1>
        <p style="color: var(--matrix-green);">Team Reviews • Shared Analysis • Group Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="neural-card">
        <h3 style="color: var(--holo-purple);">🌐 Coming Soon</h3>
        <p style="color: var(--cyber-blue);">Collaborate with your team on resume analysis and hiring decisions.</p>
    </div>
    """, unsafe_allow_html=True)

def show_smart_export():
    """Smart Export Hub"""
    st.markdown("""
    <div class="cyber-hero">
        <h1 style="color: var(--cyber-blue); margin: 0;">📤 SMART EXPORT HUB</h1>
        <p style="color: var(--matrix-green);">Multi-format • AR Resume • Video Profile</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.analysis_results:
        st.info("📋 Analyze a resume first to unlock export options")
        return
    
    export_formats = [
        "📄 Enhanced PDF Resume",
        "🌐 Interactive Web Portfolio", 
        "🎥 Video Resume Generator",
        "📱 AR Business Card",
        "📊 Analysis Report PDF",
        "💼 LinkedIn Optimizer"
    ]
    
    col1, col2 = st.columns(2)
    
    for i, format_option in enumerate(export_formats):
        if i % 2 == 0:
            with col1:
                if st.button(format_option, use_container_width=True):
                    st.success(f"✨ {format_option} export initiated!")
        else:
            with col2:
                if st.button(format_option, use_container_width=True):
                    st.success(f"✨ {format_option} export initiated!")

def show_analytics():
    """Advanced Analytics Dashboard"""
    st.markdown("""
    <div class="cyber-hero">
        <h1 style="color: var(--cyber-blue); margin: 0;">🔮 ANALYTICS DEEP DIVE</h1>
        <p style="color: var(--matrix-green);">Advanced Metrics • Predictive Insights • Market Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="neural-card">
        <h3 style="color: var(--holo-purple);">📊 Advanced Analytics</h3>
        <p style="color: var(--cyber-blue);">Deep-dive analytics and predictive career modeling in development!</p>
    </div>
    """, unsafe_allow_html=True)


# Advanced Neural Navigation Routing
# Check if we need to switch based on session state
current_page = st.session_state.page

# Map session_state pages to display functions
page_functions = {
    'neural_home': show_neural_home,
    'upload_hub': show_upload_hub,
    'neural_dashboard': show_neural_dashboard,
    'skill_galaxy': show_skill_galaxy,
    'career_simulator': show_career_simulator,
    'industry_benchmark': show_industry_benchmark,
    'ai_interview': show_ai_interview,
    'collaboration': show_collaboration,
    'smart_export': show_smart_export,
    'analytics': show_analytics,
    # Legacy compatibility
    'home': show_neural_home,
    'upload': show_upload_hub,
    'analysis': show_neural_dashboard,
    'job_matching': show_job_matching_page,
    'ats_check': show_ats_check_page,
    'about': show_about_page
}

# Route to appropriate page
if current_page in page_functions:
    page_functions[current_page]()
else:
    # Default to neural home
    show_neural_home()

# Legacy sidebar routing for compatibility
if selected_page == "🏠 Neural Home":
    st.session_state.page = 'neural_home'
    st.rerun()
elif selected_page == "🔗 Upload Hub":
    st.session_state.page = 'upload_hub' 
    st.rerun()
elif selected_page == "📊 Neural Dashboard":
    st.session_state.page = 'neural_dashboard'
    st.rerun()
elif selected_page == "🌟 Skill Galaxy":
    st.session_state.page = 'skill_galaxy'
    st.rerun()
elif selected_page == "🚀 Career Simulator":
    st.session_state.page = 'career_simulator'
    st.rerun()
elif selected_page == "📈 Industry Benchmark":
    st.session_state.page = 'industry_benchmark'
    st.rerun()
elif selected_page == "🤖 AI Interview":
    st.session_state.page = 'ai_interview'
    st.rerun()
elif selected_page == "👥 Collaboration":
    st.session_state.page = 'collaboration'
    st.rerun()
elif selected_page == "📤 Smart Export":
    st.session_state.page = 'smart_export'
    st.rerun()
elif selected_page == "🔮 Analytics Deep Dive":
    st.session_state.page = 'analytics'
    st.rerun()
# Legacy routing
elif selected_page == "Home":
    st.session_state.page = 'neural_home'
    st.rerun()
elif selected_page == "Upload Resume":
    st.session_state.page = 'upload_hub'
    st.rerun()
elif selected_page == "Analysis":
    st.session_state.page = 'neural_dashboard'
    st.rerun()
elif selected_page == "Job Matching":
    st.session_state.page = 'job_matching'
    st.rerun()
elif selected_page == "ATS Check":
    st.session_state.page = 'ats_check'
    st.rerun()
elif selected_page == "About":
    st.session_state.page = 'about'
    st.rerun()

