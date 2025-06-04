# Full Streamlit Code for Vybe Royale Integration with Quiz Logic and Milestones

import streamlit as st
import pandas as pd
import random
import time

# Load Quiz Questions from the 60-question file
@st.cache_data
def load_questions():
    df = pd.read_excel("/mnt/data/Vybe Royale_s.xlsx")
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

st.title("🎮 Vybe Royale Mini Game")

st.markdown(f"**Score:** {st.session_state.vybe_royale_score} | **VybuX:** {st.session_state.vybux}")

if st.button("Play Round"):
    if can_play():
        st.session_state.click_count += 1
        st.session_state.last_click_time = time.time()

        # Every 10 clicks, trigger quiz question
        if st.session_state.click_count % 10 == 0:
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
            # Standard click bonus
            reward = random.choice([-5, 5])
            st.session_state.vybe_royale_score += reward
            st.markdown(f"{'+5' if reward > 0 else '-5'} Vybe Royale Score this round!")

        # Check milestones
        for milestone, item in MILESTONES.items():
            if st.session_state.vybux >= milestone and item not in st.session_state.milestones_unlocked:
                st.session_state.milestones_unlocked.append(item)
                st.balloons()
                st.success(f"🎉 Milestone Reached: {item} Unlocked!")
    else:
        st.warning("⏳ Slow down! Wait a few seconds between rounds.")

# Show unlocked items
if st.session_state.milestones_unlocked:
    st.markdown("### 🔓 Unlocked Rewards")
    for item in st.session_state.milestones_unlocked:
        st.markdown(f"- {item}")

# Optional: Reset button for testing
if st.button("Reset Game"):
    st.session_state.vybe_royale_score = 100
    st.session_state.vybux = 50
    st.session_state.click_count = 0
    st.session_state.milestones_unlocked = []
    st.session_state.last_click_time = 0

