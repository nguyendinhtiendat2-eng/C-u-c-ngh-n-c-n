import random
import time
import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Hồ Câu May Mắn",
    page_icon="🎣",
    layout="centered",
)

# --- CSS TÙY CHỈNH MÀU SẮC DỊU MẮT & KHÔNG BỊ LÓA ---
st.markdown(
    """
<style>
    .stApp {
        background-color: #0f172a; /* Nền tối sang trọng, không bị chói mắt */
        color: #f8fafc;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
    }
    .fish-box {
        background-color: #1e293b;
        border: 2px solid #38bdf8;
        border-radius: 12px;
        padding: 10px 15px;
        margin: 5px;
        text-align: center;
        display: inline-block;
        font-weight: bold;
        color: #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
</style>
""",
    unsafe_allow_html=True,
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
st.markdown(
    "<h1 style='text-align: center;'>🎣 HỒ CÂU MAY MẮN 🎣</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #94a3b8;'>Trò chơi bốc thăm ngẫu nhiên phong cách câu cá</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- BỐ CỤC CHÍNH ---
col_control, col_history = st.columns([2, 1])

with col_control:
    st.subheader("👴 Người Câu & Thao Tác")
    st.info(f"🐟 Số lượng cá (người) trong hồ: **{len(st.session_state.participants)}**")

    remove_after_catch = st.checkbox(
        "Loại bỏ người chơi sau khi câu lên", value=True
    )

    if st.button(
        "🎣 Quăng Cần Câu Ngay!", type="primary", use_container_width=True
    ):
        if not st.session_state.participants:
            st.warning("Hồ đã cạn cá! Vui lòng thêm người ở Sidebar.")
        else:
            st.session_state.fishing = True
            st.session_state.hooked_person = None
            st.rerun()

    # Xử lý hiệu ứng câu cá
    if st.session_state.fishing:
        with st.spinner("🌊 Đang thả mồi... Chờ cá cắn câu..."):
            time.sleep(1.5)

        chosen = random.choice(st.session_state.participants)
        st.session_state.hooked_person = chosen
        st.session_state.fishing = False
        st.session_state.history.insert(0, chosen)

        if remove_after_catch:
            st.session_state.participants.remove(chosen)

        st.rerun()

    # Hiển thị kết quả bắt được
    if st.session_state.hooked_person:
        st.success(
            f"🎉 Chúc mừng! Bạn đã câu được: **{st.session_state.hooked_person}** 🐟"
        )
        st.balloons()
        st.session_state.hooked_person = None

with col_history:
    st.subheader("📋 Lịch sử")
    if st.session_state.history:
        for idx, person in enumerate(st.session_state.history[:10]):
            st.write(f"{idx + 1}. **{person}**")
        if st.button("🗑️ Xóa lịch sử"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("Chưa có ai cắn câu.")

# --- KHU VỰC HIỂN THỊ HỒ CÁ ---
st.markdown("---")
st.subheader("🌊 Hồ Nước (Danh sách các chú cá đang bơi)")

if st.session_state.participants:
    # Tạo các thẻ cá hiển thị trực quan không bị lỗi code HTML
    fish_html = ""
    for person in st.session_state.participants:
        fish_html += f'<div class="fish-box">🐟 {person}</div>'
    st.markdown(fish_html, unsafe_allow_html=True)
else:
    st.warning("Hồ đang trống rỗng! Hãy thêm tên người chơi vào ở phần Cài đặt.")

# --- THANH BÊN (SIDEBAR) QUẢN LÝ ---
with st.sidebar:
    st.header("⚙️ Quản lý danh sách")

    bulk_input = st.text_area(
        "Nhập danh sách (mỗi người một dòng):",
        value="\n".join(st.session_state.participants),
        height=300,
    )

    if st.button("🔄 Cập nhật Hồ Cá", use_container_width=True):
        names = [n.strip() for n in bulk_input.split("\n") if n.strip()]
        if names:
            st.session_state.participants = names
            st.success("Đã cập nhật danh sách thành công!")
            st.rerun()
        else:
            st.error("Danh sách không được để trống.")
          
