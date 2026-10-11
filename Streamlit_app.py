import random
import time
import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Game Câu Cá Emoji",
    page_icon="🎣",
    layout="centered",
)

# --- KHỞI TẠO SESSION STATE ---
if "participants" not in st.session_state:
    st.session_state.participants = [
        "Nguyễn Văn A",
        "Trần Thị B",
        "Lê Văn C",
        "Phạm Thị D",
        "Hoàng Văn E",
    ]

if "history" not in st.session_state:
    st.session_state.history = []

if "hooked_person" not in st.session_state:
    st.session_state.hooked_person = None

if "fishing" not in st.session_state:
    st.session_state.fishing = False

# --- TIÊU ĐỀ ---
st.title("🎣 Game Câu Cá May Mắn")
st.write("---")

# --- PHẦN 1: TRÊN BỜ - NGƯỜI CÂU CÁ ---
st.subheader("🌿 Trên Bờ")
col_fisher_1, col_fisher_2 = st.columns([1, 2])

with col_fisher_1:
    # Biểu tượng icon người câu cá đơn giản
    st.markdown(
        "<h1 style='text-align: center; font-size: 3.5rem; margin: 0;'>👴🎣</h1>",
        unsafe_allow_html=True,
    )

with col_fisher_2:
    st.write(f"Số lượng cá dưới hồ: **{len(st.session_state.participants)}** con")
    remove_after_catch = st.checkbox(
        "Bắt xong thả ra ngoài (Xóa khỏi hồ)", value=True
    )

    if st.button("🎣 Quăng Cần Câu!", type="primary"):
        if not st.session_state.participants:
            st.warning("Hồ đã hết cá! Vui lòng thêm tên ở thanh bên trái (Sidebar).")
        else:
            st.session_state.fishing = True
            st.session_state.hooked_person = None
            st.rerun()

# Xử lý hiệu ứng câu cá
if st.session_state.fishing:
    with st.spinner("🌊 Đang thả mồi... Cá đang cắn câu..."):
        time.sleep(1.2)

    chosen = random.choice(st.session_state.participants)
    st.session_state.hooked_person = chosen
    st.session_state.fishing = False
    st.session_state.history.insert(0, chosen)

    if remove_after_catch:
        st.session_state.participants.remove(chosen)
    st.rerun()

# Hiển thị kết quả khi câu được
if st.session_state.hooked_person:
    st.success(f"🎉 Cắn câu! Đã kéo lên bờ: **{st.session_state.hooked_person}** 🐟")
    st.balloons()
    st.session_state.hooked_person = None

st.write("---")

# --- PHẦN 2: DƯỚI NƯỚC - NHỮNG CHÚ CÁ CHỨA TÊN ---
st.subheader("🌊 Dưới Nước (Hồ Cá)")

if st.session_state.participants:
    # Hiển thị danh sách các con cá dạng icon mộc mạc, rõ ràng
    fish_display = " &nbsp; &nbsp; ".join(
        [f"🐟 **{p}**" for p in st.session_state.participants]
    )
    st.markdown(
        f"<div style='font-size: 1.2rem; padding: 10px; background-color: #e0f2fe; border-radius: 10px; color: #0369a1;'>{fish_display}</div>",
        unsafe_allow_html=True,
    )
else:
    st.info("Hồ nước hiện đang trống rỗng!")

st.write("---")

# --- LỊCH SỬ CÂU ---
st.subheader("📋 Lịch sử đã câu lên bờ")
if st.session_state.history:
    for idx, person in enumerate(st.session_state.history[:10]):
        st.write(f"{idx + 1}. 🐟 **{person}**")
    if st.button("🗑️ Xóa lịch sử"):
        st.session_state.history = []
        st.rerun()
else:
    st.write("Chưa có ai được câu lên.")

# --- SIDEBAR: QUẢN LÝ DANH SÁCH ---
with st.sidebar:
    st.header("⚙️ Cài đặt danh sách")
    bulk_input = st.text_area(
        "Nhập tên (mỗi người một dòng):",
        value="\n".join(st.session_state.participants),
        height=300,
    )
    if st.button("Cập nhật danh sách cá"):
        names = [n.strip() for n in bulk_input.split("\n") if n.strip()]
        if names:
            st.session_state.participants = names
            st.success("Đã cập nhật thành công!")
            st.rerun()
        else:
            st.error("Không được để trống danh sách.")
  
