import streamlit as st
import random
import time
from PIL import Image, ImageDraw, ImageFont

# Thiết lập trang Streamlit
st.set_page_config(page_title="Game Câu Cá Streamlit", page_icon="🎣", layout="centered")

# --- QUẢN LÝ TRẠNG THÁI (SESSION STATE) ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "lake_history" not in st.session_state:
    st.session_state.lake_history = []

# --- TIÊU ĐỀ & TRÌNH PHÁT NHẠC ---
st.title("🎣 Game Câu Cá Siêu Cấp")
st.caption("Ứng dụng game tương tác đơn giản tích hợp nhạc nền bằng Streamlit")

# Khu vực thêm nhạc
st.sidebar.header("🎵 Tải nhạc nền")
uploaded_music = st.sidebar.file_uploader("Chọn tệp âm thanh (MP3/WAV/OGG)", type=["mp3", "wav", "ogg"])

if uploaded_music is not None:
    st.sidebar.audio(uploaded_music, format="audio/mp3", loop=True)
    st.sidebar.success(f"Đang sẵn sàng phát: {uploaded_music.name}")

# --- VẼ HÌNH ẢNH HỒ CÁ (Dùng Pillow) ---
def render_lake(hook_depth, cast_location):
    # Tạo canvas ảnh 600x350
    img = Image.new("RGB", (600, 350), color="#87CEEB") # Bầu trời
    draw = ImageDraw.Draw(img)
    
    # Bầu trời & Nước
    draw.rectangle([0, 80, 600, 350], fill="#1E90FF") # Mặt nước
    draw.rectangle([0, 70, 100, 80], fill="#8B4513")  # Bờ gỗ
    
    # Cần thủ (Đơn giản hóa)
    draw.ellipse([30, 40, 50, 60], fill="#FFD700")   # Đầu
    draw.line([40, 60, 40, 75], fill="#000000", width=3) # Thân
    draw.line([40, 65, 90, 50], fill="#8B4513", width=3) # Cần câu
    
    # Tính toán vị trí thả câu
    # cast_location: 1 (Gần bờ) -> 5 (Xa bờ) => X từ 120 -> 520
    hook_x = 100 + (cast_location * 85)
    # hook_depth: 0 (Mặt nước) -> 100 (Đáy hồ) => Y từ 90 -> 330
    hook_y = 90 + int(hook_depth * 2.4)
    
    # Vẽ dây câu & Lưỡi câu
    draw.line([90, 50, hook_x, hook_y], fill="#FFFFFF", width=1)
    draw.ellipse([hook_x-3, hook_y-3, hook_x+3, hook_y+3], fill="#FF0000") # Lưỡi câu
    
    # Vẽ vài con cá ngẫu nhiên dưới nước để trang trí
    random.seed(42) # Cố định vị trí trang trí
    for _ in range(6):
        fx = random.randint(120, 550)
        fy = random.randint(110, 320)
        draw.ellipse([fx, fy, fx+15, fy+8], fill="#FFA500")
        
    return img

# --- BẢNG ĐIỀU KHIỂN CÂU CÁ ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🌊 Hồ câu")
    # Điều khiển vị trí quăng câu & độ sâu
    cast_loc = st.slider("1. Khoảng cách quăng câu (Gần -> Xa)", min_value=1, max_value=5, value=3)
    depth = st.slider("2. Độ sâu lưỡi câu (%)", min_value=0, max_value=100, value=50)

    # Hiển thị ảnh khung cảnh câu cá
    lake_img = render_lake(depth, cast_loc)
    st.image(lake_img, use_container_width=True)

with col2:
    st.subheader("📊 Thành tích")
    st.metric(label="Điểm số hiện tại", value=f"{st.session_state.score} điểm")
    
    # Nút bấm hành động
    if st.button("🎣 Giật Cần!", use_container_width=True, type="primary"):
        with st.spinner("Đang giật cần..."):
            time.sleep(0.8) # Tạo hiệu ứng chờ
            
            # Tỷ lệ trúng cá dựa trên độ sâu
            catch_chance = random.random()
            
            if depth < 10:
                st.warning("⚠️ Lưỡi câu còn ở quá gần mặt nước, khó có cá!")
            elif catch_chance > 0.4:
                # Danh sách các loại cá
                fish_types = [
                    {"name": "Cá Rô Đồng 🐟", "pts": 10},
                    {"name": "Cá Chép Vàng 🐠", "pts": 25},
                    {"name": "Cá Lóc 🐊", "pts": 40},
                    {"name": "Món Đồ Cổ / Rác 👟", "pts": -5}
                ]
                caught = random.choice(fish_types)
                st.session_state.score += caught["pts"]
                
                if caught["pts"] > 0:
                    st.balloons()
                    st.success(f"🎉 Bạn đã câu được **{caught['name']}** (+{caught['pts']} điểm)!")
                else:
                    st.error(f"😅 Ôi không! Bạn vớt phải **{caught['name']}** ({caught['pts']} điểm).")
                
                st.session_state.lake_history.append(f"Câu được {caught['name']}")
            else:
                st.info("💧 Cá đã ăn mất mồi nhưng không dính câu! Thử lại xem.")

# --- LỊCH SỬ CÂU ---
if st.session_state.lake_history:
    with st.expander("📜 Lịch sử các lần giật cần"):
        for item in reversed(st.session_state.lake_history[-5:]):
            st.write(f"- {item}")
  
