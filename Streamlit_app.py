import random
import time
import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Game Câu Cá", page_icon="🎣")

# 1. KHỞI TẠO DỮ LIỆU
if "player_name" not in st.session_state:
    st.session_state.player_name = "Cần thủ Tiến Đạt"
if "score" not in st.session_state:
    st.session_state.score = 0
if "logs" not in st.session_state:
    st.session_state.logs = []

st.title("🎣 Game Câu Cá Streamlit")

# 2. BẢNG NHẬP TÊN VÀ ÂM THANH (Ở SIDEBAR)
with st.sidebar:
    st.header("⚙️ Cấu Hình Game")

    # Bảng nhập tên người chơi
    new_name = st.text_input(
        "Tên người chơi:", value=st.session_state.player_name
    )
    if new_name:
        st.session_state.player_name = new_name

    st.divider()

    # Nhạc nền: Hỗ trợ dán đường link MP3 trực tuyến hoặc mở file ngoài
    st.subheader("🎵 Nhạc Nền")
    audio_url = st.text_input(
        "Link nhạc MP3 từ bên ngoài:",
        value="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    )
    if audio_url:
        st.audio(audio_url, format="audio/mp3")

    st.divider()
    if st.button("🔄 Chơi Lại Từ Đầu"):
        st.session_state.score = 0
        st.session_state.logs = []

# 3. GIAO DIỆN CHÍNH
st.write(f"👋 Chào mừng cần thủ: **{st.session_state.player_name}**")
st.metric(label="🏆 Điểm số", value=f"{st.session_state.score} điểm")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Khu vực câu cá")

    # Nút bấm thả câu
    if st.button("🎯 THẢ LƯỠI CÂU", type="primary", use_container_width=True):
        with st.spinner("Đang chờ cá cắn mồi... 🌊"):
            time.sleep(1.5)

        # Tính kết quả ngẫu nhiên
        outcome = random.choice(["fish", "junk", "nothing"])

        if outcome == "fish":
            fish, pts = random.choice(
                [
                    ("Cá Rô Phi", 5),
                    ("Cá Chép Vàng", 10),
                    ("Cá Mập Cảnh", 25),
                ]
            )
            st.session_state.score += pts
            log_item = f"🎉 {st.session_state.player_name} bắt được {fish} (+{pts}đ)"
            st.session_state.logs.insert(0, log_item)
            st.success(log_item)

        elif outcome == "junk":
            log_item = (
                f"👞 {st.session_state.player_name} câu phải một chiếc giày cũ!"
            )
            st.session_state.logs.insert(0, log_item)
            st.error(log_item)

        else:
            log_item = "🌊 Cá ăn mất mồi rồi bơi đi..."
            st.session_state.logs.insert(0, log_item)
            st.info(log_item)

with col2:
    st.subheader("📜 Nhật Ký")
    if not st.session_state.logs:
        st.write("Chưa có lịch sử.")
    for item in st.session_state.logs[:5]:
        st.write(f"- {item}")
      
