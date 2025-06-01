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
if "secret_tabs_unlocked" not in st.session_state:
    st.session_state.secret_tabs_unlocked = []

UNLOCKS = {
    "Visionary": ["Futurecast", "Clarity Surge"],
    "Empath": ["Emowave", "Kindforce"],
    "Rebel": ["Chaos Control", "Solo Surge"],
    "Seeker": ["Pathfinder", "Inner Echo"],
    "Strategist": ["Mind Grid", "Flow Hack"],
    "Healer": ["Heartlight", "Mendstorm"],
    "Shadow": ["Veil Pierce", "Echo Lock"],
    "Sage": ["Wisdom Well", "Golden Thread"],
    "Dreamer": ["Lucid Leap", "Echo Pulse"],
    "Explorer": ["Trailcode", "Wander Blink"],
    "Phoenix": ["Flareborn", "Ash Reboot"],
    "Anchor": ["Groundflare", "Soul Hold"]
}

VYBER_THEMES = {
    "Visionary": "#6c63ff",
    "Empath": "#ff69b4",
    "Rebel": "#ff4500",
    "Seeker": "#2e8b57",
    "Strategist": "#4682b4",
    "Healer": "#98fb98",
    "Shadow": "#333333",
    "Sage": "#daa520",
    "Dreamer": "#8a2be2",
    "Explorer": "#00ced1",
    "Phoenix": "#ff6347",
    "Anchor": "#1e90ff"
}

# --- Secret Tabs Unlock Logic ---
def check_secret_tabs():
    if (st.session_state.vybe_royale_score >= 200 and
        len(st.session_state.unlocked_skills) >= 4 and
        st.session_state.vyber_type in ["Strategist", "Dreamer"]):
        if "Echo Core" not in st.session_state.secret_tabs_unlocked:
            st.session_state.secret_tabs_unlocked.append("Echo Core")

    if (len(st.session_state.mood_log) >= 3 and
        any(mood[1] in ["sad", "angry", "anxious"] for mood in st.session_state.mood_log) and
        st.session_state.coachbot_data["message_count"] > 5):
        if "Nullwave Anomaly" not in st.session_state.secret_tabs_unlocked:
            st.session_state.secret_tabs_unlocked.append("Nullwave Anomaly")

    if (st.session_state.custom_bg and
        st.session_state.bg_scroll_position <= -1500 and
        st.session_state.vyber_type in ["Shadow", "Explorer"]):
        if "Hidden Chamber" not in st.session_state.secret_tabs_unlocked:
            st.session_state.secret_tabs_unlocked.append("Hidden Chamber")

    if ("I remember..." in [msg[1] for msg in st.session_state.messages] and
        time.strftime("%A") == "Sunday"):
        if "Legacy Mode" not in st.session_state.secret_tabs_unlocked:
            st.session_state.secret_tabs_unlocked.append("Legacy Mode")

check_secret_tabs()

# --- Render Tabs ---
tabs = st.tabs(["Main", "Vybe Royale", "Mood Tracker", "Profile", "Personality Kwyz"] + st.session_state.secret_tabs_unlocked)

# --- Main Tab ---
with tabs[0]:
    st.title("🌟 Welcome to Vyral")
    st.markdown("Your control center for everything Vybe.")
    st.metric("💸 Vybux", st.session_state.vybux)
    if st.session_state.vyber_type:
        st.markdown(f"Today’s Wisdom for {st.session_state.vyber_type}: _Stay rooted, and rise._")
    else:
        st.markdown("Take the Personality Kwyz to begin your path.")

# --- Vybe Royale Tab ---
with tabs[1]:
    st.subheader("🎮 Vybe Royale")
    st.markdown("Battle vibes, dodge noise, and collect clarity.")
    st.write(f"Score: {st.session_state.vybe_royale_score}")
    if st.button("🔥 Run a Match"):
        st.session_state.vybe_royale_score -= random.randint(5, 20)
        st.session_state.vybux += random.randint(10, 30)
        st.success("Match complete! Score adjusted. Vybux gained.")
    if st.button("Auto Run Mode"):
        st.session_state.auto_run_royale = not st.session_state.auto_run_royale
    if st.session_state.auto_run_royale:
        st.warning("Auto Running... Press again to stop.")
        time.sleep(2)
        st.session_state.vybe_royale_score -= random.randint(1, 10)
        st.session_state.vybux += random.randint(5, 15)

# --- Mood Tracker Tab ---
with tabs[2]:
    st.subheader("📈 Mood Tracker")
    mood = st.selectbox("Your current mood:", ["happy", "sad", "angry", "anxious", "chill", "excited"])
    if st.button("Log Mood"):
        st.session_state.mood_log.append((time.strftime("%Y-%m-%d"), mood))
        st.success("Mood logged!")
    if len(st.session_state.mood_log) >= 2:
        mood_df = pd.DataFrame(st.session_state.mood_log, columns=["Date", "Mood"])
        mood_df["Mood Score"] = mood_df["Mood"].map({"happy": 3, "chill": 2, "excited": 2, "sad": -2, "angry": -3, "anxious": -1})
        st.line_chart(mood_df.set_index("Date")["Mood Score"])

# --- Profile Tab ---
with tabs[3]:
    st.subheader("🧑‍🎤 Profile")
    if st.session_state.vyber_type:
        st.markdown(f"### Your Type: {st.session_state.vyber_type}")
        st.markdown(f"**Unlocked Skills:** {', '.join(UNLOCKS.get(st.session_state.vyber_type, []))}")
        st.markdown(f"<div style='background:{VYBER_THEMES[st.session_state.vyber_type]};padding:1em;border-radius:10px;color:white;'>You are on the {st.session_state.vyber_type} path. Let your unique strengths shine!</div>", unsafe_allow_html=True)
        st.metric("💸 Vybux", st.session_state.vybux)
        st.markdown("**Badges:** 🏅Path Unlocked | 🎯Quiz Complete")
        st.image(f"images/{st.session_state.vyber_type.lower()}.png", caption="Your Energy Avatar", use_column_width=True)
    else:
        st.info("Take the Personality Kwyz to build your profile.")

# --- Personality Kwyz Tab ---
with tabs[4]:
    st.subheader("🧪 Personality Kwyz")
    st.write("Find out what kind of Vyber you are!")
    
    questions = [
        ("You walk into a new space. What's your instinct?", ["Observe and plan", "Talk to someone", "Find the exit", "Touch everything"]),
        ("When you're stressed, you...", ["Retreat inward", "Call a friend", "Channel it into art", "Challenge yourself to solve it"]),
        ("You’d rather be known for your...", ["Wisdom", "Compassion", "Drive", "Curiosity"]),
        ("Which sound feels the most like you?", ["Crackling fire", "Ocean waves", "Typing keyboard", "Echo in a cave"]),
        ("If your mind had a color, it’d be...", ["Deep blue", "Electric orange", "Bright gold", "Smoky grey"]),
        ("Your vibe is most aligned with...", ["Mystery", "Logic", "Heart", "Adventure"]),
        ("You’d rather time travel to...", ["Ancient past", "Far future", "A different self", "A dream world"]),
        ("Biggest strength in a crisis?", ["Staying calm", "Helping others", "Solving fast", "Finding meaning"]),
        ("You often wonder...", ["Why things happen", "What others feel", "What’s next", "What’s hidden"]),
        ("At your core, you’re...", ["A seeker", "A rebel", "A protector", "A thinker"]),
    ]

    vyber_counter = {key: 0 for key in VYBER_THEMES.keys()}

    for i, (q, options) in enumerate(questions):
        st.markdown(f"**{i+1}. {q}**")
        choice = st.radio("", options, key=f"q{i}")
        if choice:
            if "calm" in choice or "thinker" in choice:
                vyber_counter["Strategist"] += 1
            elif "others" in choice or "compassion" in choice:
                vyber_counter["Empath"] += 1
            elif "hidden" in choice or "mystery" in choice:
                vyber_counter["Shadow"] += 1
            elif "dream" in choice or "curiosity" in choice:
                vyber_counter["Dreamer"] += 1
            elif "fire" in choice or "drive" in choice:
                vyber_counter["Phoenix"] += 1
            elif "plan" in choice or "logic" in choice:
                vyber_counter["Sage"] += 1
            elif "adventure" in choice or "explorer" in choice:
                vyber_counter["Explorer"] += 1
            elif "heart" in choice or "protector" in choice:
                vyber_counter["Healer"] += 1
            elif "seeker" in choice or "meaning" in choice:
                vyber_counter["Seeker"] += 1
            elif "rebel" in choice or "challenge" in choice:
                vyber_counter["Rebel"] += 1
            else:
                vyber_counter["Visionary"] += 1

    if st.button("Submit Quiz"):
        top_type = max(vyber_counter, key=vyber_counter.get)
        st.session_state.vyber_type = top_type
        st.success(f"You are a {top_type}! Welcome to the {top_type} path.")
        st.balloons()

# --- Echo Core Example Secret Tab ---
if "Echo Core" in st.session_state.secret_tabs_unlocked:
    with tabs[-len(st.session_state.secret_tabs_unlocked)]:
        st.subheader("🧠 Echo Core")
        st.markdown("This is your memory web. Rearrange fragments to find the truth.")
        fragments = [
            {"id": 1, "title": "The Day I Froze", "type": "Emotion Swirl", "details": "An anxious shutdown moment in Bio class."},
            {"id": 2, "title": "The CoachBot Paradox", "type": "Thought Pulse", "details": "You once told CoachBot a lie... why?"},
            {"id": 3, "title": "Zayn’s Question", "type": "Old Message", "details": "You brushed off Zayn’s curiosity, but it stuck with you."},
        ]
        for frag in fragments:
            with st.expander(f"{frag['type']} - {frag['title']}"):
                st.markdown(f"**Fragment ID:** {frag['id']}")
                st.markdown(f"**Details:** {frag['details']}")

