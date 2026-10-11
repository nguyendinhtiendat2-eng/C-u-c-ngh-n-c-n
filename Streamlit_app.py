import random
import time
import streamlit as st

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(
    page_title="Hồ Câu Cá May Mắn",
    page_icon="🎣",
    layout="wide",
)

# --- CSS TÙY CHỈNH HIỆU ỨNG HỒ CÁ & CÁC CHÚ CÁ ---
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(to bottom, #1e3a8a, #0f172a);
        color: #ffffff;
    }
    
    /* Khung hồ cá phong cách hoạt hình */
    .lake-box {
        background: linear-gradient(180deg, #0284c7 0%, #0369a1 100%);
        border: 4px solid #38bdf8;
        border-radius: 20px;
        padding: 25px;
        min-height: 380px;
        box-shadow: inset 0 10px 20px rgba(0,0,0,0.4);
        position: relative;
    }

    /* Thẻ chứa tên từng chú cá trong hồ */
    .fish-item {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        border: 2px dashed #bae6fd;
        backdrop-filter: blur(5px);
        padding: 10px 18px;
        margin: 8px;
        border-radius: 30px;
        font-weight: bold;
        font-size: 1.1rem;
        color: #e0f2fe;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .fish-item:hover {
        transform: scale(1.08);
        background: rgba(255, 255, 255, 0.3);
    }

    /* Khu vực người câu / thuyền câu */
    .fisherman-panel {
        background: rgba(30, 41, 59, 0.7);
        border: 2px solid #475569;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
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
        "Linh",
        "Long",
    ]

if "history" not in st.session_state:
    st.session_state.history = []

if "hooked_person" not in st.session_state:
    st.session_state.hooked_person = None

if "fishing" not in st.session_state:
    st.session_state.fishing = False

# --- TIÊU ĐỀ TRÒ CHƠI ---
st.markdown(
    "<h1 style='text-align: center; color: #38bdf8;'>🎣 HỒ CÂU CÁ MAY MẮN 🎣</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #94a3b8;'>Trò chơi chọn người ngẫu nhiên mô phỏng hoạt cảnh câu cá</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- BỐC CỤC CHÍNH: CỘT ĐIỀU KHIỂN & CỘT LỊCH SỬ ---
col_main, col_sidebar_history = st.columns([3, 1])

with col_main:
    # Chia nhỏ màn hình game thành: Ông câu cá (bên trái) và Hồ cá bơi lội (bên phải)
    col_fisher, col_lake = st.columns([1, 2])

    with col_fisher:
        st.markdown('<div class="fisherman-panel">', unsafe_allow_html=True)
        st.markdown("### 👴 Người Câu")
        st.markdown(
            "<h1 style='font-size: 4rem; margin: 0;'>🎣</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"Số cá trong hồ: **{len(st.session_state.participants)}** con"
        )

        remove_after_catch = st.checkbox(
            "Bắt xong thả ra ngoài",
            value=True,
            help="Loại bỏ người chơi đã câu được khỏi hồ",
        )

        if st.button(
            "🎣 QUĂNG CẦN CÂU!", type="primary", use_container_width=True
        ):
            if not st.session_state.participants:
                st.warning("Hồ đã cạn cá! Vui lòng thêm người chơi ở Sidebar.")
            else:
                st.session_state.fishing = True
                st.session_state.hooked_person = None
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Xử lý hiệu ứng câu cá
        if st.session_state.fishing:
            with st.spinner("🌊 Đang thả mồi... Cần câu đang rung..."):
                time.sleep(1.8)  # Tạo độ hồi hộp

            chosen = random.choice(st.session_state.participants)
            st.session_state.hooked_person = chosen
            st.session_state.fishing = False
            st.session_state.history.insert(0, chosen)

            if remove_after_catch:
                st.session_state.participants.remove(chosen)
            st.rerun()

        # Hiển thị kết quả câu được
        if st.session_state.hooked_person:
            st.success(
                f"🎉 Cắn câu rồi! Chúc mừng **{st.session_state.hooked_person}** đã được kéo lên! 🐟"
            )
            st.balloons()
            st.session_state.hooked_person = None

    with col_lake:
        st.markdown('<div class="lake-box">', unsafe_allow_html=True)
        st.markdown(
            "<h3 style='text-align: center; color: #bae6fd; margin-top: 0;'>🌊 Hồ Nước Sâu (Các Chú Cá Đang Bơi) 🌊</h3>",
            unsafe_allow_html=True,
        )

        if st.session_state.participants:
            fish_container_html = "<div style='text-align: center; padding-top: 10px;'>"
            for person in st.session_state.participants:
                fish_container_html += (
                    f'<div class="fish-item">🐟 {person}</div>'
                )
            fish_container_html += "</div>"
            st.markdown(fish_container_html, unsafe_allow_html=True)
        else:
            st.markdown(
                "<h3 style='text-align: center; color: #f87171; margin-top: 50px;'>Hồ trống không! Không còn con cá nào.</h3>",
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

with col_sidebar_history:
    st.markdown("### 📋 Lịch Sử Câu")
    if st.session_state.history:
        for idx, person in enumerate(st.session_state.history[:10]):
            st.write(f"{idx + 1}. **{person}**")
        if st.button("🗑️ Xóa lịch sử", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("Chưa có ai bị câu lên.")

# --- THANH CÀI ĐẶT DANH SÁCH Ở SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Quản lý Hồ Cá")
    bulk_input = st.text_area(
        "Danh sách người chơi (mỗi dòng 1 tên):",
        value="\n".join(st.session_state.participants),
        height=320,
    )
    if st.button("🔄 Cập nhật danh sách cá", use_container_width=True):
        names = [n.strip() for n in bulk_input.split("\n") if n.strip()]
        if names:
            st.session_state.participants = names
            st.success("Đã cập nhật hồ cá thành công!")
            st.rerun()
        else:
            st.error("Danh sách không được để trống.")
              
