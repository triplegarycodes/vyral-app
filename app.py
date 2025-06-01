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
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "vyber_points" not in st.session_state:
    st.session_state.vyber_points = {
        "Spark": 0,
        "Mirror": 0,
        "Forge": 0,
        "Flux": 0,
        "Glyph": 0
    }

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

# --- COACHBOT MOOD RESPONSE ---
def coachbot_mood_response(user_input):
    mood_keywords = {
        "anxious": "🧘 Breathe deep. We can work through it.",
        "tired": "😴 Let’s build a rest-recovery plan.",
        "pumped": "🔥 You’re on fire. Let’s channel it.",
        "sad": "💙 I got you. What’s one thing you’re proud of?",
        "focused": "🎯 Locked in. Let’s sharpen your goals."
    }
    for mood, response in mood_keywords.items():
        if mood in user_input.lower():
            st.session_state.mood_log.append((time.time(), mood))
            return response
    st.session_state.mood_log.append((time.time(), "neutral"))
    return "💬 Let’s make that a SMART goal!"

# --- Quiz Questions ---
quiz_questions = [
    ("How do you usually start your day?", ["Spark", "Mirror", "Forge", "Flux", "Glyph"]),
    ("What do you do when you feel overwhelmed?", ["Spark", "Mirror", "Forge", "Flux", "Glyph"]),
    ("Which quote resonates most?", ["Spark", "Mirror", "Forge", "Flux", "Glyph"]),
    ("You’re stuck in a team project. What’s your instinct?", ["Spark", "Mirror", "Forge", "Flux", "Glyph"]),
    ("How do you react to a sudden change in plans?", ["Flux", "Mirror", "Forge", "Spark", "Glyph"]),
    ("Pick a preferred weekend vibe.", ["Mirror", "Spark", "Forge", "Flux", "Glyph"]),
    ("Your room is usually...", ["Spark", "Forge", "Mirror", "Flux", "Glyph"]),
    ("You learn best when...", ["Glyph", "Forge", "Mirror", "Spark", "Flux"]),
    ("What scares you more?", ["Mirror", "Flux", "Forge", "Spark", "Glyph"]),
    ("What do you crave most from life?", ["Spark", "Mirror", "Forge", "Flux", "Glyph"]),
]

# --- Tabs ---
tabs = st.tabs(["Chat", "Vybe Royale", "Mood Tracker", "Profile", "Kwyz"])

# --- Tab 1: Chat ---
with tabs[0]:
    st.title("🔥 CoachBot Chat")
    user_input = st.text_input("Talk to CoachBot:", placeholder="What's on your mind today?")
    if st.button("Send") and user_input:
        st.session_state.messages.append(("You", user_input))
        response = coachbot_mood_response(user_input)
        st.session_state.messages.append(("CoachBot", response))

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

# --- Tab 5: Kwyz ---
with tabs[4]:
    st.header("🧠 Vyber Personality Kwyz")

    if st.session_state.quiz_index < len(quiz_questions):
        q_text, options = quiz_questions[st.session_state.quiz_index]
        st.subheader(f"Q{st.session_state.quiz_index+1}: {q_text}")
        for i, option in enumerate(options):
            if st.button(f"{chr(65+i)}: {option}"):
                st.session_state.vyber_points[option] += 2 if st.session_state.quiz_index >= 8 else 1
                st.session_state.quiz_index += 1
                st.experimental_rerun()
    else:
        max_type = max(st.session_state.vyber_points, key=st.session_state.vyber_points.get)
        st.success(f"You are mostly: {max_type} ✨")
        st.write(st.session_state.vyber_points)
        if st.button("Retake Kwyz"):
            st.session_state.quiz_index = 0
            st.session_state.vyber_points = {k: 0 for k in st.session_state.vyber_points}
            st.experimental_rerun()

