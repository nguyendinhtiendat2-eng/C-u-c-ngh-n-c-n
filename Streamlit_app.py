import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Game Câu Tên Chạm Trực Tiếp", page_icon="🎣", layout="centered"
)

st.title("🎣 Game Câu Tên: Click Trực Tiếp Vào Màn Hình 🐟")
st.write(
    "Nhập danh sách tên, sau đó **nhấp thẳng vào khung hồ câu bên dưới** để Thả cần & Kéo cá lên!"
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

# HTML5 Canvas + JS Canvas tương tác trực tiếp bằng cách Click
interactive_game_html = f"""
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
        background: rgba(0,0,0,0.6);
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
        background: rgba(255, 255, 255, 0.95);
        padding: 20px 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        transition: transform 0.3s ease;
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
    <div id="overlayText">🖱️ CLICK VÀO MÀN HÌNH ĐỂ THẢ CẦN CÂU!</div>
    <div id="resultModal">
        <h3 style="margin:0; color:#333;">🎉 BẠN ĐÃ CÂU ĐƯỢC:</h3>
        <h1 id="caughtName" style="margin:10px 0; color:#e91e63; font-size: 32px;">TÊN</h1>
        <p style="margin:0; color:#666; font-size:12px;">Click vào màn hình để tiếp tục câu!</p>
    </div>
</div>

<script>
const canvas = document.getElementById('fishCanvas');
const ctx = canvas.getContext('2d');
const overlayText = document.getElementById('overlayText');
const resultModal = document.getElementById('resultModal');
const caughtNameElem = document.getElementById('caughtName');

// Kích thước canvas
canvas.width = 700;
canvas.height = 380;

const names = {names_json};
const colors = ['#FF5722', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4', '#4CAF50', '#FFEB3B'];

// Khởi tạo danh sách các con cá mang tên
let fishes = [];
function initFishes() {{
    fishes = [];
    let count = names.length > 0 ? names.length : 1;
    for(let i = 0; i < count; i++) {{
        fishes.push({{
            name: names[i] || "Cá May Mắn",
            x: Math.random() * (canvas.width - 100) + 50,
            y: Math.random() * 120 + 200,
            speed: (Math.random() * 1.5 + 0.8) * (Math.random() < 0.5 ? 1 : -1),
            color: colors[i % colors.length]
        }});
    }}
}}
initFishes();

// Trạng thái Game: 'IDLE', 'WAITING', 'BITING', 'CAUGHT'
let gameState = 'IDLE';
let floatY = 120;
let targetFloatY = 120;
let biteTimer = null;
let caughtName = '';

// Sự kiện Click trực tiếp vào màn hình game
document.getElementById('gameContainer').addEventListener('click', () => {{
    if (gameState === 'IDLE') {{
        // Chuyển sang thả cần
        gameState = 'WAITING';
        targetFloatY = 220;
        resultModal.classList.remove('show');
        overlayText.innerText = "⏳ Đang chờ cá cắn câu...";
        overlayText.style.background = "rgba(0,0,0,0.6)";

        // Hẹn giờ cá cắn (từ 1.5s - 3.5s)
        let waitTime = 1500 + Math.random() * 2000;
        biteTimer = setTimeout(() => {{
            if (gameState === 'WAITING') {{
                gameState = 'BITING';
                overlayText.innerText = "🚨 CÁ CẮN CÂU! CLICK MÀN HÌNH ĐỂ KÉO NGAY!";
                overlayText.style.background = "rgba(230, 57, 70, 0.9)";
            }}
        }}, waitTime);

    }} else if (gameState === 'WAITING') {{
        // Kéo quá sớm
        clearTimeout(biteTimer);
        gameState = 'IDLE';
        targetFloatY = 120;
        overlayText.innerText = "❌ Kéo quá sớm! Cá sợ chạy mất. Click để thử lại.";
        overlayText.style.background = "rgba(200, 0, 0, 0.7)";

    }} else if (gameState === 'BITING') {{
        // Câu thành công!
        clearTimeout(biteTimer);
        gameState = 'CAUGHT';
        targetFloatY = 80;

        // Bốc ngẫu nhiên 1 tên
        caughtName = names.length > 0 ? names[Math.floor(Math.random() * names.length)] : "Không tên";
        caughtNameElem.innerText = caughtName;
        resultModal.classList.add('show');

        overlayText.innerText = "🎉 CÂU THÀNH CÔNG!";
        overlayText.style.background = "rgba(46, 125, 50, 0.9)";

        setTimeout(() => {{ gameState = 'IDLE'; }}, 1000);
    }}
}});

// Vòng lặp vẽ game (Render Loop)
function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Vẽ Bầu trời & Hồ nước
    ctx.fillStyle = '#87CEEB';
    ctx.fillRect(0, 0, canvas.width, 140);
    ctx.fillStyle = '#1E88E5';
    ctx.fillRect(0, 140, canvas.width, canvas.height - 140);

    // 2. Vẽ Người câu cá
    ctx.font = '45px Arial';
    ctx.fillText('🧑‍‍🌾', 40, 120);

    // 3. Vẽ Cần câu
    ctx.strokeStyle = '#5D4037';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(80, 95);
    ctx.lineTo(220, 60);
    ctx.stroke();

    // Smooth movement cho Phao
    floatY += (targetFloatY - floatY) * 0.1;

    // 4. Vẽ Dây câu & Phao
    ctx.strokeStyle = 'rgba(255,255,255,0.8)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(220, 60);
    
    let currentFloatY = floatY;
    if (gameState === 'BITING') {{
        currentFloatY += Math.sin(Date.now() / 50) * 5; // Rung lắc khi cắn câu
    }} else if (gameState === 'WAITING') {{
        currentFloatY += Math.sin(Date.now() / 200) * 2; // Nhấp nhô nhẹ
    }}
    
    ctx.lineTo(220, currentFloatY);
    ctx.stroke();

    // Vẽ phao
    ctx.fillStyle = gameState === 'BITING' ? '#FF0000' : '#FFFFFF';
    ctx.beginPath();
    ctx.arc(220, currentFloatY, 7, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#FF0000';
    ctx.stroke();

    // 5. Vẽ các con cá có Tên bơi lội
    fishes.forEach(fish => {{
        fish.x += fish.speed;
        if (fish.x > canvas.width + 80) fish.x = -80;
        if (fish.x < -80) fish.x = canvas.width + 80;

        ctx.save();
        ctx.translate(fish.x, fish.y);
        if (fish.speed < 0) ctx.scale(-1, 1);

        // Vẽ thân cá
        ctx.fillStyle = fish.color;
        ctx.beginPath();
        ctx.ellipse(0, 0, 35, 16, 0, 0, Math.PI * 2);
        ctx.fill();

        // Vẽ đuôi cá
        ctx.beginPath();
        ctx.moveTo(-30, 0);
        ctx.lineTo(-45, -12);
        ctx.lineTo(-45, 12);
        ctx.closePath();
        ctx.fill();

        // Vẽ tên cá
        ctx.restore();
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 12px Arial';
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

# Hiển thị trực tiếp màn hình chơi game
components.html(interactive_game_html, height=400)
