import streamlit as st
import random

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Game Câu Cá & Chọn Nhân Vật", 
    page_icon="🎣", 
    layout="centered"
)

# Khởi tạo trạng thái phiên (session_state) nếu chưa có
if "screen" not in st.session_state:
    st.session_state.screen = "select"  # "select", "playing", "gameover"
if "character" not in st.session_state:
    st.session_state.character = {"name": "Bác nông dân", "avatar": "👨‍🌾"}
if "score" not in st.session_state:
    st.session_state.score = 0
if "time_left" not in st.session_state:
    st.session_state.time_left = 30

# Danh sách nhân vật (Cần thủ)
CHARACTERS = [
    {"name": "Bác nông dân", "avatar": "👨‍🌾", "desc": "Kinh nghiệm dạn dày, chuyên câu cá lớn."},
    {"name": "Mèo tinh nghịch", "avatar": "🐱", "desc": "Nhanh nhẹn, phản xạ siêu tốc."},
    {"name": "Cậu bé tập câu", "avatar": "👦", "desc": "Nhiệt huyết và đam mê khám phá."}
]

# --- MÀN HÌNH 1: CHỌN NHÂN VẬT ---
if st.session_state.screen == "select":
    st.title("🎣 CHỌN CẦN THỦ CỦA BẠN")
    st.write("Hãy chọn một nhân vật đồng hành cùng bạn trong chuyến đi câu cá này nhé!")

    col1, col2, col3 = st.columns(3)
    
    selected_idx = 0
    for i, char in enumerate(CHARACTERS):
        with [col1, col2, col3][i]:
            st.markdown(f"<h1 style='text-align: center;'>{char['avatar']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center;'>{char['name']}</h3>", unsafe_allow_html=True)
            st.write(char['desc'])
            if st.button(f"Chọn {char['name']}", key=f"char_{i}I"):
                st.session_state.character = char
                st.success(f"Đã chọn: {char['name']}!")

    st.markdown("---")
    st.info(f"Nhân vật hiện tại: **{st.session_state.character['avatar']} {st.session_state.character['name']}**")
    
    if st.button("🚀 BẮT ĐẦU CÂU CÁ", use_container_width=True):
        st.session_state.screen = "playing"
        st.session_state.score = 0
        st.session_state.time_left = 30
        st.rerun()

# --- MÀN HÌNH 2: TRÒ CHƠI CÂU CÁ ---
elif st.session_state.screen == "playing":
    st.title(f"🌊 Vùng Biển Đảo - Cần thủ: {st.session_state.character['avatar']} {st.session_state.character['name']}")

    # Hiển thị thông tin điểm số và thời gian
    col_score, col_time = st.columns(2)
    with col_score:
        st.metric(label="🏆 Điểm số", value=st.session_state.score)
    with col_time:
        st.metric(label="⏳ Thời gian còn lại", value=f"{st.session_state.time_left}s")

    st.markdown("---")
    st.write("### Nhấn nút bên dưới để thả câu và thu hoạch cá ngẫu nhiên!")

    # Mô phỏng hành động câu cá tương tác qua nút bấm Streamlit
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎣 THẢ CÂU NGAY!", use_container_width=True):
            # Random loại cá bắt được
            fish_types = [
                {"name": "Cá nhỏ", "points": 10, "emoji": "🐟"},
                {"name": "Cá vàng", "points": 20, "emoji": "🐠"},
                {"name": "Cá mập con", "points": 50, "emoji": "🦈"},
                {"name": "Kho báu bí ẩn", "points": 100, "emoji": "🎁"}
            ]
            caught = random.choice(fish_types)
            st.session_state.score += caught["points"]
            st.success(f"Tuyệt vời! Bạn đã câu được **{caught['name']}** {caught['emoji']} (+{caught['points']} điểm)")

    with col_btn2:
        if st.button("⏱️ Kết thúc sớm / Xem kết quả", use_container_width=True):
            st.session_state.screen = "gameover"
            st.rerun()

    # Thanh điều hướng phụ giả lập thời gian trôi qua mỗi khi bấm tương tác
    if st.session_state.time_left > 0:
        st.session_state.time_left -= 1
        if st.session_state.time_left <= 0:
            st.session_state.screen = "gameover"
            st.rerun()
            
    # Tự động làm mới UI để mô phỏng vòng lặp game
    if st.button("🔄 Tiếp tục câu lượt tiếp theo"):
        st.rerun()

# --- MÀN HÌNH 3: KẾT THÚC TRÒ CHƠI ---
elif st.session_state.screen == "gameover":
    st.title("🏁 HẾT GIỜ - TỔNG KẾT CHUYẾN CÂU")
    st.balloons()
    
    st.markdown(f"""
    ### Nhân vật: {st.session_state.character['avatar']} {st.session_state.character['name']}
    ### 🏆 Tổng điểm đạt được: **{st.session_state.score} điểm**
    """)
    
    if st.session_state.score >= 150:
        st.success("🌟 Xuất sắc! Bạn là một bậc thầy câu cá thực thụ!")
    elif st.session_state.score >= 50:
        st.info("👍 Khá lắm! Một chuyến đi câu thành công.")
    else:
        st.warning("⚠️ Cố gắng rèn luyện thêm tay nghề ở lần sau nhé!")

    if st.button("🔄 CHƠI LẠI TỪ ĐẦU", use_container_width=True):
        st.session_state.screen = "select"
        st.session_state.score = 0
        st.session_state.time_left = 30
        st.rerun()
  
