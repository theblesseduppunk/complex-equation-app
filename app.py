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
