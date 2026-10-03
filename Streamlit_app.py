import time
import random
import streamlit as st

st.set_page_config(page_title="Đua Vịt Câu Cá", page_icon="🦆", layout="centered")

# CSS tuỳ chỉnh giao diện đường đua và hiệu ứng
st.markdown(
    """
    <style>
    .stButton button {
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        padding: 15px;
    }
    .track-container {
        background: linear-gradient(to bottom, #81d4fa 0%, #0288d1 100%);
        padding: 20px;
        border-radius: 15px;
        border: 3px solid #004d40;
        margin-bottom: 20px;
    }
    .lane {
        font-size: 28px;
        padding: 10px 0;
        border-bottom: 2px dashed rgba(255, 255, 255, 0.4);
        white-space: nowrap;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🦆 ĐUA VỊT KẾT HỢP CÂU CÁ 🎣")
st.write(
    "Cuộc đua giữa 2 chú vịt! Ai về đích trước sẽ là mục tiêu cho chiếc lưỡi câu may mắn."
)

# Khởi tạo trạng thái game
if "race_started" not in st.session_state:
    st.session_state.race_started = False
if "pos1" not in st.session_state:
    st.session_state.pos1 = 0
if "pos2" not in st.session_state:
    st.session_state.pos2 = 0
if "winner" not in st.session_state:
    st.session_state.winner = None
if "hook_stage" not in st.session_state:
    st.session_state.hook_stage = 0  # 0: Chưa thả, 1: Đang thả, 2: Đã câu lên


def reset_game():
    st.session_state.race_started = False
    st.session_state.pos1 = 0
    st.session_state.pos2 = 0
    st.session_state.winner = None
    st.session_state.hook_stage = 0


# Khu vực điều khiển
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)

with col_ctrl1:
    if st.button("🚀 Bắt Đầu Đua!", type="primary"):
        reset_game()
        st.session_state.race_started = True

with col_ctrl2:
    if st.button("🔄 Chơi Lại"):
        reset_game()
        st.rerun()

# Độ dài đường đua (tính bằng số bước)
track_length = 30

# Hiển thị đường đua
st.markdown("### 🏁 Đường Đua")

track_html = f"""
<div class="track-container">
    <div class="lane">
        P1 (Vịt Vàng): {"-" * st.session_state.pos1}🦆{'-' * max(0, track_length - st.session_state.pos1)} 🏁
    </div>
    <div class="lane">
        P2 (Vịt Trắng): {"-" * st.session_state.pos2}🐥{'-' * max(0, track_length - st.session_state.pos2)} 🏁
    </div>
</div>
"""
track_slot = st.empty()
track_slot.markdown(track_html, unsafe_allow_html=True)

# Thông báo kết quả / trạng thái
status_slot = st.empty()

# Vòng lặp mô phỏng cuộc đua khi bấm Bắt Đầu
if st.session_state.race_started and st.session_state.winner is None:
    progress_bar = st.progress(0)

    while (
        st.session_state.pos1 < track_length
        and st.session_state.pos2 < track_length
    ):
        # Tiến ngẫu nhiên mỗi lượt
        st.session_state.pos1 += random.randint(1, 3)
        st.session_state.pos2 += random.randint(1, 3)

        # Giới hạn không vượt quá đích
        if st.session_state.pos1 > track_length:
            st.session_state.pos1 = track_length
        if st.session_state.pos2 > track_length:
            st.session_state.pos2 = track_length

        # Cập nhật giao diện đường đua
        track_html = f"""
        <div class="track-container">
            <div class="lane">
                P1 (Vịt Vàng): {"-" * st.session_state.pos1}🦆{'-' * max(0, track_length - st.session_state.pos1)} 🏁
            </div>
            <div class="lane">
                P2 (Vịt Trắng): {"-" * st.session_state.pos2}🐥{'-' * max(0, track_length - st.session_state.pos2)} 🏁
            </div>
        </div>
        """
        track_slot.markdown(track_html, unsafe_allow_html=True)
        time.sleep(0.1)

    # Xác định người thắng
    if (
        st.session_state.pos1 >= track_length
        and st.session_state.pos2 >= track_length
    ):
        st.session_state.winner = random.choice([1, 2])  # Hòa thì random
    elif st.session_state.pos1 >= track_length:
        st.session_state.winner = 1
    else:
        st.session_state.winner = 2

    st.rerun()

# Xử lý hiệu ứng câu cá sau khi có người về đích
if st.session_state.winner is not None:
    winner_name = (
        "P1 (Vịt Vàng 🦆)"
        if st.session_state.winner == 1
        else "P2 (Vịt Trắng 🐥)"
    )
    status_slot.markdown(
        f"### 🎉 {winner_name} đã về đích đầu tiên! Chuẩn bị thả lưỡi câu..."
    )
    time.sleep(1)

    status_slot.markdown(
        f"### 🪝 Đang thả lưỡi câu từ trên trời xuống để tóm gọn {winner_name}..."
    )
    time.sleep(1.5)

    status_slot.markdown(
        f"### 🎣 **ĐÃ CÂU THÀNH CÔNG!** Chúc mừng {winner_name} là nhà vô địch tuyệt đối!"
    )

<FollowUp label="Want me to add manual keyboard controls for 2 players in Streamlit?" query="How can I add manual keyboard controls for two players in a Streamlit app to race ducks in real-time?" />
      
