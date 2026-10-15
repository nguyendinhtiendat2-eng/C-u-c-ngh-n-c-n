import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Game Câu Cá - Đa Nền Tảng", 
    page_icon="🎣", 
    layout="centered"
)

# Hàm chuyển đổi file MP3 local sang dạng Base64
def get_audio_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            return base64.b64encode(audio_bytes).decode()
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
    st.session_state.difficulty = "Trung bình"
if "enable_music" not in st.session_state:
    st.session_state.enable_music = True

CHARACTERS = [
    {"name": "Bác nông dân", "avatar": "👨‍🌾", "desc": "Kinh nghiệm dạn dày, chuyên câu cá lớn.", "color": "#c0392b"},
    {"name": "Mèo tinh nghịch", "avatar": "🐱", "desc": "Nhanh nhẹn, phản xạ siêu tốc.", "color": "#e67e22"},
    {"name": "Cậu bé tập câu", "avatar": "👦", "desc": "Nhiệt huyết và đam mê khám phá.", "color": "#2980b9"}
]

# --- MÀN HÌNH 1: CÀI ĐẶT TRẬN ĐẤU, NHÂN VẬT & NHẠC NỀN ---
if st.session_state.screen == "select":
    st.title("🎣 CHỌN TÊN & CÀI ĐẶT TRẬN ĐẤU")
    st.write("Hãy thiết lập thông tin và âm nhạc trước khi bắt đầu hành trình chinh phục sông nước!")

    st.session_state.player_name = st.text_input("👤 Tên cần thủ:", value=st.session_state.player_name)

    st.markdown("---")
    st.subheader("1️⃣ Chọn nhân vật:")
    col1, col2, col3 = st.columns(3)
    
    for i, char in enumerate(CHARACTERS):
        with [col1, col2, col3][i]:
            st.markdown(f"<h1 style='text-align: center;'>{char['avatar']}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center;'>{char['name']}</h3>", unsafe_allow_html=True)
            st.write(char['desc'])
            if st.button(f"Chọn {char['name']}", key=f"char_{i}"):
                st.session_state.character = char
                st.success(f"Đã chọn: {char['name']}!")

    st.markdown("---")
    
    col_time, col_diff = st.columns(2)
    with col_time:
        st.subheader("⏱️ Thời gian (giây)")
        st.session_state.game_duration = st.selectbox(
            "Chọn thời lượng:",
            options=[20, 30, 40, 60, 90],
            index=2,
            label_visibility="collapsed"
        )

    with col_diff:
        st.subheader("⚡ Mức độ khó")
        st.session_state.difficulty = st.selectbox(
            "Chọn mức độ:",
            options=["Dễ (Cá chậm)", "Trung bình", "Khó (Cá siêu tốc)"],
            index=1,
            label_visibility="collapsed"
        )

    st.markdown("---")
    st.subheader("🎵 Cài đặt âm nhạc")
    st.session_state.enable_music = st.checkbox("Bật nhạc nền \"Sandwich and story.mp3\"", value=st.session_state.enable_music)

    p_name = st.session_state.player_name if st.session_state.player_name else "Cần thủ"
    st.info(f"Cần thủ: **{p_name}** | Nhân vật: **{st.session_state.character['avatar']} {st.session_state.character['name']}** | Thời gian: **{st.session_state.game_duration}s** | Độ khó: **{st.session_state.difficulty}**")
    
    if st.button("🚀 BẮT ĐẦU VÀO TRẬN CÂU", use_container_width=True):
        st.session_state.screen = "playing"
        st.rerun()

# --- MÀN HÌNH 2: GIAO DIỆN GAME CHÍNH ---
elif st.session_state.screen == "playing":
    player_name = st.session_state.player_name if st.session_state.player_name else "Cần thủ"
    st.title("🌊 Sông Nước Quê Hương")
    st.write(f"💡 **{player_name}** ({st.session_state.character['avatar']} {st.session_state.character['name']}) | Độ khó: **{st.session_state.difficulty}** | Dùng phím PC, chạm màn hình hoặc bấm nút bên dưới để chơi!")

    char_avatar = st.session_state.character['avatar']
    boat_color = st.session_state.character['color']
    duration = str(st.session_state.game_duration)
    
    diff_setting = st.session_state.difficulty
    if "Dễ" in diff_setting:
        speed_multiplier = 0.7
    elif "Khó" in diff_setting:
        speed_multiplier = 1.6
    else:
        speed_multiplier = 1.0

    raw_html = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                margin: 0;
                background: #1e272e;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
            }
            .game-wrapper {
                position: relative;
                cursor: pointer;
                outline: none;
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
            .modal-btn:hover {
                background: #219653;
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
                background: #f1c40f;
                color: #2c3e50;
                border: none;
                padding: 5px 10px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
                cursor: pointer;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                transition: 0.1s;
            }
            .virtual-btn:active {
                transform: scale(0.95);
                background: #d4ac0d;
            }
            .btn-drop {
                width: 130px;
                background: #e74c3c;
                color: white;
            }
            .btn-drop:active {
                background: #c0392b;
            }
            .music-player-box {
                margin-top: 4px;
                width: 750px;
                background: #2f3640;
                padding: 6px 12px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-sizing: border-box;
            }
            .music-player-box span {
                color: #f5f6fa;
                font-size: 13px;
                font-weight: bold;
            }
            .music-player-box audio {
                height: 32px;
                outline: none;
            }
        </style>
    </head>
    <body>
        <div class="game-wrapper" id="gameWrapper">
            <div class="hud" id="hudText">Điểm: 0 | Thời gian: __DURATION__s</div>
            <canvas id="gameCanvas" width="750" height="450" tabindex="0"></canvas>
            
            <div id="scoreModal">
                <h2>🏆 KẾT THÚC TRẬN CÂU 🎣</h2>
                <p>Cần thủ: __PLAYER_NAME__</p>
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

        __MUSIC_PLAYER_HTML__

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
            let hookY = 100;
            const maxHookY = 410;
            let caughtFish = null;
            let waveOffset = 0;
            let isGameOver = false;

            let fishes = [
                {x: 50, y: 310, rx: 18, ry: 10, color: '#ff6b6b', speed: 1.2 * SPEED_MUL},
                {x: 700, y: 370, rx: 16, ry: 9, color: '#feca57', speed: -1.5 * SPEED_MUL},
                {x: 200, y: 400, rx: 20, ry: 12, color: '#ff9ff3', speed: 1.0 * SPEED_MUL},
                {x: 600, y: 340, rx: 15, ry: 8, color: '#48dbfb', speed: -1.3 * SPEED_MUL},
                {x: 350, y: 390, rx: 18, ry: 10, color: '#10ac84', speed: 1.1 * SPEED_MUL}
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
                    hookY += 18;
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
                    hookY -= 18;
                    if (caughtFish) {
                        caughtFish.x = boatX;
                        caughtFish.y = hookY;
                    }
                    if (hookY <= 100) {
                        if (caughtFish) {
                            score += Math.round(50 / caughtFish.rx * 15);
                            caughtFish = null;
                            let baseSpeed = (Math.random() * 0.6 + 0.8) * SPEED_MUL;
                            let finalSpeed = baseSpeed * (Math.random() < 0.5 ? 1 : -1);
                            fishes.push({
                                x: Math.random() < 0.5 ? -40 : canvas.width + 40,
                                y: Math.random() * 100 + 300,
                                rx: Math.random() * 5 + 15,
                                ry: Math.random() * 3 + 8,
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

                let statusText = hookState === 'IDLE' ? "Sẵn sàng câu!" : (hookState === 'DOWN' ? "Đang thả dây..." : "Đang kéo lên!");
                document.getElementById('hudText').innerText = "Điểm: " + score + " | Thời gian: " + timeLeft + "s | " + statusText;
            }

            function loop() {
                update();
                draw();
                if (!isGameOver) {
                    requestAnimationFrame(loop);
                }
            }

            loop();
        </script>
    </body>
    </html>
    """

    # Đọc và mã hóa file MP3 "Sandwich and story.mp3" sang chuỗi Base64
    audio_b64 = get_audio_base64("Sandwich and story.mp3")
    
    if st.session_state.enable_music and audio_b64:
        music_player_html = f'''
        <div class="music-player-box">
            <span>🎵 Sandwich and story.mp3</span>
            <audio controls loop autoplay>
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
        </div>
        '''
    elif st.session_state.enable_music and not audio_b64:
        music_player_html = '''
        <div class="music-player-box">
            <span style="color: #e74c3c;">⚠️ Chưa tìm thấy file Sandwich and story.mp3 trong thư mục!</span>
        </div>
        '''
    else:
        music_player_html = ''

    game_html = raw_html.replace("__DURATION__", duration)\
                         .replace("__PLAYER_NAME__", player_name)\
                         .replace("__BOAT_COLOR__", boat_color)\
                         .replace("__CHAR_AVATAR__", char_avatar)\
            
