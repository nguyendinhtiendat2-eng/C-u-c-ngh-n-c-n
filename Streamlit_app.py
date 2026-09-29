import streamlit as st
import time
import random

st.set_page_config(
    page_title="Game Đua Vịt Trên Sông 🦆🌊",
    page_icon="🦆",
    layout="wide"
)

st.title("🦆🌊 Game Đua Vịt Trên Dòng Sông 🌊🦆")
st.caption("Nhập tên các chú vịt và theo dõi chúng trôi theo dòng sông về đích!")

# Khởi tạo danh sách vịt trong Session State
if "ducks" not in st.session_state:
    st.session_state.ducks = [
        {"name": "Vịt Donald", "color": "#FFD700"},
        {"name": "Vịt Psyduck", "color": "#FF5733"},
        {"name": "Vịt Bối Rối", "color": "#33FF57"},
        {"name": "Vịt Quay", "color": "#FF33A8"}
    ]

# Cấu hình đường đua ở Sidebar
st.sidebar.header("⚙️ Cấu hình dòng sông")
track_length = st.sidebar.slider("Độ dài đường đua (m):", min_value=50, max_value=200, value=100, step=10)
race_speed = st.sidebar.slider("Tốc độ dòng chảy (giây/bước):", min_value=0.02, max_value=0.3, value=0.08, step=0.02)

# --- QUẢN LÝ TÊN VÀ MÀU VỊT ---
st.subheader("📝 Danh sách thí sinh vịt đua")

with st.expander("➕ Thêm chú vịt mới", expanded=False):
    col_add1, col_add2, col_add3 = st.columns([3, 2, 1])
    with col_add1:
        new_name = st.text_input("Tên vịt:", key="new_duck_name")
    with col_add2:
        new_color = st.color_picker("Màu bảng tên:", "#FFD700", key="new_duck_color")
    with col_add3:
        st.write(" ")
        st.write(" ")
        if st.button("Thêm vịt", type="secondary"):
            if new_name.strip():
                st.session_state.ducks.append({"name": new_name.strip(), "color": new_color})
                st.rerun()

ducks_to_remove = []
for idx, duck in enumerate(st.session_state.ducks):
    c1, c2, c3 = st.columns([4, 2, 1])
    with c1:
        updated_name = st.text_input(
            f"Tên Vịt #{idx+1}", 
            value=duck["name"], 
            key=f"name_{idx}", 
            label_visibility="collapsed"
        )
        st.session_state.ducks[idx]["name"] = updated_name
    with c2:
        updated_color = st.color_picker(
            f"Màu #{idx+1}", 
            value=duck["color"], 
            key=f"color_{idx}", 
            label_visibility="collapsed"
        )
        st.session_state.ducks[idx]["color"] = updated_color
    with c3:
        if st.button("❌", key=f"del_{idx}"):
            ducks_to_remove.append(idx)

if ducks_to_remove:
    for index in sorted(ducks_to_remove, reverse=True):
        st.session_state.ducks.pop(index)
    st.rerun()

st.divider()

# --- ĐƯỜNG ĐUA DÒNG SÔNG ---
if len(st.session_state.ducks) < 2:
    st.warning("⚠️ Cần ít nhất 2 chú vịt để bắt đầu cuộc đua trên sông!")
    st.stop()

if st.button("🚀 BẮT ĐẦU THẢ VỊT XUỐNG SÔNG!", type="primary", use_container_width=True):
    positions = {duck["name"]: 0 for duck in st.session_state.ducks}
    winner = None

    race_area = st.empty()

    while not winner:
        for duck in st.session_state.ducks:
            name = duck["name"]
            # Tạo chuyển động sóng ngẫu nhiên (vịt nhích lên từ 1 đến 5 mét)
            step = random.randint(1, 5)
            positions[name] += step
            
            if positions[name] >= track_length and not winner:
                winner = name

        # Giao diện dòng sông bằng HTML/CSS
        with race_area.container():
            st.write("### 🏁 DÒNG SÔNG ĐANG ĐUA...")
            
            for duck in st.session_state.ducks:
                name = duck["name"]
                color = duck["color"]
                pos = positions[name]
                pct = min(100, int((pos / track_length) * 100))

                # Render dòng sông xanh và con vịt trôi cùng bảng tên
                st.markdown(f"""
                    <div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); 
                                border-radius: 15px; 
                                padding: 10px; 
                                margin-bottom: 15px; 
                                position: relative; 
                                border: 2px solid #00d2ff;
                                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <!-- Vạch đích -->
                        <div style="position: absolute; right: 15px; top: 0; bottom: 0; border-right: 3px dashed #ff4757; z-index: 1;">
                            <span style="color: white; font-size: 10px; background: #ff4757; padding: 2px 4px; border-radius: 3px;">ĐÍCH</span>
                        </div>
                        
                        <!-- Con Vịt + Bảng Tên trôi theo tỷ lệ % -->
                        <div style="margin-left: calc({pct}% - 60px if {pct} > 10 else {pct}%); 
                                    transition: margin-left 0.1s linear; 
                                    display: inline-block; 
                                    white-space: nowrap;
                                    position: relative; 
                                    z-index: 2;">
                            <span style="font-size: 28px; vertical-align: middle;">🦆</span>
                            <span style="background-color: {color}; 
                                         color: #000; 
                                         font-weight: bold; 
                                         padding: 4px 10px; 
                                         border-radius: 12px; 
                                         border: 1px solid #fff;
                                         box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                                         font-size: 14px;">
                                {name} ({min(pos, track_length)}m)
                            </span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        time.sleep(race_speed)

    # Hiệu ứng kết quả
    st.balloons()
    st.success(f"🏆 **CHÚC MỪNG {winner.upper()} ĐÃ VỀ ĐÍCH ĐẦU TIÊN TẠI DÒNG SÔNG!** 🎉")

    # Bảng xếp hạng chung cuộc
    st.write("### 📊 Bảng Xếp Hạng Chung Cuộc")
    sorted_ducks = sorted(positions.items(), key=lambda x: x[1], reverse=True)
    for rank, (name, pos) in enumerate(sorted_ducks, 1):
        icon = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        st.write(f"{icon} **{name}** — Vị trí: {min(pos, track_length)}m")
  
