import streamlit as st
import pandas as pd

st.title("The Complex Equation Simulator")

# Sliders for parameters
attention = st.slider("Attention (A)", 0.1, 2.0, 1.0, 0.05)
memory = st.slider("Memory (M)", 0.1, 2.0, 0.7, 0.05)
sensory = st.slider("Sensory Processing (S)", 1, 20, 10, 1)
higher_dim = st.slider("Higher-Dimensional Space (Dₙ)", 1.0, 10.0, 4.0, 0.1)

# Constants / fixed parameters (you can make these sliders too if you want)
R = 100
alpha = 1.5
beta = 2.0
theta = 1.0
Q = 1.0
E = 1.0

def calculate_complexity(R, alpha, theta, S, Q, A, E, M, Dn, beta):
    numerator = R * (alpha ** theta) * S * Q * (1.2 * A) * E * (1.5 * M)
    denominator = Dn * (beta ** theta)
    C = numerator / denominator
    return C

# Calculate current complexity
C = calculate_complexity(R, alpha, theta, sensory, Q, attention, E, memory, higher_dim, beta)

st.markdown(f"### Calculated Complexity (C): {C:.2f}")

# Prepare sample values for visualization (vary Attention and Memory)
attention_vals = [0.5, 0.7, 0.9, 1.0, 1.2]
memory_vals = [0.4, 0.6, 0.7, 0.8, 1.0]

complexity_attention = [
    calculate_complexity(R, alpha, theta, sensory, Q, a, E, memory, higher_dim, beta) for a in attention_vals
]
complexity_memory = [
    calculate_complexity(R, alpha, theta, sensory, Q, attention, E, m, higher_dim, beta) for m in memory_vals
]

df = pd.DataFrame({
    "Varying Attention": complexity_attention,
    "Varying Memory": complexity_memory
}, index=attention_vals)

st.line_chart(df)
