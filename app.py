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
# Variables
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
# Tabs
# ------------------------------
sim_tab, possibilities_tab, aibuddy_tab = st.tabs(["🧠 Simulation", "🌌 Possibilities", "🤖 AIBuddy Hub"])

# ------------------------------
# Simulation Tab
# ------------------------------
with sim_tab:
    st.markdown('<div id="simulation-section"></div>', unsafe_allow_html=True)
    st.subheader(f"📊 Result for {target_variable}")
    st.markdown(f"<div class='metric-display' style='font-size:2em;color:#00ffff'>{C:.4f}</div>", unsafe_allow_html=True)
    
    # 2D Plot
    x = np.linspace(0.1,10,50)
    y = (slider_values["R"]*(slider_values["alpha"]**slider_values["theta"])*x*slider_values["Q"]*(1.3*slider_values["A"])*slider_values["E"]*(1.6*slider_values["M"]))/(slider_values["Dn"]*(slider_values["beta"]**slider_values["theta"]))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y,mode="lines+markers",marker=dict(color="#00ffff")))
    fig.update_layout(title=f"{target_variable} vs S",xaxis_title="S",yaxis_title=f"{target_variable}",template="plotly_dark")
    st.plotly_chart(fig,use_container_width=True)

# ------------------------------
# Possibilities Tab
# ------------------------------
with possibilities_tab:
    st.markdown("""
    <div style='color:#00ffff;'>
    <h2>🚀 Unlocking Infinite Possibilities</h2>
    <p>Explore consciousness, cognitive states, memory, attention, and environmental interactions.</p>
    <h3>🌟 Potential Applications:</h3>
    <ul><li>Human-AI cognitive modeling</li><li>Mind-state prediction and optimization</li><li>Virtual scenario testing</li><li>Education & neuroscience simulations</li></ul>
    <h3>🔬 Possible Simulations:</h3>
    <ul><li>High-attention, high-memory environments</li><li>Randomized cognitive state exploration</li><li>AI-guided scenario creation</li><li>Multi-dimensional surface exploration</li></ul>
    <h3>💡 Insights:</h3>
    <ul><li>Influence of each variable on consciousness</li><li>Correlation patterns across simulations</li><li>Creative AI scenario suggestions</li></ul>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# AIBuddy Hub Tab
# ------------------------------
with aibuddy_tab:
    st.subheader("🎛️ Hologram Controls")
    show_hologram = st.checkbox("Enable Hologram", value=True)
    enable_tts = st.checkbox("Enable Voice", value=True)
    holo_gender = st.radio("Hologram Gender", ["Female","Male"])
    avatar_url = "https://i.imgur.com/FemaleHolo.png" if holo_gender=="Female" else "https://i.imgur.com/MaleHolo.png"

    holo_container = st.empty()
    if show_hologram:
        holo_html = f"""
        <div id="hologram-container" style="
            position: fixed; bottom:20px; right:20px; width:320px; height:420px;
            background: rgba(0,255,255,0.1); backdrop-filter: blur(12px);
            border:2px solid cyan; border-radius:15px; padding:15px;
            font-family:'Roboto Mono', monospace; color:#00ffff; z-index:9999;
            box-shadow:0 0 25px cyan, 0 0 35px magenta; overflow-y:auto;
        ">
            <h3 style="text-align:center;color:#ff00ff;">🤖 AIBuddy Hologram</h3>
            <img src="{avatar_url}" style="width:100%; border-radius:10px; margin-bottom:10px;">
            <div id="hologram-text" data-sliders='{json.dumps(st.session_state.sliders)}' data-C='{C}'></div>
        </div>
        <script>
        function speakMessage(text){{
            if(!{str(enable_tts).lower()}) return;
            const utter = new SpeechSynthesisUtterance(text);
            const voices = window.speechSynthesis.getVoices();
            if("{holo_gender}"==="Female"){{
                utter.voice = voices.find(v=>v.name.includes("Female"))||voices[0]; utter.pitch=0.9; utter.rate=1.0;
            }} else {{
                utter.voice = voices.find(v=>v.name.includes("Male"))||voices[0]; utter.pitch=1.0; utter.rate=1.0;
            }}
            window.speechSynthesis.speak(utter);
        }}
        function typeWriterWithVoice(text){{
            let n=0;
            function step(){{
                if(n<text.length){{document.getElementById('hologram-text').innerHTML=text.substring(0,n+1)+'|'; n++; setTimeout(step,25);}}
                else{{document.getElementById('hologram-text').innerHTML=text; speakMessage(text);}}
            }}
            step();
        }}
        function updateHoloCommentary(){{
            const holoDiv = document.getElementById('hologram-text');
            const sliders = JSON.parse(holoDiv.dataset.sliders);
            const C = parseFloat(holoDiv.dataset.C);
            let maxVar = Object.entries(sliders).reduce((a,b)=>a[1]>b[1]?a:b)[0];
            let commentary = `Current Consciousness (C): ${C.toFixed(2)}. Most influential: ${maxVar}. Adjust sliders to explore!`;
            typeWriterWithVoice(commentary);
        }}
        window.speechSynthesis.onvoiceschanged=function(){{updateHoloCommentary();}};
        </script>
        """
        holo_container.markdown(holo_html, unsafe_allow_html=True)

    st.subheader("💡 AI Suggestions")
    ai_choices = ai_suggestions(slider_values)
    ai_names = [name for name,_ in ai_choices]
    ai_selected = st.selectbox("Select AI Scenario", ai_names)
    if st.button("Apply Scenario"):
        selected_vals = dict(dict(ai_choices)[ai_selected])
        st.session_state.sliders.update(selected_vals)

    st.subheader("💬 Ask AIBuddy")
    user_question = st.text_input("Type a question:")
    if st.button("Consult AIBuddy"):
        if user_question.strip():
            response = f"AIBuddy Response: Adjusting 'A' and 'S' may optimize {target_variable}. Explore creative scenarios!"
            st.markdown(f"<div style='color:#ff00ff;'>{response}</div>", unsafe_allow_html=True)
        else:
            st.warning("Type a question to get a response.")
