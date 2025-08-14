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
# Styles
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
body, h1, h2, h3, p, div, span, button, label { font-family:'Roboto Mono', monospace !important; color:#00ffff !important; }
@keyframes fadeIn {from {opacity:0; transform:translateY(-10px);} to {opacity:1; transform:translateY(0);} }
@keyframes pulse {0% {box-shadow:0 0 10px cyan;} 50% {box-shadow:0 0 20px magenta;} 100% {box-shadow:0 0 10px cyan;}}
.welcome-box {animation: fadeIn 1.5s ease-out forwards; padding:30px; border-radius:15px; background: rgba(0,0,0,0.7); backdrop-filter: blur(10px); box-shadow: 0 0 30px rgba(0,255,255,0.5); text-align:center; margin-bottom:30px;}
.launch-btn {background: linear-gradient(90deg, cyan, magenta); border:none; padding:15px 30px; border-radius:25px; color:black; font-size:1.3em; font-weight:bold; cursor:pointer; transition:all 0.3s ease;}
.launch-btn:hover { transform: scale(1.05); box-shadow: 0 0 25px cyan, 0 0 25px magenta; }
.slider-label {color:#00ffff; font-weight:bold;}
.metric-display {animation: pulse 2s infinite; font-family:'Roboto Mono', monospace;}
.possibility {margin:10px 0; padding:10px; border-radius:10px; background: rgba(0,0,0,0.5); border:1px solid #00ffff; box-shadow:0 0 15px #ff00ff;}
</style>
<script>
function scrollToSimulation() { const element = document.getElementById('simulation-section'); if (element) { element.scrollIntoView({ behavior: 'smooth' }); } }
</script>
<div class="welcome-box">
    <div style="font-size:2.8em; font-weight:bold;">🚀 MindScape</div>
    <div style="margin-top:10px; font-size:1.3em;">
        The Complex Equation Simulator by <b>Sam Andrews Rodriguez II</b>.<br>
        Explore consciousness, cognitive states, memory, attention, environment, and AI scenarios.
    </div>
    <hr style="border:0.5px solid #00ffff; margin:15px 0;">
    <button class="launch-btn" onclick="scrollToSimulation()">🔥 Launch Simulation</button>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar & Variables
# ------------------------------
st.sidebar.header("Adjust Parameters / Generate Scenarios")
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

# Sidebar buttons
if st.sidebar.button("📈 Load Demo Scenario"): st.session_state.sliders.update(demo_values); st.markdown('<script>scrollToSimulation()</script>', unsafe_allow_html=True)
if st.sidebar.button("🎲 Generate Random Scenario"): st.session_state.sliders.update(generate_random_scenario()); st.markdown('<script>scrollToSimulation()</script>', unsafe_allow_html=True)

# Slider Inputs
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
# Hologram Settings
# ------------------------------
show_hologram = st.sidebar.checkbox("Enable AI Hologram", value=True)
enable_animations = st.sidebar.checkbox("Enable Hologram Animations", value=True)
enable_tts = st.sidebar.checkbox("Enable AIBuddy Voice", value=True)
holo_gender = st.sidebar.radio("Hologram Gender:", ["Female", "Male"])
avatar_url = "https://i.imgur.com/FemaleHolo.png" if holo_gender=="Female" else "https://i.imgur.com/MaleHolo.png"

if show_hologram:
    st.markdown(f"""
    <style>
    @keyframes floatHolo {{0% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }} 100% {{ transform: translateY(0px); }} }}
    .hologram {{
        position: fixed; bottom:20px; right:20px; width:320px; height:420px;
        background: rgba(0,255,255,0.1); backdrop-filter: blur(12px);
        border:2px solid cyan; border-radius:15px; padding:15px;
        font-family:'Roboto Mono', monospace; color:#00ffff; z-index:9999;
        box-shadow:0 0 25px cyan, 0 0 35px magenta; overflow-y:auto;
        animation: {"floatHolo 3s ease-in-out infinite" if enable_animations else "none"};
    }}
    .hologram h3 {{text-align:center;color:#ff00ff;font-size:1.3em;}}
    .hologram img {{width:100%; border-radius:10px; margin-bottom:10px; filter:drop-shadow(0 0 8px cyan) drop-shadow(0 0 5px magenta);}}
    </style>
    <div class="hologram">
        <h3>🤖 AIBuddy Hologram</h3>
        <img src="{avatar_url}">
        <div id="hologram-text"></div>
    </div>
    <script>
    const messages = [
        "Welcome! I am your AI companion.",
        "I explain how each variable affects consciousness.",
        "I suggest new scenarios and provide insights.",
        "Adjust sliders and watch how the system responds!"
    ];
    let i = 0;
    const holoText = document.getElementById('hologram-text');
    const ttsEnabled = {str(enable_tts).lower()};
    const selectedGender = "{holo_gender}";
    function speakMessage(text) {{
        if (!ttsEnabled) return;
        const utter = new SpeechSynthesisUtterance(text);
        const voices = window.speechSynthesis.getVoices();
        if(selectedGender==="Female"){{ utter.voice = voices.find(v=>v.name.includes("Google UK English Female")||v.name.includes("female"))||voices[0]; utter.pitch=0.9; utter.rate=1.0; }}
        else{{ utter.voice = voices.find(v=>v.name.includes("Google US English Male")||v.name.includes("male"))||voices[0]; utter.pitch=1.0; utter.rate=1.0; }}
        window.speechSynthesis.speak(utter);
    }}
    function typeWriterWithVoice(text,n,callback){{
        if(n<text.length){{ holoText.innerHTML=text.substring(0,n+1)+'|'; setTimeout(()=>typeWriterWithVoice(text,n+1,callback),40); }}
        else{{ holoText.innerHTML=text; speakMessage(text); setTimeout(callback,1000); }}
    }}
    function showMessagesWithVoice(){{
        typeWriterWithVoice(messages[i],0,function(){{ i=(i+1)%messages.length; showMessagesWithVoice(); }});
    }}
    showMessagesWithVoice();
    </script>
    """, unsafe_allow_html=True)

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

    # 3D Surface
    st.subheader("🌐 3D Variable Interaction Map")
    X = np.linspace(0.1,10,30); Y = np.linspace(0.1,10,30); Z = np.zeros((len(X),len(Y)))
    for i,xv in enumerate(X):
        for j,yv in enumerate(Y):
            vals = slider_values.copy(); vals["S"]=xv; vals["A"]=yv; Z[i,j]=compute_consciousness(**vals)
    fig3d = go.Figure(data=[go.Surface(z=Z,x=X,y=Y,colorscale='Viridis')])
    fig3d.update_layout(scene=dict(xaxis_title="S",yaxis_title="A",zaxis_title="C"),template="plotly_dark",height=600)
    st.plotly_chart(fig3d,use_container_width=True)

    # Scenario History / Download
    st.subheader("📋 Scenario History / Comparison")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df)
    data = {**st.session_state.sliders,"C":C}
    df = pd.DataFrame([data]); csv_buffer = StringIO(); df.to_csv(csv_buffer,index=False)
    st.download_button("Download Result as CSV",csv_buffer.getvalue(),"mindscape_result.csv","text/csv")
    st.download_button("Download Result as JSON",json.dumps(data,indent=4),"mindscape_result.json","application/json")

with possibilities_tab:
    st.markdown("""
    <div style='color:#00ffff;'>
    <h2>🚀 Unlocking Infinite Possibilities</h2>
    <p>This simulator is capable of exploring consciousness, cognitive states, memory, attention, and environmental interactions.</p>
    <h3>🌟 Potential Applications:</h3>
    <ul><li>Human-AI cognitive modeling</li><li>Mind-state prediction and optimization</li>
    <li>Virtual scenario testing for creative and analytical insights</li><li>Education and neuroscience simulations</li></ul>
    <h3>🔬 Possible Simulations:</h3>
    <ul><li>High-attention, high-memory environments</li>
    <li>Randomized cognitive state exploration</li><li>AI-guided scenario creation (AIBuddy)</li>
    <li>Variable interactions & multi-dimensional surfaces</li></ul>
    <h3>💡 Discoveries & Insights:</h3>
    <ul><li>Influence of each variable on consciousness</li><li>Correlation patterns across multiple simulations</li>
    <li>Creative AI scenario suggestions</li></ul></div>
    """, unsafe_allow_html=True)

    # AIBuddy Panel
    st.subheader("🤖 AIBuddy Interactive Console")
    user_question = st.text_input("Ask AIBuddy for a suggestion or insight:")
    if st.button("💬 Consult AIBuddy"):
        if user_question.strip():
            response = f"AIBuddy Suggestion: Adjusting 'A' and 'S' may maximize {target_variable}. Explore creative scenarios for novel insights!"
            st.markdown(f"<div style='color:#ff00ff;'>{response}</div>", unsafe_allow_html=True)
        else:
            st.warning("Type a question for AIBuddy to respond.")
