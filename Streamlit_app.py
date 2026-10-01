import streamlit as st
import random
import time

# Cấu hình trang
st.set_page_config(
    page_title="Game Câu Cá Chọn Người",
    page_icon="🎣",
    layout="centered"
)

# Khởi tạo Session State lưu danh sách người chơi
if "players" not in st.session_state:
    st.session_state.players = [
        "Nguyễn Văn A", "Trần Thị B", "Lê Văn C", 
        "Phạm Thị D", "Hoàng Văn E", "Vũ Thị F"
    ]

if "winner" not in st.session_state:
    st.session_state.winner = None

st.title("🎣 Game Câu Cá Chọn Người May Mắn")
st.caption("Ứng dụng quay số / bốc thăm ngẫu nhiên giao diện sinh động")

# Sidebar: Quản lý danh sách người chơi
with st.sidebar:
    st.header("⚙️ Quản lý người chơi")
    
    # Ô nhập thêm người mới
    new_player = st.text_input("Thêm tên người chơi:")
    if st.button("➕ Thêm người", use_container_width=True):
        if new_player.strip():
            if new_player.strip() not in st.session_state.players:
                st.session_state.players.append(new_player.strip())
                st.success(f"Đã thêm {new_player.strip()}!")
                st.rerun()
            else:
                st.warning("Tên này đã có trong danh sách.")
        else:
            st.warning("Vui lòng nhập tên hợp lệ.")

    st.divider()
    
    # Danh sách hiện tại
    st.subheader(f"Danh sách ({len(st.session_state.players)})")
    for i, name in enumerate(st.session_state.players):
        col1, col2 = st.columns([3, 1])
        col1.write(f"{i+1}. {name}")
        if col2.button("❌", key=f"del_{i}"):
            st.session_state.players.pop(i)
            st.rerun()

    st.divider()
    if st.button("🔄 Khôi phục danh sách mặc định", use_container_width=True):
        st.session_state.players = [
            "Nguyễn Văn A", "Trần Thị B", "Lê Văn C", 
            "Phạm Thị D", "Hoàng Văn E", "Vũ Thị F"
        ]
        st.session_state.winner = None
        st.rerun()

# CSS hiển thị bể cá và hiệu ứng bơi lội
def render_ocean(players):
    fish_html = ""
    colors = ["#ff7b00", "#ff0055", "#00b4d8", "#70e000", "#9d4edd", "#ffb703"]
    
    for i, name in enumerate(players):
        top_pos = random.randint(15, 75)
        duration = random.randint(5, 10)
        delay = random.uniform(0, 3)
        color = colors[i % len(colors)]
        
        fish_html += f"""
        <div class="fish" style="
            top: {top_pos}%;
            animation-duration: {duration}s;
            animation-delay: -{delay}s;
            background-color: {color};
        ">
            🐟 {name}
        </div>
        """

    css = f"""
    <style>
        .ocean {{
            position: relative;
            width: 100%;
            height: 320px;
            background: linear-gradient(180deg, #0077be 0%, #002b49 100%);
            border-radius: 15px;
            border: 3px solid #00ffff;
            overflow: hidden;
            box-shadow: 0 0 15px rgba(0,255,255,0.4);
            margin-bottom: 20px;
        }}
        .fish {{
            position: absolute;
            padding: 6px 14px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 14px;
            white-space: nowrap;
            border: 1px solid rgba(255,255,255,0.8);
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            animation: swim linear infinite;
        }}
        @keyframes swim {{
            0% {{ left: -20%; transform: scaleX(1); }}
            49% {{ transform: scaleX(1); }}
            50% {{ left: 105%; transform: scaleX(-1); }}
            99% {{ transform: scaleX(-1); }}
            100% {{ left: -20%; transform: scaleX(1); }}
        }}
    </style>
    <div class="ocean">
        {fish_html}
    </div>
    """
    st.markdown(css, unsafe_allow_html=True)

# Hiển thị bể cá
render_ocean(st.session_state.players)

# Nút thả câu
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    start_btn = st.button("🎣 BẮT ĐẦU CÂU CÁ!", use_container_width=True, type="primary")

# Xử lý logic câu cá
if start_btn:
    if len(st.session_state.players) == 0:
        st.error("Danh sách người chơi đang trống! Vui lòng thêm người ở thanh bên.")
    else:
        # Hiệu ứng chờ câu
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        status_text.text("🌊 Đang thả cần câu xuống biển...")
        for percent in range(1, 101):
            time.sleep(0.02)
            progress_bar.progress(percent)
            if percent == 40:
                status_text.text("🐠 Các chú cá đang cắn câu...")
            elif percent == 80:
                status_text.text("🪝 Đã dính câu! Đang kéo lên...")

        status_text.empty()
        progress_bar.empty()

        # Chọn người may mắn
        winner = random.choice(st.session_state.players)
        st.session_state.winner = winner
        
        # Hiệu ứng pháo hoa mừng kết quả
        st.balloons()

# Hiển thị kết quả
if st.session_state.winner:
    st.success(f"🎉 **CHÚC MỪNG MẶT HÀNG MAY MẮN: {st.session_state.winner.upper()}!** 🎉")
      
