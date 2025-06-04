# Full Streamlit Code for Vybe Royale Integration with Quiz Logic, Milestones, Vybe Shop, and Avatar Profiles

import streamlit as st
import pandas as pd
import random
import time

# Load Quiz Questions from the CSV file for faster performance
@st.cache_data
def load_questions():
    df = pd.read_csv("/mnt/data/Vybe Royale _s - Sheet1.csv")
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
if "owned_items" not in st.session_state:
    st.session_state.owned_items = []
if "selected_avatar" not in st.session_state:
    st.session_state.selected_avatar = "None"

MILESTONES = {
    100: "Alt Avatar Frame",
    150: "Secret Echo Fragment",
    200: "Vyber Sound Pack",
    250: "Custom Gradient Pack",
    300: "Mystery Bonus Box"
}

SHOP_ITEMS = {
    "Cosmic Trail": 40,
    "Name Glow (Blue)": 30,
    "Double XP Boost (10 min)": 50,
    "Vybe Emote Pack": 25,
    "Echo Avatar: Horizon Fox": 75,
    "Echo Avatar: Neon Ghost": 75
}

AVATAR_OPTIONS = ["None", "Horizon Fox", "Neon Ghost"]

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

# Show unlocked milestone rewards
if st.session_state.milestones_unlocked:
    st.markdown("### 🔓 Unlocked Rewards")
    for item in st.session_state.milestones_unlocked:
        st.markdown(f"- {item}")

# Vybe Shop Section
st.markdown("---")
st.header("🛍️ Vybe Shop")
for item, cost in SHOP_ITEMS.items():
    if st.button(f"Buy {item} - {cost} VybuX"):
        if st.session_state.vybux >= cost:
            if item not in st.session_state.owned_items:
                st.session_state.vybux -= cost
                st.session_state.owned_items.append(item)
                st.success(f"✅ Purchased: {item}!")
            else:
                st.info("You already own this item.")
        else:
            st.warning("Not enough VybuX!")

# Avatar Selector Section
st.markdown("---")
st.header("🎭 Avatar Selector")
st.session_state.selected_avatar = st.selectbox("Choose Your Avatar", AVATAR_OPTIONS)
st.markdown(f"**Current Avatar:** {st.session_state.selected_avatar}")

# Reset button for testing
if st.button("Reset Game"):
    st.session_state.vybe_royale_score = 100
    st.session_state.vybux = 50
    st.session_state.click_count = 0
    st.session_state.milestones_unlocked = []
    st.session_state.owned_items = []
    st.session_state.last_click_time = 0
    st.session_state.selected_avatar = "None"


