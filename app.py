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
if "vyber_type" not in st.session_state:
    st.session_state.vyber_type = None

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

# --- TABS ---
tabs = st.tabs(["Chat", "Vybe Royale", "Mood Tracker", "Profile", "Kwyz"])

# --- Tab 1: Chat ---
with tabs[0]:
    st.title("🔥 CoachBot Chat")
    user_input = st.text_input("Talk to CoachBot:", placeholder="What's on your mind today?")
    if st.button("Send") and user_input:
        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("CoachBot", "Let’s make that a SMART goal!"))

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
def profile_card(name, score, skills, vyber_type):
    type_desc = f"<p><strong>Vyber Type:</strong> {vyber_type}</p>" if vyber_type else "<p><em>Take the Kwyz to discover your Vyber Type!</em></p>"
    st.markdown(f"""
        <div style='border-radius: 15px; padding: 1.5rem; margin: 1rem 0; background: linear-gradient(145deg, #e6e6e6, #ffffff); box-shadow: 6px 6px 12px #cccccc, -6px -6px 12px #ffffff;'>
            <h3 style='margin-bottom: 0.5rem;'>{name}</h3>
            <p><strong>Vybe Score:</strong> {score}</p>
            <p><strong>Skills:</strong> {', '.join(skills)}</p>
            {type_desc}
        </div>
    """, unsafe_allow_html=True)

with tabs[3]:
    st.header("💼 Vyber Profile")
    profile_card("You", st.session_state.vybe_royale_score, st.session_state.unlocked_skills, st.session_state.vyber_type)

# --- Tab 5: Kwyz ---
with tabs[4]:
    st.header("🔮 Personality Kwyz")

    quiz = [
        ("You wake up and the first thing you do is:", ["Check your phone", "Write your dreams down", "Plan your day", "Blast music"]),
        ("Your friend cancels plans last-minute. You:", ["Get annoyed", "Feel relieved", "Worry about them", "Throw a solo party"]),
        ("Pick a vibe:", ["Chill", "Driven", "Mysterious", "Creative"]),
        ("When you’re overwhelmed, you:", ["Take a walk", "Cry it out", "Make a to-do list", "Zone out to music"]),
        ("Biggest flex:", ["Empathy", "Discipline", "Imagination", "Adaptability"]),
        ("Pick a setting:", ["Forest", "Skyscraper rooftop", "Bedroom", "Desert"]),
        ("What motivates you most?", ["Success", "Love", "Ideas", "Chaos"]),
        ("Choose your weapon:", ["Journal", "Laptop", "Microphone", "Sketchpad"]),
        ("When life feels empty, what fills the gap?", ["Faith", "Friends", "Dreams", "Silence"]),
        ("What’s your biggest fear?", ["Being forgotten", "Losing control", "Never knowing the truth", "Letting people down"])
    ]

    scores = {
        "Visionary": 0, "Empath": 0, "Rebel": 0, "Seeker": 0,
        "Strategist": 0, "Healer": 0, "Shadow": 0, "Sage": 0,
        "Dreamer": 0, "Explorer": 0, "Phoenix": 0, "Anchor": 0
    }

    combinations = {
        ("Write your dreams down", "Mysterious", "Imagination"): "Dreamer",
        ("Plan your day", "Driven", "Discipline"): "Strategist",
        ("Cry it out", "Empathy", "Love"): "Healer",
        ("Throw a solo party", "Creative", "Chaos"): "Rebel",
        ("Blast music", "Adaptability", "Microphone"): "Phoenix",
        ("Check your phone", "Chill", "Friends"): "Anchor"
    }

    for i, (q, options) in enumerate(quiz):
        st.write(f"{i+1}. {q}")
        choice = st.radio("", options, key=f"q{i}")
        st.session_state.quiz_answers.append(choice)

    if st.button("Reveal Vyber Type"):
        answers = st.session_state.quiz_answers[-10:]
        for comb, result in combinations.items():
            if all(opt in answers for opt in comb):
                st.success(f"You are a **{result}** ✨")
                st.session_state.vyber_type = result
                break
        else:
            chosen = random.choice(list(scores.keys()))
            st.success(f"You are a **{chosen}** ✨")
            st.session_state.vyber_type = chosen

