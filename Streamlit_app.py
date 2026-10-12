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

# --- MÀN HÌNH 2: GIAO DIỆN GAME CÂU CÁ (CÁ THẬT HƠN, TỐC ĐỘ CHẬM) ---
elif st.session_state.screen == "playing":
    st.title(f"🌊 Vùng Biển Câu Cá - Cần thủ: {st.session_state.character['avatar']} {st.session_state.character['name']}")
    st.write("💡 **Hướng dẫn:** Dùng phím **Trái / Phải** di chuyển thuyền để thả dây câu đón đường cá bơi tới. Cá bơi chậm và chân thực hơn!")

    char_avatar = st.session_state.character['avatar']
    boat_color = st.session_state.character['color']

    game_html = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                background: #0c2461;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
            }}
            canvas {{
                background: linear-gradient(to bottom, #87CEEB 0%, #87CEEB 35%, #1e3799 35%, #0c2461 100%);
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.5);
            }}
            .hud {{
                position: absolute;
                top: 10px;
                left: 20px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                text-shadow: 1px 1px 2px black;
            }}
        </style>
    </head>
    <body>
        <div style="position: relative;">
            <div class="hud" id="hudText">Điểm: 0 | Thời gian: 40s</div>
            <canvas id="gameCanvas" width="750" height="500"></canvas>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');

            let score = 0;
            let timeLeft = 40;
            let boatX = 375;
            const hookY = 320; // Vị trí móc câu dưới nước
            let caughtFish = null;

            // Tốc độ cá được giảm lại cho dễ câu, có thêm thuộc tính scale/hình dáng
            let fishes = [
                {{x: 50, y: 300, rx: 20, ry: 12, color: '#ff6b6b', speed: 1.0}},
                {{x: 700, y: 350, rx: 18, ry: 10, color: '#feca57', speed: -1.2}},
                {{x: 200, y: 410, rx: 22, ry: 14, color: '#ff9ff3', speed: 0.8}},
                {{x: 600, y: 270, rx: 16, ry: 9, color: '#48dbfb', speed: -1.4}},
                {{x: 350, y: 440, rx: 20, ry: 12, color: '#10ac84', speed: 0.9}}
            ];

            // Đếm ngược thời gian
            const timer = setInterval(() => {{
                timeLeft--;
                if (timeLeft <= 0) {{
                    clearInterval(timer);
                    alert("Hết giờ! Tổng điểm câu cá của bạn là: " + score);
                    window.location.reload();
                }}
            }}, 1000);

            // Điều khiển thuyền qua lại bằng phím mũi tên
            window.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowLeft' && boatX > 50) boatX -= 25;
                if (e.key === 'ArrowRight' && boatX < canvas.width - 50) boatX += 25;
            }});

            function update() {{
                if (!caughtFish) {{
                    fishes.forEach((f, index) => {{
                        // Kiểm tra khoảng cách va chạm với móc câu (boatX, hookY)
                        let dist = Math.hypot(boatX - f.x, hookY - f.y);
                        if (dist < f.rx + 6) {{
                            caughtFish = f;
                            fishes.splice(index, 1);
                        }}
                    }});
                }} else {{
                    // Khi cá dính câu, tự động kéo lên thuyền
                    caughtFish.x = boatX;
                    caughtFish.y -= 6;
                    if (caughtFish.y <= 130) {{
                        score += Math.round(50 / caughtFish.rx * 15);
                        caughtFish = null;
                        // Sinh cá mới bơi vào
                        fishes.push({{
                            x: Math.random() < 0.5 ? -40 : canvas.width + 40,
                            y: Math.random() * 180 + 260,
                            rx: Math.random() * 6 + 16,
                            ry: Math.random() * 4 + 9,
                            color: ['#ff6b6b', '#feca57', '#ff9ff3', '#48dbfb', '#10ac84', '#e67e22'][Math.floor(Math.random()*6)],
                            speed: (Math.random() * 0.6 + 0.8) * (Math.random() < 0.5 ? 1 : -1)
                        }});
                    }}
                }}

                // Cập nhật vị trí cá bơi chậm rãi, tự nhiên
                fishes.forEach(f => {{
                    f.x += f.speed;
                    if (f.x > canvas.width + 50) {{
                        f.speed = -Math.abs(f.speed);
                    }} else if (f.x < -50) {{
                        f.speed = Math.abs(f.speed);
                    }}
                }});
            }}

            // Hàm vẽ hình con cá sống động (Thân bầu dục + Đuôi tam giác + Vây)
            function drawFish(x, y, rx, ry, color, speed, isCaught) {{
                ctx.save();
                ctx.translate(x, y);
                if (speed < 0 && !isCaught) {{
                    ctx.scale(-1, 1); // Lật hướng cá khi bơi sang trái
                }}
                if (isCaught) {{
                    ctx.rotate(Math.PI / 2); // Xuyên dọc khi bị kéo lên
                }}

                // Vẽ đuôi cá
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.moveTo(-rx, 0);
                ctx.lineTo(-rx - 12, -ry - 4);
                ctx.lineTo(-rx - 12, ry + 4);
                ctx.closePath();
                ctx.fill();

                // Vẽ thân cá (bầu dục)
                ctx.beginPath();
                ctx.ellipse(0, 0, rx, ry, 0, 0, Math.PI * 2);
                ctx.fill();

                // Vẽ vây lưng và vây bụng nhỏ
                ctx.beginPath();
                ctx.moveTo(-3, -ry);
                ctx.lineTo(4, -ry - 6);
                ctx.lineTo(8, -ry);
                ctx.closePath();
                ctx.fill();

                // Mắt cá
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(rx * 0.5, -ry * 0.3, 3.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#000000';
                ctx.beginPath();
                ctx.arc(rx * 0.5, -ry * 0.3, 1.5, 0, Math.PI * 2);
                ctx.fill();

                ctx.restore();
            }}

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Vẽ mây trời phía trên
                ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
                ctx.beginPath();
                ctx.arc(150, 50, 30, 0, Math.PI * 2);
                ctx.arc(180, 40, 40, 0, Math.PI * 2);
                ctx.arc(220, 50, 30, 0, Math.PI * 2);
                ctx.arc(550, 60, 35, 0, Math.PI * 2);
                ctx.arc(590, 45, 45, 0, Math.PI * 2);
                ctx.fill();

                // Vẽ đáy cát biển và rong rêu
                ctx.fillStyle = "#d2b48c";
                ctx.fillRect(0, canvas.height - 30, canvas.width, 30);
                
                ctx.fillStyle = "#27ae60";
                for(let i=50; i<canvas.width; i+=120) {{
                    ctx.beginPath();
                    ctx.moveTo(i, canvas.height - 30);
                    ctx.quadraticCurveTo(i - 15, canvas.height - 90, i + 10, canvas.height - 120);
                    ctx.quadraticCurveTo(i + 25, canvas.height - 70, i + 30, canvas.height - 30);
                    ctx.fill();
                }}

                // Vẽ dây câu
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(boatX, 110);
                let currentHookY = caughtFish ? caughtFish.y : hookY;
                ctx.lineTo(boatX, currentHookY);
                ctx.stroke();

                // Vẽ móc câu
                ctx.fillStyle = '#f1c40f';
                ctx.beginPath();
                ctx.arc(boatX, currentHookY, 5, 0, Math.PI * 2);
                ctx.fill();

                // Vẽ Thuyền
                ctx.fillStyle = "{boat_color}";
                ctx.beginPath();
                ctx.moveTo(boatX - 45, 95);
                ctx.lineTo(boatX + 45, 95);
                ctx.lineTo(boatX + 30, 125);
                ctx.lineTo(boatX - 30, 125);
                ctx.closePath();
                ctx.fill();

                // Số trên thuyền & Avatar nhân vật
                ctx.fillStyle = "white";
                ctx.font = "bold 14px Arial";
                ctx.textAlign = "center";
                ctx.fillText("3", boatX, 115);

                ctx.font = "24px Arial";
                ctx.fillText("{char_avatar}", boatX, 85);

                // Vẽ các con cá đang bơi
                fishes.forEach(f => {{
                    drawFish(f.x, f.y, f.rx, f.ry, f.color, f.speed, false);
                }});

                // Vẽ con cá đang dính câu kéo lên
                if (caughtFish) {{
                    drawFish(caughtFish.x, caughtFish.y, caughtFish.rx, caughtFish.ry, caughtFish.color, caughtFish.speed, true);
                }}

                // Cập nhật HUD hiển thị
                document.getElementById('hudText').innerText = "Điểm: " + score + " | Thời gian: " + timeLeft + "s";
            }}

            function loop() {{
                update();
                draw();
                requestAnimationFrame(loop);
            }}

            loop();
        </script>
    </body>
    </html>
    """.format(boat_color=boat_color, char_avatar=char_avatar)

    st.components.v1.html(game_html, height=530)

    col_back, _ = st.columns(2)
    with col_back:
        if st.button("⬅️ Quay lại chọn nhân vật"):
            st.session_state.screen = "select"
            st.rerun()
  
