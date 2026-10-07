import streamlit as st
import random
import time

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Game Câu Cá - Streamlit Edition",
    page_icon="🎣",
    layout="centered"
)

# Custom CSS giao diện đại dương
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #87CEEB 0%, #1E90FF 40%, #00008B 100%);
        color: white;
    }
    .game-card {
        background-color: rgba(255, 255, 255, 0.15);
        padding: 15px;
        border-radius: 12px;
        backdrop-filter: blur(5px);
        text-align: center;
        margin-bottom: 15px;
    }
    .catch-box {
        font-size: 24px;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Khởi tạo trạng thái game (Session State)
if "score" not in st.session_state:
    st.session_state.score = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "time_left" not in st.session_state:
    st.session_state.time_left = 30
if "game_active" not in st.session_state:
    st.session_state.game_active = False
if "last_event" not in st.session_state:
    st.session_state.last_event = "Bấm 'Bắt đầu câu' để ra khơi!"
if "fishes_caught" not in
