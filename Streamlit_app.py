import random
import time
import streamlit as st

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(
    page_title="Hồ Câu Cá May Mắn",
    page_icon="🎣",
    layout="wide",
)

# --- CSS TÙY CHỈNH GIAO DIỆN HỒ CÁ VÀ CHÚ CÁ ---
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(to bottom, #0f172a, #1e3a8a);
        color: #ffffff;
    }
    
    /* Khung hồ nước */
    .lake-container {
        background: linear-gradient(180deg, #0284c7 0%, #0369a1 100%);
        border: 4px solid #38bdf8;
        border-radius: 20px;
        padding: 20px;
        min-height: 400px;
        box-shadow: inset 0 10px 25px rgba(0,0,0,0.5);
    }

    /* Thẻ chú cá chứa tên (Giao diện thẻ cá trực quan) */
    .fish-card {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #0284c7;
        padding: 8px 15px;
        margin: 8px;
        border-radius: 30px;
        font-weight: bold;
        color: #0f172a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    
    .fish-card:hover {
        transform: scale(1.1);
        background: #ffffff;
    }

    /* Khung người câu */
    .fisherman-box {
        background: rgba(30, 41, 59, 0.8);
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
    ]

if "history" not in st.session_state:
    st.session_state.history = []

if "hooked_person" not in st.session_state:
    st.session_state.hooked_person = None

if "fishing" not in st.session_state:
    st.session_state.fishing = False

# --- TIÊU ĐỀ ---
st.markdown(
    "<h1 style='text-align: center; color: #38bdf8;'>🎣 HỒ CÂU CÁ MAY MẮN 🎣</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- BỐ CỤC CHÍNH ---
col_game, col_history = st.columns([3, 1])

with col_game:
    col_fisher, col_lake = st.columns([1, 2])

    # 1. Khu vực Người câu
    with col_fisher:
        st.markdown('<div class="fisherman-box">', unsafe_allow_html=True)
        st.markdown("### 🧑‍✈️ Người Câu")
        # Hiển thị icon hình người câu cá trực quan
        st.markdown(
            "<h1 style='font-size: 4rem; margin: 0;'>🎣</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"Số cá trong hồ: **{len(st.session_state.participants)}**"
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
            with st.spinner("🌊 Đang thả mồi... Cá đang cắn câu..."):
                time.sleep(1.5)

            chosen = random.choice(st.session_state.participants)
            st.session_state.hooked_person = chosen
            st.session_state.fishing = False
            st.session_state.history.insert(0, chosen)

            if remove_after_catch:
                st.session_state.participants.remove(chosen)
            st.rerun()

        # Hiển thị kết quả khi câu được
        if st.session_state.hooked_person:
            st.success(
                f"🎉 Thành công! Đã câu được: **{st.session_state.hooked_person}**! 🐟"
            )
            st.balloons()
            st.session_state.hooked_person = None

    # 2. Khu vực Hồ nước chứa các chú cá
    with col_lake:
        st.markdown('<div class="lake-container">', unsafe_allow_html=True)
        st.markdown(
            "<h3 style='text-align: center; color: #bae6fd; margin-top: 0;'>🌊 HỒ NƯỚC (CÁC CHÚ CÁ ĐANG BƠI) 🌊</h3>",
            unsafe_allow_html=True,
        )

        if st.session_state.participants:
            # Tạo danh sách các chú cá hiển thị trực quan kèm icon con cá 🐟
            fish_html = "<div style='text-align: center; padding-top: 15px;'>"
            for person in st.session_state.participants:
                fish_html += f'<div class="fish-card">🐟 &nbsp; {person}</div>'
            fish_html += "</div>"
            st.markdown(fish_html, unsafe_allow_html=True)
        else:
            st.markdown(
                "<h3 style='text-align: center; color: #f87171; margin-top: 80px;'>Hồ trống không! Không còn chú cá nào.</h3>",
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

# 3. Cột lịch sử bên phải
with col_history:
    st.markdown("### 📋 Lịch Sử Câu")
    if st.session_state.history:
        for idx, person in enumerate(st.session_state.history[:10]):
            st.write(f"{idx + 1}. **{person}**")
        if st.button("🗑️ Xóa lịch sử", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("Chưa có ai bị câu lên.")

# --- SIDEBAR QUẢN LÝ ---
with st.sidebar:
    st.header("⚙️ Cài đặt danh sách")
    bulk_input = st.text_area(
        "Nhập danh sách (mỗi dòng một tên):",
        value="\n".join(st.session_state.participants),
        height=320,
    )
    if st.button("🔄 Cập nhật Hồ Cá", use_container_width=True):
        names = [n.strip() for n in bulk_input.split("\n") if n.strip()]
        if names:
            st.session_state.participants = names
            st.success("Đã cập nhật hồ cá thành công!")
            st.rerun()
        else:
            st.error("Danh sách không được để trống.")
  
