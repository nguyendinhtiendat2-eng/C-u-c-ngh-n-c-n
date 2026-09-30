import time
import random
import streamlit as st

st.set_page_config(
    page_title="Trò Chơi Câu Tên May Mắn", page_icon="🎣", layout="centered"
)

st.title("🎣 Minigame: Câu Tên May Mắn 🐟")
st.write(
    "Nhập danh sách tên của bạn vào hồ, thả cần câu và xem bạn sẽ 'câu' được tên ai lên đầu tiên nhé!"
)

# Khởi tạo Session State
if "fishing_status" not in st.session_state:
    st.session_state.fishing_status = "idle"  # idle, waiting, biting
if "bite_time" not in st.session_state:
    st.session_state.bite_time = 0
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("---")

# Ô nhập danh sách tên
default_names = "An\nBình\nCường\nDung\nHoàng\nLan\nMinh\nPhương"
names_input = st.text_area(
    "Nhập danh sách tên có trong hồ (mỗi tên một dòng):",
    value=default_names,
    height=100,
)

# Xử lý danh sách tên từ text area
names_list = [n.strip() for n in names_input.split("\n") if n.strip()]

st.markdown("### 🌊 Khu Vực Hồ Câu")

col1, col2 = st.columns(2)
with col1:
    throw_btn = st.button("🎣 Thả Cần Câu")
with col2:
    pull_btn = st.button("⚡ KÉO CẦN LÊN NGAY!")

message_area = st.empty()

# Logic thả cần
if throw_btn:
    if len(names_list) < 1:
        st.warning("Vui lòng nhập ít nhất 1 tên vào hồ câu!")
    elif st.session_state.fishing_status == "idle":
        st.session_state.fishing_status = "waiting"
        # Thời gian chờ cá cắn ngẫu nhiên từ 1 đến 2.5 giây
        st.session_state.bite_time = time.time() + random.uniform(1.0, 2.5)
        st.rerun()

# Kiểm tra trạng thái chờ
if st.session_state.fishing_status == "waiting":
    if time.time() >= st.session_state.bite_time:
        st.session_state.fishing_status = "biting"
        st.rerun()
    else:
        message_area.info("⏳ Phao đang bập bềnh... Chờ cá cắn câu...")
        time.sleep(0.3)
        st.rerun()
elif st.session_state.fishing_status == "biting":
    message_area.warning(
        "🚨 **CÓ CON CÁ MANG TÊN CẮN CÂU RỒI! BẤM 'KÉO CẦN LÊN NGAY' NHANH TAY!**"
    )

# Logic kéo cần
if pull_btn:
    if st.session_state.fishing_status == "biting":
        # Chọn ngẫu nhiên 1 tên từ danh sách
        caught_name = random.choice(names_list)
        st.session_state.fishing_status = "idle"
        st.session_state.history.insert(0, caught_name)

        message_area.success(
            f"🎉 **CÂU THÀNH CÔNG!** Bạn đã câu được chú cá mang tên: **{caught_name}** 🐟✨"
        )
        st.rerun()
    elif st.session_state.fishing_status == "waiting":
        st.session_state.fishing_status = "idle"
        message_area.error(
            "❌ Bạn kéo quá sớm! Cá chưa kịp cắn đã sợ chạy mất tiêu."
        )
        st.rerun()
    else:
        message_area.info("⚠️️ Bạn chưa thả cần câu xuống hồ mà!")

# Hiển thị lịch sử các tên đã câu được
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Lịch Sử Câu Được")
    for idx, name in enumerate(st.session_state.history[:5], 1):
        st.write(f"{idx}. 🐟 **{name}**")

    if st.button("🗑️ Xóa lịch sử"):
        st.session_state.history = []
        st.rerun()
  
