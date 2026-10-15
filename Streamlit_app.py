import streamlit as st

st.set_page_config(
    page_title="Game Câu Cá & Chọn Nhân Vật", 
    page_icon="🎣", 
    layout="centered"
)

# Khởi tạo session state
if "screen" not in st.session_state:
    st.session_state.screen = "select"
if "player_name" not in st.session_state:
    st.session_state.player_name = "Cần thủ"
if "character" not in st.session_state:
    st.session_state.character = {"name": "Bác nông dân", "avatar": "👨‍🌾", "color": "#c0392b"}
if "game_duration" not in st.session_state:
    st.session_state.game_duration = 40  # Mặc định 40 giây

CHARACTERS = [
    {"name": "Bác nông dân", "avatar": "👨‍🌾", "desc": "Kinh nghiệm dạn dày, chuyên câu cá lớn.", "color": "#c0392b"},
    {"name": "Mèo tinh nghịch", "avatar": "🐱", "desc": "Nhanh nhẹn, phản xạ siêu tốc.", "color": "#e67e22"},
    {"name": "Cậu bé tập câu", "avatar": "👦", "desc": "Nhiệt huyết và đam mê khám phá.", "color": "#2980b9"}
]

# --- MÀN HÌNH 1: NHẬP TÊN, CHỌN NHÂN VẬT VÀ CÀI ĐẶT ---
if st.session_state.screen == "select":
    st.title("🎣 CHỌN TÊN & CẦN THỦ")
    st.write("Hãy điền tên của bạn, chọn nhân vật đồng hành và thời gian cho chuyến đi câu cá nhé!")

    st.session_state.player_name = st.text_input("👤 Nhập tên của bạn:", value=st.session_state.player_name)

    st.markdown("---")
    st.subheader("Chọn nhân vật:")
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
    
    st.subheader("⏱️ Chọn thời gian trận đấu")
    st.session_state.game_duration = st.selectbox(
        "Chọn thời lượng (giây):",
        options=[20, 30, 40, 60, 90],
        index=2
    )

    p_name = st.session_state.player_name if st.session_state.player_name else "Cần thủ"
    st.info(f"Người chơi: **{p_name}** | Nhân vật: **{st.session_state.character['avatar']} {st.session_state.character['name']}** | Thời gian: **{st.session_state.game_duration} giây**")
    
    if st.button("🚀 BẮT ĐẦU VÀO TRẬN CÂU", use_container_width=True):
        st.session_state.screen = "playing"
        st.rerun()

# --- MÀN HÌNH 2: GIAO DIỆN GAME SÔNG NƯỚC (CÓ NHẠC ZING MP3 "VẾT THƯƠNG") ---
elif st.session_state.screen == "playing":
    player_name = st.session_state.player_name if st.session_state.player_name else "Cần thủ"
    st.title(f"🌊 Sông Nước Quê Hương")
    st.write(f"💡 **Cần thủ:** {player_name} ({st.session_state.character['avatar']} {st.session_state.character['name']}) | Chạm nửa trái/phải để di chuyển, chạm nửa trên để thả câu!")

    char_avatar = st.session_state.character['avatar']
    boat_color = st.session_state.character['color']
    duration = st.session_state.game_duration

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
            }}
            canvas {{
                background: linear-gradient(to bottom, #dff9fb 0%, #74b9ff 28%, #0984e3 28%, #00cec9 100%);
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.5);
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
            .controls {{
                display: flex;
                gap: 10px;
                margin-top: 10px;
                justify-content: center;
                flex-wrap: wrap;
            }}
            .ctrl-btn {{
                background: #f1c40f;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            }}
            .ctrl-btn:active {{
                background: #d4ac0d;
                transform: scale(0.95);
            }}
            .music-box {{
                margin-top: 8px;
                width: 750px;
                border-radius: 12px;
                overflow: hidden;
            }}
        </style>
    </head>
    <body>
        <div class="game-wrapper" id="gameWrapper">
            <div class="hud" id="hudText">Điểm: 0 | Thời gian: {duration}s</div>
            <canvas id="gameCanvas" width="750" height="450"></canvas>
            
            <div id="scoreModal">
                <h2>🏆 KẾT THÚC TRẬN CÂU 🎣</h2>
                <p>Cần thủ: {player_name}</p>
                <p>Tổng điểm: <span id="finalScore">0</span> điểm</p>
                <p style="font-size: 14px; color: #7f8c8d;">Tuyệt vời! Chuyến đi câu đã kết thúc.</p>
                <button class="modal-btn" onclick="location.reload()">Chơi lại ngay 🔄</button>
            </div>
        </div>

        <!-- Khung phát nhạc Zing MP3 chuẩn (Bài Vết Thương) -->
        <div class="music-box">
            <iframe src="https://zingmp3.vn/embed/song/Z6C0DZZ9?autoplay=false" width="100%" height="90" scrolling="no" frameborder="0" allowfullscreen="true"></iframe>
        </div>

        <div class="controls">
            <button class="ctrl-btn" onclick="moveLeft()">◀ Trái</button>
            <button class="ctrl-btn" style="background: #e74c3c; color: white;" onclick="actionDrop()">🎣 Thả Cần</button>
            <button class="ctrl-btn" onclick="moveRight()">Phải ▶</button>
        </div>

        <script>
            const BOAT_COLOR = '{boat_color}';
            const CHAR_AVATAR = '{char_avatar}';

            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');

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
                {{x: 50, y: 310, rx: 18, ry: 10, color: '#ff6b6b', speed: 1.2}},
                {{x: 700, y: 370, rx: 16, ry: 9, color: '#feca57', speed: -1.5}},
                {{x: 200, y: 400, rx: 20, ry: 12, color: '#ff9ff3', speed: 1.0}},
                {{x: 600, y: 340, rx: 15, ry: 8, color: '#48dbfb', speed: -1.3}},
                {{x: 350, y: 390, rx: 18, ry: 10, color: '#10ac84', speed: 1.1}}
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
                if (!isGameOver && boatX > 60) boatX -= 30;
            }}
            function moveRight() {{
                if (!isGameOver && boatX < canvas.width - 60) boatX += 30;
            }}
            
            function actionDrop() {{
                if (!isGameOver && hookState === 'IDLE') {{
                    hookState = 'DOWN';
                }}
            }}

            canvas.addEventListener('click', (e) => {{
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

            window.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowLeft') moveLeft();
                if (e.key === 'ArrowRight') moveRight();
                if (e.code === 'Space') actionDrop();
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
                            fishes.push({{
                                x: Math.random() < 0.5 ? -40 : canvas.width + 40,
                                y: Math.random() * 100 + 300,
                                rx: Math.random() * 5 + 15,
                                ry: Math.random() * 3 + 8,
                                color: ['#ff6b6b', '#feca57', '#ff9ff3', '#48dbfb', '#10ac84', '#e67e22'][Math.floor(Math.random()*6)],
                                speed: (Math.random() * 0.6 + 0.8) * (Math.random() < 0.5 ? 1 : -1)
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

                let statusText = hookState === 'IDLE' ? "Sẵn sàng câu!" : (hookState === 'DOWN' ? "Đang thả dây sâu..." : "Đang kéo lên!");
                document.getElementById('hudText').innerText = "Điểm: " + score + " | Thời gian: " + timeLeft + "s | " + statusText;
            }

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

    st.components.v1.html(game_html, height=650)

    col_back, _ = st.columns(2)
    with col_back:
        if st.button("⬅️ Quay lại chọn nhân vật & cài đặt"):
            st.session_state.screen = "select"
            st.rerun()
  
