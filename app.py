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
if "positive_streak" not in st.session_state:
    st.session_state.positive_streak = 0

MILESTONES = {
    100: "Alt Avatar Frame",
    150: "Secret Echo Fragment",
    200: "Vyber Sound Pack",
    250: "Custom Gradient Pack",
    300: "Mystery Bonus Box"
}

NORMAL_EVENTS = [
    ("Your crush friend-zones you over text (ouch...)", -10, -4),
    ("You find $5 in your hoodie pocket!", +5, +3),
    ("Lost your AirPods at lunch... again", -5, -6),
    ("Helped a friend study — they passed!", +4, +2),
    ("Accidentally liked a 3-year-old Instagram post...", -6, -2),
    ("Won your school talent show!", +10, +5),
    ("Late to class but teacher didn’t notice", +2, 0),
    ("Spilled your lunch in the cafeteria", -8, -3),
    ("Perfect score on a surprise quiz", +7, +6),
    ("Phone died during your favorite part of a convo", -4, -2),
    ("Someone called your fit fire 🔥", +3, +1),
    ("Tripped in the hallway — someone saw", -5, -1),
    ("Crushed it in gym class dodgeball", +6, +3),
    ("You got featured on the school’s social media", +4, +2),
    ("You made someone laugh who was having a rough day", +5, +5),
    ("You forgot your locker combo again", -2, -2),
    ("Free cookies in the cafeteria today!", +3, +2),
    ("Hit your head getting off the bus...", -3, -1),
    ("Your joke landed perfectly at lunch", +4, +3),
    ("Homework vanished into thin air — teacher believed you?!", +6, +4)
]

# Cooldown logic (e.g., 5 seconds between valid plays)
def can_play():
    return time.time() - st.session_state.last_click_time >= 5

# Main UI Navigation Tabs
tabs = st.tabs(["Vybe Royale", "Profile", "VybeCheck"])

with tabs[0]:
    st.title("🎮 Vybe Royale Mini Game")
    st.markdown(f"**Score:** {st.session_state.vybe_royale_score} | **VybuX:** {st.session_state.vybux}")

    if st.button("Play Round"):
        if can_play():
            st.session_state.click_count += 1
            st.session_state.last_click_time = time.time()

            if st.session_state.click_count % st.session_state.next_quiz_threshold == 0:
                st.session_state.next_quiz_threshold = random.randint(1, 5)
                st.markdown("### Bonus Round: Answer to earn!")

                row = questions_df.sample(1).iloc[0]
                question = row["Question"]
                option_a = row["Option A"]
                option_b = row["Option B"]
                option_c = row["Option C"]
                correct_answer_text = row[row["Correct Answer"]]

                options = [option_a, option_b, option_c]
                random.shuffle(options)

                user_answer = st.radio(question, options=options, index=None, key=f"quiz_{st.session_state.click_count}")

                if user_answer:
                    if user_answer == correct_answer_text:
                        st.success("✅ Correct! +5 VybuX")
                        st.session_state.vybux += 5
                        st.session_state.positive_streak += 1
                    else:
                        st.error("❌ Incorrect. -5 Vybe Royale Score")
                        st.session_state.vybe_royale_score -= 5
                        st.session_state.positive_streak = 0
            else:
                event, score_change, vybux_change = random.choice(NORMAL_EVENTS)
                st.markdown(f"**{event}**")
                st.session_state.vybe_royale_score += score_change
                st.session_state.vybux += vybux_change
                if score_change > 0:
                    st.session_state.positive_streak += 1
                else:
                    st.session_state.positive_streak = 0
                st.markdown(f"Score Change: {score_change:+}, VybuX Change: {vybux_change:+}")

            if st.session_state.positive_streak >= 3:
                st.success("🔥 You're on a hot streak! Bonus +2 VybuX!")
                st.session_state.vybux += 2

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
        st.session_state.positive_streak = 0

with tabs[1]:
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

with tabs[2]:
    st.title("📝 VybeCheck – Your Goals & Logs")
    goal = st.text_input("What's on your mind or to-do?")
    if st.button("Log Entry") and goal:
        st.session_state.vybecheck_log.append((goal, time.strftime("%Y-%m-%d %H:%M:%S")))
        st.success("Goal Logged Successfully!")

    if st.session_state.vybecheck_log:
        st.markdown("### 📓 Your VybeCheck Logs")
        for entry, timestamp in reversed(st.session_state.vybecheck_log):
            st.markdown(f"- [{timestamp}] {entry}")


