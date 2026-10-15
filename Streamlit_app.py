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

# --- MÀN HÌNH 1: CÀI ĐẶT TRẬN ĐẤU & GIAO DIỆN CHỦ ĐỀ CÂU CÁ ---
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

# --- MÀN HÌNH 2: GIAO DIỆN GAME CHÍNH (ĐỒ HỌA CHÂN THỰC & SỐNG ĐỘNG) ---
elif st.session_state.screen == "playing":
    player_name = st.session_state.player_name if st.session_state.player_name else "Cần thủ"
    st.title("🌊 Sông Nước Quê Hương")
    st.write(f"💡 **{player_name}** ({st.session_state.character['avatar']} {st.session_state.character['name']}) | Thời gian: **{st.session_state.game_duration}s** | Độ khó: **{st.session_state.difficulty}**")

    audio_b64 = get_audio_base64("Sandwich and story.mp3")
    audio_tag = ""
    if st.session_state.enable_music and audio_b64:
        audio_tag = f'''
        <div style="margin-top: 6px; width: 750px; background: #1e293b; padding: 8px 14px; border-radius: 10px; display: flex; align-items: center; justify-content: space-between; box-sizing: border-box; border: 1px solid #38bdf8;">
            <span style="color: #38bdf8; font-size: 13px; font-weight: bold;">🎵 Sandwich and story.mp3</span>
            <audio controls loop autoplay style="height: 30px; outline: none;">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
        </div>
        '''

    char_avatar = st.session_state.character['avatar']
    boat_color = st.session_state.character['color']
    duration_str = str(int(st.session_state.game_duration))
    
    diff_setting = st.session_state.difficulty
    if diff_setting == "Dễ":
        speed_multiplier = "1.0"
    elif diff_setting == "Khó":
        speed_multiplier = "2.8"
    else:
        speed_multiplier = "1.8"

    raw_html = """
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
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .game-wrapper {
                position: relative;
                cursor: pointer;
                outline: none;
            }
            canvas {
                background: linear-gradient(to bottom, #a0e9ff 0%, #38bdf8 25%, #0284c7 25%, #0369a1 60%, #0c4a6e 100%);
                border-radius: 14px;
                box-shadow: 0 12px 30px rgba(0,0,0,0.6);
                touch-action: none;
            }
            .hud {
                position: absolute;
                top: 12px;
                left: 18px;
                color: #ffffff;
                font-size: 16px;
                font-weight: 800;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
                z-index: 10;
                pointer-events: none;
            }
            #scoreModal {
                display: none;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(15, 23, 42, 0.95);
                border: 2px solid #38bdf8;
                padding: 35px;
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.8);
                text-align: center;
                z-index: 100;
                width: 340px;
                color: white;
            }
            #scoreModal h2 {
                color: #38bdf8;
                margin-top: 0;
                font-size: 24px;
            }
            #scoreModal p {
                font-size: 20px;
                color: #f43f5e;
                font-weight: bold;
            }
            .modal-btn {
                background: linear-gradient(135deg, #22c55e, #16a34a);
                color: white;
                border: none;
                padding: 12px 25px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                cursor: pointer;
                margin-top: 15px;
                box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
                transition: 0.2s;
            }
            .modal-btn:hover {
                transform: scale(1.05);
            }
            .on-screen-controls {
                display: flex;
                gap: 12px;
                margin-top: 10px;
                justify-content: center;
                width: 750px;
            }
            .virtual-btn {
                width: 120px;
                background: linear-gradient(135deg, #38bdf8, #0284c7);
                color: #ffffff;
                border: none;
                padding: 10px 14px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(56, 189, 248, 0.3);
                transition: 0.1s;
            }
            .virtual-btn:active {
                transform: scale(0.95);
            }
            .btn-drop {
                width: 140px;
                background: linear-gradient(135deg, #f43f5e, #e11d48);
                color: white;
                box-shadow: 0 4px 10px rgba(244, 63, 94, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="game-wrapper" id="gameWrapper">
            <div class="hud" id="hudText">🐟 Điểm: 0 | ⏱️ Thời gian: __DURATION__s</div>
            <canvas id="gameCanvas" width="750" height="450" tabindex="0"></canvas>
            
            <div id="scoreModal">
                <h2>🏆 KẾT THÚC TRẬN CÂU 🎣</h2>
                <p>Cần thủ: __PLAYER_NAME__</p>
                <p>Tổng điểm: <span id="finalScore">0</span> điểm</p>
                <p style="font-size: 13px; color: #94a3b8;">Chuyến đi câu tuyệt vời đã khép lại!</p>
                <button class="modal-btn" onclick="location.reload()">Chơi Lại Ngay 🔄</button>
            </div>
        </div>

        <div class="on-screen-controls">
            <button class="virtual-btn" onclick="moveLeft()">◀ Trái</button>
            <button class="virtual-btn btn-drop" onclick="actionDrop()">🎣 Thả Cần</button>
            <button class="virtual-btn" onclick="moveRight()">Phải ▶</button>
        </div>

        __AUDIO_TAG__

        <script>
            const BOAT_COLOR = '__BOAT_COLOR__';
            const CHAR_AVATAR = '__CHAR_AVATAR__';
            const SPEED_MUL = __SPEED_MUL__;

            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            canvas.focus();

            let score = 0;
            let timeLeft = __DURATION__;
            let boatX = 375;
            
            let hookState = 'IDLE';
            let hookY = 110;
            const maxHookY = 415;
            let caughtFish = null;
            let waveOffset = 0;
            let isGameOver = false;

            let fishes = [
                {x: 50, y: 320, rx: 20, ry: 11, color: '#ff6b6b', speed: 1.5 * SPEED_MUL},
                {x: 700, y: 380, rx: 16, ry: 9, color: '#feca57', speed: -1.8 * SPEED_MUL},
                {x: 350, y: 410, rx: 24, ry: 13, color: '#48dbfb', speed: 1.6 * SPEED_MUL},
                {x: 200, y: 350, rx: 15, ry: 8, color: '#ff9ff3', speed: -2.0 * SPEED_MUL}
            ];

            let bubbles = Array.from({length: 12}, () => ({
                x: Math.random() * 750,
                y: Math.random() * 300 + 150,
                radius: Math.random() * 3 + 1,
                speed: Math.random() * 0.8 + 0.4
            }));

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
                waveOffset += 0.04;

                bubbles.forEach(b => {
                    b.y -= b.speed;
                    if (b.y < 120) b.y = 440;
                });

                if (hookState === 'DOWN') {
                    hookY += 22;
                    if (hookY >= maxHookY) {
                        hookY = maxHookY;
                        hookState = 'UP';
                    }
                    fishes.forEach((f, index) => {
                        let dist = Math.hypot(boatX - f.x, hookY - f.y);
                        if (dist < f.rx + 14) {
                            caughtFish = f;
                            fishes.splice(index, 1);
                            hookState = 'UP';
                        }
                    });
                } 
                else if (hookState === 'UP') {
                    hookY -= 22;
                    if (caughtFish) {
                        caughtFish.x = boatX;
                        caughtFish.y = hookY;
                    }
                    if (hookY <= 110) {
                        if (caughtFish) {
                            score += Math.round(60 / caughtFish.rx * 20);
                            caughtFish = null;
                            let baseSpeed = (Math.random() * 0.8 + 1.4) * SPEED_MUL;
                            let finalSpeed = baseSpeed * (Math.random() < 0.5 ? 1 : -1);
                            fishes.push({
                                x: Math.random() < 0.5 ? -40 : canvas.width + 40,
                                y: Math.random() * 150 + 260,
                                rx: Math.random() * 8 + 14,
                                ry: Math.random() * 5 + 7,
                                color: ['#ff6b6b', '#feca57', '#ff9ff3', '#48dbfb', '#10ac84', '#e67e22'][Math.floor(Math.random()*6)],
                                speed: finalSpeed
                            });
                        }
                        hookState = 'IDLE';
                        hookY = 110;
                    }
                }

                fishes.forEach(f => {
                    if (f !== caughtFish) {
                        f.x += f.speed;
                        if (f.x > canvas.width + 50) f.speed = -Math.abs(f.speed);
                        if (f.x < -50) f.speed = Math.abs(f.speed);
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
                ctx.lineTo(-rx - 12, -ry - 4);
                ctx.lineTo(-rx - 12, ry + 4);
                ctx.closePath();
                ctx.fill();

                ctx.beginPath();
                ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(0, -ry);
                ctx.lineTo(-6, -ry - 8);
                ctx.lineTo(6, -ry);
                ctx.closePath();
                ctx.fill();

                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(rx * 0.5, -ry * 0.3, 3.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#1e293b';
                ctx.beginPath();
                ctx.arc(rx * 0.5, -ry * 0.3, 1.5, 0, Math.PI * 2);
                ctx.fill();

                ctx.restore();
            }

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#15803d";
                ctx.fillRect(0, 105, canvas.width, 22);

                ctx.fillStyle = "#16a34a";
                for (let i = 0; i < canvas.width; i += 30) {
                    ctx.beginPath();
                    ctx.arc(i, 110, 14, 0, Math.PI, true);
                    ctx.fill();
                }

                ctx.strokeStyle = "rgba(255, 255, 255, 0.35)";
                ctx.lineWidth = 1.8;
                for (let y = 145; y < canvas.height - 10; y += 45) {
                    ctx.beginPath();
                    for (let x = 0; x < canvas.width; x += 25) {
                        let waveY = y + Math.sin(x * 0.04 + waveOffset) * 4;
                        if (x === 0) ctx.moveTo(x, waveY);
                        else ctx.lineTo(x, waveY);
                    }
                    ctx.stroke();
                }

                ctx.fillStyle = "rgba(255, 255, 255, 0.4)";
                bubbles.forEach(b => {
                    ctx.beginPath();
                    ctx.arc(b.x, b.y, b.radius, 0, Math.PI * 2);
                    ctx.fill();
                });

                ctx.fillStyle = "#334155";
                ctx.fillRect(0, canvas.height - 15, canvas.width, 15);

                ctx.fillStyle = BOAT_COLOR;
                ctx.beginPath();
                ctx.moveTo(boatX - 45, 75);
                ctx.lineTo(boatX + 45, 75);
                ctx.lineTo(boatX + 28, 106);
                ctx.lineTo(boatX - 28, 106);
                ctx.closePath();
                ctx.fill();

                ctx.strokeStyle = "rgba(255,255,255,0.4)";
                ctx.lineWidth = 2;
                ctx.stroke();

                ctx.fillStyle = "white";
                ctx.font = "bold 12px Arial";
                ctx.textAlign = "center";
                ctx.fillText("🎣", boatX, 98);

                ctx.font 
