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
# Intro / Welcome Panel
# ------------------------------
st.markdown("""
<style>
@keyframes fadeIn { from {opacity:0; transform:translateY(-10px);} to {opacity:1; transform:translateY(0);} }
.welcome-box {
    animation: fadeIn 1.5s ease-out forwards;
    padding: 25px; border-radius: 15px;
    background: linear-gradient(135deg, rgba(0,0,0,0.85), rgba(20,20,40,0.9));
    box-shadow: 0 0 15px rgba(0,255,255,0.5); color: white;
    font-family: 'Futura', sans-serif; margin-bottom: 30px;
}
.launch-btn { background: linear-gradient(90deg, cyan, magenta); border:none; padding:12px 24px; border-radius:25px; color:black; font-size:1.1em; font-weight:bold; cursor:pointer; transition:all 0.3s ease; }
.launch-btn:hover { transform: scale(1.05); box-shadow: 0px 0px 15px rgba(0,255,255,0.7); }
</style>
<script>
function scrollToSimulation() {
    const element = document.getElementById('simulation-section');
    if (element) { element.scrollIntoView({ behavior: 'smooth' }); }
}
</script>
<div class="welcome-box">
    <div style="font-size:2em;font-weight:bold;color:cyan;">🚀 Welcome to The Complex Equation</div>
    <div style="margin-top:10px;font-size:1.2em;">
        This is a **next-generation simulation engine** created by <b>Sam Andrews Rodriguez II</b>.  
        Explore consciousness, cognitive states, sensory effects, and environmental interactions in one unified framework.
    </div>
    <hr style="border:0.5px solid rgba(0,255,255,0.3);margin:10px 0;">
    <ul>
        <li>🧠 Model consciousness dynamics and human cognition</li>
        <li>🎯 Simulate learning, attention, and memory effects</li>
        <li>🌍 Explore environmental and global system interactions</li>
        <li>🤖 Test AI behavior or neural network responses</li>
        <li>🔬 Discover hidden variable patterns and relationships</li>
        <li>🎨 Inspire new forms of art, storytelling, and immersive experiences</li>
    </ul>
    <button class="launch-btn" onclick="scrollToSimulation()">🔥 Launch Simulation</button>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar - Variables & Random Scenario
# ------------------------------
st.sidebar.header("Adjust Parameters or Generate Random Scenario")

def random_scenario():
    return {k: round(random.uniform(0.1, 10.0), 1) for k in ["R","S","Q","A","E","M","Dn"]}
scenario_button = st.sidebar.button("🎲 Generate Random Scenario")

# Initial slider defaults
default_values = {"R":5.0,"alpha":1.0,"theta":1.0,"S":5.0,"Q":5.0,"A":5.0,"E":5.0,"M":5.0,"Dn":5.0,"beta":1.0}

# If random scenario generated, override defaults
if scenario_button:
    scenario_values = random_scenario()
    # Animate sliders (pseudo animation)
    for key in scenario_values:
        default_values[key] = scenario_values[key]

# Sliders
R = st.sidebar.slider("Sensory Processing (R)", 0.1, 10.0, default_values["R"], 0.1, help="How strongly the system responds to sensory input")
alpha = st.sidebar.slider("Alpha (α)", 0.1, 5.0, default_values["alpha"], 0.1)
theta = st.sidebar.slider("Theta (θ)", 0.1, 5.0, default_values["theta"], 0.1)
S = st.sidebar.slider("Stimulus (S)", 0.1, 10.0, default_values["S"], 0.1)
Q = st.sidebar.slider("Quality (Q)", 0.1, 10.0, default_values["Q"], 0.1)
A = st.sidebar.slider("Attention (A)", 0.1, 10.0, default_values["A"], 0.1)
E = st.sidebar.slider("Environment (E)", 0.1, 10.0, default_values["E"], 0.1)
M = st.sidebar.slider("Memory (M)", 0.1, 10.0, default_values["M"], 0.1)
Dn = st.sidebar.slider("Distraction (Dₙ)", 0.1, 10.0, default_values["Dn"], 0.1)
beta = st.sidebar.slider("Beta (β)", 0.1, 5.0, default_values["beta"], 0.1)

# ------------------------------
# Cached computation
# ------------------------------
@st.cache_data
def compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta):
    return (R * (alpha ** theta) * S * Q * (1.3 * A) * E * (1.6 * M)) / (Dn * (beta ** theta))

C = compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta)

# ------------------------------
# Sensitivity
# ------------------------------
most_influential = max({"R":R,"A":A,"S":S,"Q":Q,"E":E,"M":M}.items(), key=lambda x:x[1])[0]
st.info(f"Currently, **{most_influential}** has the largest impact on Consciousness (C)")

# ------------------------------
# Simulation Section
# ------------------------------
st.markdown('<div id="simulation-section"></div>', unsafe_allow_html=True)

st.subheader("📊 Equation Result")
st.metric(label="Consciousness Level (C)", value=f"{C:.4f}")

# ------------------------------
# Visualization
# ------------------------------
x = np.linspace(0.1, 10, 50)
y = (R*(alpha**theta)*x*Q*(1.3*A)*E*(1.6*M))/(Dn*(beta**theta))
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name="C vs S", marker=dict(color="cyan")))
fig.update_layout(title="Consciousness Level vs Stimulus (S)", xaxis_title="Stimulus (S)", yaxis_title="Consciousness Level (C)", template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Download CSV/JSON
# ------------------------------
data = {"R":[R],"alpha":[alpha],"theta":[theta],"S":[S],"Q":[Q],"A":[A],"E":[E],"M":[M],"Dn":[Dn],"beta":[beta],"C":[C]}
df = pd.DataFrame(data)
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
st.download_button("Download Result as CSV", csv_buffer.getvalue(), "complex_equation_result.csv", "text/csv")
st.download_button("Download Result as JSON", json.dumps(data, indent=4), "complex_equation_result.json", "application/json")
