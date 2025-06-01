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
if "equipped_animation" not in st.session_state:
    st.session_state.equipped_animation = None
if "user_stats" not in st.session_state:
    st.session_state.user_stats = {
        "level": 1,
        "xp": 0,
        "strength": 5,
        "focus": 5,
        "creativity": 5,
        "resilience": 5
    }

# --- Unlockable Skills ---
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

# --- Custom Theme Colors ---
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
tabs = st.tabs(["Main", "Vybe Royale", "Mood Tracker", "Profile", "Personality Kwyz", "VybeShop", "Characters"] + st.session_state.secret_tabs_unlocked)

with tabs[0]:
    st.title("🌟 Welcome to Vyral")
    st.write("Main features and dashboard will go here.")

with tabs[1]:
    st.subheader("🎮 Vybe Royale")
    st.write("Play the game and earn rewards.")

with tabs[2]:
    st.subheader("📈 Mood Tracker")
    st.write("Track and visualize your mood over time.")
    if st.session_state.equipped_animation == "Mood Sparkle Animation":
        st.markdown("<div style='color: #FFD700; font-size: 24px;'>✨✨ You're glowing with Mood Sparkle ✨✨</div>", unsafe_allow_html=True)

with tabs[3]:
    st.subheader("🧑‍🎤 Profile")
    if st.session_state.vyber_type:
        st.markdown(f"### Your Type: {st.session_state.vyber_type}")
        st.markdown(f"**Unlocked Skills:** {', '.join(UNLOCKS.get(st.session_state.vyber_type, []))}")
        st.markdown(f"<div style='background:{VYBER_THEMES[st.session_state.vyber_type]};padding:1em;border-radius:10px;color:white;'>You are on the {st.session_state.vyber_type} path. Let your unique strengths shine!</div>", unsafe_allow_html=True)
        st.image(f"images/{st.session_state.vyber_type.lower()}.png", caption="Your Energy Avatar", use_column_width=True)

with tabs[4]:
    st.subheader("🧪 Personality Kwyz")
    st.write("Find out what kind of Vyber you are!")
    # ... existing quiz code ...

with tabs[5]:
    st.subheader("🛍️ VybeShop")
    st.markdown(f"You have **{st.session_state.vybux} VybuX**")

    shop_items = {
        "Mood Sparkle Animation": 20,
        "Alt Avatar Frame": 35,
        "Secret Echo Fragment": 50,
        "Custom Gradient Pack": 40,
        "Vyber Sound Pack": 30,
        "Mystery Box": 10,
    }

    for item, price in shop_items.items():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{item}** - {price} VybuX")
        with col2:
            if st.button(f"Buy {item}", key=f"buy_{item}"):
                if st.session_state.vybux >= price:
                    st.session_state.vybux -= price
                    if item not in st.session_state.unlocked_animations:
                        st.session_state.unlocked_animations.append(item)
                    st.success(f"Purchased {item}!")
                else:
                    st.error("Not enough VybuX 😢")
        with col3:
            if item in st.session_state.unlocked_animations:
                if st.button(f"Equip {item}", key=f"equip_{item}"):
                    st.session_state.equipped_animation = item
                    st.success(f"Equipped {item}!")

with tabs[6]:
    st.subheader("📇 Characters")
    for player in st.session_state.players:
        st.markdown(f"### {player}")
        st.markdown("- Level: {}".format(st.session_state.user_stats["level"]))
        st.markdown("- XP: {}".format(st.session_state.user_stats["xp"]))
        st.markdown("- Strength: {}".format(st.session_state.user_stats["strength"]))
        st.markdown("- Focus: {}".format(st.session_state.user_stats["focus"]))
        st.markdown("- Creativity: {}".format(st.session_state.user_stats["creativity"]))
        st.markdown("- Resilience: {}".format(st.session_state.user_stats["resilience"]))
        st.markdown("---")

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

