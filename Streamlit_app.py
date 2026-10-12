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

# --- MÀN HÌNH 2: GIAO DIỆN GAME SÔNG NƯỚC (CÁ TỰ BƠI ĐẾN DÂY CÂU) ---
elif st.session_state.screen == "playing":
    st.title(f"🌊 Sông Nước Quê Hương - Cần thủ: {st.session_state.character['avatar']} {st.session_state.character['name']}")
    st.write("💡 **Hướng dẫn:** Dùng phím **Trái / Phải** di chuyển thuyền. Nhấn **Phím Space (Cách)** để thả dây câu xuống nước, một chú cá ngẫu nhiên sẽ tự bơi tới cắn câu!")

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
            const hookY = 330; // Độ sâu cố định của móc câu dưới nước
            let currentHookY = 115;
            let hookState = 'IDLE'; // IDLE (chờ thả), DROPPING (đang thả dây), WAITING (chờ cá bơi đến), REELING (kéo lên)
            let targetFish = null; 
            let waveOffset = 0;

            let fishes = [
                {x: 50, y: 310, rx: 20, ry: 12, color: '#ff6b6b'},
                {x: 700, y: 360, rx: 18, ry: 10, color: '#feca57'},
                {x: 200, y: 410, rx: 22, ry: 14, color: '#ff9ff3'},
                {x: 600, y: 280, rx: 16, ry: 9, color: '#48dbfb'},
                {x: 350, y: 440, rx: 20, ry: 12, color: '#10ac84'}
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
                
                // Nhấn Space để thả dây câu xuống nước nếu đang ở trạng thái nghỉ
                if (e.code === 'Space' && hookState === 'IDLE') {
                    hookState = 'DROPPING';
                }
            });

            function update() {
                waveOffset += 0.05;

                if (hookState === 'DROPPING') {
                    currentHookY += 8;
                    if (currentHookY >= hookY) {
                        currentHookY = hookY;
                        hookState = 'WAITING';
                        // Chọn ngẫu nhiên 1 con cá để bơi tới cắn câu
                        if (fishes.length > 0) {
                            targetFish = fishes[Math.floor(Math.random() * fishes.length)];
                        }
                    }
                } 
                else if (hookState === 'WAITING') {
                    if (targetFish) {
                        // Con cá được chọn tự bơi hướng thẳng đến móc câu (boatX, hookY)
                        let angle = Math.atan2(hookY - targetFish.y, boatX - targetFish.x);
                        targetFish.x += Math.cos(angle) * 1.8;
                        targetFish.y += Math.sin(angle) * 1.4;

                        let dist = Math.hypot(boatX - targetFish.x, hookY - targetFish.y);
                        if (dist < targetFish.rx + 6) {
                            hookState = 'REELING';
                        }
                    } else {
                        hookState = 'IDLE';
                    }
                } 
                else if (hookState === 'REELING') {
                    if (targetFish) {
                        targetFish.x = boatX;
                        targetFish.y -= 7;
                        currentHookY = targetFish.y;
                        if (targetFish.y <= 115) {
                            score += Math.round(50 / targetFish.rx * 15);
                            fishes = fishes.filter(f => f !== targetFish);
                            targetFish = null;
                            hookState = 'IDLE';
                            currentHookY = 115;

                            fishes.push({
                                x: Math.random() < 0.5 ? -40 : canvas.width + 40,
                                y: Math.random() * 160 + 280,
                                rx: Math.random() * 6 + 16,
                                ry: Math.random() * 4 + 9,
                                color: ['#ff6b6b', '#feca57', '#ff9ff3', '#48dbfb', '#10ac84', '#e67e22'][Math.floor(Math.random()*6)]
                            });
                        }
                    }
                }

                // Các con cá khác bơi lội tự do nhẹ nhàng
                fishes.forEach(f => {
                    if (f !== targetFish || hookState !== 'WAITING') {
                        f.x += (Math.random() - 0.5) * 2;
                        f.y += (Math.random() - 0.5) * 1;
                        if (f.x < 40) f.x = 40;
                        if (f.x > canvas.width - 40) f.x = canvas.width - 40;
                        if (f.y < 200) f.y = 200;
                        if (f.y > canvas.height - 40) f.y = canvas.height - 40;
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

                // --- BỜ CỎ VEN SÔNG ---
                ctx.fillStyle = "#2ecc71";
                ctx.fillRect(0, 130, canvas.width, 20);

                ctx.fillStyle = "#27ae60";
                for (let i = 0; i < canvas.width; i += 40) {
                    ctx.beginPath();
                    ctx.arc(i, 135, 15, 0, Math.PI, true);
                    ctx.fill();
                }

                // --- SÓNG NƯỚC SÔNG ---
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

                // --- CẦN CÂU VÀ DÂY ---
                ctx.strokeStyle = '#8B4513';
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.moveTo(boatX + 10, 100);
                ctx.lineTo(boatX + 25, 80);
                ctx.stroke();

                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(boatX + 25, 80);
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
                    let isCaught = (f === targetFish && hookState === 'REELING');
                    drawFish(f.x, f.y, f.rx, f.ry, f.color, isCaught);
                });

                let statusText = hookState === 'IDLE' ? "Nhấn Space để thả dây câu xuống sông!" : (hookState === 'DROPPING' ? "Đang thả dây..." : (hookState === 'WAITING' ? "Cá đang bơi tới cắn mồi..." : "Đang kéo cá lên!"));
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
          
