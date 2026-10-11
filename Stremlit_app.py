import streamlit as st
import random
import time

st.set_page_config(
    page_title="Game Câu Cá May Mắn",
    page_icon="🎣",
    layout="centered"
)

# --- KHỞI TẠO STATE ---
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "money" not in st.session_state:
    st.session_state.money = 100
if "rod_level" not in st.session_state:
    st.session_state.rod_level = 1
if "inventory" not in st.session_state:
    st.session_state.inventory = {}
if "total_catches" not in st.session_state:
    st.session_state.total_catches = 0
if "logs" not in st.session_state:
    st.session_state.logs = []
if "last_catch" not in st.session_state:
    st.session_state.last_catch = {"name": "Sẵn sàng thả câu", "icon": "🌊", "rarity": "Bắt đầu"}

FISH_TYPES = [
    {"name": "Rác / Giày cũ", "price": 0, "rarity": "Rác", "weight": 35, "icon": "👞"},
    {"name": "Cá Chép", "price": 20, "rarity": "Phổ thông", "weight": 35, "icon": "🐟"},
    {"name": "Cá Hồi", "price": 50, "rarity": "Hiếm", "weight": 18, "icon": "🐠"},
    {"name": "Cá Ngừ", "price": 120, "rarity": "Cực hiếm", "weight": 9, "icon": "🐡"},
    {"name": "Cá Mập Vàng", "price": 500, "rarity": "Huyền thoại", "weight": 3, "icon": "🦈"},
]

ROD_UPGRADES = {
    1: {"name": "Cần Trúc", "cost": 0, "luck_bonus": 0},
    2: {"name": "Cần Máy", "cost": 200, "luck_bonus": 5},
    3: {"name": "Cần Carbon", "cost": 600, "luck_bonus": 12},
}

# --- MÀN HÌNH BẮT ĐẦU ---
if not st.session_state.game_started:
    st.title("🎣 CHÀO MỪNG ĐẾN VỚI GAME CÂU CÁ")
    st.markdown("### Thử vận may - Săn cá khủng ngay trên điện thoại!")
    
    st.info("""
    **Luật chơi:**
    * Bắt đầu với **100 xu**. Thả câu tốn **5 xu**.
    * Bán cá thu xu để nâng cấp cần câu câu cá hiếm!
    """)
    
    st.write("")
    if st.button("🚀 BẮT ĐẦU CHƠI NGAY", use_container_width=True, type="primary"):
        st.session_state.game_started = True
        st.rerun()

else:
    # --- GIAO DIỆN CHÍNH ---
    st.title("🎣 Game May Rủi: Câu Cá Đổi Thưởng")

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Xu", f"{st.session_state.money}")
    col2.metric("🎣 Cần", ROD_UPGRADES[st.session_state.rod_level]["name"])
    col3.metric("🐟 Số lần", f"{st.session_state.total_catches}")

    st.divider()

    tab_play, tab_shop, tab_inventory = st.tabs(["🎮 Câu cá", "🛒 Cửa hàng", "🎒 Túi đồ"])

    with tab_play:
        st.subheader("🏞️ Hồ Câu Trực Quan")
        
        # Khung hoạt ảnh bờ sông và cá bơi lội
        scene_html = f"""
        <style>
            @keyframes swim1 {{
                0% {{ transform: translateX(-30px); }}
                100% {{ transform: translateX(250px); }}
            }}
            @keyframes swim2 {{
                0% {{ transform: translateX(230px); }}
                100% {{ transform: translateX(-20px); }}
            }}
            @keyframes wave {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            .game-scene {{
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                border: 2px solid #ddd;
            }}
            .bank-area {{
                background-color: #dcedc8;
                padding: 12px 15px;
                font-size: 20px;
                border-bottom: 3px dashed #8bc34a;
            }}
