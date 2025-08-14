import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import json
from io import StringIO
import random

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="MindScape (The Complex Equation Simulator)", page_icon="🧠", layout="wide")

# ------------------------------
# Animated HUD CSS
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

body, h1, h2, h3, p, div, span, button, label { 
    font-family:'Roboto Mono', monospace !important; 
    color:#00ffff !important; 
    background-color:#0a0a0a;
}

@keyframes pulse {0% {text-shadow:0 0 5px cyan;} 50% {text-shadow:0 0 15px magenta;} 100% {text-shadow:0 0 5px cyan;}}
@keyframes flicker {0%,19%,21%,23%,25%,54%,56%,100% {opacity:1;} 20%,22%,24%,55% {opacity:0.85;}}
@keyframes glowPulse {0%{box-shadow:0 0 10px cyan;}50%{box-shadow:0 0 20px magenta;}100%{box-shadow:0 0 10px cyan;}}

.hud-box {
    background: rgba(0,0,0,0.5);
    border: 2px solid #00ffff;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 0 20px #00ffff, 0 0 30px #ff00ff;
    animation: flicker 3s infinite;
}

.neon-header {
    color:#00ffff; 
    font-size:2em; 
    font-weight:bold; 
    text-shadow:0 0 5px cyan, 0 0 10px magenta;
    animation: pulse 2s infinite;
}

.neon-button {
    background: linear-gradient(90deg, cyan, magenta); 
    border:none; 
    padding:15px 30px; 
    border-radius:25px; 
    color:black; 
    font-size:1.3em; 
    font-weight:bold; 
    cursor:pointer; 
    transition:all 0.3s ease;
}
.neon-button:hover { transform: scale(1.05); animation: glowPulse 1.5s infinite; }

.slider-label {color:#00ffff; font-weight:bold;}
.metric-display {
    animation: pulse 2s infinite, glowPulse 3s infinite; 
    font-family:'Roboto Mono', monospace; 
    color:#00ffff; 
    font-size:2.5em; 
    text-align:center;
}

.possibility {margin:10px 0; padding:10px; border-radius:10px; background: rgba(0,0,0,0.3); border:1px solid #00ffff; box-shadow:0 0 15px #ff00ff;}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Welcome Box
# ------------------------------
st.markdown("""
<div class="hud-box" style="text-align:center;">
    <div class="neon-header">🚀 MindScape</div>
    <div style="font-size:1.2em; margin-top:10px;">
        The Complex Equation Simulator by <b>Sam Andrews Rodriguez II</b><br>
        Simulation creator, the first of its kind.<br>
        Explore consciousness, cognitive states, memory, attention, environment, and AI scenarios.
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# Variables & Defaults
# ------------------------------
variables = ["R","alpha","theta","S","Q","A","E","M","Dn","beta","C"]
default_values = {"R":5.0,"alpha":1.0,"theta":1.0,"S":5.0,"Q":5.0,"A":5.0,"E":5.0,"M":5.0,"Dn":5.0,"beta":1.0}
demo_values = {"R":7.0,"alpha":1.2,"theta":1.0,"S":8.0,"Q":7.0,"A":9.0,"E":6.0,"M":8.0,"Dn":2.0,"beta":1.0}

if "sliders" not in st.session_state: st.session_state.sliders = default_values.copy()
if "history" not in st.session_state: st.session_state.history = []

def generate_random_scenario(): return {k: round(random.uniform(0.1,10.0),1) for k in st.session_state.sliders.keys()}
def compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta): return (R*(alpha**theta)*S*Q*(1.3*A)*E*(1.6*M))/(Dn*(beta**theta))
def ai_suggestions(current_values):
    suggestions = []
    balanced = {k:5.0 for k in current_values.keys()}; suggestions.append(("Balanced", balanced))
    high_c = {k: round(random.uniform(7.5,10.0),1) for k in current_values.keys()}; suggestions.append(("High Consciousness", high_c))
    creative = {k: round(random.uniform(0.5,10.0),1) for k in current_values.keys()}; suggestions.append(("Creative AI Insight", creative))
    return suggestions

# ------------------------------
# Sidebar
# ------------------------------
st.sidebar.header("Adjust Parameters / Generate Scenarios")
target_variable = st.sidebar.selectbox("Select variable to solve for:", variables, index=variables.index("C"))
col1, col2 = st.sidebar.columns(2)
slider_values = {}
for idx, var in enumerate(default_values.keys()):
    col = col1 if idx % 2 == 0 else col2
    slider_values[var] = col.slider(f"{var}",0.1,10.0,st.session_state.sliders[var],0.1)

if st.sidebar.button("📈 Load Demo Scenario"): st.session_state.sliders.update(demo_values)
if st.sidebar.button("🎲 Generate Random Scenario"): st.session_state.sliders.update(generate_random_scenario())

# Compute C
C = compute_consciousness(**slider_values)
st.session_state.sliders.update(slider_values)
st.session_state.history.append({**st.session_state.sliders,"C":C})

# ------------------------------
# Tabs
# ------------------------------
sim_tab, possibilities_tab, aibuddy_tab = st.tabs(["🧠 Simulation", "🌌 Possibilities", "🤖 AIBuddy Hub"])

# ------------------------------
# Simulation Tab
# ------------------------------
with sim_tab:
    st.markdown('<div id="simulation-section"></div>', unsafe_allow_html=True)
    st.markdown(f"<div class='hud-box'><div class='neon-header'>📊 Result for {target_variable}</div><div class='metric-display'>{C:.4f}</div></div>", unsafe_allow_html=True)
    
    # 2D Plot
    x = np.linspace(0.1,10,50)
    y = (slider_values["R"]*(slider_values["alpha"]**slider_values["theta"])*x*slider_values["Q"]*(1.3*slider_values["A"])*slider_values["E"]*(1.6*slider_values["M"]))/(slider_values["Dn"]*(slider_values["beta"]**slider_values["theta"]))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y,mode="lines+markers",marker=dict(color="#00ffff")))
    fig.update_layout(title=f"{target_variable} vs S",xaxis_title="S",yaxis_title=f"{target_variable}",template="plotly_dark")
    st.plotly_chart(fig,use_container_width=True)

    # 3D Surface
    st.subheader("🌐 3D Variable Interaction Map")
    var_x, var_y = st.columns(2)
    with var_x: x_var = st.selectbox("X-axis variable:", list(slider_values.keys()), index=list(slider_values.keys()).index("S"))
    with var_y: y_var = st.selectbox("Y-axis variable:", list(slider_values.keys()), index=list(slider_values.keys()).index("A"))

    X = np.linspace(0.1,10,30)
    Y = np.linspace(0.1,10,30)
    Z = np.zeros((len(X),len(Y)))
    for i,xv in enumerate(X):
        for j,yv in enumerate(Y):
            vals = slider_values.copy()
            vals[x_var] = xv
            vals[y_var] = yv
            Z[i,j] = compute_consciousness(**vals)

    fig3d = go.Figure(data=[go.Surface(z=Z,x=X,y=Y,colorscale='Viridis')])
    fig3d.update_layout(scene=dict(xaxis_title=x_var, yaxis_title=y_var, zaxis_title="C"),template="plotly_dark",height=600)
    st.plotly_chart(fig3d,use_container_width=True)

    # Scenario History
    st.subheader("📋 Scenario History / Comparison")
    st.dataframe(pd.DataFrame(st.session_state.history))

# ------------------------------
# Possibilities Tab
# ------------------------------
with possibilities_tab:
    st.markdown("""
    <div class='hud-box'>
    <h2 class='neon-header'>🚀 Unlocking Infinite Possibilities</h2>
    <ul class='possibility'>
        <li>Human-AI cognitive modeling</li>
        <li>Mind-state prediction & optimization</li>
        <li>Virtual scenario testing</li>
        <li>Education & neuroscience simulations</li>
        <li>High-attention, high-memory environments</li>
        <li>Randomized cognitive state exploration</li>
        <li>AI-guided scenario creation</li>
        <li>Multi-dimensional surface exploration</li>
        <li>Influence analysis of each variable on consciousness</li>
        <li>Creative AI scenario suggestions</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# AIBuddy Hub Tab
# ------------------------------
with aibuddy_tab:
    st.subheader("💡 AI Suggestions")
    ai_choices = ai_suggestions(slider_values)
    ai_names = [name for name,_ in ai_choices]
    ai_selected = st.selectbox("Select AI Scenario", ai_names)
    if st.button("Apply Scenario"):
        selected_vals = dict(dict(ai_choices)[ai_selected])
        st.session_state.sliders.update(selected_vals)
        st.experimental_rerun()

    st.subheader("💬 Ask AIBuddy")
    user_question = st.text_input("Type a question:")
    if st.button("Consult AIBuddy"):
        if user_question.strip():
            response = f"AIBuddy Response: Adjust variables such as 'A' and 'S' to optimize {target_variable}. Explore creative scenarios!"
            st.markdown(f"<div class='hud-box'>{response}</div>", unsafe_allow_html=True)
        else:
            st.warning("Type a question to get a response.")
