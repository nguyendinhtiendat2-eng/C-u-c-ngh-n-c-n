import time
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hồ Câu Tên May Mắn", page_icon="🎣", layout="centered"
)

st.title("🎣 Hồ Câu Tên May Mắn 🐟")

# Khởi tạo Session State
if "fishing_status" not in st.session_state:
    st.session_state.fishing_status = "idle"  # idle, waiting, biting
if "bite_time" not in st.session_state:
    st.session_state.bite_time = 0
if "last_caught" not in st.session_state:
    st.session_state.last_caught = None
if "history" not in st.session_state:
    st.session_state.history = []

# Nhập danh sách tên
default_names = "An\nBình\nCường\nDung\nHoàng\nLan\nMinh\nPhúc"
names_input = st.text_area(
    "📝 Nhập danh sách tên có trong hồ (mỗi tên 1 dòng):",
    value=default_names,
    height=90,
)
names_list = [n.strip() for n in names_input.split("\n") if n.strip()]

# ----------------- HÌNH ẢNH HỒ CÂU VÀ CÁ CÓ TÊN (HTML/CSS) -----------------
# Xây dựng các chú cá có gắn tên để thả vào hồ
fish_html_elements = ""
colors = [
    "#FF5722",
    "#FF9800",
    "#E91E63",
    "#9C27B0",
    "#00BCD4",
    "#4CAF50",
    "#FFEB3B",
]

for idx, name in enumerate(names_list):
    color = colors[idx % len(colors)]
    top_pos = random.randint(110, 240)
    anim_duration = random.uniform(6, 12)
    anim_delay = random.uniform(0, 5)

    fish_html_elements += f"""
    <div class="fish" style="top: {top_pos}px; animation-duration: {anim_duration}s; animation-delay: -{anim_delay}s;">
        <span class="fish-body" style="background: {color};">
            <span class="fish-name">{name}</span>
            <span class="fish-tail" style="border-right-color: {color};"></span>
        </span>
    </div>
    """

# Hiệu ứng trạng thái dây câu/phao
float_class = ""
line_height = "100px"
if st.session_state.fishing_status == "waiting":
    line_height = "160px"
    float_class = "waiting"
elif st.session_state.fishing_status == "biting":
    line_height = "165px"
    float_class = "biting"

lake_visual_html = f"""
<style>
    .lake-container {{
        position: relative;
        width: 100%;
        height: 300px;
        background: linear-gradient(180deg, #87CEEB 0%, #87CEEB 35%, #1E88E5 35%, #0D47A1 100%);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        font-family: Arial, sans-serif;
    }}
    
    /* Người ngồi câu */
    .fisherman {{
        position: absolute;
        top: 40px;
        left: 20px;
        font-size: 50px;
        z-index: 10;
    }}
    .rod {{
        position: absolute;
        top: 60px;
        left: 65px;
        width: 100px;
        height: 4px;
        background: #5D4037;
        transform: rotate(-25deg);
        transform-origin: left center;
        z-index: 9;
    }}
    
    /* Dây câu & Phao */
    .fishing-line {{
        position: absolute;
        top: 20px;
        left: 155px;
        width: 2px;
        height: {line_height};
        background: rgba(255, 255, 255, 0.8);
        transition: height 0.3s ease;
        z-index: 8;
    }}
    .float {{
        position: absolute;
        bottom: -8px;
        left: -5px;
        width: 12px;
        height: 12px;
        background: red;
        border-radius: 50%;
        border: 2px solid white;
    }}
    .float.waiting {{
        animation: bob 1s infinite alternate ease-in-out;
    }}
    .float.biting {{
        background: #FF0000;
        box-shadow: 0 0 10px #FF0000;
        animation: bite 0.2s infinite alternate;
    }}

    @keyframes bob {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(5px); }}
    }}
    @keyframes bite {{
        0% {{ transform: translateY(-3px) scale(1.1); }}
        100% {{ transform: translateY(6px) scale(0.9); }}
    }}

    /* Cá bơi có tên */
    .fish {{
        position: absolute;
        right: -120px;
        animation: swim linear infinite;
        z-index: 5;
    }}
    .fish-body {{
        position: relative;
        display: inline-block;
        padding: 4px 12px;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        font-size: 13px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        white-space: nowrap;
    }}
    .fish-tail {{
        position: absolute;
        right: -10px;
        top: 3px;
        width: 0;
        height: 0;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
        border-right: 12px solid #FF5722;
    }}

    @keyframes swim {{
        0% {{ transform: translateX(0) scaleX(1); }}
        50% {{ transform: translateX(-650px) scaleX(1); }}
        50.1% {{ transform: translateX(-650px) scaleX(-1); }}
        100% {{ transform: translateX(0) scaleX(-1); }}
    }}
</style>

<div class="lake-container">
    <!-- Người & Cần câu -->
    <div class="fisherman">🧑‍🌾</div>
    <div class="rod"></div>
    
    <!-- Dây câu & Phao -->
    <div class="fishing-line">
        <div class="float {float_class}"></div>
    </div>

    <!-- Cá bơi trong hồ -->
    {fish_html_elements}
</div>
"""

# Hiển thị đồ họa hồ câu
components.html(lake_visual_html, height=310)

# ----------------- NÚT BẤM ĐIỀU KHIỂN & LOGIC -----------------
col1, col2 = st.columns(2)
with col1:
    throw_btn = st.button("🎣 THẢ CẦN CÂU", use_container_width=True)
with col2:
    pull_btn = st.button("⚡ KÉO CẦN NGAY!", use_container_width=True)

msg_box = st.empty()

# Logic Thả cần
if throw_btn:
    if len(names_list) == 0:
        st.warning("Hãy nhập ít nhất 1 tên vào danh sách trước khi thả câu!")
    elif st.session_state.fishing_status == "idle":
        st.session_state.fishing_status = "waiting"
        st.session_state.bite_time = time.time() + random.uniform(1.2, 3.0)
        st.session_state.last_caught = None
        st.rerun()

# Logic Chờ cá cắn
if st.session_state.fishing_status == "waiting":
    if time.time() >= st.session_state.bite_time:
        st.session_state.fishing_status = "biting"
        st.rerun()
    else:
        msg_box.info(
            "⏳ Phao đang nhấp nhô... Các chú cá tên đang tò mò bơi lại gần..."
        )
        time.sleep(0.3)
        st.rerun()

elif st.session_state.fishing_status == "biting":
    msg_box.warning(
        "🚨 **CÓ CÁ MANG TÊN ĐÃ CẮN CÂU! BẤM 'KÉO CẦN NGAY' TỰC THÌ!**"
    )

# Logic Kéo cần
if pull_btn:
    if st.session_state.fishing_status == "biting":
        caught_name = random.choice(names_list)
        st.session_state.fishing_status = "idle"
        st.session_state.last_caught = caught_name
        st.session_state.history.insert(0, caught_name)
        st.rerun()
    elif st.session_state.fishing_status == "waiting":
        st.session_state.fishing_status = "idle"
        msg_box.error(
            "❌ Kéo quá giật cục! Con cá mang tên đã giật mình bơi mất."
        )
        st.rerun()
    else:
        msg_box.info("⚠️ Bạn chưa thả cần câu xuống hồ!")

# Hiển thị kết quả vừa câu được
if st.session_state.last_caught:
    st.balloons()
    st.success(
        f"🎉 **BẠN ĐÃ CÂU ĐƯỢC CHÚ CÁ MANG TÊN:** 🔥 **{st.session_state.last_caught}** 🔥"
    )

# Lịch sử câu
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Danh sách các tên đã câu lên")
    st.write(", ".join([f"**{n}**" for n in st.session_state.history]))
  
