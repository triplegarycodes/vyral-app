import streamlit as st
import random
import time
import graphviz

st.set_page_config(layout="wide")

# Initialize state
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
if "last_auto_run" not in st.session_state:
    st.session_state.last_auto_run = time.time()

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
        st.snow()
    elif "+" in outcome:
        value = int(outcome.split('+')[-1].split(' ')[0])
        st.session_state.vybe_royale_score += value
        st.balloons()
    st.session_state.reward_animation = outcome
    return outcome

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
if st.button("Play Round 🎲"):
    result = simulate_vybe_royale()
    st.success(f"Result: {result}")

st.metric("🧠 Mental Health Points", st.session_state.vybe_royale_score)
