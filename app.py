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
st.set_page_config(page_title="The Complex Equation", page_icon="🧠", layout="wide")

# ------------------------------
# Welcome Panel + CSS + JS
# ------------------------------
st.markdown("""
<style>
@keyframes fadeIn { from {opacity:0; transform:translateY(-10px);} to {opacity:1; transform:translateY(0);} }
.welcome-box {
    animation: fadeIn 1.5s ease-out forwards;
    padding: 30px; border-radius: 15px;
    background: linear-gradient(135deg, rgba(0,0,0,0.85), rgba(20,20,40,0.9));
    box-shadow: 0 0 20px rgba(0,255,255,0.5); color: white;
    font-family: 'Futura', sans-serif; margin-bottom: 30px;
    text-align: center;
}
.launch-btn {
    background: linear-gradient(90deg, cyan, magenta); border:none; 
    padding:15px 30px; border-radius:25px; color:black; font-size:1.2em; font-weight:bold; cursor:pointer; 
    transition:all 0.3s ease;
}
.launch-btn:hover { transform: scale(1.05); box-shadow: 0px 0px 20px rgba(0,255,255,0.7); }
</style>

<script>
function scrollToSimulation() {
    const element = document.getElementById('simulation-section');
    if (element) { element.scrollIntoView({ behavior: 'smooth' }); }
}
</script>

<div class="welcome-box">
    <div style="font-size:2.5em;font-weight:bold;color:cyan;">🚀 Welcome to The Complex Equation</div>
    <div style="margin-top:15px;font-size:1.3em;">
        This is a **next-generation simulation engine** created by <b>Sam Andrews Rodriguez II</b>.
        Explore consciousness, cognitive states, sensory effects, memory, attention, and environmental interactions in one unified framework.
    </div>
    <hr style="border:0.5px solid rgba(0,255,255,0.3);margin:15px 0;">
    <div style="font-size:1.1em;">
        With this app, you can:
        <ul>
            <li>🧠 Model the dynamics of consciousness and human cognition</li>
            <li>🎯 Simulate attention, learning, and memory processes</li>
            <li>🌍 Explore how environmental factors affect cognitive states</li>
            <li>🤖 Test AI or neural network behavior in multi-variable scenarios</li>
            <li>🔬 Discover hidden relationships between complex variables</li>
            <li>🎨 Inspire new forms of art, storytelling, and immersive experiences</li>
            <li>📊 Generate and export results for analysis (CSV/JSON)</li>
        </ul>
    </div>
    <button class="launch-btn" onclick="scrollToSimulation()">🔥 Launch Simulation</button>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar - Variables & Scenarios
# ------------------------------
st.sidebar.header("Adjust Parameters or Generate Scenarios")
default_values = {"R":5.0,"alpha":1.0,"theta":1.0,"S":5.0,"Q":5.0,"A":5.0,"E":5.0,"M":5.0,"Dn":5.0,"beta":1.0}
if "sliders" not in st.session_state:
    st.session_state.sliders = default_values.copy()
if "history" not in st.session_state:
    st.session_state.history = []

demo_values = {"R":7.0,"alpha":1.2,"theta":1.0,"S":8.0,"Q":7.0,"A":9.0,"E":6.0,"M":8.0,"Dn":2.0,"beta":1.0}

# ------------------------------
# Functions for Scenarios
# ------------------------------
def generate_random_scenario():
    return {k: round(random.uniform(0.1,10.0),1) for k in st.session_state.sliders.keys()}

def animate_sliders(target_values, steps=20, delay=0.03):
    for i in range(1, steps+1):
        for key in st.session_state.sliders:
            current = st.session_state.sliders[key]
            st.session_state.sliders[key] = current + (target_values[key]-current)*(i/steps)
        time.sleep(delay)
        st.experimental_rerun()

def compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta):
    return (R*(alpha**theta)*S*Q*(1.3*A)*E*(1.6*M))/(Dn*(beta**theta))

# ------------------------------
# Buttons
# ------------------------------
if st.sidebar.button("📈 Load Demo Scenario"):
    animate_sliders(demo_values)
    st.markdown('<script>scrollToSimulation()</script>', unsafe_allow_html=True)

if st.sidebar.button("🎲 Generate Random Scenario"):
    animate_sliders(generate_random_scenario())
    st.markdown('<script>scrollToSimulation()</script>', unsafe_allow_html=True)

# ------------------------------
# Display Sliders
# ------------------------------
R = st.sidebar.slider("Sensory Processing (R)",0.1,10.0,st.session_state.sliders["R"],0.1, help="How strongly the senses influence consciousness")
alpha = st.sidebar.slider("Alpha (α)",0.1,5.0,st.session_state.sliders["alpha"],0.1, help="Scaling factor for attention and learning")
theta = st.sidebar.slider("Theta (θ)",0.1,5.0,st.session_state.sliders["theta"],0.1, help="Exponent for sensitivity")
S = st.sidebar.slider("Stimulus (S)",0.1,10.0,st.session_state.sliders["S"],0.1)
Q = st.sidebar.slider("Quality (Q)",0.1,10.0,st.session_state.sliders["Q"],0.1)
A = st.sidebar.slider("Attention (A)",0.1,10.0,st.session_state.sliders["A"],0.1)
E = st.sidebar.slider("Environment (E)",0.1,10.0,st.session_state.sliders["E"],0.1)
M = st.sidebar.slider("Memory (M)",0.1,10.0,st.session_state.sliders["M"],0.1)
Dn = st.sidebar.slider("Distraction (Dₙ)",0.1,10.0,st.session_state.sliders["Dn"],0.1)
beta = st.sidebar.slider("Beta (β)",0.1,5.0,st.session_state.sliders["beta"],0.1)

# ------------------------------
# Compute Consciousness
# ------------------------------
C = compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta)

# Save scenario to history
st.session_state.history.append({**st.session_state.sliders, "C": C})

# ------------------------------
# Sensitivity Highlight
# ------------------------------
influences = {"R":R,"A":A,"S":S,"Q":Q,"E":E,"M":M}
most_influential = max(influences.items(), key=lambda x:x[1])[0]
st.info(f"Currently, **{most_influential}** has the largest impact on Consciousness (C)")

# ------------------------------
# Simulation Section
# ------------------------------
st.markdown('<div id="simulation-section"></div>', unsafe_allow_html=True)
st.subheader("📊 Equation Result")
st.metric(label="Consciousness Level (C)", value=f"{C:.4f}")

# Dynamic description
desc = f"Consciousness (C) is influenced most by **{most_influential}**. Adjust sliders to explore how changes affect C."
st.markdown(desc)

# ------------------------------
# Visualization
# ------------------------------
x = np.linspace(0.1,10,50)
y = (R*(alpha**theta)*x*Q*(1.3*A)*E*(1.6*M))/(Dn*(beta**theta))
color = f"rgb({min(255,int(C*5))},0,{255-min(255,int(C*5))})"
fig = go.Figure()
fig.add_trace(go.Scatter(x=x,y=y,mode="lines+markers",name="C vs S",marker=dict(color=color)))
fig.update_layout(title="Consciousness Level vs Stimulus (S)",xaxis_title="Stimulus (S)",yaxis_title="Consciousness Level (C)",template="plotly_dark")
st.plotly_chart(fig,use_container_width=True)

# ------------------------------
# Scenario History Table
# ------------------------------
st.subheader("📋 Scenario History / Comparison")
history_df = pd.DataFrame(st.session_state.history)
st.dataframe(history_df)

# ------------------------------
# Download CSV/JSON
# ------------------------------
data = {**st.session_state.sliders,"C": C}
df = pd.DataFrame([data])
csv_buffer = StringIO()
df.to_csv(csv_buffer,index=False)
st.download_button("Download Result as CSV",csv_buffer.getvalue(),"complex_equation_result.csv","text/csv")
st.download_button("Download Result as JSON",json.dumps(data,indent=4),"complex_equation_result.json","application/json")
