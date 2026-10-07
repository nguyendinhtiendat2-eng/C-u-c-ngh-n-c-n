import streamlit as st
import random
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Game Câu Cá Bối Bối",
    page_icon="🎣",
    layout="centered"
)

# --- TÙY CHỈNH CSS CHO GIAO DIỆN BEAUTIFUL ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #87CEEB 0%, #1E90FF 50%, #00008B 100%);
        color: white;
    }
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #FFD700;
        text-shadow: 2px 2px 4px #000;
        margin-bottom: 20px;
    }
    .stat-card {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        backdrop-filter: blur(5px);
        margin-bottom: 20px;
    }
    .fish-display {
        font-size: 5rem;
        text-align: center;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- QUẢN LÝ TRẠNG THÁI (SESSION STATE) ---
if "game_state" not in st.session_state:
    st.session_state.game_state = "START"  # Các trạng thái: START, FISHING, HOOKED, RESULT
if "score" not in st.session_state:
    st.session_state.score = 0
if "catches" not in st.session_state:
    st.session_state.catches = []
if "current_fish" not in st.session_state:
    st.session_state.current_fish = None

# --- DANH SÁCH CÁC LOẠI CÁ ---
FISH_TYPES = [
    {"name": "Cá Rô Nhỏ", "icon": "🐟", "points": 10, "rarity": "Phổ biến"},
    {"name": "Cá Chép Vàng", "icon": "🐠", "points": 25, "rarity": "Hiếm"},
    {"name": "Cá Ngừ Đại Dương", "icon": "🐡", "points": 50, "rarity": "Rất hiếm"},
    {"name": "Cá Mập Xanh", "icon": "🦈", "points": 100, "rarity": "Huyền thoại"},
    {"name": "Giày Cũ 👟", "icon": "👟", "points": 0, "rarity": "Rác"},
]

# --- HÀM CHỌN CÁ NGẪU NHIÊN ---
def get_random_fish():
    weights = [50, 25, 15, 5, 5]  # Tỷ lệ xuất hiện (%)
    return random.choices(FISH_TYPES, weights=weights, k=1)[0]

# --- 1. MÀN HÌNH BẮT ĐẦU (START SCREEN) ---
if st.session_state.game_state == "START":
    st.markdown("<h1 class='main-title'>🎣 GAME CÂU CÁ KỲ THÚ</h1>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; font-size: 1.2rem; margin-bottom: 30px;'>
            Chào mừng bạn đến với hồ câu cá! Hãy thử vận may để bắt những chú cá quý hiếm nhất.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=500", use_column_width=True)
        st.write("")
        if st.button("🚀 BẮT ĐẦU CÂU CÁ", use_container_width=True, type="primary"):
            st.session_state.game_state = "FISHING"
            st.rerun()

# --- GIAO DIỆN KHI ĐANG TRONG GAME ---
else:
    # Bảng điểm & thông tin
    st.markdown("<h1 class='main-title'>🎣 ĐANG CÂU CÁ...</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='stat-card'><h3>🏆 Điểm số</h3><h2>{st.session_state.score}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.
