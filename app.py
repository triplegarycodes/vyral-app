import streamlit as st
import random
import time
import graphviz

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

# --- THEME FUNCTION ---
def apply_theme(theme_name):
    css_dict = {
        "Focus Drift": """
            <style>
            .main, .stApp {
                background: radial-gradient(circle, #cceeff, #ffffff);
                animation: drift 5s infinite alternate;
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
            }
            @keyframes heatup {
                from { filter: hue-rotate(0deg); }
                to { filter: hue-rotate(30deg); }
            }
            </style>
        """
    }
    st.markdown(css_dict.get(theme_name, ""), unsafe_allow_html=True)

# --- SPLASH ANIMATIONS ---
def splash_animation(effect):
    if effect == "clout":
        st.markdown("""
            <style>
            .main, .stApp {
                animation: cloutflash 1s ease-in-out infinite alternate;
            }
            @keyframes cloutflash {
                from { background-color: #ffeecc; }
                to { background-color: #fff0f0; }
            }
            </style>
        """, unsafe_allow_html=True)
    elif effect == "unlock":
        st.markdown("""
            <style>
            .main, .stApp {
                background: radial-gradient(circle, #aaffaa, #ffffff);
                animation: unlockshine 3s ease-in-out;
            }
            @keyframes unlockshine {
                from { transform: scale(0.9); }
                to { transform: scale(1.1); }
            }
            </style>
        """, unsafe_allow_html=True)
    elif effect == "shake":
        st.markdown("""
            <style>
            .main, .stApp {
                animation: shake 0.5s;
            }
            @keyframes shake {
                0% { transform: translate(1px, 1px) rotate(0deg); }
                25% { transform: translate(-1px, -2px) rotate(-1deg); }
                50% { transform: translate(-3px, 0px) rotate(1deg); }
                75% { transform: translate(1px, 2px) rotate(0deg); }
                100% { transform: translate(1px, -1px) rotate(1deg); }
            }
            </style>
        """, unsafe_allow_html=True)

# --- PROFILE CARD COMPONENT ---
def profile_card(name, score, skills):
    st.markdown(f"""
        <div style='border-radius: 15px; padding: 1.5rem; margin: 1rem 0; background: linear-gradient(145deg, #e6e6e6, #ffffff); box-shadow: 6px 6px 12px #cccccc, -6px -6px 12px #ffffff;'>
            <h3 style='margin-bottom: 0.5rem;'>{name}</h3>
            <p><strong>Vybe Score:</strong> {score}</p>
            <p><strong>Skills:</strong> {', '.join(skills)}</p>
        </div>
    """, unsafe_allow_html=True)

# --- APPLY THEME BASED ON STATE ---
if st.session_state.vybe_royale_score > 150:
    apply_theme("Heat Up Mode")
elif len(st.session_state.coachbot_data["emotions"]) + len(st.session_state.coachbot_data["topics"]) > 5:
    apply_theme("Mood Burst")
else:
    apply_theme("Focus Drift")

# --- Main App Content ---
st.title("🔥 CoachBot Chat + Vybe Royale | Vyral App")
st.caption("CoachBot adapts to your vibes and tracks your journey live ✨")

user_input = st.text_input("Talk to CoachBot:", placeholder="What's on your mind today?")
if st.button("Send") and user_input:
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("CoachBot", "Let's make that a SMART goal!"))

for speaker, msg in st.session_state.messages:
    with st.chat_message(name=speaker):
        st.markdown(msg)

st.header("🎮 Vybe Royale Zone")

# --- Vybe Royale Function ---
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
        splash_animation("shake")
    elif "+" in outcome:
        value = int(outcome.split('+')[-1].split(' ')[0])
        st.session_state.vybe_royale_score += value
        splash_animation("unlock")
    st.session_state.reward_animation = outcome
    return outcome

if st.button("Play Round 🎲"):
    result = simulate_vybe_royale()
    st.success(f"Result: {result}")

st.metric("🧠 Mental Health Points", st.session_state.vybe_royale_score)

# --- Profile Card Section ---
st.header("💼 Vyber Profile")
profile_card("You", st.session_state.vybe_royale_score, st.session_state.unlocked_skills)

