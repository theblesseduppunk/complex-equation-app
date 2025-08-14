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
st.set_page_config(page_title="MindScape (The Complex Equation Simulator)", page_icon="🧠", layout="wide")

# ------------------------------
# CSS: Modern Dark Cyberpunk Theme
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

body, h1, h2, h3, p, div, span, button, label { 
    font-family:'Roboto Mono', monospace !important; 
    background-color:#070707; margin:0; padding:0;
    color:#eee;
}

/* HUD boxes */
.hud-box {
    background: rgba(0,0,0,0.35); 
    border:1.5px solid #00cccc; 
    border-radius:15px; 
    padding:15px; 
    margin-bottom:20px; 
    box-shadow:0 0 20px #00cccc,0 0 25px #cc00ff;
}

/* Neon headers for tabs */
.sim-header {color:#00cccc; text-shadow:0 0 5px #00cccc,0 0 10px #cc00ff;}
.poss-header {color:#cc00ff; text-shadow:0 0 5px #cc00ff,0 0 10px #00cccc;}
.aibuddy-header {color:#ffcc00; text-shadow:0 0 5px #ffcc00,0 0 10px #ffaa00;}

/* Metric display */
.metric-display {animation: pulse 2s infinite, glowPulse 3s infinite; font-size:2.5em; text-align:center; color:#00cccc;}
@keyframes pulse {0%{text-shadow:0 0 5px #00cccc;}50%{text-shadow:0 0 12px #cc00ff;}100%{text-shadow:0 0 5px #00cccc;}}
@keyframes glowPulse {0%{box-shadow:0 0 10px #00cccc;}50%{box-shadow:0 0 18px #cc00ff;}100%{box-shadow:0 0 10px #00cccc;}}

/* Particle overlay */
.particle-overlay {position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0; transition: all 1.5s ease;}
.particle {position:absolute; width:2px; height:2px; background:#00cccc; border-radius:50%; opacity:0.6; animation: floatStars linear infinite;}
.neon-streak {position:absolute; width:2px; height:100px; background:linear-gradient(180deg,#cc00ff,#00cccc); opacity:0.5; animation: streakMove linear infinite;}
@keyframes floatStars {0%{transform: translateY(0) translateX(0);}100%{transform: translateY(-110vh) translateX(50px);}}
@keyframes streakMove {0%{transform: translateY(100vh) translateX(0);}100%{transform: translateY(-100vh) translateX(50px);}}
</style>

<div class="particle-overlay" id="particle-container"></div>

<script>
function createParticles(state) {
    const container = document.getElementById('particle-container');
    container.innerHTML = '';
    let count = 50;
    let colorPrimary = '#00cccc';
    let colorSecondary = '#cc00ff';
    if(state === 'chaotic'){ count = 100; colorPrimary='#ff6600'; colorSecondary='#ff00cc';}
    for(let i=0;i<count;i++){
        const el = document.createElement('div');
        el.className = (state==='chaotic')?'neon-streak':'particle';
        el.style.left = Math.random()*100 + 'vw';
        el.style.animationDuration = (2 + Math.random()*3)+'s';
        el.style.height = (state==='chaotic')? (50 + Math.random()*100)+'px':'2px';
        el.style.background = (state==='chaotic')? `linear-gradient(180deg, ${colorSecondary}, ${colorPrimary})` : colorPrimary;
        container.appendChild(el);
    }
}
</script>
""", unsafe_allow_html=True)

# ------------------------------
# Welcome Box
# ------------------------------
st.markdown("""
<div class="hud-box" style="text-align:center;">
    <div class="sim-header" style="font-size:2em;">🚀 MindScape</div>
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
# Dynamic Background + Particle Overlay
# ------------------------------
particle_state = "starry" if C < 4 else "balanced" if C<=6 else "chaotic"
st.markdown(f"<script>createParticles('{particle_state}');</script>", unsafe_allow_html=True)

# ------------------------------
# Tabs
# ------------------------------
sim_tab, possibilities_tab, aibuddy_tab = st.tabs(["🧠 Simulation", "🌌 Possibilities", "🤖 AIBuddy Hub"])

# ------------------------------
# Simulation Tab
# ------------------------------
with sim_tab:
    st.markdown('<div id="simulation-section"></div>', unsafe_allow_html=True)
    st.markdown(f"<div class='hud-box'><div class='sim-header'>📊 Result for {target_variable}</div><div class='metric-display'>{C:.4f}</div></div>", unsafe_allow_html=True)

    # 2D Plot
    x = np.linspace(0.1,10,50)
    y = (slider_values["R"]*(slider_values["alpha"]**slider_values["theta"])*x*slider_values["Q"]*(1.3*slider_values["A"])*slider_values["E"]*(1.6*slider_values["M"]))/(slider_values["Dn"]*(slider_values["beta"]**slider_values["theta"]))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y,mode="lines+markers",marker=dict(color="#00cccc")))
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
# Expanded Possibilities Tab
# ------------------------------
with possibilities_tab:
    st.markdown("""
    <div class='hud-box'>
    <h2 class='poss-header'>🚀 Unlocking Infinite Possibilities</h2>
    
    <h3 style='color:#00ffcc;'>🌐 Real World Scenarios</h3>
    <ul class='possibility'>
        <li>Human cognitive optimization in workplace settings</li>
        <li>Stress & attention management for learning</li>
        <li>Social interaction prediction and outcome analysis</li>
        <li>Memory enhancement exercises</li>
    </ul>

    <h3 style='color:#cc00ff;'>🕹 Virtuality Scenarios</h3>
    <ul class='possibility'>
        <li>Immersive VR simulations of cognitive states</li>
        <li>Virtual collaborative problem solving</li>
        <li>Scenario-based learning in virtual environments</li>
        <li>Adaptive AI-driven training simulations</li>
    </ul>

    <h3 style='color:#ffaa00;'>🤖 AI & Hybrid Scenarios</h3>
    <ul class='possibility'>
        <li>AI-guided human decision modeling</li>
        <li>AI-assisted scenario creation for complex environments</li>
        <li>Joint real-world + AI simulations for behavioral analysis</li>
        <li>Virtual worlds predicting real-world outcomes</li>
        <li>AI-driven multi-agent interactions in hybrid spaces</li>
    </ul>

    <h3 style='color:#00ffff;'>🌌 Mixed Reality / Infinite Possibilities</h3>
    <ul class='possibility'>
        <li>Predictive cognition simulations linking VR and real life</li>
        <li>AI-enhanced social experiment modeling</li>
        <li>Joint virtuality + AI-guided training</li>
        <li>Exploration of consciousness under hybrid reality conditions</li>
        <li>Dynamic simulations of attention, memory, and perception in real & virtual environments</li>
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
