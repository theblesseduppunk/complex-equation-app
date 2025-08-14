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
st.set_page_config(page_title="The Complex Equation", page_icon="🧠", layout="wide")

st.title("🧠 The Complex Equation")
st.markdown("""
This app models **The Complex Equation** — a theoretical framework developed by **Sam Andrews Rodriguez II**  
to explore the interplay between consciousness, sensory processing, attention, and environmental factors.
""")

# ------------------------------
# Sidebar - Variable Inputs
# ------------------------------
st.sidebar.header("Adjust Parameters or Generate Random Scenario")

def random_scenario():
    return {
        "R": round(random.uniform(0.1, 10.0), 1),
        "alpha": round(random.uniform(0.1, 5.0), 1),
        "theta": round(random.uniform(0.1, 5.0), 1),
        "S": round(random.uniform(0.1, 10.0), 1),
        "Q": round(random.uniform(0.1, 10.0), 1),
        "A": round(random.uniform(0.1, 10.0), 1),
        "E": round(random.uniform(0.1, 10.0), 1),
        "M": round(random.uniform(0.1, 10.0), 1),
        "Dn": round(random.uniform(0.1, 10.0), 1),
        "beta": round(random.uniform(0.1, 5.0), 1)
    }

# Button triggers random scenario
if st.sidebar.button("🎲 Generate Random Scenario"):
    scenario = random_scenario()
    # Inject JavaScript to scroll to simulation section
    st.markdown("""
    <script>
    const element = document.getElementById('simulation-section');
    if (element) { element.scrollIntoView({ behavior: 'smooth' }); }
    </script>
    """, unsafe_allow_html=True)
else:
    scenario = None

# Slider values with tooltips
R = st.sidebar.slider("Sensory Processing (R)", 0.1, 10.0, scenario["R"] if scenario else 5.0, 0.1, help="How strongly the system responds to sensory input")
alpha = st.sidebar.slider("Alpha (α)", 0.1, 5.0, scenario["alpha"] if scenario else 1.0, 0.1)
theta = st.sidebar.slider("Theta (θ)", 0.1, 5.0, scenario["theta"] if scenario else 1.0, 0.1)
S = st.sidebar.slider("Stimulus (S)", 0.1, 10.0, scenario["S"] if scenario else 5.0, 0.1)
Q = st.sidebar.slider("Quality (Q)", 0.1, 10.0, scenario["Q"] if scenario else 5.0, 0.1)
A = st.sidebar.slider("Attention (A)", 0.1, 10.0, scenario["A"] if scenario else 5.0, 0.1)
E = st.sidebar.slider("Environment (E)", 0.1, 10.0, scenario["E"] if scenario else 5.0, 0.1)
M = st.sidebar.slider("Memory (M)", 0.1, 10.0, scenario["M"] if scenario else 5.0, 0.1)
Dn = st.sidebar.slider("Distraction (Dₙ)", 0.1, 10.0, scenario["Dn"] if scenario else 5.0, 0.1)
beta = st.sidebar.slider("Beta (β)", 0.1, 5.0, scenario["beta"] if scenario else 1.0, 0.1)

# ------------------------------
# Cached computation
# ------------------------------
@st.cache_data
def compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta):
    return (R * (alpha ** theta) * S * Q * (1.3 * A) * E * (1.6 * M)) / (Dn * (beta ** theta))

C = compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta)

# ------------------------------
# Sensitivity / suggestion
# ------------------------------
most_influential = max(
    {"R": R, "A": A, "S": S, "Q": Q, "E": E, "M": M}.items(),
    key=lambda x: x[1]
)[0]

st.info(f"Currently, **{most_influential}** has the largest impact on Consciousness (C)")

# ------------------------------
# Section marker for smooth scroll
# ------------------------------
st.markdown('<div id="simulation-section"></div>', unsafe_allow_html=True)

# ------------------------------
# Equation Result
# ------------------------------
st.subheader("📊 Equation Result")
st.metric(label="Consciousness Level (C)", value=f"{C:.4f}")

# ------------------------------
# Visualization
# ------------------------------
x = np.linspace(0.1, 10, 50)
y = (R * (alpha ** theta) * x * Q * (1.3 * A) * E * (1.6 * M)) / (Dn * (beta ** theta))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name="C vs S", marker=dict(color="cyan")))
fig.update_layout(
    title="Consciousness Level vs Stimulus (S)",
    xaxis_title="Stimulus (S)",
    yaxis_title="Consciousness Level (C)",
    template="plotly_dark"
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Download CSV and JSON
# ------------------------------
data = {
    "R": [R], "alpha": [alpha], "theta": [theta], "S": [S], "Q": [Q], "A": [A],
    "E": [E], "M": [M], "Dn": [Dn], "beta": [beta], "C": [C]
}
df = pd.DataFrame(data)

csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
st.download_button(
    label="Download Result as CSV",
    data=csv_buffer.getvalue(),
    file_name="complex_equation_result.csv",
    mime="text/csv"
)

st.download_button(
    label="Download Result as JSON",
    data=json.dumps(data, indent=4),
    file_name="complex_equation_result.json",
    mime="application/json"
)
