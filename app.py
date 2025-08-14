# Complex Equation App — Full Version
# Author: Sam Andrews Rodriguez II

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.optimize import curve_fit

st.set_page_config(page_title="Complex Equation App", layout="wide")

# ------------------------
# Custom CSS Animations
# ------------------------
st.markdown("""
<style>
@keyframes fadeSlide {0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); }}
.possibility { animation: fadeSlide 1s ease-out forwards; margin-bottom: 20px; padding: 10px; border-radius: 10px;
background: linear-gradient(135deg, rgba(30,30,30,0.9), rgba(60,60,60,0.8)); border: 1px solid rgba(255,255,255,0.3);
box-shadow: 0px 0px 10px rgba(0,255,255,0.5); font-family: 'Futura', sans-serif; color: white; display: flex; align-items: center; gap: 10px; }
.possibility-1 { animation-delay: 0.2s; } .possibility-2 { animation-delay: 0.4s; } .possibility-3 { animation-delay: 0.6s; }
.possibility-4 { animation-delay: 0.8s; } .possibility-5 { animation-delay: 1s; } .possibility-6 { animation-delay: 1.2s; }
.possibility-7 { animation-delay: 1.4s; } .possibility-8 { animation-delay: 1.6s; } .possibility-9 { animation-delay: 1.8s; }
.possibility-10 { animation-delay: 2s; } .possibility-11 { animation-delay: 2.2s; } .possibility-12 { animation-delay: 2.4s; }
.emoji { font-size: 1.5em; }
</style>
""", unsafe_allow_html=True)

# ------------------------
# Possibilities Section
# ------------------------
possibilities = [
    ("🧠", "Model Consciousness Dynamics"), ("🎯", "Simulate Cognitive States"),
    ("📚", "Analyze Learning Processes"), ("👁", "Explore Sensory Processing Effects"),
    ("✨", "Study Higher-Dimensional Influences"), ("🤖", "Test AI or Neural Network Behavior"),
    ("🧬", "Investigate Neurological Conditions"), ("📜", "Support Philosophical Inquiry"),
    ("🎓", "Enhance Educational Tools"), ("🚀", "Drive Innovation in Technology"),
    ("🌍", "Visualize Complex Systems"), ("🔗", "Facilitate Cross-Disciplinary Research")
]
for i, (emoji, text) in enumerate(possibilities, start=1):
    st.markdown(f'<div class="possibility possibility-{i}"><span class="emoji">{emoji}</span> {text}</div>', unsafe_allow_html=True)

# ------------------------
# Sidebar Inputs
# ------------------------
st.sidebar.title("Parameters & Settings")
equation_mode = st.sidebar.radio("Select Equation Mode:", ["Original Equation", "Power Law", "Inverted-U", "Saturation"],
                                 help="Choose which model you want to explore.")

R = st.sidebar.slider("Reality / Sensory Processing (R)", 0.1, 10.0, 1.0, 0.1)
alpha = st.sidebar.slider("Alpha (α)", 0.1, 2.0, 1.0, 0.01)
beta = st.sidebar.slider("Beta (β)", 0.1, 2.0, 1.0, 0.01)
theta = st.sidebar.slider("Theta (θ)", 0.1, 5.0, 1.0, 0.1)
S = st.sidebar.slider("Quality of Info (S)", 0.1, 10.0, 1.0, 0.1)
Q = st.sidebar.slider("Information Quality (Q)", 0.1, 10.0, 1.0, 0.1)
A = st.sidebar.slider("Attention (A)", 0.1, 10.0, 1.0, 0.1)
E = st.sidebar.slider("Emotional State (E)", 0.1, 10.0, 1.0, 0.1)
M = st.sidebar.slider("Memory (M)", 0.1, 10.0, 1.0, 0.1)
Dn = st.sidebar.slider("Neural Complexity (Dₙ)", 0.1, 10.0, 1.0, 0.1)

preset = st.sidebar.selectbox("Presets / Scenarios", ["None", "Creative Boost", "Cognitive Mode", "Physics Mode"])
if preset == "Creative Boost": R, Dn, A, M = 5.0, 2.0, 8.0, 7.0
elif preset == "Cognitive Mode": R, Dn, A, M = 3.0, 5.0, 5.0, 8.0
elif preset == "Physics Mode": R, Dn, A, M = 6.0, 6.0, 4.0, 4.0

show_surface = st.sidebar.checkbox("Show 3D Surface", True)
enable_fitting = st.sidebar.checkbox("Enable Data Fitting Mode", False)

# ------------------------
# Equations
# ------------------------
def original_equation(R, alpha, beta, theta, S, Q, A, E, M, Dn):
    return (R * alpha**theta * S * Q * (1.3 * A) * E * (1.6 * M)) / (Dn * beta**theta)
def power_law(R, D, p=1.0): return R / D**p
def inverted_U(R, D, p=1.0, lam=0.1, scale=1.0): return scale * R * D**p * np.exp(-lam * D)
def saturation(R, D, p=1.0, k=1.0, scale=1.0): return scale * R * (D**p)/(D**p + k)

# ------------------------
# Compute C
# ------------------------
if equation_mode=="Original Equation": C=original_equation(R, alpha, beta, theta, S, Q, A, E, M, Dn)
elif equation_mode=="Power Law": C=power_law(R,Dn)
elif equation_mode=="Inverted-U": C=inverted_U(R,Dn)
elif equation_mode=="Saturation": C=saturation(R,Dn)

st.subheader("✅ Computed Output")
st.metric("C (Complexity / Consciousness)", round(C,3))

# ------------------------
# 3D Plot
# ------------------------
if show_surface:
    A_range = np.linspace(0.1,10,20); M_range = np.linspace(0.1,10,20)
    A_grid,M_grid=np.meshgrid(A_range,M_range)
    C_grid = original_equation(R,alpha,beta,theta,S,Q,A_grid,E,M_grid,Dn) if equation_mode=="Original Equation" else C*np.ones_like(A_grid)
    fig = go.Figure(data=[go.Surface(z=C_grid,x=A_range,y=M_range)])
    fig.update_layout(scene=dict(xaxis_title='Attention (A)',yaxis_title='Memory (M)',zaxis_title='C'),
                      title="3D Surface: Attention & Memory vs Complexity")
    st.plotly_chart(fig,use_container_width=True)

# ------------------------
# Data Fitting Mode
# ------------------------
if enable_fitting:
    st.subheader("📂 Data Fitting Mode")
    uploaded_file = st.file_uploader("Upload CSV (columns: R,D,C_obs)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file); st.write("Data Preview:",df.head())
        R_data = df['R'].values; D_data=df['D'].values; C_obs=df['C_obs'].values
        try:
            popt,_=curve_fit(lambda D,p: power_law(R_data,D,p),D_data,C_obs,p0=[1.0])
            st.write(f"Fitted Power Law exponent p = {popt[0]:.3f}")
        except Exception as e: st.error(f"Error fitting data: {e}")

# ------------------------
# AI Discovery Mode
# ------------------------
st.sidebar.subheader("🤖 AI Discovery Mode")
enable_ai_discovery = st.sidebar.checkbox("Enable AI Discovery", False)

if enable_ai_discovery:
    st.subheader("🤖 AI Discovery Mode: Suggested Parameter Sets")
    num_samples = st.sidebar.slider("Number of Random Trials", 10, 500, 100)
    best_results = []
    for _ in range(num_samples):
        R_rand = np.random.uniform(0.1,10); alpha_rand=np.random.uniform(0.1,2); beta_rand=np.random.uniform(0.1,2)
        theta_rand=np.random.uniform(0.1,5); S_rand=np.random.uniform(0.1,10); Q_rand=np.random.uniform(0.1,10)
        A_rand=np.random.uniform(0.1,10); E_rand=np.random.uniform(0.1,10); M_rand=np.random.uniform(0.1,10)
        Dn_rand=np.random.uniform(0.1,10)
        if equation_mode=="Original Equation":
            C_rand=original_equation(R_rand, alpha_rand, beta_rand, theta_rand, S_rand, Q_rand, A_rand, E_rand, M_rand, Dn_rand)
        elif equation_mode=="Power Law": C_rand=power_law(R_rand,Dn_rand)
        elif equation_mode=="Inverted-U": C_rand=inverted_U(R_rand,Dn_rand)
        elif equation_mode=="Saturation": C_rand=saturation(R_rand,Dn_rand)
        best_results.append((C_rand,R_rand,alpha_rand,beta_rand,theta_rand,S_rand,Q_rand,A_rand,E_rand,M_rand,Dn_rand))
    best_results.sort(reverse=True,key=lambda x:x[0])
    top_n=5; top_results=best_results[:top_n]
    results_df=pd.DataFrame(top_results, columns=["C","R","α","β","θ","S","Q","A","E","M","Dₙ"])
    st.dataframe(results_df)

# ------------------------
# Universe Simulation Mode
# ------------------------
st.sidebar.subheader("🌌 Universe Simulation Mode")
enable_universe_sim = st.sidebar.checkbox("Enable Universe Simulation", False)

if enable_universe_sim:
    st.subheader("🌌 Universe Simulation")
    num_universes = st.sidebar.slider("Number of Universes", 1, 10, 3)
    time_steps = st.sidebar.slider("Time Steps", 10, 100, 50)
    randomness = st.sidebar.slider("Random Perturbation Magnitude", 0.0, 1.0, 0.1)
    
    universe_results = []
    
    for u in range(num_universes):
        R_u, alpha_u, beta_u, theta_u, S_u, Q_u, A_u, E_u, M_u, Dn_u = np.random.uniform(0.5,5), np.random.uniform(0.8,1.5), np.random.uniform(0.8,1.5), np.random.uniform(0.5,3), np.random.uniform(0.5,5), np.random.uniform(0.5,5), np.random.uniform(0.5,5), np.random.uniform(0.5,5), np.random.uniform(0.5,5), np.random.uniform(0.5,5)
        C_timeline=[]
        for t in range(time_steps):
            if equation_mode=="Original Equation": C_t=original_equation(R_u, alpha_u, beta_u, theta_u, S_u, Q_u, A_u, E_u, M_u, Dn_u)
            elif equation_mode=="Power Law": C_t=power_law(R_u,Dn_u)
            elif equation_mode=="Inverted-U": C_t=inverted_U(R_u,Dn_u)
            elif equation_mode=="Saturation": C_t=saturation(R_u,Dn_u)
            C_timeline.append(C_t)
            # Random perturbations
            R_u += np.random.uniform(-randomness, randomness)
            alpha_u += np.random.uniform(-randomness*0.1, randomness*0.1)
            beta_u += np.random.uniform(-randomness*0.1, randomness*0.1)
            theta_u += np.random.uniform(-randomness*0.1, randomness*0.1)
            A_u += np.random.uniform(-randomness*0.1, randomness*0.1)
            M_u += np.random.uniform(-randomness*0.1, randomness*0.1)
        universe_results.append(C_timeline)
    
    universe_df = pd.DataFrame(universe_results).T
    universe_df.columns = [f"Universe {i+1}" for i in range(num_universes)]
    st.line_chart(universe_df)
