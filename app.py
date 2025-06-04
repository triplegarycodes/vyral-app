# Full Streamlit Code for Vybe Royale Integration with Quiz Logic, Milestones, Profile Tabs, and VybeCheck

import streamlit as st
import pandas as pd
import random
import time

# Load Quiz Questions from Google Sheets CSV Export
@st.cache_data
def load_questions():
    url = "https://docs.google.com/spreadsheets/d/1QDpJ103Rx-px0mDve3XLpp-RKKxd9O7hDi4d71edwMY/export?format=csv&id=1QDpJ103Rx-px0mDve3XLpp-RKKxd9O7hDi4d71edwMY&gid=750088929"
    df = pd.read_csv(url)
    df.dropna(inplace=True)
    return df

questions_df = load_questions()

# Initialize session state
if "click_count" not in st.session_state:
    st.session_state.click_count = 0
if "vybe_royale_score" not in st.session_state:
    st.session_state.vybe_royale_score = 100
if "vybux" not in st.session_state:
    st.session_state.vybux = 50
if "last_click_time" not in st.session_state:
    st.session_state.last_click_time = 0
if "milestones_unlocked" not in st.session_state:
    st.session_state.milestones_unlocked = []
if "next_quiz_threshold" not in st.session_state:
    st.session_state.next_quiz_threshold = random.randint(1, 5)
if "vybecheck_log" not in st.session_state:
    st.session_state.vybecheck_log = []

MILESTONES = {
    100: "Alt Avatar Frame",
    150: "Secret Echo Fragment",
    200: "Vyber Sound Pack",
    250: "Custom Gradient Pack",
    300: "Mystery Bonus Box"
}

# Cooldown logic (e.g., 5 seconds between valid plays)
def can_play():
    return time.time() - st.session_state.last_click_time >= 5

# Sidebar navigation
page = st.sidebar.selectbox("Navigate", ["Vybe Royale", "Profile", "VybeCheck"])

if page == "Vybe Royale":
    st.title("🎮 Vybe Royale Mini Game")
    st.markdown(f"**Score:** {st.session_state.vybe_royale_score} | **VybuX:** {st.session_state.vybux}")

    if st.button("Play Round"):
        if can_play():
            st.session_state.click_count += 1
            st.session_state.last_click_time = time.time()

            # Trigger quiz question every N rounds where N is randomized
            if st.session_state.click_count % st.session_state.next_quiz_threshold == 0:
                st.session_state.next_quiz_threshold = random.randint(1, 5)
                st.markdown("### Bonus Round: Answer to earn!")
                row = questions_df.sample(1).iloc[0]
                question, a, b, c, correct = row["Question"], row["Option A"], row["Option B"], row["Option C"], row["Correct Answer"]

                user_answer = st.radio(question, options=["Option A", "Option B", "Option C"], index=None, key=f"quiz_{st.session_state.click_count}")

                if user_answer:
                    if user_answer == correct:
                        st.success("✅ Correct! +5 VybuX")
                        st.session_state.vybux += 5
                    else:
                        st.error("❌ Incorrect. -5 Vybe Royale Score")
                        st.session_state.vybe_royale_score -= 5
            else:
                reward = random.choice([-5, 5])
                st.session_state.vybe_royale_score += reward
                st.markdown(f"{'+5' if reward > 0 else '-5'} Vybe Royale Score this round!")

            for milestone, item in MILESTONES.items():
                if st.session_state.vybux >= milestone and item not in st.session_state.milestones_unlocked:
                    st.session_state.milestones_unlocked.append(item)
                    st.balloons()
                    st.success(f"🎉 Milestone Reached: {item} Unlocked!")
        else:
            st.warning("⏳ Slow down! Wait a few seconds between rounds.")

    if st.session_state.milestones_unlocked:
        st.markdown("### 🔓 Unlocked Rewards")
        for item in st.session_state.milestones_unlocked:
            st.markdown(f"- {item}")

    if st.button("Reset Game"):
        st.session_state.vybe_royale_score = 100
        st.session_state.vybux = 50
        st.session_state.click_count = 0
        st.session_state.milestones_unlocked = []
        st.session_state.last_click_time = 0

elif page == "Profile":
    st.title("👤 Your Profile")
    st.markdown(f"**Vybe Royale Score:** {st.session_state.vybe_royale_score}")
    st.markdown(f"**VybuX Balance:** {st.session_state.vybux}")

    if st.session_state.vybe_royale_score >= 250:
        st.success("🔥 Status: LEGENDARY")
    elif st.session_state.vybe_royale_score >= 150:
        st.info("🌟 Status: Elite")
    elif st.session_state.vybe_royale_score >= 100:
        st.warning("💬 Status: Explorer")
    else:
        st.error("📉 Status: Rookie")

    if st.session_state.milestones_unlocked:
        st.markdown("### 🧩 Rewards You've Unlocked")
        for item in st.session_state.milestones_unlocked:
            st.markdown(f"- {item}")

elif page == "VybeCheck":
    st.title("📝 VybeCheck – Your Goals & Logs")
    goal = st.text_input("What's on your mind or to-do?")
    if st.button("Log Entry") and goal:
        st.session_state.vybecheck_log.append((goal, time.strftime("%Y-%m-%d %H:%M:%S")))
        st.success("Goal Logged Successfully!")

    if st.session_state.vybecheck_log:
        st.markdown("### 📓 Your VybeCheck Logs")
        for entry, timestamp in reversed(st.session_state.vybecheck_log):
            st.markdown(f"- [{timestamp}] {entry}")


