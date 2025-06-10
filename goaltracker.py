import streamlit as st
import google.generativeai as genai
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime

# --- Gemini Setup ---
genai.configure(api_key="AIzaSyD-q5-mcoLn6Horgx-tPD_q4V5N_GV7uQE")
model = genai.GenerativeModel("gemini-2.0-flash")

def get_daily_quote():
    prompt = "Give a short motivational quote with 1-2 relevant emojis."
    response = model.generate_content(prompt)
    return response.text

# --- Session State Setup ---
if 'page' not in st.session_state:
    st.session_state.page = 'onboarding'

if 'goals' not in st.session_state:
    st.session_state.goals = []

# --- Style ---
st.set_page_config(page_title="🎯 Goal Tracker", layout="wide")
st.markdown("""
<style>
body {
    font-family: 'Poppins', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #ffffff, #f0f4f8);
}
.card {
    background: #fff0f6;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    padding: 20px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Light / Dark Mode Toggle ---
mode = st.toggle("🌗 Toggle Dark Mode")
if mode:
    st.markdown("""
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
    }
    .card {
        background: #2c2c2c;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Onboarding ---
if st.session_state.page == 'onboarding':
    st.title("🎯 Goal Tracker with Motivational Quotes")
    st.image("https://cdn-icons-png.flaticon.com/512/833/833472.png", width=200)
    st.markdown("""
    Welcome to your personal growth companion!

    ✅ Track goals  
    💡 Stay motivated daily  
    🎉 Celebrate small wins  
    
    Built for Gen Z & Millennials who love self-growth 💖
    """)
    if st.button("🚀 Get Started"):
        st.session_state.page = 'goal_setup'

# --- Goal Setup Page ---
elif st.session_state.page == 'goal_setup':
    st.header("🎯 Set Your Goal")
    goal_type = st.selectbox("Select Goal Type", ["🏋️‍♀️ Fitness", "💼 Career", "🎓 Education", "💰 Finance"])
    goal_title = st.text_input("Goal Title")
    deadline = st.date_input("Deadline")
    subtasks = st.text_area("Sub-tasks (separate with commas)")

    if st.button("✅ Save Goal"):
        st.session_state.goals.append({
            'type': goal_type,
            'title': goal_title,
            'deadline': deadline,
            'subtasks': [s.strip() for s in subtasks.split(',') if s.strip()],
            'progress': 0
        })
        st.success("Goal Added Successfully!")
        st.balloons()
        st.session_state.page = 'dashboard'

# --- Dashboard ---
elif st.session_state.page == 'dashboard':
    st.title("📊 Dashboard")
    st.subheader("Your Active Goals")

    for idx, goal in enumerate(st.session_state.goals):
        with st.container():
            st.markdown(f"""
            <div class='card'>
            <h4>{goal['type']} {goal['title']}</h4>
            <p>Deadline: {goal['deadline'].strftime('%b %d, %Y')}</p>
            <p>Progress: {goal['progress']}%</p>
            </div>
            """, unsafe_allow_html=True)

    st.subheader("🌟 Today's Motivation")
    st.info(get_daily_quote())
    if st.button("✨ View Daily Tip & Quote"):
        st.session_state.page = 'daily_tip'

# --- Daily Tip + Quote ---
elif st.session_state.page == 'daily_tip':
    st.title("💡 Daily Tip & Quote")
    quote = get_daily_quote()
    st.success(quote)
    st.image("https://cdn-icons-png.flaticon.com/512/3159/3159066.png", width=150)
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = 'dashboard'

# --- Notifications ---
elif st.session_state.page == 'notifications':
    st.title("🔔 Reminders & Nudges")
    for goal in st.session_state.goals:
        st.warning(f"Don't forget to work on **{goal['title']}** today! 💪")

# --- Profile Page ---
elif st.session_state.page == 'profile':
    st.title("👤 Profile & Achievements")
    st.markdown("""
    - 🏆 Goals Completed: 2  
    - 🔥 Current Streak: 6 days  
    - ❤️ Favorite Quote: "Believe in yourself 💖"
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/1077/1077012.png", width=100)

# --- Sidebar Navigation ---
st.sidebar.title("📂 Navigation")
if st.sidebar.button("🏠 Onboarding"): st.session_state.page = 'onboarding'
if st.sidebar.button("🎯 Goal Setup"): st.session_state.page = 'goal_setup'
if st.sidebar.button("📊 Dashboard"): st.session_state.page = 'dashboard'
if st.sidebar.button("💡 Daily Tip"): st.session_state.page = 'daily_tip'
if st.sidebar.button("🔔 Notifications"): st.session_state.page = 'notifications'
if st.sidebar.button("👤 Profile"): st.session_state.page = 'profile'
