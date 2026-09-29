import streamlit as st
import random
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Đua Vịt Sôi Nổi - Duck Race",
    page_icon="🦆",
    layout="wide"
)

# --- CSS TÙY CHỈNH DÀNH CHO GAME ---
st.markdown("""
<style>
    .race-track {
        background-color: #e0f7fa;
        border: 3px solid #0288d1;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .duck-row {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        background-color: #ffffff;
        padding: 8px 12px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .duck-name {
        width: 140px;
        font-weight: bold;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: #333;
    }
    .lane {
        flex-grow: 1;
        background-color: #b2ebf2;
        height: 36px;
        border-radius: 18px;
        position: relative;
        margin: 0 10px;
        border: 1px dashed #0097a7;
    }
    .duck-avatar {
        position: absolute;
        top: 2px;
        font-size: 24px;
        transition: left 0.1s linear;
    }
    .finish-line {
        position: absolute;
        right: 10px;
        top: 0;
        bottom: 0;
        width: 4px;
        background-color: #e53935;
    }
    .winner-box {
        background-color: #fff8e1;
        border: 2px solid #ffb300;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_allowed_html=True)

# --- KHỞI TẠO STATE (LƯU TRẠNG THÁI) ---
if 'ducks' not in st.session_state:
    st.session_state.ducks = [
        {"name": "Vịt Vàng 🐣", "color": "#FFD700"},
        {"name": "Vịt Xanh 🦆", "color": "#4CAF50"},
        {"name": "Vịt Hồng 🦩", "color": "#FF69B4"},
        {"name": "Vịt Cam 🍊", "color": "#FF8C00"}
    ]

if 'history' not in st.session_state:
    st.session_state.history = []

# --- TIÊU ĐỀ & ÂM THANH ---
st.title("🦆 Game Đua Vịt Sôi Nổi")
st.caption("Ứng dụng phát triển bằng Streamlit & Python")

# Tải file nhạc
st.sidebar.header("🎵 Cài đặt Âm thanh")
audio_file = st.sidebar.file_uploader("Tải nhạc nền (MP3, WAV, OGG):", type=["mp3", "wav", "ogg"])

if audio_file is not None:
    st.sidebar.audio(audio_file, format="audio/mp3", autoplay=True, loop=True)
else:
    st.sidebar.info("💡 Bạn có thể tải file nhạc từ máy tính lên để làm nhạc nền đua vịt!")

# --- BẢNG ĐIỀU KHIỂN & CÀI ĐẶT VỊT ---
st.sidebar.header("⚙️ Quản lý Vịt Đua")

# Thêm vịt mới
new_duck_name = st.sidebar.text_input("Tên chú vịt mới:")
if st.sidebar.button("➕ Thêm Vịt"):
    if new_duck_name.strip():
        st.session_state.ducks.append({"name": new_duck_name.strip(), "color": "#FFD700"})
        st.rerun()

# Danh sách vịt hiện tại
st.sidebar.subheader("Danh sách tham gia:")
for idx, duck in enumerate(st.session_state.ducks):
    cols = st.sidebar.columns([3, 1])
    cols[0].write(f"{idx+1}. {duck['name']}")
    if len(st.session_state.ducks) > 2:
        if cols[1].button("❌", key=f"del_{idx}"):
            st.session_state.ducks.pop(idx)
            st.rerun()

# --- GIAO DIỆN ĐƯỜNG ĐƯA ---
col_race, col_rank = st.columns([3, 1])

with col_race:
    st.subheader("🏁 Đường Đua")
    
    # Nút Bắt đầu
    start_race = st.button("🚀 BẮT ĐẦU ĐUA!", type="primary", use_container_width=True)
    
    race_placeholder = st.empty()

    def render_track(positions):
        html_content = "<div class='race-track'>"
        for idx, duck in enumerate(st.session_state.ducks):
            pos = positions.get(idx, 0)
            html_content += f"""
            <div class='duck-row'>
                <div class='duck-name'>{duck['name']}</div>
                <div class='lane'>
                    <div class='finish-line'></div>
                    <div class='duck-avatar' style='left: calc({pos}% - 20px);'>🦆</div>
                </div>
                <div style='width: 45px; text-align: right; font-weight: bold;'>{int(pos)}%</div>
            </div>
            """
        html_content += "</div>"
        return html_content

    # Hiển thị đường đua ban đầu
    initial_positions = {i: 0 for i in range(len(st.session_state.ducks))}
    race_placeholder.markdown(render_track(initial_positions), unsafe_allow_html=True)

# --- XỬ LÝ ĐUA VỊT ---
if start_race:
    positions = {i: 0 for i in range(len(st.session_state.ducks))}
    winner = None
    
    # Vòng lặp đua
    while True:
        time.sleep(0.15)  # Cập nhật mỗi 0.15 giây
        
        # Tăng tiến trình ngẫu nhiên cho từng chú vịt
        for i in range(len(st.session_state.ducks)):
            if positions[i] < 100:
                step = random.uniform(1.0, 4.5)
                # Tỉ lệ bứt phá tốc độ
                if random.random() < 0.1:
                    step += random.uniform(3.0, 6.0)
                positions[i] = min(100, positions[i] + step)
                
                if positions[i] >= 100 and winner is None:
                    winner = st.session_state.ducks[i]['name']
        
        # Cập nhật giao diện đường đua
        race_placeholder.markdown(render_track(positions), unsafe_allow_html=True)
        
        # Kiểm tra nếu tất cả đã về đích
        if all(pos >= 100 for pos in positions.values()):
            break

    # Màn chúc mừng chiến thắng
    if winner:
        st.balloons()  # Hiệu ứng bóng bay/pháo hoa ăn mừng của Streamlit
        st.markdown(f"""
        <div class='winner-box'>
            <h2>🎉 CHÚC MƯỜNG XIN CHÚC MƯỜNG! 🎉</h2>
            <h3 style='color: #d32f2f;'>🏆 Nhà vô địch: {winner} 🏆</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Lưu lịch sử
        st.session_state.history.insert(0, winner)

# --- BẢNG XẾP HẠNG & LỊCH SỬ ---
with col_rank:
    st.subheader("📜 Bảng Vàng Chiến Thắng")
    if st.session_state.history:
        for i, w_name in enumerate(st.session_state.history[:10]):
            st.write(f"**Trận {len(st.session_state.history)-i}:** 🏆 {w_name}")
    else:
        st.info("Chưa có trận đua nào diễn ra.")
          
