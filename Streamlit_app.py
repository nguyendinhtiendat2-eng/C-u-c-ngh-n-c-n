import streamlit as st
import time
import random

st.set_page_config(
    page_title="Game Đua Vịt 🦆",
    page_icon="🦆",
    layout="wide"
)

st.title("🦆 Game Đua Vịt Tùy Chỉnh Tên 🦆")
st.caption("Thêm, sửa, xóa tên trực tiếp và bắt đầu cuộc đua!")

# Khởi tạo danh sách vịt trong Session State
if "ducks" not in st.session_state:
    st.session_state.ducks = [
        {"name": "Vịt Donald", "color": "#FF5733"},
        {"name": "Vịt Psyduck", "color": "#33FF57"},
        {"name": "Vịt Bối Rối", "color": "#3357FF"},
        {"name": "Vịt Quay", "color": "#F39C12"}
    ]

# Cấu hình cuộc đua ở Sidebar
st.sidebar.header("⚙️ Cấu hình đường đua")
track_length = st.sidebar.slider("Độ dài đường đua (m):", min_value=50, max_value=200, value=100, step=10)
race_speed = st.sidebar.slider("Tốc độ cập nhật (giây/bước):", min_value=0.02, max_value=0.3, value=0.08, step=0.02)

# --- QUẢN LÝ VÀ ĐIỀU CHỈNH TÊN VỊT ---
st.subheader("📝 Danh sách & Điều chỉnh tên Vịt")

# Form thêm vịt mới
with st.expander("➕ Thêm vịt mới", expanded=False):
    col_add1, col_add2, col_add3 = st.columns([3, 2, 1])
    with col_add1:
        new_name = st.text_input("Tên vịt mới:", key="new_duck_name")
    with col_add2:
        new_color = st.color_picker("Màu sắc:", "#FFD700", key="new_duck_color")
    with col_add3:
        st.write(" ")
        st.write(" ")
        if st.button("Thêm", type="secondary"):
            if new_name.strip():
                st.session_state.ducks.append({"name": new_name.strip(), "color": new_color})
                st.rerun()

# Bảng chỉnh sửa tên và màu sắc
st.write("Chỉnh sửa tên hoặc xóa các chú vịt bên dưới:")
ducks_to_remove = []

for idx, duck in enumerate(st.session_state.ducks):
    c1, c2, c3 = st.columns([4, 2, 1])
    with c1:
        # Chỉnh sửa tên trực tiếp
        updated_name = st.text_input(
            f"Vịt #{idx+1}", 
            value=duck["name"], 
            key=f"name_{idx}", 
            label_visibility="collapsed"
        )
        st.session_state.ducks[idx]["name"] = updated_name
    with c2:
        # Chọn màu
        updated_color = st.color_picker(
            f"Color #{idx+1}", 
            value=duck["color"], 
            key=f"color_{idx}", 
            label_visibility="collapsed"
        )
        st.session_state.ducks[idx]["color"] = updated_color
    with c3:
        # Nút xóa
        if st.button("❌", key=f"del_{idx}"):
            ducks_to_remove.append(idx)

# Xóa vịt đã chọn
if ducks_to_remove:
    for index in sorted(ducks_to_remove, reverse=True):
        st.session_state.ducks.pop(index)
    st.rerun()

st.divider()

# --- BẮT ĐẦU ĐUA ---
if len(st.session_state.ducks) < 2:
    st.warning("⚠️ Cần ít nhất 2 chú vịt để tổ chức cuộc đua!")
    st.stop()

if st.button("🚀 BẮT ĐẦU ĐUA NGHỆT THỞ!", type="primary", use_container_width=True):
    positions = {duck["name"]: 0 for duck in st.session_state.ducks}
    winner = None

    race_area = st.empty()

    while not winner:
        # Nhích vị trí ngẫu nhiên
        for duck in st.session_state.ducks:
            name = duck["name"]
            step = random.randint(1, 6)
            positions[name] += step
            
            if positions[name] >= track_length and not winner:
                winner = name

        # Render giao diện đường đua
        with race_area.container():
            st.subheader("🏁 ĐƯỜNG ĐUA ĐANG DIỄN RA")
            for duck in st.session_state.ducks:
                name = duck["name"]
                color = duck["color"]
                pos = positions[name]
                pct = min(100, int((pos / track_length) * 100))

                # Render thanh đường đua bằng HTML/CSS tùy chỉnh màu sắc
                st.markdown(f"""
                    <div style="margin-bottom: 12px;">
                        <strong>🦆 {name}</strong> ({min(pos, track_length)}m)
                        <div style="background-color: #e0e0e0; border-radius: 10px; height: 24px; width: 100%; overflow: hidden;">
                            <div style="background-color: {color}; width: {pct}%; height: 100%; border-radius: 10px; transition: width 0.1s;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        time.sleep(race_speed)

    # Kết quả
    st.balloons()
    st.success(f"🏆 **CHÚC MỪNG {winner.upper()} ĐÃ VỀ ĐÍCH ĐẦU TIÊN!** 🎉")

    # Bảng xếp hạng
    st.write("### 📊 Bảng xếp hạng chung cuộc")
    sorted_ducks = sorted(positions.items(), key=lambda x: x[1], reverse=True)
    for rank, (name, pos) in enumerate(sorted_ducks, 1):
        icon = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        st.write(f"{icon} **{name}** — {min(pos, track_length)}m")
                        
