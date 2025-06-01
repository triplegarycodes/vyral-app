import streamlit as st
import random
import time
import graphviz
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance
import io
import base64

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
if "custom_bg" not in st.session_state:
    st.session_state.custom_bg = None
if "hue_adjust" not in st.session_state:
    st.session_state.hue_adjust = 1.0
if "bg_scroll_position" not in st.session_state:
    st.session_state.bg_scroll_position = 0
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = []

# --- CUSTOM BACKGROUND UPLOAD ---
st.sidebar.subheader("🌅 Customize Background")
bg_file = st.sidebar.file_uploader("Upload background image", type=["png", "jpg", "jpeg"])
hue = st.sidebar.slider("Adjust hue/saturation", 0.5, 2.0, 1.0, 0.1)
scroll_offset = st.sidebar.slider("Scroll background vertically", -2000, 2000, 0, step=10)
st.session_state.hue_adjust = hue
st.session_state.bg_scroll_position = scroll_offset

if bg_file:
    image = Image.open(bg_file).convert("RGBA")
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(hue)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    bg_str = buffered.getvalue()
    encoded_bg = "data:image/png;base64," + base64.b64encode(bg_str).decode()
    custom_css = f"""
        <style>
        .main, .stApp {{
            background-image: url('{encoded_bg}');
            background-size: cover;
            background-position: center {scroll_offset}px;
        }}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# --- PERSONALITY QUIZ ---
quiz_data = [
    {
        "question": "When faced with a challenge, you usually...",
        "options": [
            {"text": "Break it down logically and step through it", "type": "Strategist"},
            {"text": "Tackle it head-on and adjust as you go", "type": "Executor"},
            {"text": "Pause and reflect deeply before acting", "type": "Seeker"},
            {"text": "Talk it out with someone you trust", "type": "Connector"}
        ]
    },
    {
        "question": "Your ideal weekend activity involves...",
        "options": [
            {"text": "Planning your next big idea", "type": "Strategist"},
            {"text": "Doing something bold and spontaneous", "type": "Executor"},
            {"text": "Meditating or journaling", "type": "Seeker"},
            {"text": "Hanging out with friends or family", "type": "Connector"}
        ]
    },
    {
        "question": "When working on a project, you're the one who...",
        "options": [
            {"text": "Draws the diagrams and plans", "type": "Strategist"},
            {"text": "Gets hands-on and just starts", "type": "Executor"},
            {"text": "Finds the deeper meaning in the task", "type": "Seeker"},
            {"text": "Collaborates and motivates the team", "type": "Connector"}
        ]
    },
    {
        "question": "In a group chat, you're most likely to...",
        "options": [
            {"text": "Drop a helpful link or plan", "type": "Strategist"},
            {"text": "Start the hype or take initiative", "type": "Executor"},
            {"text": "Ask meaningful questions", "type": "Seeker"},
            {"text": "Keep the convo alive with jokes", "type": "Connector"}
        ]
    },
    {
        "question": "You feel most fulfilled when...",
        "options": [
            {"text": "You’ve solved something complex", "type": "Strategist"},
            {"text": "You’ve finished a big task", "type": "Executor"},
            {"text": "You’ve had a deep realization", "type": "Seeker"},
            {"text": "You’ve made someone’s day better", "type": "Connector"}
        ]
    },
    {
        "question": "What’s your study style?",
        "options": [
            {"text": "Structured and outlined", "type": "Strategist"},
            {"text": "Quick and efficient", "type": "Executor"},
            {"text": "Reflective and thematic", "type": "Seeker"},
            {"text": "Study groups all day", "type": "Connector"}
        ]
    },
    {
        "question": "Your dream job likely involves...",
        "options": [
            {"text": "Strategizing solutions", "type": "Strategist"},
            {"text": "Getting results fast", "type": "Executor"},
            {"text": "Inspiring deep change", "type": "Seeker"},
            {"text": "Helping or leading others", "type": "Connector"}
        ]
    },
    {
        "question": "When you’re stuck, you usually...",
        "options": [
            {"text": "Rethink the approach", "type": "Strategist"},
            {"text": "Just try something else immediately", "type": "Executor"},
            {"text": "Search inward for clarity", "type": "Seeker"},
            {"text": "Call a friend or vent", "type": "Connector"}
        ]
    },
    {
        "question": "Which quote hits the hardest?",
        "options": [
            {"text": "Plans are nothing; planning is everything.", "type": "Strategist"},
            {"text": "Done is better than perfect.", "type": "Executor"},
            {"text": "The unexamined life is not worth living.", "type": "Seeker"},
            {"text": "We rise by lifting others.", "type": "Connector"}
        ]
    },
    {
        "question": "You want to be remembered as...",
        "options": [
            {"text": "The mastermind who changed things", "type": "Strategist"},
            {"text": "The force who made it happen", "type": "Executor"},
            {"text": "The soul who understood everything", "type": "Seeker"},
            {"text": "The heart that connected people", "type": "Connector"}
        ]
    }
]

# --- QUIZ TAB ---
quiz_tab = st.sidebar.checkbox("Take Personality Kwyz")
if quiz_tab:
    st.title("🧬 Vyber Personality Kwyz")
    responses = {}
    for i, q in enumerate(quiz_data):
        st.subheader(f"Q{i+1}: {q['question']}")
        selected = st.radio("", [opt["text"] for opt in q["options"]], key=f"q_{i}")
        for opt in q["options"]:
            if opt["text"] == selected:
                responses[i] = opt["type"]
    if st.button("Submit Quiz"):
        result_counts = {}
        for t in responses.values():
            result_counts[t] = result_counts.get(t, 0) + 1
        sorted_results = sorted(result_counts.items(), key=lambda x: x[1], reverse=True)
        top_type = sorted_results[0][0]
        st.success(f"You are a **{top_type}**!")
        if len(sorted_results) > 1 and sorted_results[0][1] == sorted_results[1][1]:
            st.info(f"Tied vibe detected! You also align with **{sorted_results[1][0]}**.")

# --- Tabs ---
tabs = st.tabs(["Chat", "Vybe Royale", "Mood Tracker", "Profile"])

# --- Tab 1: Chat ---
with tabs[0]:
    st.title("🔥 CoachBot Chat")
    user_input = st.text_input("Talk to CoachBot:", placeholder="What's on your mind today?")
    if st.button("Send") and user_input:
        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("CoachBot", "💬 Let’s make that a SMART goal!"))
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
