import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Game Câu Tên Siêu Tốc", page_icon="⚡", layout="centered"
)

st.title("⚡ Game Câu Tên Tốc Độ Bàn Thờ 🐟")
st.write(
    "Đã tăng tốc độ tối đa! **Click liên tục vào màn hình** để câu tên cực nhanh!"
)

# Nhập danh sách tên
default_names = "An\nBình\nCường\nDung\nHoàng\nLan\nMinh\nPhúc"
names_input = st.text_area(
    "📝 Danh sách tên dưới hồ (mỗi tên 1 dòng):",
    value=default_names,
    height=80,
)
names_list = [n.strip() for n in names_input.split("\n") if n.strip()]
names_json = str(names_list)

# HTML5 Canvas + JS Canvas siêu tốc
fast_game_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        margin: 0;
        padding: 0;
        user-select: none;
        font-family: Arial, sans-serif;
    }}
    #gameContainer {{
        position: relative;
        width: 100%;
        max-width: 700px;
        height: 380px;
        margin: 0 auto;
        border-radius: 12px;
        overflow: hidden;
        cursor: pointer;
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
    }}
    canvas {{
        display: block;
        width: 100%;
        height: 100%;
    }}
    #overlayText {{
        position: absolute;
        top: 15px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.7);
        color: #fff;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 15px;
        font-weight: bold;
        pointer-events: none;
        text-align: center;
    }}
    #resultModal {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0);
        background: rgba(255, 255, 255, 0.98);
        padding: 15px 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        transition: transform 0.1s ease-out; /* Tăng tốc hiệu ứng hiển thị */
        pointer-events: none;
        z-index: 10;
    }}
    #resultModal.show {{
        transform: translate(-50%, -50%) scale(1);
    }}
</style>
</head>
<body>

<div id="gameContainer">
    <canvas id="fishCanvas"></canvas>
    <div id="overlayText">⚡ CLICK ĐỂ CÂU NGAY!</div>
    <div id="resultModal">
        <h3 style="margin:0; color:#333; font-size:16px;">🎉 BẠN ĐÃ CÂU ĐƯỢC:</h3>
        <h1 id="caughtName" style="margin:5px 0; color:#e91e63; font-size: 36px;">TÊN</h1>
        <p style="margin:0; color:#666; font-size:12px;">Click để tiếp tục câu siêu tốc!</p>
    </div>
</div>

<script>
const canvas = document.getElementById('fishCanvas');
const ctx = canvas.getContext('2d');
const overlayText = document.getElementById('overlayText');
const resultModal = document.getElementById('resultModal');
const caughtNameElem = document.getElementById('caughtName');

canvas.width = 700;
canvas.height = 380;

const names = {names_json};
const colors = ['#FF5722', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4', '#4CAF50', '#FFEB3B'];

// Khởi tạo các chú cá bơi siêu nhanh
let fishes = [];
function initFishes() {{
    fishes = [];
    let count = names.length > 0 ? names.length : 1;
    for(let i = 0; i < count; i++) {{
        fishes.push({{
            name: names[i] || "Cá Siêu Tốc",
            x: Math.random() * (canvas.width - 100) + 50,
            y: Math.random() * 120 + 200,
            // Tốc độ cá bơi cực nhanh (gấp 3 lần cũ)
            speed: (Math.random() * 4 + 3) * (Math.random() < 0.5 ? 1 : -1),
            color: colors[i % colors.length]
        }});
    }}
}}
initFishes();

let gameState = 'IDLE';
let floatY = 120;
let targetFloatY = 120;
let biteTimer = null;

// Click phản hồi tức thì
document.getElementById('gameContainer').addEventListener('click', () => {{
    if (gameState === 'IDLE') {{
        gameState = 'WAITING';
        targetFloatY = 220;
        resultModal.classList.remove('show');
        overlayText.innerText = "⏳ Đang thả câu...";
        overlayText.style.background = "rgba(0,0,0,0.7)";

        // THỜI GIAN CHỜ CỰC PHÍM: Chỉ 0.3s đến 0.8s là cắn liền!
        let waitTime = 300 + Math.random() * 500;
        biteTimer = setTimeout(() => {{
            if (gameState === 'WAITING') {{
                gameState = 'BITING';
                overlayText.innerText = "🚨 CẮN CÂU RỒI! CLICK KÉO BÂY GIỜ!";
                overlayText.style.background = "#FF0000";
            }}
        }}, waitTime);

    }} else if (gameState === 'WAITING') {{
        // Giảm hình phạt, nếu lỡ tay click nhanh quá vẫn chuyển trạng thái cắn luôn
        clearTimeout(biteTimer);
        gameState = 'BITING';
        overlayText.innerText = "🚨 GIẬT CẦN NGAY!";
        overlayText.style.background = "#FF0000";

    }} else if (gameState === 'BITING') {{
        // Kéo lên nhận kết quả tức thì!
        clearTimeout(biteTimer);
        gameState = 'CAUGHT';
        targetFloatY = 80;

        let caughtName = names.length > 0 ? names[Math.floor(Math.random() * names.length)] : "Không tên";
        caughtNameElem.innerText = caughtName;
        resultModal.classList.add('show');

        overlayText.innerText = "🎉 XONG!";
        overlayText.style.background = "#4CAF50";

        // Reset về trạng thái chờ sẵn cực nhanh (chỉ 0.2s)
        setTimeout(() => {{ gameState = 'IDLE'; }}, 200);
    }}
}});

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Môi trường
    ctx.fillStyle = '#87CEEB';
    ctx.fillRect(0, 0, canvas.width, 140);
    ctx.fillStyle = '#1E88E5';
    ctx.fillRect(0, 140, canvas.width, canvas.height - 140);

    // Người & Cần
    ctx.font = '45px Arial';
    ctx.fillText('🧑‍🌾', 40, 120);

    ctx.strokeStyle = '#5D4037';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(80, 95);
    ctx.lineTo(220, 60);
    ctx.stroke();

    // Phao di chuyển nhanh gấp 3 lần (0.32 lerp)
    floatY += (targetFloatY - floatY) * 0.32;

    // Dây câu & Phao
    ctx.strokeStyle = 'rgba(255,255,255,0.9)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(220, 60);
    
    let currentFloatY = floatY;
    if (gameState === 'BITING') {{
        currentFloatY += Math.sin(Date.now() / 20) * 8; // Bão giật rung cực mạnh
    }}
    
    ctx.lineTo(220, currentFloatY);
    ctx.stroke();

    ctx.fillStyle = gameState === 'BITING' ? '#FF0000' : '#FFFFFF';
    ctx.beginPath();
    ctx.arc(220, currentFloatY, 8, 0, Math.PI * 2);
    ctx.fill();

    // Cá bơi siêu tốc
    fishes.forEach(fish => {{
        fish.x += fish.speed;
        if (fish.x > canvas.width + 80) fish.x = -80;
        if (fish.x < -80) fish.x = canvas.width + 80;

        ctx.save();
        ctx.translate(fish.x, fish.y);
        if (fish.speed < 0) ctx.scale(-1, 1);

        ctx.fillStyle = fish.color;
        ctx.beginPath();
        ctx.ellipse(0, 0, 35, 16, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(-30, 0);
        ctx.lineTo(-45, -12);
        ctx.lineTo(-45, 12);
        ctx.closePath();
        ctx.fill();

        ctx.restore();
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 13px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(fish.name, fish.x, fish.y + 4);
    }});

    requestAnimationFrame(draw);
}}

draw();
</script>
</body>
</html>
"""

components.html(fast_game_html, height=400)
