import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="The Complex Equation", layout="wide")

st.title("🧠 The Complex Equation")
st.markdown("""
This app models **The Complex Equation** — a theoretical framework developed by **Sam Andrews Rodriguez II**  
to explore the interplay between consciousness, sensory processing, attention, and environmental factors.
""")

# ------------------------------
# Sidebar - Variable Inputs
# ------------------------------
st.sidebar.header("Adjust Parameters")

R = st.sidebar.slider("Sensory Processing (R)", 0.1, 10.0, 5.0, 0.1)
alpha = st.sidebar.slider("Alpha (α)", 0.1, 5.0, 1.0, 0.1)
theta = st.sidebar.slider("Theta (θ)", 0.1, 5.0, 1.0, 0.1)
S = st.sidebar.slider("Stimulus (S)", 0.1, 10.0, 5.0, 0.1)
Q = st.sidebar.slider("Quality (Q)", 0.1, 10.0, 5.0, 0.1)
A = st.sidebar.slider("Attention (A)", 0.1, 10.0, 5.0, 0.1)
E = st.sidebar.slider("Environment (E)", 0.1, 10.0, 5.0, 0.1)
M = st.sidebar.slider("Memory (M)", 0.1, 10.0, 5.0, 0.1)
Dn = st.sidebar.slider("Distraction (Dₙ)", 0.1, 10.0, 5.0, 0.1)
beta = st.sidebar.slider("Beta (β)", 0.1, 5.0, 1.0, 0.1)

# ------------------------------
# The Complex Equation
# ------------------------------
C = (R * (alpha ** theta) * S * Q * (1.3 * A) * E * (1.6 * M)) / (Dn * (beta ** theta))

st.subheader("📊 Equation Result")
st.metric(label="Consciousness Level (C)", value=f"{C:.4f}")

# ------------------------------
# Visualization
# ------------------------------
x = np.linspace(0.1, 10, 50)
y = (R * (alpha ** theta) * x * Q * (1.3 * A) * E * (1.6 * M)) / (Dn * (beta ** theta))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="C vs S"))
fig.update_layout(
    title="Consciousness Level vs Stimulus (S)",
    xaxis_title="Stimulus (S)",
    yaxis_title="Consciousness Level (C)",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.markdown("**Created by Sam Andrews Rodriguez II — The Complex Equation**")
import streamlit as st

# App settings
st.set_page_config(page_title="The Complex Equation", page_icon="🧠", layout="wide")

# Custom JS for smooth scrolling
scroll_js = """
<script>
function scrollToSimulation() {
    const element = document.getElementById('simulation-section');
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}
</script>
"""

st.markdown(scroll_js, unsafe_allow_html=True)

# CSS styles for welcome + possibilities
st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlide {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}
.welcome-box {
    animation: fadeIn 1.5s ease-out forwards;
    padding: 25px;
    border-radius: 15px;
    background: linear-gradient(135deg, rgba(0,0,0,0.85), rgba(20,20,40,0.9));
    box-shadow: 0 0 15px rgba(0,255,255,0.5);
    color: white;
    font-family: 'Futura', sans-serif;
    margin-bottom: 30px;
}
.welcome-title {
    font-size: 2.2em;
    font-weight: bold;
    color: cyan;
}
.welcome-sub {
    font-size: 1.2em;
    margin-top: 10px;
}
.possibility {
    animation: fadeSlide 1s ease-out forwards;
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(30,30,30,0.9), rgba(60,60,60,0.8));
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0px 0px 10px rgba(0,255,255,0.5);
    font-family: 'Futura', sans-serif;
    color: white;
    display: flex;
    align-items: center;
    gap: 10px;
}
.launch-btn {
    background: linear-gradient(90deg, cyan, magenta);
    border: none;
    padding: 12px 24px;
    border-radius: 25px;
    color: black;
    font-size: 1.1em;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}
.launch-btn:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px rgba(0,255,255,0.7);
}
</style>
""", unsafe_allow_html=True)

# Welcome panel
st.markdown("""
<div class="welcome-box">
    <div class="welcome-title">🚀 Welcome to The Complex Equation</div>
    <div class="welcome-sub">
        A next-generation simulation and discovery engine for humans and AI alike.
        This app models consciousness, simulates cognitive states, explores sensory processing, and unites multi-dimensional variables into a single powerful framework.
    </div>
    <hr style="border: 0.5px solid rgba(0,255,255,0.3);">
    <p><b>In the world, this technology could:</b></p>
    <ul>
        <li>🧠 Advance neuroscience by mapping unknown consciousness patterns.</li>
        <li>🌍 Predict global systems — climate, economy, and social evolution.</li>
        <li>🤖 Help AI achieve creativity, emotion, and even self-awareness.</li>
        <li>🔬 Accelerate scientific discovery by revealing hidden variable links.</li>
        <li>🎨 Inspire new forms of art, storytelling, and immersive experiences.</li>
    </ul>
    <p><i>This is more than an app — it’s a launchpad for the next era of knowledge.</i></p>
    <button class="launch-btn" onclick="scrollToSimulation()">🔥 Launch Simulation</button>
</div>
""", unsafe_allow_html=True)

# Possibilities list
possibilities = [
    ("🧠", "Model Consciousness Dynamics"),
    ("🎯", "Simulate Cognitive States"),
    ("📚", "Analyze Learning Processes"),
    ("👁", "Explore Sensory Processing Effects"),
    ("✨", "Study Higher-Dimensional Influences"),
    ("🤖", "Test AI or Neural Network Behavior"),
    ("🧬", "Investigate Neurological Conditions"),
    ("📜", "Support Philosophical Inquiry"),
    ("🎓", "Enhance Educational Tools"),
    ("🚀", "Drive Innovation in Technology"),
    ("🌌", "Visualize Alternate Universes"),
    ("🔗", "Facilitate Cross-Disciplinary Research")
]

for i, (emoji, text) in enumerate(possibilities, start=1):
    st.markdown(f"""
    <div class="possibility possibility-{i}">
        <span class="emoji">{emoji}</span> {text}
    </div>
    """, unsafe_allow_html=True)

# Section marker for smooth scroll
st.markdown('<div id="simulation-section"></div>', unsafe_allow_html=True)
