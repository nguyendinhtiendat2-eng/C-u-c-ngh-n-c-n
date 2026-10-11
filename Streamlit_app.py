import streamlit as st
import random
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Game Câu Cá May Mắn",
    page_icon="🎣",
    layout="centered"
)

# --- KHỞI TẠO STATE ---
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

# --- DỮ LIỆU CÁ & CẦN CÂU ---
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

# --- PHẦN PHÁT ÂM THANH (Web Audio API) ---
def play_sound(sound_type):
    if sound_type == "catch":
        js = """
        <script>
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.connect(gain); gain.connect(ctx.destination);
        osc.frequency.setValueAtTime(440, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.3, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
        osc.start(); osc.stop(ctx.currentTime + 0.3);
        </script>
        """
    else:
        js = """
        <script>
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.connect(gain); gain.connect(ctx.destination);
        osc.frequency.setValueAtTime(200, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(100, ctx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2);
        osc.start(); osc.stop(ctx.currentTime + 0.2);
        </script>
        """
    st.components.v1.html(js, height=0)

# --- HÀM XỬ LÝ CÂU CÁ ---
def cast_line():
    luck = ROD_UPGRADES[st.session_state.rod_level]["luck_bonus"]
    weights = []
    for fish in FISH_TYPES:
        w = fish["weight"]
        if fish["rarity"] != "Rác":
            w += luck / 4
        weights.append(max(w, 1))

    caught_fish = random.choices(FISH_TYPES, weights=weights, k=1)[0]
    
    st.session_state.total_catches += 1
    fish_name = caught_fish["name"]
    st.session_state.inventory[fish_name] = st.session_state.inventory.get(fish_name, 0) + 1
    st.session_state.last_catch = caught_fish
    
    log_entry = f"{caught_fish['icon']} Bạn đã câu được **{fish_name}** ({caught_fish['rarity']}) - Trị giá: {caught_fish['price']} xu"
    st.session_state.logs.insert(0, log_entry)
    
    return caught_fish

# --- GIAO DIỆN CHÍNH ---
st.title("🎣 Game May Rủi: Câu Cá Đổi Thưởng")

# Hiển thị chỉ số
col1, col2, col3 = st.columns(3)
col1.metric("💰 Xu hiện có", f"{st.session_state.money} xu")
col2.metric("🎣 Cần câu", ROD_UPGRADES[st.session_state.rod_level]["name"])
col3.metric("🐟 Số lần đã câu", f"{st.session_state.total_catches}")

st.divider()

tab_play, tab_shop, tab_inventory = st.tabs(["🎮 Bắt đầu câu", "🛒 Cửa hàng", "🎒 Túi đồ"])

with tab_play:
    st.subheader("🏞️ Hồ Câu Trực Quan")
    
    # Giao diện chia rõ bờ sông (trên) và dòng nước có cá bơi (dưới)
    scene_html = f"""
    <style>
        @keyframes swim1 {{
            0% {{ transform: translateX(-40px); }}
            100% {{ transform: translateX(280px); }}
        }}
        @keyframes swim2 {{
            0% {{ transform: translateX(260px); }}
            100% {{ transform: translateX(-30px); }}
        }}
        @keyframes wave {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .game-scene {{
            border-radius: 12
  
