import streamlit as st
import random
import time
import graphviz
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "coachbot_data" not in st.session_state:
    st.session_state.coachbot_data = {
        "topics": set(),
        "emotions": set(),
        "message_count": 0
    }
if "vybe_royale_score" not in st.session_state:
    st.session_state.vybe_royale_score = 100
if "players" not in st.session_state:
    st.session_state.players = ["Zayn", "Wren", "Aari", "CoachBot", "You"]
if "reward_animation" not in st.session_state:
    st.session_state.reward_animation = None
if "vybux" not in st.session_state:
    st.session_state.vybux = 50
if "unlocked_animations" not in st.session_state:
    st.session_state.unlocked_animations = []
if "auto_run_royale" not in st.session_state:
    st.session_state.auto_run_royale = False
if "unlocked_skills" not in st.session_state:
    st.session_state.unlocked_skills = {"Root Skill"}
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []
if "theme_choice" not in st.session_state:
    st.session_state.theme_choice = "Focus Drift"

# --- THEME FUNCTION ---
def apply_theme(theme_name):
    css_dict = {
        "Focus Drift": """
            <style>
            .main, .stApp {
                background: radial-gradient(circle, #cceeff, #ffffff);
                animation: drift 5s infinite alternate;
                color: #111 !important;
            }
            @keyframes drift {
                from { filter: brightness(0.95); }
                to { filter: brightness(1.05); }
            }
            </style>
        """,
        "Mood Burst": """
            <style>
            .main, .stApp {
                background: linear-gradient(to right, #ffb3ba, #ffdfba, #ffffba, #baffc9, #bae1ff);
                background-size: 500% 500%;
                animation: moodburst 15s ease infinite;
                color: #111 !important;
            }
            @keyframes moodburst {
                0% { background-position: 0% 50%; }
                100% { background-position: 100% 50%; }
            }
            </style>
        """,
        "Heat Up Mode": """
            <style>
            .main, .stApp {
                background: linear-gradient(45deg, #ff4e50, #f9d423);
                animation: heatup 2s infinite alternate;
                color: #111 !important;
            }
            @keyframes heatup {
                from { filter: hue-rotate(0deg); }
                to { filter: hue-rotate(30deg); }
            }
            </style>
        """
    }
    st.markdown(css_dict.get(theme_name, ""), unsafe_allow_html=True)

apply_theme(st.session_state.theme_choice)

# --- Theme Selector ---
st.sidebar.header("🖌️ Theme Settings")
st.session_state.theme_choice = st.sidebar.selectbox("Choose Theme", ["Focus Drift", "Mood Burst", "Heat Up Mode"])

# --- Tabs ---
tabs = st.tabs(["Chat", "Vybe Royale", "Mood Tracker", "Profile"])

# --- Tab 1: Chat ---
with tabs[0]:
    st.title("🔥 CoachBot Chat")
    user_input = st.text_input("Talk to CoachBot:", placeholder="What's on your mind today?")
    if st.button("Send") and user_input:
        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("CoachBot", "Let's make that a SMART goal!"))

    for speaker, msg in st.session_state.messages:
        with st.chat_message(name=speaker):
            st.markdown(msg)

# --- Tab 2: Vybe Royale ---
with tabs[1]:
    st.header("🎮 Vybe Royale Zone")

    def simulate_vybe_royale():
        outcomes = [
            "🌟 Bonus confidence unlocked +30 points",
            "🔮 Future vision unlocked +20 clout",
            "🌝 Epiphany moment! +30 clout",
            "🌀 Tornado of distraction -20 points",
            "🔥 Overheated by pressure -15 points",
            "💰 Rare clarity moment! +50 clout"
        ]
        outcome = random.choice(outcomes)
        if "-" in outcome:
            value = int(outcome.split('-')[-1].split(' ')[0])
            st.session_state.vybe_royale_score -= value
        elif "+" in outcome:
            value = int(outcome.split('+')[-1].split(' ')[0])
            st.session_state.vybe_royale_score += value
        st.session_state.reward_animation = outcome
        return outcome

    if st.button("Play Round 🎲"):
        result = simulate_vybe_royale()
        st.success(f"Result: {result}")

    st.metric("🧠 Mental Health Points", st.session_state.vybe_royale_score)

# --- Tab 3: Mood Tracker ---
with tabs[2]:
    st.header("📊 Mood Tracker")
    if st.session_state.mood_log:
        df = pd.DataFrame(st.session_state.mood_log, columns=["timestamp", "mood"])
        df["time"] = pd.to_datetime(df["timestamp"], unit="s")
        mood_counts = df.groupby(["time", "mood"]).size().unstack(fill_value=0)
        st.line_chart(mood_counts)
    else:
        st.info("Start chatting with CoachBot to track your mood!")

# --- Tab 4: Profile ---
def profile_card(name, score, skills):
    st.markdown(f"""
        <div style='border-radius: 15px; padding: 1.5rem; margin: 1rem 0; background: linear-gradient(145deg, #e6e6e6, #ffffff); box-shadow: 6px 6px 12px #cccccc, -6px -6px 12px #ffffff;'>
            <h3 style='margin-bottom: 0.5rem;'>{name}</h3>
            <p><strong>Vybe Score:</strong> {score}</p>
            <p><strong>Skills:</strong> {', '.join(skills)}</p>
        </div>
    """, unsafe_allow_html=True)

with tabs[3]:
    st.header("💼 Vyber Profile")
    profile_card("You", st.session_state.vybe_royale_score, st.session_state.unlocked_skills)

