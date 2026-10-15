import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Game Câu Cá - Sông Nước Quê Hương", 
    page_icon="🎣", 
    layout="centered"
)

# Hàm chuyển đổi file MP3 local sang dạng Base64 an toàn tuyệt đối
def get_audio_base64(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as audio_file:
                return base64.b64encode(audio_file.read()).decode()
    except Exception:
        pass
    return None

# Khởi tạo session state
if "screen" not in st.session_state:
    st.session_state.screen = "select"
if "player_name" not in st.session_state:
    st.session_state.player_name = "Cần thủ"
if "character" not in st.session_state:
    st.session_state.character = {"name": "Bác nông dân", "avatar": "👨‍🌾", "color": "#c0392b"}
if "game_duration" not in st.session_state:
    st.session_state.game_duration = 40
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Vừa"
if "enable_music" not in st.session_state:
    st.session_state.enable_music = True

CHARACTERS = [
    {"name": "Nông dân", "avatar": "👨‍🌾", "color": "#c0392b"},
    {"name": "Mèo", "avatar": "🐱", "color": "#e67e22"},
    {"name": "Cậu bé", "avatar": "👦", "color": "#2980b9"}
]

# CSS tùy chỉnh giao diện màn hình bắt đầu cực chất giống mẫu
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0b0e;
        color: #ffffff;
    }
    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: 900;
        color: #ff5722;
        text-shadow: 0 0 15px rgba(255, 87, 34, 0.6);
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-size: 14px;
        color: #aaa;
        letter-spacing: 2px;
        margin-bottom: 25px;
    }
    .section-label {
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        color: #ddd;
        margin: 15px 0 8px 0;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# --- MÀN HÌNH 1: CÀI ĐẶT TRẬN ĐẤU & GIAO DIỆN TỐI RỰC RỠ ---
if st.session_state.screen == "select":
    st.markdown("<div class='main-title'>🔥 SÔNG NƯỚC RỰC CHÁY 🔥</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>🎣 FISHING ROAD RACING 🎣</div>", unsafe_allow_html=True)

    st.session_state.player_name = st.text_input("👤 Tên cần thủ:", value=st.session_state.player_name)

    # Cài đặt Nhạc
    st.markdown("<div class='section-label'>🎵 ÂM NHẠC</div>", unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if st.button("🎵 Bật Nhạc", use_container_width=True, type="primary" if st.session_state.enable_music else "secondary"):
            st.session_state.enable_music = True
            st.rerun()
    with col_m2:
        if st.button("🔇 Tắt Nhạc", use_container_width=True, type="primary" if not st.session_state.enable_music else "secondary"):
            st.session_state.enable_music = False
            st.rerun()

    # Chọn Độ Khó
    st.markdown("<div class='section-label'>⚡ ĐỘ KHÓ</div>", unsafe_allow_html=True)
    d_col1, d_col2, d_col3 = st.columns(3)
    difficulties = ["Dễ", "Vừa", "Khó"]
    for i, diff in enumerate(difficulties):
        with [d_col1, d_col2, d_col3][i]:
            is_selected = (st.session_state.difficulty == diff)
            if st.button(diff, use_container_width=True, type="primary" if is_selected else "secondary"):
                st.session_state.difficulty = diff
                st.rerun()

    # Chọn Nhân Vật (Xe)
    st.markdown("<div class='section-label'>🚗 CHỌN NHÂN VẬT</div>", unsafe_allow_html=True)
    c_col1, c_col2, c_col3 = st.columns(3)
    for i, char in enumerate(CHARACTERS):
        with [c_col1, c_col2, c_col3][i]:
            is_selected = (st.session_state.character["name"] == char["name"])
            btn_label = f"{char['avatar']} {char['name']}"
            if st.button(btn_label, use_container_width=True, type="primary" if is_selected else "secondary"):
                st.session_state.character = char
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Nút Bắt Đầu Lớn
    if st.button("🔥 BẮT ĐẦU 🔥", use_container_width=True, type="primary"):
        st.session_state.screen = "playing"
        st.rerun()

# --- MÀN HÌNH 2: GIAO DIỆN GAME CHÍNH ---
elif st.session_state.screen == "playing":
    player_name = st.session_state.player_name if st.session_state.player_name else "Cần thủ"
    st.title("🌊 Sông Nước Quê Hương")
    st.write(f"💡 **{player_name}** ({st.session_state.character['avatar']} {st.session_state.character['name']}) | Độ khó: **{st.session_state.difficulty}**")

    char_avatar = st.session_state.character['avatar']
    boat_color = st.session_state.character['color']
    duration = 40  # Mặc định thời gian
    
    diff_setting = st.session_state.difficulty
    if diff_setting == "Dễ":
        speed_multiplier = 0.7
    elif diff_setting == "Khó":
        speed_multiplier = 1.6
    else:
        speed_multiplier = 1.0

    audio_b64 = get_audio_base64("Sandwich and story.mp3")
    audio_tag = ""
    if st.session_state.enable_music and audio_b64:
        audio_tag = f'''
        <div style="margin-top: 4px; width: 750px; background: #2f3640; padding: 6px 12px; border-radius: 8px; display: flex; align-items: center; justify-content: space-between; box-sizing: border-box;">
            <span style="color: #f5f6fa; font-size: 13px; font-weight: bold;">🎵 Sandwich and story.mp3</span>
            <audio controls loop autoplay style="height: 32px; outline: none;">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
        </div>
        '''

    game_html = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                background: #1e272e;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
            }}
            .game-wrapper {{
                position: relative;
                cursor: pointer;
                outline: none;
            }}
            canvas {{
                background: linear-gradient(to bottom, #dff9fb 0%, #74b9ff 28%, #0984e3 28%, #00cec9 100%);
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.5);
                touch-action: none;
            }}
            .hud {{
                position: absolute;
                top: 10px;
                left: 15px;
                color: white;
                font-size: 15px;
                font-weight: bold;
                text-shadow: 1px 1px 2px black;
                z-index: 10;
                pointer-events: none;
            }}
            #scoreModal {{
                display: none;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                text-align: center;
                z-index: 100;
                width: 320px;
            }}
            #scoreModal h2 {{
                color: #2c3e50;
                margin-top: 0;
            }}
            #scoreModal p {{
                font-size: 18px;
                color: #e74c3c;
                font-weight: bold;
            }}
            .modal-btn {{
                background: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                margin-top: 10px;
            }}
            .modal-btn:hover {{
                background: #219653;
            }}
            .on-screen-controls {{
                display: flex;
                gap: 8px;
                margin-top: 6px;
                justify-content: center;
                width: 750px;
            }}
            .virtual-btn {{
                width: 110px;
                background: #f1c40f;
                color: #2c3e50;
                border: none;
                padding: 5px 10px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }}
            .virtual-btn:active {{
                transform: scale(0.95);
                background: #d4ac0d;
            }}
            .btn-drop {{
                width: 130px;
                background: #e74c3c;
                color: white;
            }}
            .btn-drop:active {{
                background: #c0392b;
            }}
        </style>
    </head>
    <body>
        <div class="game-wrapper" id="gameWrapper">
            <div class="hud" id="hudText">Điểm: 0 | Thời gian: {duration}s</div>
            <canvas id="gameCanvas" width="750" height="450" tabindex="0"></canvas>
            
            <div id="scoreModal">
                <h2>🏆 KẾT THÚC TRẬN CÂU 🎣</h2>
                <p>Cần thủ: {player_name}</p>
                <p>Tổng điểm: <span id="finalScore">0</span> điểm</p>
                <p style="font-size: 14px; color: #7f8c8d;">Chuyến đi câu đã hoàn tất!</p>
                <button class="modal-btn" onclick="location.reload()">Chơi lại ngay 🔄</button>
            </div>
        </div>

        <div class="on-screen-controls">
            <button class="virtual-btn" onclick="moveLeft()">◀ Trái</button>
            <button class="virtual-btn btn-drop" onclick="actionDrop()">🎣 Thả Cần</button>
            <button class="virtual-btn" onclick="moveRight()">Phải ▶</button>
        </div>

        {audio_tag}

        <script>
            const BOAT_COLOR = '{boat_color}';
            const CHAR_AVATAR = '{char_avatar}';
            const SPEED_MUL = {speed_multiplier};

            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            canvas.focus();

            let score = 0;
            let timeLeft = {duration};
            let boatX = 375;
            
            let hookState = 'IDLE';
            let hookY = 100;
            const maxHookY = 410;
            let caughtFish = null;
            let waveOffset = 0;
            let isGameOver = false;

            let fishes = [
                {{x: 50, y: 310, rx: 18, ry: 10, color: '#ff6b6b', speed: 1.2 * SPEED_MUL}},
                {{x: 700, y: 370, rx: 16, ry: 9, color: '#feca57', speed: -1.5 * SPEED_MUL}},
                {{x: 200, y: 400, rx: 20, ry: 12, color: '#ff9ff3', speed: 1.0 * SPEED_MUL}},
                {{x: 600, y: 340, rx: 15, ry: 8, color: '#48dbfb', speed: -1.3 * SPEED_MUL}},
                {{x: 350, y: 390, rx: 18, ry: 10, color: '#10ac84', speed: 1.1 * SPEED_MUL}}
            ];

            const timer = setInterval(() => {{
                if (!isGameOver) {{
                    timeLeft--;
                    if (timeLeft <= 0) {{
                        clearInterval(timer);
                        isGameOver = true;
                        document.getElementById('finalScore').innerText = score;
                        document.getElementById('scoreModal').style.display = 'block';
                    }}
                }}
            }}, 1000);

            function moveLeft() {{
                if (!isGameOver && boatX > 60) boatX -= 35;
            }}
            function moveRight() {{
                if (!isGameOver && boatX < canvas.width - 60) boatX += 35;
            }}
            
            function actionDrop() {{
                if (!isGameOver && hookState === 'IDLE') {{
                    hookState = 'DOWN';
                }}
            }}

            window.addEventListener('keydown', (e) => {{
                if (['ArrowLeft', 'KeyA'].includes(e.code) || e.key === 'ArrowLeft') {{
                    moveLeft();
                    e.preventDefault();
                }}
                if (['ArrowRight', 'KeyD'].includes(e.code) || e.key === 'ArrowRight') {{
                    moveRight();
                    e.preventDefault();
                }}
                if (['Space', 'ArrowDown', 'KeyS'].includes(e.code) || e.key === ' ') {{
                    actionDrop();
                    e.preventDefault();
                }}
            }});

            canvas.addEventListener('pointerdown', (e) => {{
                if (isGameOver) return;
                const rect = canvas.getBoundingClientRect();
                const clickX = e.clientX - rect.left;
                const clickY = e.clientY - rect.top;

                if (clickY < 180) {{
                    actionDrop();
                }} else {{
                    if (clickX < canvas.width / 2) {{
                        moveLeft();
                    }} else {{
                        moveRight();
                    }}
                }}
            }});

            function update() {{
                if (isGameOver) return;
                waveOffset += 0.05;

                if (hookState === 'DOWN') {{
                    hookY += 18;
                    if (hookY >= maxHookY) {{
                        hookY = maxHookY;
                        hookState = 'UP';
                    }}
                    fishes.forEach((f, index) => {{
                        let dist = Math.hypot(boatX - f.x, hookY - f.y);
                        if (dist < f.rx + 12) {{
                            caughtFish = f;
                            fishes.splice(index, 1);
                            hookState = 'UP';
                        }}
                    }});
                }} 
                else if (hookState === 'UP') {{
                    hookY -= 18;
                    if (caughtFish) {{
                        caughtFish.x = boatX;
                        caughtFish.y = hookY;
                    }}
                    if (hookY <= 100) {{
                        if (caughtFish) {{
                            score += Math.round(50 / caughtFish.rx * 15);
                            caughtFish = null;
                            let baseSpeed = (Math.random() * 0.6 + 0.8) * SPEED_MUL;
                            let finalSpeed = baseSpeed * (Math.random() < 0.5 ? 1 : -1);
                            fishes.push({{
                                x: Math.random() < 0.5 ? -40 : canvas.width + 40,
                                y: Math.random() * 100 + 300,
                                rx: Math.random() * 5 + 15,
                                ry: Math.random() * 3 + 8,
                                color: ['#ff6b6b', '#feca57', '#ff9ff3', '#48dbfb', '#10ac84', '#e67e22'][Math.floor(Math.random()*6)],
                                speed: finalSpeed
                            }});
                        }}
                        hookState = 'IDLE';
                        hookY = 100;
                    }}
                }}

                fishes.forEach(f => {{
                    if (f !== caughtFish) {{
                        f.x += f.speed;
                        if (f.x > canvas.width + 40) f.speed = -Math.abs(f.speed);
                        if (f.x < -40) f.speed = Math.abs(f.speed);
                    }}
                }});
            }}

            function drawFish(x, y, rx, ry, color, speed, isCaught) {{
                ctx.save();
                ctx.translate(x, y);
                if (speed < 0 && !isCaught) {{
                    ctx.scale(-1, 1);
                }}
                if (isCaught) {{
                    ctx.rotate(Math.PI / 2);
                }}

                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.moveTo(-rx, 0);
                ctx.lineTo(-rx - 10, -ry - 3);
                ctx.lineTo(-rx - 10, ry + 3);
                ctx.closePath();
                ctx.fill();

                ctx.beginPath();
                ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(rx * 0.5, -ry * 0.3, 3, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#000000';
                ctx.beginPath();
                ctx.arc(rx * 0.5, -ry * 0.3, 1, 0, Math.PI * 2);
                ctx.fill();

                ctx.restore();
            }}

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#2ecc71";
                ctx.fillRect(0, 110, canvas.width, 18);

                ctx.fillStyle = "#27ae60";
                for (let i = 0; i < canvas.width; i += 35) {{
                    ctx.beginPath();
                    ctx.arc(i, 114, 12, 0, Math.PI, true);
                    ctx.fill();
                }}

                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
                ctx.lineWidth = 1.5;
                for (let y = 140; y < canvas.height; y += 40) {{
                    ctx.beginPath();
                    for (let x = 0; x < canvas.width; x += 30) {{
                        let waveY = y + Math.sin(x * 0.05 + waveOffset) * 3;
                        if (x === 0) ctx.moveTo(x, waveY);
                        else ctx.lineTo(x, waveY);
                    }}
                    ctx.stroke();
                }}

                ctx.fillStyle = "#b2bec3";
                ctx.fillRect(0, canvas.height - 20, canvas.width, 20);

                ctx.fillStyle = BOAT_COLOR;
                ctx.beginPath();
                ctx.moveTo(boatX - 40, 80);
                ctx.lineTo(boatX + 40, 80);
                ctx.lineTo(boatX + 25, 105);
                ctx.lineTo(boatX - 25, 105);
                ctx.closePath();
                ctx.fill();

                ctx.fillStyle = "white";
                ctx.font = "bold 13px Arial";
                ctx.textAlign = "center";
                ctx.fillText("3", boatX, 98);

                ctx.font = "22px Arial";
                ctx.fillText(CHAR_AVATAR, boatX, 74);

                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.2;
                ctx.beginPath();
                ctx.moveTo(boatX, 100);
                ctx.lineTo(boatX, hookY);
                ctx.stroke();

                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(boatX, hookY, 4, 0, Math.PI * 2);
                ctx.fill();

                fishes.forEach(f => {{
                    drawFish(f.x, f.y, f.rx, f.ry, f.color, f.speed, false);
                }});

                if (caughtFish) {{
                    drawFish(caughtFish.x, caughtFish.y, caughtFish.rx, caughtFish.ry, caughtFish.color, caughtFish.speed, true);
                }}

                let statusText = hookState === 'IDLE' ? "Sẵn sàng câu!" : (hookState === 'DOWN' ? "Đang thả dây..." : "Đang kéo lên!");
                document.getElementById('hudText').innerText = "Điểm: " + score + " | Thời gian: " + timeLeft + "s | " + statusText;
            }}

            function loop() {{
                update();
                draw();
                if (!isGameOver) {{
                    requestAnimationFrame(loop);
                }}
            }}

            loop();
        </script>
    </body>
    </html>
    """

    st.components.v1.html(game_html, height=620)

    col_back, _ = st.columns(2)
    with col_back:
        if st.button("⬅️ Quay lại cài đặt"):
            st.session_state.screen = "select"
            st.rerun()
