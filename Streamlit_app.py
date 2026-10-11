import random
import time
import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Game Câu Cá May Mắn",
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

if "current_catch" not in st.session_state:
    st.session_state.current_catch = None

if "game_state" not in st.session_state:
    st.session_state.game_state = "IDLE"  # IDLE, FISHING, CAUGHT

# --- TIÊU ĐỀ ---
st.title("🎣 Game Câu Cá May Mắn")
st.write("---")

# --- HIỂN THỊ KHU VỰC TRÊN BỜ (NGƯỜI CÂU) & DƯỚI NƯỚC (HỒ CÁ) ---
st.subheader("🌿 Trên Bờ & Dưới Sông")

col1, col2 = st.columns([1, 2])

with col1:
    # Biểu tượng ông câu cá thay đổi trạng thái
    if st.session_state.game_state == "FISHING":
        st.markdown(
            "<h1 style='text-align: center; font-size: 3.5rem; margin: 0;'>👴🎣⬇️</h1>",
            unsafe_allow_html=True,
        )
        st.caption("Đang thả mồi xuống nước...")
    else:
        st.markdown(
            "<h1 style='text-align: center; font-size: 3.5rem; margin: 0;'>👴🎣</h1>",
            unsafe_allow_html=True,
        )
        st.caption("Sẵn sàng quăng cần")

with col2:
    st.write(f"Số lượng cá trong hồ: **{len(st.session_state.participants)}** con")
    remove_after_catch = st.checkbox(
        "Bắt xong thả ra ngoài (Xóa khỏi hồ)", value=True
    )

    # Nút quăng cần
    if st.session_state.game_state != "FISHING":
        if st.button(
            "🎣 Quăng Cần Câu Xuống Nước!",
            type="primary",
            use_container_width=True,
        ):
            if not st.session_state.participants:
                st.warning(
                    "Hồ đã hết cá! Vui lòng thêm tên ở thanh bên trái (Sidebar)."
                )
            else:
                st.session_state.game_state = "FISHING"
                st.session_state.current_catch = None
                st.rerun()

# --- XỬ LÝ QUÁ TRÌNH CÂU CÁ (QUĂNG CẦN -> CÁ BƠI TỚI -> HIỆN THỊ) ---
if st.session_state.game_state == "FISHING":
    st.write("---")
    # Hiển thị mô phỏng con cá đang bơi tới
    st.markdown(
        "<h3 style='text-align: center; color: #0284c7;'>🌊 🐟💨 Có một con cá đang bơi tới cắn câu...</h3>",
        unsafe_allow_html=True,
    )

    # Thời gian chờ tạo cảm giác cá bơi tới
    time.sleep(1.5)

    # Chọn ngẫu nhiên một người
    chosen = random.choice(st.session_state.participants)
    st.session_state.current_catch = chosen
    st.session_state.history.insert(0, chosen)

    if remove_after_catch:
        st.session_state.participants.remove(chosen)

    st.session_state.game_state = "CAUGHT"
    st.rerun()

# --- HIỂN THỊ TOÀN BỘ KẾT QUẢ KHI CÁ CẮN CÂU ĐƯỢC KÉO LÊN ---
if st.session_state.game_state == "CAUGHT":
    st.write("---")
    st.success("🎉 CẮN CÂU RỒI! ĐÃ KÉO LÊN BỜ THÀNH CÔNG! 🎉")

    # Hiển thị nổi bật con cá chứa tên người chơi vừa bơi tới
    st.markdown(
        f"""
        <div style='text-align: center; padding: 20px; background-color: #e0f2fe; border: 3px dashed #0284c7; border-radius: 15px;'>
            <h1 style='color: #0369a1; margin: 0;'>🐟 {st.session_state.current_catch} 🐟</h1>
            <p style='color: #334155; margin-top: 10px; font-weight: bold;'>Là người chơi may mắn được câu lên!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.balloons()

    if st.button("🔄 Tiếp tục câu lượt mới", use_container_width=True):
        st.session_state.game_state = "IDLE"
        st.session_state.current_catch = None
        st.rerun()

st.write("---")

# --- HIỂN THỊ DANH SÁCH CÁ CÒN LẠI DƯỚI HỒ ---
st.subheader("🌊 Hồ Nước Hiện Tại")
if st.session_state.participants:
    fish_display = " &nbsp; &nbsp; ".join(
        [f"🐟 {p}" for p in st.session_state.participants]
    )
    st.markdown(
        f"<div style='font-size: 1.1rem; padding: 10px; background-color: #f8fafc; border-radius: 10px; border: 1px solid #cbd5e1;'>{fish_display}</div>",
        unsafe_allow_html=True,
    )
else:
    st.info("Hồ nước hiện tại đã trống rỗng!")

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
