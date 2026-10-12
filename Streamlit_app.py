import streamlit as st

st.set_page_config(
    page_title="Game Câu Cá & Chọn Nhân Vật", 
    page_icon="🎣", 
    layout="centered"
)

# Khởi tạo session state
if "screen" not in st.session_state:
    st.session_state.screen = "select"
if "character" not in st.session_state:
    st.session_state.character = {"name": "Bác nông dân", "avatar": "👨‍🌾", "color": "#c0392b"}

CHARACTERS = [
    {"name": "Bác nông dân", "avatar": "👨‍🌾", "desc": "Kinh nghiệm dạn dày, chuyên câu cá lớn.", "color": "#c0392b"},
    {"name": "Mèo tinh nghịch", "avatar": "🐱", "desc": "Nhanh nhẹn, phản xạ siêu tốc.", "color": "#e67e22"},
    {"name": "Cậu bé tập câu", "avatar": "👦", "desc": "Nhiệt huyết và đam mê khám phá.", "color": "#2980b9"}
]

# --- MÀN HÌNH 1: CHỌN NHÂN VẬT ---
if st.session_state.screen == "select":
    st.title("🎣 CHỌN CẦN THỦ CỦA BẠN")
    st.write("Hãy chọn một nhân vật đồng hành cùng bạn trong chuyến đi câu cá này nhé!")

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
    st.info(f"Nhân vật hiện tại: **{st.session_state.character['avatar']} {st.session_state.character['name']}**")
    
    if st.button("🚀 BẮT ĐẦU VÀO TRẬN CÂU", use_container_width=True):
        st.session_state.screen = "playing"
        st.rerun()

# --- MÀN HÌNH 2: GIAO DIỆN GAME SÔNG NƯỚC (ĐÃ FIX TRIỆT ĐỂ LỖI ĐƠ CÁ) ---
elif st.session_state.screen == "playing":
    st.title(f"🌊 Sông Nước Quê Hương - Cần thủ: {st.session_state.character['avatar']} {st.session_state.character['name']}")
    st.write("💡 **Hướng dẫn:** Dùng nút **Trái / Phải** di chuyển thuyền. Nhấn nút **Thả Cần** để thả dây xuống nước và kéo cá lên khi cá cắn câu!")

    char_avatar = st.session_state.character['avatar']
    boat_color = st.session_state.character['color']

    game_html = """
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
            }
            canvas {
                background: linear-gradient(to bottom, #dff9fb 0%, #74b9ff 28%, #0984e3 28%, #00cec9 100%);
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.5);
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
            }
            .controls {
                display: flex;
                gap: 12px;
                margin-top: 12px;
                justify-content: center;
            }
            .ctrl-btn {
                background: #f1c40f;
                border: none;
                padding: 10px 22px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            }
            .ctrl-btn:active {
                background: #d4ac0d;
                transform: scale(0.95);
            }
        </style>
    </head>
    <body>
        <div class="game-wrapper">
            <div class="hud" id="hudText">Điểm: 0 | Thời gian: 40s</div>
            <canvas id="gameCanvas" width="750" height="450"></canvas>
        </div>

        <div class="controls">
            <button class="ctrl-btn" onclick="moveLeft()">◀ Trái</button>
            <button class="ctrl-btn" style="background: #e74c3c; color: white;" onclick="actionSpace()">🎣 Thả Cần</button>
            <button class="ctrl-btn" onclick="moveRight()">Phải ▶</button>
        </div>

        <script>
            const BOAT_COLOR = '""" + boat_color + """';
            const CHAR_AVATAR = '""" + char_avatar + """';

            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');

            let score = 0;
            let timeLeft = 40;
            let boatX = 375;
            const hookY = 300; 
            let currentHookY = 95;
            let hookState = 'IDLE'; 
            let targetFish = null; 
            let waveOffset = 0;

            let fishes = [
                {x: 50, y: 280, rx: 18, ry: 10, color: '#ff6b6b'},
                {x: 700, y: 330, rx: 16, ry: 9, color: '#feca57'},
                {x: 200, y: 380, rx: 20, ry: 12, color: '#ff9ff3'},
                {x: 600, y: 260, rx: 15, ry: 8, color: '#48dbfb'},
                {x: 350, y: 400, rx: 18, ry: 10, color: '#10ac84'}
            ];

            const timer = setInterval(() => {
                timeLeft--;
                if (timeLeft <= 0) {
                    clearInterval(timer);
                    alert("Hết giờ! Tổng điểm câu cá của bạn là: " + score);
                    window.location.reload();
                }
            }, 1000);

            function moveLeft() {
                if (boatX > 60) boatX -= 30;
            }
            function moveRight() {
                if (boatX < canvas.width - 60) boatX += 30;
            }
            function actionSpace() {
                if (hookState === 'IDLE') {
                    hookState = 'DROPPING';
                }
            }

            window.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft') moveLeft();
                if (e.key === 'ArrowRight') moveRight();
                if (e.code === 'Space') actionSpace();
            });

            function update() {
                waveOffset += 0.05;

                if (hookState === 'DROPPING') {
                    currentHookY += 10;
                    if (currentHookY >= hookY) {
                        currentHookY = hookY;
                        hookState = 'WAITING';
                        if (fishes.length > 0) {
                            targetFish = fishes[Math.floor(Math.random() * fishes.length)];
                        }
                    }
                } 
                else if (hookState === 'WAITING') {
                    if (targetFish) {
                        let angle = Math.atan2(hookY - targetFish.y, boatX - targetFish.x);
                        targetFish.x += Math.cos(angle) * 2.5;
                        targetFish.y += Math.sin(angle) * 2.0;

                        let dist = Math.hypot(boatX - targetFish.x, hookY - targetFish.y);
                        if (dist < targetFish.rx + 10) {
                            hookState = 'REELING';
                        }
                    } else {
                        hookState = 'IDLE';
                    }
                } 
                else if (hookState === 'REELING') {
                    if (targetFish) {
                        targetFish.x = boatX;
                        targetFish.y -= 12; // Kéo cá lên nhanh và dứt khoát
                        currentHookY = targetFish.y;
                        
                        // Đảm bảo khi cá lên tới mốc mặt nước (<= 95) sẽ được xử lý gọn gàng ngay lập tức
                        if (targetFish.y <= 95) {
                            score += Math.round(50 / targetFish.rx * 15);
                            fishes = fishes.filter(f => f !== targetFish);
                            targetFish = null;
                            hookState = 'IDLE';
                            currentHookY = 95;

                            // Sinh cá mới bơi vào màn hình
                            fishes.push({
                                x: Math.random() < 0.5 ? -40 : canvas.width + 40,
                                y: Math.random() * 120 + 260,
                                rx: Math.random() * 5 + 15,
                                ry: Math.random() * 3 + 8,
                                color: ['#ff6b6b', '#feca57', '#ff9ff3', '#48dbfb', '#10ac84', '#e67e22'][Math.floor(Math.random()*6)]
                            });
                        }
                    } else {
                        hookState = 'IDLE';
                        currentHookY = 95;
                    }
                }

                fishes.forEach(f => {
                    if (f !== targetFish || hookState !== 'WAITING') {
                        f.x += (Math.random() - 0.5) * 2;
                        f.y += (Math.random() - 0.5) * 1;
                        if (f.x < 40) f.x = 40;
                        if (f.x > canvas.width - 40) f.x = canvas.width - 40;
                        if (f.y < 180) f.y = 180;
                        if (f.y > canvas.height - 35) f.y = canvas.height - 35;
                    }
                });
            }

            function drawFish(x, y, rx, ry, color, isCaught) {
                ctx.save();
                ctx.translate(x, y);
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

                // Bờ cỏ ven sông
                ctx.fillStyle = "#2ecc71";
                ctx.fillRect(0, 110, canvas.width, 18);

                ctx.fillStyle = "#27ae60";
                for (let i = 0; i < canvas.width; i += 35) {
                    ctx.beginPath();
                    ctx.arc(i, 114, 12, 0, Math.PI, true);
                    ctx.fill();
                }

                // Sóng nước sông
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

                // Đáy sông
                ctx.fillStyle = "#b2bec3";
                ctx.fillRect(0, canvas.height - 20, canvas.width, 20);

                // Thuyền & Nhân vật
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

                // Cần câu & Dây câu
                ctx.strokeStyle = '#8B4513';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(boatX + 8, 80);
                ctx.lineTo(boatX + 20, 62);
                ctx.stroke();

                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.2;
                ctx.beginPath();
                ctx.moveTo(boatX + 20, 62);
                ctx.lineTo(boatX, currentHookY);
                ctx.stroke();

                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(boatX, currentHookY, 4, 0, Math.PI * 2);
                ctx.fill();

                // Vẽ cá
                fishes.forEach(f => {
                    let isCaught = (f === targetFish && hookState === 'REELING');
                    drawFish(f.x, f.y, f.rx, f.ry, f.color, isCaught);
                });

                let statusText = hookState === 'IDLE' ? "Nhấn Thả Cần để câu!" : (hookState === 'DROPPING' ? "Đang thả dây..." : (hookState === 'WAITING' ? "Cá đang bơi tới..." : "Đang kéo lên!"));
                document.getElementById('hudText').innerText = "Điểm: " + score + " | Thời gian: " + timeLeft + "s | " + statusText;
            }

            function loop() {
                update();
                draw();
                requestAnimationFrame(loop);
            }

            loop();
        </script>
    </body>
    </html>
    """

    st.components.v1.html(game_html, height=520)

    col_back, _ = st.columns(2)
    with col_back:
        if st.button("⬅️ Quay lại chọn nhân vật"):
            st.session_state.screen = "select"
            st.rerun()
                                  
