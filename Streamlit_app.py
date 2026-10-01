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

# Tạo 2 cột chính: Cột trái (Người câu + Hồ cá) và Cột phải (Bảng danh sách)
col_game, col_board = st.columns([7, 3])

# --- CỘT TRÁI: NGƯỜI CÂU VÀ HỒ NƯỚC ---
with col_game:
    # Hàm dựng toàn bộ mô hình người câu + hồ nước + cá ghi tên
    def render_fishing_scene(players):
        fish_html = ""
        colors = ["#ff7b00", "#ff0055", "#00b4d8", "#70e000", "#9d4edd", "#ffb703", "#e63946", "#06d6a0"]
        
        # Tạo danh sách các con cá bơi ngẫu nhiên
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
            /* Khung toàn cảnh */
            .fishing-scene {{
                width: 100%;
                background: #87CEEB;
                border-radius: 15px;
                padding-top: 10px;
                overflow: hidden;
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            }}

            /* Bờ hồ và người câu cá */
            .fisherman-area {{
                text-align: center;
                font-size: 55px;
                line-height: 1;
                margin-bottom: -15px;
                position: relative;
                z-index: 2;
                user-select: none;
            }}

            /* Hồ nước */
            .lake {{
                position: relative;
                width: 100%;
                height: 350px;
                background: linear-gradient(180deg, #1e90ff 0%, #00008b 100%);
                border-top: 4px solid #4682B4;
                overflow: hidden;
            }}

            /* Hiệu ứng cá bơi */
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
            <!-- Thêm hình ảnh Cần thủ / Người câu cá -->
            <div class="fisherman-area">
                🧔🎣
            </div>
            <!-- Hồ nước chứa cá -->
            <div class="lake">
                {fish_html}
            </div>
        </div>
        """
        st.markdown(css_and_html, unsafe_allow_html=True)

    # Hiển thị mô hình
    render_fishing_scene(st.session_state.players)

    st.write("")
    # Nút thả câu
    if st.button("🎣 BẮT ĐẦU CÂU CÁ!", use_container_width=True, type="primary"):
        if len(st.session_state.players) == 0:
            st.error("Hồ nước đang trống! Vui lòng thêm người chơi vào danh sách.")
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

            # Chọn ngẫu nhiên
            winner = random.choice(st.session_state.players)
            st.session_state.winner = winner
            st.balloons()

    # Hiển thị thông báo khi có kết quả
    if st.session_state.winner:
        st.success(f"🎉 **NGƯỜI MAY MẮN ĐƯỢC CÂU TRÚNG: {st.session_state.winner.upper()}** 🎉")


# --- CỘT PHẢI: BẢNG GHI TÊN NGƯỜI CHƠI ---
with col_board:
    st.subheader("📋 Bảng Danh Sách Người Chơi")
    
    # Ô nhập để thêm người chơi mới
    with st.form("add_player_form", clear_on_submit=True):
        new_player = st.text_input("Nhập tên người chơi mới:")
        submitted = st.form_submit_button("➕ Thêm vào danh sách", use_container_width=True)
        if submitted:
            if new_player.strip():
                if new_player.strip() not in st.session_state.players:
                    st.session_state.players.append(new_player.strip())
                    st.rerun()
                else:
                    st.warning("Tên này đã có trong danh sách!")
            else:
                st.warning("Vui lòng nhập tên hợp lệ!")

    st.divider()

    # Bảng hiển thị danh sách người chơi
    if len(st.session_state.players) > 0:
        for idx, name in enumerate(st.session_state.players):
            col_name, col_del = st.columns([4, 1])
            col_name.markdown(f"**{idx + 1}.** 🐟 {name}")
            if col_del.button("❌", key=f"del_{idx}"):
                st.session_state.players.pop(idx)
                st.rerun()
    else:
        st.info("Chưa có người chơi nào trong hồ.")

    st.divider()
    if st.button("🔄 Đặt lại mặc định", use_container_width=True):
        st.session_state.players = [
            "Nguyễn Văn A", "Trần Thị B", "Lê Văn C", 
            "Phạm Thị D", "Hoàng Văn E", "Vũ Thị F"
        ]
        st.session_state.winner = None
        st.rerun()
          
