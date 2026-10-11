import random
import time
import streamlit as st

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(
    page_title="Hồ Câu Cá May Mắn",
    page_icon="🎣",
    layout="wide",
)

# --- CSS TÙY CHỈNH BỐ CỤC: TRÊN BỜ (NGƯỜI CÂU) & DƯỚI NƯỚC (CÁ BƠI) ---
st.markdown(
    """
<style>
    .stApp {
        background: #0f172a;
        color: #ffffff;
    }
    
    /* --- KHU VỰC TRÊN BỜ (BỜ SÔNG) --- */
    .bank-container {
        background: linear-gradient(180deg, #15803d 0%, #166534 100%); /* Màu cỏ/bờ đất */
        border: 4px solid #22c55e;
        border-radius: 20px 20px 0 0;
        padding: 20px;
        text-align: center;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.3);
    }
    
    .fisherman-avatar {
        font-size: 4rem;
        margin: 0;
        animation: bounce 2s infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    /* --- KHU VỰC DƯỚI NƯỚC (HỒ NƯỚC) --- */
    .river-container {
        background: linear-gradient(180deg, #0284c7 0%, #0369a1 100%); /* Màu nước sông sâu */
        border: 4px solid #38bdf8;
        border-top: none;
        border-radius: 0 0 20px 20px;
        padding: 30px 20px;
        min-height: 320px;
        box-shadow: inset 0 10px 20px rgba(0,0,0,0.5);
        position: relative;
    }

    /* Hiệu ứng chú cá tung tăng bơi lội */
    .swimming-fish {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #0284c7;
        padding: 10px 18px;
        margin: 10px;
        border-radius: 30px;
        font-weight: bold;
        color: #0f172a;
        font-size: 1.1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        animation: swim 3s ease-in-out infinite alternate;
        transition: transform 0.2s;
    }

    .swimming-fish:hover {
        transform: scale(1.15);
        background: #ffffff;
    }

    @keyframes swim {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-6px) rotate(2deg); }
        100% { transform: translateY(4px) rotate(-2deg); }
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
    "<h1 style='text-align: center; color: #38bdf8;'>🎣 CUỘC ĐUA CÂU CÁ MAY MẮN 🎣</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# --- BỐ CỤC CHÍNH (CHIA 2 CỘT: MÀN HÌNH GAME & LỊCH SỬ) ---
col_game, col_history = st.columns([3, 1])

with col_game:
    # 1. TẦNG TRÊN: NGƯỜI CÂU ĐỨNG TRÊN BỜ
    st.markdown('<div class="bank-container">', unsafe_allow_html=True)
    st.markdown("### 🌿 K Khu Vực Bờ Sông - Người Đang Câu 🌿")

    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.markdown(
            '<div class="fisherman-avatar">👴🎣</div>', unsafe_allow_html=True
        )
        st.markdown(
            f"Số cá đang bơi: **{len(st.session_state.participants)}** con"
        )

        remove_after_catch = st.checkbox(
            "Bắt xong thả ra ngoài",
            value=True,
            help="Loại bỏ người chơi đã câu được khỏi hồ",
        )

        if st.button(
            "🎣 QUĂNG CẦN CÂU NGAY!", type="primary", use_container_width=True
        ):
            if not st.session_state.participants:
                st.warning("Hồ đã cạn cá! Vui lòng thêm người ở Sidebar.")
            else:
                st.session_state.fishing = True
                st.session_state.hooked_person = None
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Xử lý hiệu ứng câu cá
    if st.session_state.fishing:
        with st.spinner("🌊 Cần câu đang rung... Đang kéo cá lên bờ..."):
            time.sleep(1.8)

        chosen = random.choice(st.session_state.participants)
        st.session_state.hooked_person = chosen
        st.session_state.fishing = False
        st.session_state.history.insert(0, chosen)

        if remove_after_catch:
            st.session_state.participants.remove(chosen)
        st.rerun()

    # Hiển thị kết quả khi câu thành công
    if st.session_state.hooked_person:
        st.success(
            f"🎉 Chúc mừng! Đã câu thành công: **{st.session_state.hooked_person}** lên bờ! 🐟"
        )
        st.balloons()
        st.session_state.hooked_person = None

    # 2. TẦNG DƯỚI: NHỮNG CHÚ CÁ TUNG TĂNG DƯỚI NƯỚC
    st.markdown('<div class="river-container">', unsafe_allow_html=True)
    st.markdown(
        "<h3 style='text-align: center; color: #bae6fd; margin-top: 0;'>🌊 Dưới Lòng Sông (Các Chú Cá Đang Tung Tăng Bơi Lội) 🌊</h3>",
        unsafe_allow_html=True,
    )

    if st.session_state.participants:
        fish_html = "<div style='text-align: center; padding-top: 15px;'>"
        for person in st.session_state.participants:
            fish_html += f'<div class="swimming-fish">🐟 &nbsp; {person}</div>'
        fish_html += "</div>"
        st.markdown(fish_html, unsafe_allow_html=True)
    else:
        st.markdown(
            "<h3 style='text-align: center; color: #fca5a5; margin-top: 60px;'>Hồ trống không! Không còn chú cá nào dưới nước.</h3>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# 3. CỘT LỊCH SỬ BÊN PHẢI
with col_history:
    st.markdown("### 📋 Lịch Sử Đã Câu")
    if st.session_state.history:
        for idx, person in enumerate(st.session_state.history[:10]):
            st.write(f"{idx + 1}. **{person}**")
        if st.button("🗑️ Xóa lịch sử", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("Chưa có ai được kéo lên bờ.")

# --- SIDEBAR QUẢN LÝ ---
with st.sidebar:
    st.header("⚙️ Cài Đặt Hồ Cá")
    bulk_input = st.text_area(
        "Danh sách người chơi (mỗi dòng 1 tên):",
        value="\n".join(st.session_state.participants),
        height=320,
    )
    if st.button("🔄 Cập nhật danh sách", use_container_width=True):
        names = [n.strip() for n in bulk_input.split("\n") if n.strip()]
        if names:
            st.session_state.participants = names
            st.success("Đã cập nhật đàn cá dưới hồ!")
            st.rerun()
        else:
            st.error("Danh sách không được để trống.")
  
