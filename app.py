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
# Futuristic Styles + Animations
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

body, h1, h2, h3, h4, h5, h6, p, div, span, button, label {
    font-family:'Orbitron', monospace !important;
    color:#00ffff !important;
}

@keyframes fadeIn {from {opacity:0; transform:translateY(-10px);} to {opacity:1; transform:translateY(0);} }
@keyframes pulse {0% {box-shadow:0 0 10px cyan;} 50% {box-shadow:0 0 20px magenta;} 100% {box-shadow:0 0 10px cyan;}}

.welcome-box {
    animation: fadeIn 1.5s ease-out forwards;
    padding: 30px; border-radius: 15px;
    background: rgba(0,0,0,0.7); backdrop-filter: blur(10px);
    box-shadow: 0 0 30px rgba(0,255,255,0.5);
    text-align:center; margin-bottom:30px;
}
.launch-btn {
    background: linear-gradient(90deg, cyan, magenta); border:none; 
    padding:15px 30px; border-radius:25px; color:black; font-size:1.3em; font-weight:bold; cursor:pointer; transition:all 0.3s ease;
}
.launch-btn:hover { transform: scale(1.05); box-shadow: 0 0 25px cyan, 0 0 25px magenta; }

.slider-label {color:#00ffff; font-weight:bold;}
.metric-display {animation: pulse 2s infinite; font-family:'Orbitron', monospace;}

.possibility {margin:10px 0; padding:10px; border-radius:10px; background: rgba(0,0,0,0.5); border:1px solid #00ffff; box-shadow:0 0 15px #ff00ff;}
</style>

<script>
function scrollToSimulation() {
    const element = document.getElementById('simulation-section');
    if (element) { element.scrollIntoView({ behavior: 'smooth' }); }
}
</script>

<div class="welcome-box">
    <div style="font-size:2.8em; font-weight:bold;">🚀 The Complex Equation</div>
    <div style="margin-top:10px; font-size:1.3em;">
        A <b>simulation creator, the first of its kind</b> by <b>Sam Andrews Rodriguez II</b>.<br>
        Explore consciousness, cognitive states, memory, attention, environment, and AI scenarios.
    </div>
    <hr style="border:0.5px solid #00ffff; margin:15px 0;">
    <button class="launch-btn" onclick="scrollToSimulation()">🔥 Launch Simulation</button>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar Variables
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

def compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta):
    return (R*(alpha**theta)*S*Q*(1.3*A)*E*(1.6*M))/(Dn*(beta**theta))

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
# Sidebar Buttons
# ------------------------------
if st.sidebar.button("📈 Load Demo Scenario"):
    st.session_state.sliders.update(demo_values)
    st.markdown('<script>scrollToSimulation()</script>', unsafe_allow_html=True)

if st.sidebar.button("🎲 Generate Random Scenario"):
    st.session_state.sliders.update(generate_random_scenario())
    st.markdown('<script>scrollToSimulation()</script>', unsafe_allow_html=True)

# ------------------------------
# Variable Mode & Sliders
# ------------------------------
target_variable = st.sidebar.selectbox("Select variable to solve for:", variables, index=variables.index("C"))

slider_values = {}
col1, col2 = st.sidebar.columns(2)
for idx, var in enumerate(default_values.keys()):
    col = col1 if idx % 2 == 0 else col2
    slider_values[var] = col.slider(f"{var}", 0.1, 10.0, st.session_state.sliders[var], 0.1)

# AI Suggestions
st.sidebar.subheader("🤖 AIBuddy Suggestions")
ai_choices = ai_suggestions(slider_values)
ai_names = [name for name,_ in ai_choices]
ai_selected = st.sidebar.selectbox("Choose AI Scenario:", ai_names)
if st.sidebar.button("Apply AI Scenario"):
    selected_vals = dict(dict(ai_choices)[ai_selected])
    st.session_state.sliders.update(selected_vals)

# Compute target variable
C = compute_consciousness(**slider_values)
st.session_state.sliders.update(slider_values)
st.session_state.history.append({**st.session_state.sliders,"C":C})

# ------------------------------
# Sensitivity Highlight
# ------------------------------
influences = {k:slider_values[k] for k in ["R","A","S","Q","E","M"]}
sorted_influences = sorted(influences.items(), key=lambda x:x[1], reverse=True)[:3]
st.info(f"Top 3 influences on {target_variable}: {', '.join([f'{k} ({v:.1f})' for k,v in sorted_influences])}")

# ------------------------------
# Tabs for Simulation & Possibilities
# ------------------------------
main_tab, possibilities_tab = st.tabs(["🧠 Simulation", "🌌 Possibilities & AIBuddy"])

with main_tab:
    st.markdown('<div id="simulation-section"></div>', unsafe_allow_html=True)
    st.subheader(f"📊 Result for {target_variable}")
    st.markdown(f"<div class='metric-display' style='font-size:2em;color:#00ffff'>{C:.4f}</div>", unsafe_allow_html=True)
    
    # 2D Plot
    x = np.linspace(0.1,10,50)
    y = (slider_values["R"]*(slider_values["alpha"]**slider_values["theta"])*x*slider_values["Q"]*(1.3*slider_values["A"])*slider_values["E"]*(1.6*slider_values["M"]))/(slider_values["Dn"]*(slider_values["beta"]**slider_values["theta"]))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name=f"{target_variable} vs S", marker=dict(color="#00ffff")))
    fig.update_layout(title=f"{target_variable} vs Stimulus (S)", xaxis_title="Stimulus (S)", yaxis_title=f"{target_variable}", template="plotly_dark")
    st.plotly_chart(fig,use_container_width=True)
    
    # 3D Surface & Multi-Scenario Overlay
    st.subheader("🌐 3D Variable Interaction Map")
    var_x, var_y, var_z, var_animate = st.columns(4)
    x_var = var_x.selectbox("X-axis variable:", list(slider_values.keys()), index=list(slider_values.keys()).index("S"))
    y_var = var_y.selectbox("Y-axis variable:", list(slider_values.keys()), index=list(slider_values.keys()).index("A"))
    z_var = var_z.selectbox("Z-axis variable:", ["C"] + list(slider_values.keys()), index=0)
    animate_var = var_animate.selectbox("Animate variable:", ["None"] + list(slider_values.keys()), index=0)

    @st.cache_data
    def compute_surface(slider_values, x_var, y_var, z_var):
        X = np.linspace(0.1,10,30)
        Y = np.linspace(0.1,10,30)
        Z = np.zeros((len(X),len(Y)))
        for i,xv in enumerate(X):
            for j,yv in enumerate(Y):
                vals = slider_values.copy()
                vals[x_var] = xv
                vals[y_var] = yv
                Z[i,j] = compute_consciousness(**vals) if z_var=="C" else vals[z_var]
        return X, Y, Z

    plot_area = st.empty()
    if animate_var != "None":
        steps = 20
        for val in np.linspace(0.1, 10.0, steps):
            slider_values[animate_var] = val
            X, Y, Z = compute_surface(slider_values, x_var, y_var, z_var)
            fig3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
            fig3d.update_layout(scene=dict(xaxis_title=x_var, yaxis_title=y_var, zaxis_title=z_var),
                                template="plotly_dark", height=600,
                                title=f"{z_var} surface with {animate_var}={val:.2f}")
            plot_area.plotly_chart(fig3d, use_container_width=True)
            time.sleep(0.3)
    else:
        X, Y, Z = compute_surface(slider_values, x_var, y_var, z_var)
        fig3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
        fig3d.update_layout(scene=dict(xaxis_title=x_var, yaxis_title=y_var, zaxis_title=z_var),
                            template="plotly_dark", height=600)
        plot_area.plotly_chart(fig3d, use_container_width=True)

    # Multi-Scenario Overlay
    st.subheader("🌌 Multi-Scenario Holographic 3D Map")
    available_scenarios = ["Demo", "Random"] + [name for name,_ in ai_choices]
    selected_scenarios = st.multiselect("Select scenarios to overlay/animate:", available_scenarios, default=["Demo","Random"])
    scenario_map = {
        "Demo": demo_values,
        "Random": generate_random_scenario()
    }
    for name, vals in ai_choices:
        scenario_map[name] = vals

    overlay_plot = st.empty()
    steps = 15
    animate_range = np.linspace(0.1, 10.0, steps)
    colors = ["cyan", "magenta", "lime", "orange", "pink"]
    for val in animate_range:
        fig_overlay = go.Figure()
        for i, scen_name in enumerate(selected_scenarios):
            vals = scenario_map[scen_name].copy()
            vals[x_var] = val
            X, Y = np.meshgrid(np.linspace(0.1,10,30), np.linspace(0.1,10,30))
            Z = np.zeros_like(X)
            for ix in range(len(X)):
                for iy in range(len(Y)):
                    temp = vals.copy()
                    temp[x_var] = X[ix,iy]
                    temp[y_var] = Y[ix,iy]
                    Z[ix,iy] = compute_consciousness(**temp)
            fig_overlay.add_trace(go.Surface(
                x=X, y=Y, z=Z, 
                colorscale=[[0, colors[i%len(colors)]],[1, colors[i%len(colors)]]],
                opacity=0.6, showscale=False, name=scen_name
            ))
        fig_overlay.update_layout(
            scene=dict(xaxis_title=x_var, yaxis_title=y_var, zaxis_title="C"),
            template="plotly_dark",
            height=600,
            title="Multi-Scenario Holographic Simulation"
        )
        overlay_plot.plotly_chart(fig_overlay, use_container_width=True)
        time.sleep(0.3)

    # Correlation Heatmap
    st.subheader("🌡️ Variable Correlation with C")
    corr_data = pd.DataFrame(st.session_state.history)
    if len(corr_data) > 1:
        corr_matrix = corr_data.corr()
        fig_heat = go.Figure(data=go.Heatmap(
            z=corr_matrix["C"].drop("C"),
            x=corr_matrix["C"].drop("C").index,
            y=["C"]*len(corr_matrix["C"].drop("C")),
            colorscale="Viridis"
        ))
        fig_heat.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(fig_heat, use_container_width=True)

    # Scenario History / Download
    st.subheader("📋 Scenario History / Comparison")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df)
    data = {**st.session_state.sliders,"C":C}
    df = pd.DataFrame([data])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer,index=False)
    st.download_button("Download Result as CSV",csv_buffer.getvalue(),"complex_equation_result.csv","text/csv")
    st.download_button("Download Result as JSON",json.dumps(data,indent=4),"complex_equation_result.json","application/json")

with possibilities_tab:
    st.markdown("""
    <div style='color:#00ffff;'>
    <h2>🚀 Unlocking Infinite Possibilities</h2>
    <p>This simulation creator is capable of exploring the deepest levels of consciousness, cognitive states, memory, attention, and environmental interactions.</p>
    
    <h3>🌟 Potential Applications:</h3>
    <ul>
        <li>Human-AI cognitive modeling</li>
        <li>Mind-state prediction and optimization</li>
        <li>Virtual scenario testing for creative and analytical insights</li>
        <li>Education and neuroscience simulations</li>
    </ul>

    <h3>🔬 Possible Simulations:</h3>
    <ul>
        <li>High-attention, high-memory environments</li>
        <li>Randomized cognitive state exploration</li>
        <li>AI-guided scenario creation (AIBuddy)</li>
        <li>Variable interactions & multi-dimensional surfaces</li>
    </ul>

    <h3>💡 Discoveries & Insights:</h3>
    <ul>
        <li>Influence of each variable on consciousness</li>
        <li>Correlation patterns across multiple simulations</li>
        <li>Creative AI scenario suggestions</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # AIBuddy Panel
    st.subheader("🤖 AIBuddy")
    user_question = st.text_input("Ask AIBuddy for a suggestion or insight:")
    if st.button("💬 Consult AIBuddy"):
        if user_question.strip():
            response = f"AIBuddy Suggestion: Based on current parameters, adjusting 'A' and 'S' could maximize {target_variable}. Explore creative scenarios for novel insights!"
            st.markdown(f"<div style='color:#ff00ff;'>{response}</div>", unsafe_allow_html=True)
        else:
            st.warning("Type a question for AIBuddy to respond.")
