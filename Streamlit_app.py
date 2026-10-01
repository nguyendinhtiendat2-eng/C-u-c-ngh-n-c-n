import streamlit as st
import random
import time

# Cấu hình trang
st.set_page_config(
    page_title="Game Câu Cá Chọn Người",
    page_icon="🎣",
    layout="wide"
)

# Khởi tạo danh sách người chơi mặc định
if "players" not in st.session_state:
    st.session_state.players = [
        "Nguyễn Văn A", "Trần Thị B", "Lê Văn C", 
        "Phạm Thị D", "Hoàng Văn E", "Vũ Thị F"
    ]

if "winner" not in st.session_state:
    st.session_state.winner = None

st.title("🎣 GAME CÂU CÁ CHỌN NGƯỜI MAY MẮN")

# Chia giao diện thành 2 cột: Cột trái (Hồ cá & Cần thủ), Cột phải (Bảng quản lý)
col_game, col_board = st.columns([7, 3])

# --- CỘT TRÁI: NGƯỜI CÂU VÀ HỒ NƯỚC ---
with col_game:
    def render_fishing_scene(players):
        fish_html = ""
        colors = ["#ff7b00", "#ff0055", "#00b4d8", "#70e000", "#9d4edd", "#ffb703", "#e63946", "#06d6a0"]
        
        # Sinh các con cá tương ứng với danh sách người chơi
        for i, name in enumerate(players):
            top_pos = random.randint(20, 75)
            duration = random.randint(6, 12)
            delay = random.uniform(0, 5)
            color = colors[i % len(colors)]
            
            fish_html += f"""
            <div class="fish" style="
                top: {top_pos}%;
                animation-duration: {duration}s;
                animation-delay: -{delay}s;
                background-color: {color};
            ">
                🐟 <span class="fish-name">{name}</span>
            </div>
            """

        css_and_html = f"""
        <style>
            .fishing-scene {{
                width: 100%;
                background: #87CEEB;
                border-radius: 15px;
                padding-top: 10px;
                overflow: hidden;
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            }}
            .fisherman-area {{
                text-align: center;
                font-size: 55px;
                line-height: 1;
                margin-bottom: -15px;
                position: relative;
                z-index: 2;
                user-select: none;
            }}
            .lake {{
                position: relative;
                width: 100%;
                height: 350px;
                background: linear-gradient(180deg, #1e90ff 0%, #00008b 100%);
                border-top: 4px solid #4682B4;
                overflow: hidden;
            }}
            .fish {{
                position: absolute;
                padding: 6px 16px;
                border-radius: 20px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                white-space: nowrap;
                border: 2px solid rgba(255,255,255,0.9);
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                animation: swim linear infinite;
            }}
            .fish-name {{
                text-shadow: 1px 1px 2px black;
            }}
            @keyframes swim {{
                0% {{ left: -25%; transform: scaleX(1); }}
                49% {{ transform: scaleX(1); }}
                50% {{ left: 105%; transform: scaleX(-1); }}
                99% {{ transform: scaleX(-1); }}
                100% {{ left: -25%; transform: scaleX(1); }}
            }}
        </style>

        <div class="fishing-scene">
            <div class="fisherman-area">
                🧔🎣
            </div>
            <div class="lake">
                {fish_html}
            </div>
        </div>
        """
        st.markdown(css_and_html, unsafe_allow_html=True)

    # Hiển thị hồ cá và người câu
    render_fishing_scene(st.session_state.players)

    st.write("")
    
    # Nút thực hiện câu cá
    if st.button("🎣 BẮT ĐẦU CÂU CÁ!", use_container_width=True, type="primary"):
        if len(st.session_state.players) == 0:
            st.error("Hồ nước đang trống! Vui lòng thả thêm cá vào hồ.")
        else:
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            status_text.text("🧔 Cần thủ đang thả câu xuống hồ...")
            for percent in range(1, 101):
                time.sleep(0.02)
                progress_bar.progress(percent)
                if percent == 45:
                    status_text.text("🌊 Cá đang vây quanh mồi câu...")
                elif percent == 85:
                    status_text.text("🪝 Đã dính một chú cá! Đang kéo lên...")

            status_text.empty()
            progress_bar.empty()

            # Chọn ngẫu nhiên một con cá (người chơi)
            winner = random.choice(st.session_state.players)
            st.session_state.winner = winner
            st.balloons()

    # Hiển thị thông báo khi có kết quả câu
    if st.session_state.winner:
        st.success(f"🎉 **CÂU TRÚNG CON CÁ TÊN: {st.session_state.winner.upper()}!** 🎉")


# --- CỘT PHẢI: BẢNG GHI TÊN VÀ THÊM CÁ ---
with col_board:
    st.subheader("📋 Bảng Thêm & Quản Lý Cá")
    
    # Ô nhập để thả thêm cá mới vào hồ
    with st.form("add_fish_form", clear_on_submit=True):
        new_fish_name = st.text_input("Tên con cá muốn thả vào hồ:")
        submitted = st.form_submit_button("➕ Thả cá vào hồ", use_container_width=True)
        if submitted:
            if new_fish_name.strip():
                if new_fish_name.strip() not in st.session_state.players:
                    st.session_state.players.append(new_fish_name.strip())
                    st.success(f"Đã thả con cá '{new_fish_name.strip()}' xuống hồ!")
                    st.rerun()
                else:
                    st.warning("Con cá này đã có sẵn trong hồ rồi!")
            else:
                st.warning("Vui lòng nhập tên hợp lệ!")

    st.divider()

    # Danh sách cá đang bơi trong hồ
    st.markdown(f"**Danh sách cá trong hồ ({len(st.session_state.players)} con):**")
    if len(st.session_state.players) > 0:
        for idx, name in enumerate(st.session_state.players):
            col_name, col_del = st.columns([4, 1])
            col_name.markdown(f"**{idx + 1}.** 🐟 {name}")
            if col_del.button("❌", key=f"del_{idx}"):
                st.session_state.players.pop(idx)
                st.rerun()
    else:
        st.info("Hồ đang cạn nước (không có cá).")

    st.divider()
    if st.button("🔄 Đặt lại mặc định", use_container_width=True):
        st.session_state.players = [
            "Nguyễn Văn A", "Trần Thị B", "Lê Văn C", 
            "Phạm Thị D", "Hoàng Văn E", "Vũ Thị F"
        ]
        st.session_state.winner = None
        st.rerun()
  
