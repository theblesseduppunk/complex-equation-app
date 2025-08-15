import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import json
from io import StringIO
import random
import time

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="MindScape (The Complex Equation Simulator)", 
                   page_icon="🧠", layout="wide")

# ------------------------------
# Custom CSS & Futuristic Styling
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

body {background-color:#0a0a0a; color:white; font-family:'Orbitron', monospace;}

@keyframes fadeIn {from {opacity:0; transform:translateY(-10px);} to {opacity:1; transform:translateY(0);} }
@keyframes pulse {0% {box-shadow:0 0 10px cyan;} 50% {box-shadow:0 0 20px magenta;} 100% {box-shadow:0 0 10px cyan;}}

.welcome-box {
    animation: fadeIn 1.5s ease-out forwards;
    padding: 30px; border-radius: 15px;
    background: rgba(0,0,0,0.7); backdrop-filter: blur(10px);
    box-shadow: 0 0 30px rgba(0,255,255,0.5);
    color: #00ffff; text-align:center; margin-bottom:30px;
}
.launch-btn {
    background: linear-gradient(90deg, cyan, magenta); border:none; 
    padding:15px 30px; border-radius:25px; color:black; font-size:1.3em; font-weight:bold; cursor:pointer; transition:all 0.3s ease;
}
.launch-btn:hover { transform: scale(1.05); box-shadow: 0 0 25px cyan, 0 0 25px magenta; }

.slider-label {color:#00ffff; font-weight:bold;}
.metric-display {animation: pulse 2s infinite; font-size:1.5em; color:#00ffff;}
.tab-header {font-size:2em; color:#00ffff; font-weight:bold; margin-top:10px;}
.possibility {margin:10px 0; padding:10px; border-radius:10px; background: rgba(0,0,0,0.5); border:1px solid #00ffff; box-shadow:0 0 15px #ff00ff;}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Welcome Section
# ------------------------------
st.markdown("""
<div class="welcome-box">
    <div style="font-size:2.8em; font-weight:bold;">🚀 MindScape</div>
    <div style="margin-top:10px; font-size:1.3em;">
        A simulation creator, the first of its kind, by <b>Sam Andrews Rodriguez II</b>.<br>
        Explore consciousness, creativity, dimensionality, and AI-driven scenarios.
    </div>
    <hr style="border:0.5px solid #00ffff; margin:15px 0;">
    <button class="launch-btn" onclick="window.scrollTo({top: 500, behavior: 'smooth'});">🔥 Launch Simulation</button>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar Parameters
# ------------------------------
st.sidebar.header("Adjust Parameters / Generate Scenarios")
variables = ["R","alpha","theta","S","Q","A","E","M","Dn","beta","C"]
default_values = {"R":5.0,"alpha":1.0,"theta":1.0,"S":5.0,"Q":5.0,"A":5.0,"E":5.0,"M":5.0,"Dn":5.0,"beta":1.0}

if "sliders" not in st.session_state:
    st.session_state.sliders = default_values.copy()
if "history" not in st.session_state:
    st.session_state.history = []

demo_values = {"R":7.0,"alpha":1.2,"theta":1.0,"S":8.0,"Q":7.0,"A":9.0,"E":6.0,"M":8.0,"Dn":2.0,"beta":1.0}

# ------------------------------
# Functions
# ------------------------------
def generate_random_scenario():
    return {k: round(random.uniform(0.1,10.0),1) for k in st.session_state.sliders.keys()}

def animate_sliders(target_values, steps=15, delay=0.03):
    for i in range(1, steps+1):
        for key in st.session_state.sliders:
            current = st.session_state.sliders[key]
            st.session_state.sliders[key] = current + (target_values[key]-current)*(i/steps)
        time.sleep(delay)
        st.experimental_rerun()

# Complex Equation
def compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta):
    return (R*(alpha**theta)*S*Q*(1.3*A)*E*(1.6*M)) / (Dn*(beta**theta))

# Beginner Equation
def compute_creativity(R, D3):
    return R / (D3**3)

def ai_suggestions(current_values):
    suggestions = []
    balanced = {k:5.0 for k in current_values.keys()}
    suggestions.append(("Balanced", balanced))
    high_c = {k: round(random.uniform(7.5,10.0),1) for k in current_values.keys()}
    suggestions.append(("High Consciousness", high_c))
    creative = {k: round(random.uniform(0.5,10.0),1) for k in current_values.keys()}
    suggestions.append(("Creative AI Insight", creative))
    return suggestions

# ------------------------------
# Scenario Buttons
# ------------------------------
if st.sidebar.button("📈 Load Demo Scenario"):
    animate_sliders(demo_values)
if st.sidebar.button("🎲 Generate Random Scenario"):
    animate_sliders(generate_random_scenario())

target_variable = st.sidebar.selectbox("Select variable to solve for:", variables, index=variables.index("C"))

# Display sliders
slider_values = {}
for var in default_values.keys():
    slider_values[var] = st.sidebar.slider(f"{var}",0.1,10.0,st.session_state.sliders[var],0.1)

# AI Buddy Tab Section
ai_tab = st.sidebar.expander("🤖 AIBuddy Suggestions")
ai_choices = ai_suggestions(slider_values)
for name, vals in ai_choices:
    if ai_tab.button(f"💡 {name}"):
        animate_sliders(vals)

# Compute target variable
C_complex = compute_consciousness(**slider_values)
st.session_state.sliders.update(slider_values)
st.session_state.history.append({**slider_values,"C":C_complex})

# ------------------------------
# Dynamic Full-Screen Background
# ------------------------------
def update_background(consciousness_value, min_val=0, max_val=20):
    norm = (consciousness_value - min_val) / (max_val - min_val)
    norm = max(0, min(1, norm))
    serenity_color = "#0a0f2b"
    chaos_color = "#ff00ff"
    r_ser = int(serenity_color[1:3],16)
    g_ser = int(serenity_color[3:5],16)
    b_ser = int(serenity_color[5:7],16)
    r_cha = int(chaos_color[1:3],16)
    g_cha = int(chaos_color[3:5],16)
    b_cha = int(chaos_color[5:7],16)
    r = int(r_ser + (r_cha - r_ser) * norm)
    g = int(g_ser + (g_cha - g_ser) * norm)
    b = int(b_ser + (b_cha - b_ser) * norm)
    bg_color = f"rgb({r},{g},{b})"
    st.markdown(f"""
    <style>
        body {{
            background: linear-gradient(to bottom, {bg_color}, #000000);
            transition: background 1s ease;
        }}
    </style>
    """, unsafe_allow_html=True)

update_background(C_complex, min_val=0, max_val=20)

# ------------------------------
# Tabs
# ------------------------------
tabs = st.tabs(["Simulation","Beginner Equation","Possibilities","History","About"])

# (Simulation, Beginner Equation, Possibilities, History, About code remains identical to your previous version)

# ------------------------------
# About Tab
# ------------------------------
with tabs[4]:
    st.markdown("<div class='tab-header'>📖 About MindScape</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='possibility'>
    <b>The Complex Equation:</b><br>
    C = (R × α^θ × S × Q × (1.3 × A) × E × (1.6 × M)) / (Dₙ × β^θ)<br>
    - Consciousness (C): The level of consciousness.<br>
    - Sensory processing (R): The level of sensory processing.<br>
    - Attention (A): The level of attention.<br>
    - Memory (M): The level of memory.<br>
    - Emotional state (E): The emotional state.<br>
    - Quality of information (Q): The quality of information.<br>
    - Neural complexity (Dₙ): The level of neural complexity.<br>
    - α and β: Parameters influencing variable relationships.<br>
    - θ: Non-linearity parameter.<br><br>

    <b>Beginner Equation:</b><br>
    C = R / D³<br>
    - Helps beginners explore creativity via Reality (R) and Dimensionality (D³)<br><br>

    MindScape was created by <b>Sam Andrews Rodriguez II, 2025</b>.<br>
    Explore human-AI interactions, immersive experiences, and cognitive simulations.<br>
    AI Buddy provides guided scenario suggestions for balanced, high-consciousness, or creative states.
    </div>
    """, unsafe_allow_html=True)
