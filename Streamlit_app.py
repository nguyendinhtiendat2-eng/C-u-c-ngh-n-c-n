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

# --- MÀN HÌNH 2: GIAO DIỆN GAME SÔNG NƯỚC CHÂN THỰC ---
elif st.session_state.screen == "playing":
    st.title(f"🌊 Sông Nước Quê Hương - Cần thủ: {st.session_state.character['avatar']} {st.session_state.character['name']}")
    st.write("💡 **Hướng dẫn:** Dùng phím **Trái / Phải** di chuyển thuyền. Nhấn **Phím Space (Cách)** để quăng cần câu xuống dòng sông chân thực!")

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
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
            }
            canvas {
                background: linear-gradient(to bottom, #dff9fb 0%, #74b9ff 28%, #0984e3 28%, #00cec9 100%);
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.5);
            }
            .hud {
                position: absolute;
                top: 10px;
                left: 20px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                text-shadow: 1px 1px 2px black;
            }
        </style>
    </head>
    <body>
        <div style="position: relative;">
            <div class="hud" id="hudText">Điểm: 0 | Thời gian: 40s</div>
            <canvas id="gameCanvas" width="750" height="500"></canvas>
        </div>

        <script>
            const BOAT_COLOR = '""" + boat_color + """';
            const CHAR_AVATAR = '""" + char_avatar + """';

            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');

            let score = 0;
            let timeLeft = 40;
            let boatX = 375;
            const targetHookY = 330; 
            let currentHookY = 115;
            let hookState = 'CASTING'; 
            let castProgress = 0;
            let caughtFish = null;
            let waveOffset = 0; // Hiệu ứng gợn sóng sông nước

            let fishes = [
                {x: 50, y: 310, rx: 20, ry: 12, color: '#ff6b6b', speed: 1.0},
                {x: 700, y: 360, rx: 18, ry: 10, color: '#feca57', speed: -1.2},
                {x: 200, y: 410, rx: 22, ry: 14, color: '#ff9ff3', speed: 0.8},
                {x: 600, y: 280, rx: 16, ry: 9, color: '#48dbfb', speed: -1.4},
                {x: 350, y: 440, rx: 20, ry: 12, color: '#10ac84', speed: 0.9}
            ];

            const timer = setInterval(() => {
                timeLeft--;
                if (timeLeft <= 0) {
                    clearInterval(timer);
                    alert("Hết giờ! Tổng điểm câu cá của bạn là: " + score);
                    window.location.reload();
                }
            }, 1000);

            window.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft' && boatX > 60) boatX -= 25;
                if (e.key === 'ArrowRight' && boatX < canvas.width - 60) boatX += 25;
                if (e.code === 'Space' && (hookState === 'WAITING' || hookState === 'REELING')) {
                    hookState = 'CASTING';
                    castProgress = 0;
                    caughtFish = null;
                }
            });

            function update() {
                waveOffset += 0.05; // Cập nhật sóng nước chuyển động

                if (hookState === 'CASTING') {
                    castProgress += 0.08;
                    if (castProgress >= 1) {
                        hookState = 'WAITING';
                        currentHookY = targetHookY;
                    } else {
                        currentHookY = 115 + (targetHookY - 115) * Math.sin(castProgress * Math.PI / 2);
                    }
                } 
                else if (hookState === 'WAITING') {
                    currentHookY = targetHookY;
                    fishes.forEach((f, index) => {
                        let dist = Math.hypot(boatX - f.x, currentHookY - f.y);
                        if (dist < f.rx + 6) {
                            caughtFish = f;
                            fishes.splice(index, 1);
                            hookState = 'REELING';
                        }
                    });
                } 
                else if (hookState === 'REELING') {
                    if (caughtFish) {
                        caughtFish.x = boatX;
                        caughtFish.y -= 6;
                        currentHookY = caughtFish.y;
                        if (caughtFish.y <= 115) {
                            score += Math.round(50 / caughtFish.rx * 15);
                            caughtFish = null;
                            hookState = 'CASTING';
                            castProgress = 0;
                            fishes.push({
                                x: Math.random() < 0.5 ? -40 : canvas.width + 40,
                                y: Math.random() * 160 + 280,
                                rx: Math.random() * 6 + 16,
                                ry: Math.random() * 4 + 9,
                                color: ['#ff6b6b', '#feca57', '#ff9ff3', '#48dbfb', '#10ac84', '#e67e22'][Math.floor(Math.random()*6)],
                                speed: (Math.random() * 0.6 + 0.8) * (Math.random() < 0.5 ? 1 : -1)
                            });
                        }
                    }
                }

                fishes.forEach(f => {
                    f.x += f.speed;
                    if (f.x > canvas.width + 50) {
                        f.speed = -Math.abs(f.speed);
                    } else if (f.x < -50) {
                        f.speed = Math.abs(f.speed);
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
                ctx.moveTo(-3, -ry);
                ctx.lineTo(4, -ry - 6);
                ctx.lineTo(8, -ry);
                ctx.closePath();
                ctx.fill();

                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(rx * 0.5, -ry * 0.3, 3.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#000000';
                ctx.beginPath();
                ctx.arc(rx * 0.5, -ry * 0.3, 1.5, 0, Math.PI * 2);
                ctx.fill();

                ctx.restore();
            }

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // --- CẢNH QUAN VEN SÔNG (BỜ CỎ & CÂY XANH) ---
                ctx.fillStyle = "#2ecc71";
                ctx.fillRect(0, 130, canvas.width, 20); // Bờ cỏ phía trên mặt nước

                // Vẽ các búi cây/cỏ ven bờ
                ctx.fillStyle = "#27ae60";
                for (let i = 0; i < canvas.width; i += 40) {
                    ctx.beginPath();
                    ctx.arc(i, 135, 15, 0, Math.PI, true);
                    ctx.fill();
                }

                // --- HIỆU ỨNG GỢN SÓNG TRÊN DÒNG SÔNG ---
                ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
                ctx.lineWidth = 1.5;
                for (let y = 160; y < canvas.height; y += 45) {
                    ctx.beginPath();
                    for (let x = 0; x < canvas.width; x += 30) {
                        let waveY = y + Math.sin(x * 0.05 + waveOffset) * 4;
                        if (x === 0) ctx.moveTo(x, waveY);
                        else ctx.lineTo(x, waveY);
                    }
                    ctx.stroke();
                }

                // --- ĐÁY SÔNG & RONG RÊU ---
                ctx.fillStyle = "#b2bec3";
                ctx.fillRect(0, canvas.height - 25, canvas.width, 25);
                
                ctx.fillStyle = "#00b894";
                for (let i = 40; i < canvas.width; i += 100) {
                    ctx.beginPath();
                    ctx.moveTo(i, canvas.height - 25);
                    ctx.quadraticCurveTo(i - 15, canvas.height - 70, i + 5, canvas.height - 95);
                    ctx.quadraticCurveTo(i + 20, canvas.height - 50, i + 25, canvas.height - 25);
                    ctx.fill();
                }

                // --- CẦN CÂU VÀ DÂY CÂU ---
                ctx.strokeStyle = '#8B4513';
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.moveTo(boatX + 10, 100);
                let rodTipX = hookState === 'CASTING' ? boatX + 35 + (castProgress * 20) : boatX + 25;
                let rodTipY = hookState === 'CASTING' ? 75 - Math.sin(castProgress * Math.PI) * 15 : 80;
                ctx.lineTo(rodTipX, rodTipY);
                ctx.stroke();

                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(rodTipX, rodTipY);
                ctx.lineTo(boatX, currentHookY);
                ctx.stroke();

                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(boatX, currentHookY, 5, 0, Math.PI * 2);
                ctx.fill();

                // --- THUYỀN VÀ NHÂN VẬT ---
                ctx.fillStyle = BOAT_COLOR;
                ctx.beginPath();
                ctx.moveTo(boatX - 45, 100);
                ctx.lineTo(boatX + 45, 100);
                ctx.lineTo(boatX + 30, 130);
                ctx.lineTo(boatX - 30, 130);
                ctx.closePath();
                ctx.fill();

                ctx.fillStyle = "white";
                ctx.font = "bold 14px Arial";
                ctx.textAlign = "center";
                ctx.fillText("3", boatX, 120);

                ctx.font = "24px Arial";
                ctx.fillText(CHAR_AVATAR, boatX, 90);

                // --- VẼ CÁ ---
                fishes.forEach(f => {
                    drawFish(f.x, f.y, f.rx, f.ry, f.color, f.speed, false);
                });

                if (caughtFish) {
                    drawFish(caughtFish.x, caughtFish.y, caughtFish.rx, caughtFish.ry, caughtFish.color, caughtFish.speed, true);
                }

                let statusText = hookState === 'CASTING' ? "Đang quăng cần..." : (hookState === 'WAITING' ? "Đang chờ cá cắn câu..." : "Đang kéo cá lên!");
                document.getElementById('hudText').innerText = "Điểm: " + score + " | Thời gian: " + timeLeft + "s | Trạng thái: " + statusText;
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

    st.components.v1.html(game_html, height=530)

    col_back, _ = st.columns(2)
    with col_back:
        if st.button("⬅️ Quay lại chọn nhân vật"):
            st.session_state.screen = "select"
            st.rerun()
      
