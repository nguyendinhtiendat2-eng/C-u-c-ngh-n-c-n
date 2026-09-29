import streamlit as st
import time
import random

st.set_page_config(
    page_title="Game Đua Vịt 🦆",
    page_icon="🦆",
    layout="wide"
)

st.title("🦆 Game Đua Vịt Kỳ Phùng Địch Thủ 🦆")
st.caption("Ứng dụng đua vịt chọn người may mắn ngẫu nhiên bằng Streamlit")

# Sidebar - Cấu hình Game
st.sidebar.header("⚙️ Cấu hình cuộc đua")

names_input = st.sidebar.text_area(
    "Nhập danh sách tên vịt (cách nhau bởi dấu phẩy):",
    value="Vịt Donald, Vịt Daisy, Vịt Psyduck, Vịt Bối Rối, Vịt Quay",
    height=120
)

track_length = st.sidebar.slider("Độ dài đường đua (m):", min_value=50, max_value=200, value=100, step=10)
race_speed = st.sidebar.slider("Tốc độ cập nhật (giây/bước):", min_value=0.05, max_value=0.5, value=0.1, step=0.05)

# Xử lý danh sách tên vịt
duck_names = [name.strip() for name in names_input.split(",") if name.strip()]

if not duck_names:
    st.warning("⚠️ Vui lòng nhập ít nhất 1 tên vịt để bắt đầu cuộc đua!")
    st.stop()

# Khởi tạo trạng thái Game
if "racing" not in st.session_state:
    st.session_state.racing = False

col_btn1, col_btn2 = st.columns([1, 4])

with col_btn1:
    start_race = st.button("🚀 Bắt đầu đua!", type="primary", use_container_width=True)

if start_race:
    st.session_state.racing = True

# Khu vực hiển thị trận đua
race_area = st.empty()

if st.session_state.racing:
    # Khởi tạo vị trí ban đầu
    positions = {name: 0 for name in duck_names}
    winner = None

    while not winner:
        # Cập nhật vị trí từng con vịt
        for name in duck_names:
            step = random.randint(1, 5)
            positions[name] += step
            if positions[name] >= track_length and not winner:
                winner = name

        # Hiển thị đường đua
        with race_area.container():
            st.subheader("🏁 Đường đua đang diễn ra...")
            for name, pos in positions.items():
                progress_pct = min(1.0, pos / track_length)
                
                # Hiển thị Bảng tên + Tiến trình + Biểu tượng vịt
                col_label, col_bar = st.columns([1, 4])
                with col_label:
                    st.markdown(f"**🦆 {name}** (`{min(pos, track_length)}m`)")
                with col_bar:
                    st.progress(progress_pct)

        time.sleep(race_speed)

    # Hiển thị kết quả
    st.session_state.racing = False
    st.balloons()
    st.success(f"🎉 **CHÚC MỪNG {winner.upper()} ĐÃ GIÀNH CHIẾN THẮNG!** 🏆")

    # Bảng xếp hạng chung cuộc
    st.subheader("📊 Bảng Xếp Hạng Chung Cuộc")
    sorted_ducks = sorted(positions.items(), key=lambda x: x[1], reverse=True)
    
    for idx, (name, pos) in enumerate(sorted_ducks, 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
        st.write(f"{medal} **{name}** - Khoảng cách: {min(pos, track_length)}m")
else:
    # Trạng thái chờ bắt đầu
    with race_area.container():
        st.info("👈 Bấm nút **'Bắt đầu đua!'** ở góc trái để bắt đầu cuộc đua.")
        st.write("### 📋 Danh sách vịt tham gia:")
        cols = st.columns(min(len(duck_names), 4))
        for idx, name in enumerate(duck_names):
            cols[idx % 4].metric(label=f"Thí sinh #{idx+1}", value=name)
          
