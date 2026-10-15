import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Game Câu Cá - Sông Nước Quê Hương", 
    page_icon="🎣", 
    layout="centered"
)

def get_audio_base64(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as audio_file:
                return base64.b64encode(audio_file.read()).decode()
    except Exception:
        pass
    return None

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

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #ffffff;
    }
    .main-title {
        text-align: center;
        font-size: 30px;
        font-weight: 900;
        color: #38bdf8;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-size: 14px;
        color: #94a3b8;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }
    .section-label {
        text-align: center;
        font-size: 15px;
        font-weight: bold;
        color: #cbd5e1;
        margin: 12px 0 6px 0;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# --- MÀN HÌNH 1: CÀI ĐẶT TRẬN ĐẤU & GIAO DIỆN MÀN HÌNH BẮT ĐẦU ---
if st.session_state.screen == "select":
    st.markdown("<div class='main-title'>🌊 SÔNG NƯỚC QUÊ HƯƠNG 🌊</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>🎣 ĐẠI CHIẾN CÂU CÁ 🎣</div>", unsafe_allow_html=True)

    st.session_state.player_name = st.text_input("👤 Tên cần thủ:", value=st.session_state.player_name)

    st.markdown("<div class='section-label'>🎵 ÂM NHẠC NỀN</div>", unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if st.button("🎵 Bật Nhạc", use_container_width=True, type="primary" if st.session_state.enable_music else "secondary"):
            st.session_state.enable_music = True
            st.rerun()
    with col_m2:
        if st.button("🔇 Tắt Nhạc", use_container_width=True, type="primary" if not st.session_state.enable_music else "secondary"):
            st.session_state.enable_music = False
            st.rerun()

    col_time_left, col_diff_right = st.columns(2)
    
    with col_time_left:
        st.markdown("<div class='section-label'>⏱️ THỜI GIAN (GIÂY)</div>", unsafe_allow_html=True)
        durations = [20, 30, 40, 60, 90]
        curr_idx = durations.index(st.session_state.game_duration) if st.session_state.game_duration in durations else 2
        st.session_state.game_duration = st.selectbox(
            "Thời gian trận đấu:",
            options=durations,
            index=curr_idx,
            label_visibility="collapsed"
        )

    with col_diff_right:
        st.markdown("<div class='section-label'>⚡ ĐỘ KHÓ</div>", unsafe_allow_html=True)
        diffs = ["Dễ", "Vừa", "Khó"]
        curr_diff_idx = diffs.index(st.session_state.difficulty) if st.session_state.difficulty in diffs else 1
        st.session_state.difficulty = st.selectbox(
            "Mức độ khó:",
            options=diffs,
            index=curr_diff_idx,
            label_visibility="collapsed"
        )

    st.markdown("<div class='section-label'>👨‍🌾 CHỌN CẦN THỦ</div>", unsafe_allow_html=True)
    c_col1, c_col2, c_col3 = st.columns(3)
    for i, char in enumerate(CHARACTERS):
        with [c_col1, c_col2, c_col3][i]:
            is_selected = (st.session_state.character["name"] == char["name"])
            btn_label = f"{char['avatar']} {char['name']}"
            if st.button(btn_label, use_container_width=True, type="primary" if is_selected else "secondary"):
                st.session_state.character = char
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 BẮT ĐẦU CÂU CÁ 🎣", use_container_width=True, type="primary"):
        st.session_state.screen = "playing"
        st.rerun()

# --- MÀN HÌNH 2: GIAO DIỆN GAME CHÍNH ---
elif st.session_state.screen == "playing":
    player_name = st.session_state.player_name if st.session_state.player_name else "Cần thủ"
    st.title("🌊 Sông Nước Quê Hương")
    st.write(f"💡 **{player_name}** ({st.session_state.character['avatar']} {st.session_state.character['name']}) | Thời gian: **{st.session_state.game_duration}s** | Độ khó: **{st.session_state.difficulty}**")

    audio_b64 = get_audio_base64("Sandwich and story.mp3")
    audio_html = ""
    if st.session_state.enable_music and audio_b64:
        audio_html = f'''
        <div style="margin-top: 6px; width: 750px; background: #1e293b; padding: 8px 14px; border-radius: 10px; display: flex; align-items: center; justify-content: space-between; box-sizing: border-box; border: 1px solid #38bdf8;">
            <span style="color: #38bdf8; font-size: 13px; font-weight: bold;">🎵 Sandwich and story.mp3</span>
            <audio controls loop autoplay style="height: 30px; outline: none;">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
        </div>
        '''

    char_avatar = st.session_state.character['avatar']
    boat_color = st.session_state.character['color']
    duration_val = int(st.session_state.game_duration)
    
    # Tốc độ cá bơi siêu nhanh theo từng mức độ
    diff_setting = st.session_state.difficulty
    if diff_setting == "Dễ":
        speed_mul = 2.0
    elif diff_setting == "Khó":
        speed_mul = 4.5
    else:
        speed_mul = 3.0

    html_code = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                margin: 0;
                background: #0f172a;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
            }
            .game-wrapper {
                position: relative;
            }
            canvas {
                background: linear-gradient(to bottom, #dff9fb 0%, #74b9ff 28%, #0984e3 28%, #00cec9 100%);
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.5);
                touch-action: none;
            }
            .hud {
                position: absolute;
                top: 10px;
                left: 15px;
                color: white;
                font-size: 15px;
                font-weight: bold;
                text-shadow: 1px 1px 2px black;
                z-index: 10;
                pointer-events: none;
            }
            .score-badge {
                position: absolute;
                top: 10px;
                right: 15px;
                background: #f43f5e;
                color: white;
                padding: 4px 12px;
                border-radius: 15px;
                font-size: 15px;
                font-weight: bold;
                box-shadow: 0 2px 6px rgba(0,0,0,0.4);
                z-index: 10;
                pointer-events: none;
            }
            #scoreModal {
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
            }
            #scoreModal h2 {
                color: #2c3e50;
                margin-top: 0;
            }
            #scoreModal p {
                font-size: 18px;
                color: #e74c3c;
                font-weight: bold;
            }
            .modal-btn {
                background: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                margin-top: 10px;
            }
            .on-screen-controls {
                display: flex;
                gap: 8px;
                margin-top: 6px;
                justify-content: center;
                width: 750px;
            }
            .virtual-btn {
                width: 110px;
                background: #38bdf8;
                color: #0f172a;
                border: none;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 5px;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .virtual-btn:active {
                transform: scale(0.95);
            }
            .btn-drop {
                width: 130px;
                background: #f43f5e;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="game-wrapper">
            <div class="hud" id="hudText">⏱️ Thời gian: VAR_DURATIONs | Trạng thái: Sẵn sàng</div>
            <div class="score-badge" id="scoreBadge">🏆 Điểm: 0</div>
            <canvas id="gameCanvas" width="750" height="450" tabindex="0"></canvas>
            
            <div id="scoreModal">
                <h2>🏆 KẾT THÚC TRẬN CÂU 🎣</h2>
                <p>Cần thủ: VAR_PLAYER_NAME</p>
                <p>Tổng điểm: <span id="finalScore">0</span> điểm</p>
                <button class="modal-btn" onclick="location.reload()">Chơi lại ngay 🔄</button>
            </div>
        </div>

        <div class="on-screen-controls">
            <button class="virtual-btn" onclick="moveLeft()">◀ Trái</button>
            <button class="virtual-btn btn-drop" onclick="actionDrop()">🎣 Thả Cần</button>
            <button class="virtual-btn" onclick="moveRight()">Phải ▶</button>
        </div>

        VAR_AUDIO_HTML

        <script>
            const BOAT_COLOR = 'VAR_BOAT_COLOR';
            const CHAR_AVATAR = 'VAR_CHAR_AVATAR';
            const SPEED_MUL = VAR_SPEED_MUL;

            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            canvas.focus();

            let score = 0;
            let timeLeft = VAR_DURATION;
            let boatX = 375;
            
            let hookState = 'IDLE';
            let hookY = 100;
            const maxHookY = 410;
            let caughtFish = null;
            let waveOffset = 0;
            let isGameOver = false;

            let fishes = [
                {x: 50, y: 320, rx: 18, ry: 10, color: '#ff6b6b', speed: 2.2 * SPEED_MUL},
                {x: 700, y: 380, rx: 16, ry: 9, color: '#feca57', speed: -2.5 * SPEED_MUL},
                {x: 350, y: 410, rx: 20, ry: 12, color: '#48dbfb', speed: 2.3 * SPEED_MUL},
                {x: 200, y: 350, rx: 15, ry: 8, color: '#ff9ff3', speed: -2.7 * SPEED_MUL}
            ];

            const timer = setInterval(() => {
                if (!isGameOver) {
                    timeLeft--;
                    if (timeLeft <= 0) {
                        clearInterval(timer);
                        isGameOver = true;
                        document.getElementById('finalScore').innerText = score;
                        document.getElementById('scoreModal').style.display = 'block';
                    }
                }
            }, 1000);

            function moveLeft() {
                if (!isGameOver && boatX > 60) boatX -= 35;
            }
            function moveRight() {
                if (!isGameOver && boatX < canvas.width - 60) boatX += 35;
            }
            
            function actionDrop() {
                if (!isGameOver && hookState === 'IDLE') {
                    hookState = 'DOWN';
                }
            }

            window.addEventListener('keydown', (e) => {
                if (['ArrowLeft', 'KeyA'].includes(e.code) || e.key === 'ArrowLeft') {
                    moveLeft();
                    e.preventDefault();
                }
                if (['ArrowRight', 'KeyD'].includes(e.code) || e.key === 'ArrowRight') {
                    moveRight();
                    e.preventDefault();
                }
                if (['Space', 'ArrowDown', 'KeyS'].includes(e.code) || e.key === ' ') {
                    actionDrop();
                    e.preventDefault();
                }
            });

            canvas.addEventListener('pointerdown', (e) => {
                if (isGameOver) return;
                const rect = canvas.getBoundingClientRect();
                const clickX = e.clientX - rect.left;
                const clickY = e.clientY - rect.top;

                if (clickY < 180) {
                    actionDrop();
                } else {
                    if (clickX < canvas.width / 2) {
                        moveLeft();
                    } else {
                        moveRight();
                    }
                }
            });

            function update() {
                if (isGameOver) return;
                waveOffset += 0.05;

                if (hookState === 'DOWN') {
                    hookY += 24;
                    if (hookY >= maxHookY) {
                        hookY = maxHookY;
                        hookState = 'UP';
                    }
                    fishes.forEach((f, index) => {
                        let dist = Math.hypot(boatX - f.x, hookY - f.y);
                        if (dist < f.rx + 12) {
                            caughtFish = f;
                            fishes.splice(index, 1);
                            hookState = 'UP';
                        }
                    });
                } 
                else if (hookState === 'UP') {
                    hookY -= 24;
                    if (caughtFish) {
                        caughtFish.x = boatX;
                        caughtFish.y = hookY;
                    }
                    if (hookY <= 100) {
                        if (caughtFish) {
                            score += Math.round(50 / caughtFish.rx * 15);
                            caughtFish = null;
                            let baseSpeed = (Math.random() * 1.0 + 1.8) * SPEED_MUL;
                            let finalSpeed = baseSpeed * (Math.random() < 0.5 ? 1 : -1);
                            fishes.push({
                                x: Math.random() < 0.5 ? -40 : canvas.width + 40,
                                y: Math.random() * 120 + 280,
                                rx: Math.random() * 6 + 14,
                                ry: Math.random() * 4 + 7,
                                color: ['#ff6b6b', '#feca57', '#ff9ff3', '#48dbfb', '#10ac84', '#e67e22'][Math.floor(Math.random()*6)],
                                speed: finalSpeed
                            });
                        }
                        hookState = 'IDLE';
                        hookY = 100;
                    }
                }

                fishes.forEach(f => {
                    if (f !== caughtFish) {
                        f.x += f.speed;
                        if (f.x > canvas.width + 40) f.speed = -Math.abs(f.speed);
                        if (f.x < -40) f.speed = Math.abs(f.speed);
                    }
                });
            }

            function drawFish(x, y, rx, ry, color, speed, isCaught) {
                ctx.save();
                ctx.translate(x, y);
                if (speed < 0 && !isCaught) {
                    ctx.scale(-1, 1);
                }
                if (isCaught) {
                    ctx.rotate(Math.PI / 2);
                }

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
            }

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#2ecc71";
                ctx.fillRect(0, 110, canvas.width, 18);

                ctx.fillStyle = "#27ae60";
                for (let i = 0; i < canvas.width; i += 35) {
                    ctx.beginPath();
                    ctx.arc(i, 114, 12, 0, Math.PI, true);
                    ctx.fill();
                }

                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
                ctx.lineWidth = 1.5;
                for (let y = 140; y < canvas.height; y += 40) {
                    ctx.beginPath();
                    for (let x = 0; x < canvas.width; x += 30) {
                        let waveY = y + Math.sin(x * 0.05 + waveOffset) * 3;
                        if (x === 0) ctx.moveTo(x, waveY);
                        else ctx.lineTo(x, waveY);
                    }
                    ctx.stroke();
                }

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

                fishes.forEach(f => {
                    drawFish(f.x, f.y, f.rx, f.ry, f.color, f.speed, false);
                });

                if (caughtFish) {
                    drawFish(caughtFish.x, caughtFish.y, caughtFish.rx, caughtFish.ry, caughtFish.color, caughtFish.speed, true);
                }

                let statusText = hookState === 'IDLE' ? "Sẵn sàng" : (hookState === 'DOWN' ? "Đang thả dây" : "Đang kéo cá");
                document.getElementById('hudText').innerText = "⏱️ Thời gian: " + timeLeft + "s | Trạng thái: " + statusText;
                document.getElementById('scoreBadge').innerText = "🏆 Điểm: " + score;
            }

            function loop() {
                update();
                draw();
     
