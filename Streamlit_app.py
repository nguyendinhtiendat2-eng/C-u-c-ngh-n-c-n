import streamlit as st

st.set_page_config(
    page_title="Game Câu Cá & Chọn Nhân Vật", 
    page_icon="🎣", 
    layout="centered"
)

# Khởi tạo session state
if "screen" not in st.session_state:
    st.session_state.screen = "select"  # "select", "playing", "gameover"
if "character" not in st.session_state:
    st.session_state.character = {"name": "Bác nông dân", "avatar": "👨‍🌾", "color": "#c0392b"}

# Danh sách nhân vật
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

# --- MÀN HÌNH 2: GIAO DIỆN GAME CÂU CÁ (HTML5 CANVAS MÔ PHỎNG GIỐNG ẢNH MẪU) ---
elif st.session_state.screen == "playing":
    st.title(f"🌊 Vùng Biển Câu Cá - Cần thủ: {st.session_state.character['avatar']} {st.session_state.character['name']}")
    st.write("💡 **Hướng dẫn:** Sử dụng các phím mũi tên **Trái / Phải** để di chuyển thuyền, nhấn **Phím Cách (Space)** hoặc **Click** vào canvas để thả câu bắt cá!")

    char_avatar = st.session_state.character['avatar']
    boat_color = st.session_state.character['color']

    # Mã HTML/JS nhúng Canvas game câu cá trực quan sinh động
    game_html = f"""
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
                cursor: pointer;
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
            <div class="hud" id="hudText">Điểm: 0 | Thời gian: 30s</div>
            <canvas id="gameCanvas" width="750" height="500"></canvas>
        </div>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');

            let score = 0;
            let timeLeft = 30;
            let boatX = 375;
            let hookY = 130;
            let hookState = 'IDLE'; // IDLE, DROPPING, REELING
            let caughtFish = null;

            // Danh sách cá bơi lội
            let fishes = [
                {{x: 100, y: 250, radius: 15, color: '#ff6b6b', speed: 2, dir: 1}},
                {{x: 300, y: 320, radius: 12, color: '#feca57', speed: -3, dir: -1}},
                {{x: 500, y: 400, radius: 18, color: '#ff9ff3', speed: 1.5, dir: 1}},
                {{x: 650, y: 280, radius: 10, color: '#48dbfb', speed: -2.5, dir: -1}},
                {{x: 200, y: 450, radius: 16, color: '#10ac84', speed: 2.2, dir: 1}}
            ];

            // Đếm ngược thời gian
            const timer = setInterval(() => {{
                timeLeft--;
                if (timeLeft <= 0) {{
                    clearInterval(timer);
                    alert("Hết giờ! Tổng điểm của bạn là: " + score);
                    window.location.reload();
                }}
            }}, 1000);

            // Điều khiển bàn phím
            window.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowLeft' && boatX > 50) boatX -= 25;
                if (e.key === 'ArrowRight' && boatX < canvas.width - 50) boatX += 25;
                if (e.code === 'Space' && hookState === 'IDLE') {{
                    hookState = 'DROPPING';
                }}
            }});

            // Click chuột để thả câu
            canvas.addEventListener('click', () => {{
                if (hookState === 'IDLE') {{
                    hookState = 'DROPPING';
                }}
            }});

            function update() {{
                // Xử lý móc câu
                if (hookState === 'DROPPING') {{
                    hookY += 6;
                    if (hookY >= canvas.height - 40) {{
                        hookState = 'REELING';
                    }}
                    // Kiểm tra bắt cá
                    fishes.forEach((f, index) => {{
                        let dist = Math.hypot(boatX - f.x, hookY - f.y);
                        if (dist < f.radius + 10) {{
                            caughtFish = f;
                            fishes.splice(index, 1);
                            hookState = 'REELING';
                        }}
                    }});
                }} else if (hookState === 'REELING') {{
                    hookY -= 8;
                    if (caughtFish) {{
                        caughtFish.x = boatX;
                        caughtFish.y = hookY;
                    }}
                    if (hookY <= 130) {{
                        if (caughtFish) {{
                            score += Math.round(50 / caughtFish.radius * 10);
                            caughtFish = null;
                            // Tạo lại cá mới
                            fishes.push({{
                                x: Math.random() < 0.5 ? -30 : canvas.width + 30,
                                y: Math.random() * 200 + 250,
                                radius: Math.random() * 8 + 10,
                                color: ['#ff6b6b', '#feca57', '#ff9ff3', '#48dbfb', '#10ac84'][Math.floor(Math.random()*5)],
                                speed: (Math.random() * 2 + 1) * (Math.random() < 0.5 ? 1 : -1),
                                dir: 1
                            }});
                        }}
                        hookState = 'IDLE';
                        hookY = 130;
                    }}
                }}

                // Cập nhật vị trí cá bơi
                fishes.forEach(f => {{
                    f.x += f.speed;
                    if (f.x > canvas.width + 40) f.x = -40;
                    if (f.x < -40) f.x = canvas.width + 40;
                }});
            }}

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Vẽ mây trời (phía trên)
                ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
                ctx.beginPath();
                ctx.arc(150, 50, 30, 0, Math.PI * 2);
                ctx.arc(180, 40, 40, 0, Math.PI * 2);
                ctx.arc(220, 50, 30, 0, Math.PI * 2);
                ctx.arc(550, 60, 35, 0, Math.PI * 2);
                ctx.arc(590, 45, 45, 0, Math.PI * 2);
                ctx.fill();

                // Vẽ đáy biển & rong rêu trang trí
                ctx.fillStyle = "#d2b48c";
                ctx.fillRect(0, canvas.height - 30, canvas.width, 30); // Cát đáy biển
                
                ctx.fillStyle = "#27ae60"; // Rong rêu
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
                ctx.moveTo(boatX
  
