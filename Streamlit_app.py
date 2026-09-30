import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Game Câu Tên Chi Tiết", page_icon="🎣", layout="centered"
)

st.title("🎣 Game Câu Tên: Mô Phỏng Cá Đớp Câu Chi Tiết 🐟")

# Nhập danh sách tên
default_names = "An\nBình\nCường\nDung\nHoàng\nLan\nMinh\nPhúc"
names_input = st.text_area(
    "📝 Danh sách tên dưới hồ (mỗi tên 1 dòng):",
    value=default_names,
    height=80,
)
names_list = [n.strip() for n in names_input.split("\n") if n.strip()]
names_json = str(names_list)

# HTML5 Canvas + JS Canvas Mô phỏng cá đớp chi tiết
detailed_fishing_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        margin: 0;
        padding: 0;
        user-select: none;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
    #startScreen {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #00b4db, #0083b0);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 20;
        color: white;
        text-align: center;
    }}
    #startBtn {{
        background: #ff9800;
        color: white;
        border: none;
        padding: 14px 32px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(255,152,0,0.4);
        transition: transform 0.1s;
        margin-top: 15px;
    }}
    #startBtn:active {{
        transform: scale(0.95);
    }}
    #overlayText {{
        position: absolute;
        top: 15px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.7);
        color: #fff;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        pointer-events: none;
        text-align: center;
        display: none;
    }}
    #resultModal {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0);
        background: rgba(255, 255, 255, 0.98);
        padding: 20px 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        transition: transform 0.15s cubic-bezier(0.175, 0.885, 0.32, 1.275);
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
    <!-- Màn hình Bắt đầu -->
    <div id="startScreen">
        <h1 style="margin: 0; font-size: 30px;">🎣 GAME CÂU TÊN VUI NHỘN 🐟</h1>
        <p style="margin-top: 8px; opacity: 0.9;">Nhìn cá bơi đến đớp phao rồi giựt lên ngay nhé!</p>
        <button id="startBtn">▶ BẮT ĐẦU CHƠI</button>
    </div>

    <canvas id="fishCanvas"></canvas>
    <div id="overlayText">CLICK VÀO MÀN HÌNH ĐỂ THẢ CẦN!</div>
    
    <div id="resultModal">
        <h3 style="margin:0; color:#555; font-size:15px;">🎉 ĐÃ GIỰT ĐƯỢC CÁ MANG TÊN:</h3>
        <h1 id="caughtName" style="margin:8px 0; color:#e91e63; font-size: 34px;">TÊN</h1>
        <p style="margin:0; color:#777; font-size:12px;">Click vào màn hình để câu tiếp!</p>
    </div>
</div>

<script>
const canvas = document.getElementById('fishCanvas');
const ctx = canvas.getContext('2d');
const overlayText = document.getElementById('overlayText');
const resultModal = document.getElementById('resultModal');
const caughtNameElem = document.getElementById('caughtName');
const startScreen = document.getElementById('startScreen');
const startBtn = document.getElementById('startBtn');

canvas.width = 700;
canvas.height = 380;

const names = {names_json};
const colors = ['#FF5722', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4', '#4CAF50', '#FFEB3B'];

let gameStarted = false;

// Bắt đầu game
startBtn.addEventListener('click', (e) => {{
    e.stopPropagation();
    startScreen.style.display = 'none';
    overlayText.style.display = 'block';
    gameStarted = true;
}});

// Khởi tạo Cá
let fishes = [];
function initFishes() {{
    fishes = [];
    let count = names.length > 0 ? names.length : 1;
    for(let i = 0; i < count; i++) {{
        fishes.push({{
            id: i,
            name: names[i] || "Cá May Mắn",
            x: Math.random() * (canvas.width - 120) + 60,
            y: Math.random() * 100 + 220,
            speedX: (Math.random() * 2 + 1.5) * (Math.random() < 0.5 ? 1 : -1),
            color: colors[i % colors.length],
            isBiting: false,
            isCaught: false
        }});
    }}
}}
initFishes();

// Trạng thái: 'IDLE', 'CASTING', 'WAITING', 'BITING', 'CAUGHT'
let gameState = 'IDLE';
let floatX = 260;
let floatY = 120;
let targetFloatY = 120;
let bitingFish = null;
let bubbles = [];

// Xử lý sự kiện click màn hình
document.getElementById('gameContainer').addEventListener('click', () => {{
    if (!gameStarted) return;

    if (gameState === 'IDLE') {{
        // Thả câu
        gameState = 'WAITING';
        targetFloatY = 220; // Phao hạ xuống mặt nước
        resultModal.classList.remove('show');
        overlayText.innerText = "⏳ Phao đã thả... Chờ cá tiến lại đớp câu!";
        overlayText.style.background = "rgba(0,0,0,0.7)";

        // Sau 1.2s - 2.5s chọn 1 con cá tiến lại đớp
        setTimeout(() => {{
            if (gameState === 'WAITING') {{
                gameState = 'BITING';
                bitingFish = fishes[Math.floor(Math.random() * fishes.length)];
                bitingFish.isBiting = true;
                overlayText.innerText = "🚨 CÁ ĐÃ ĐỚP DÂY CÂU! GIỰT LÊN NGAY!";
                overlayText.style.background = "#FF0000";
            }}
        }}, 1200 + Math.random() * 1300);

    }} else if (gameState === 'WAITING') {{
        // Giựt sớm khi cá chưa đớp
        gameState = 'IDLE';
        targetFloatY = 120;
        overlayText.innerText = "❌ Giựt quá sớm! Cá giật mình bơi mất.";
        overlayText.style.background = "#d32f2f";

    }} else if (gameState === 'BITING') {{
        // Giựt cá thành công!
        gameState = 'CAUGHT';
        targetFloatY = 70; // Giựt cá lên cao

        if (bitingFish) {{
            bitingFish.isBiting = false;
            bitingFish.isCaught = true;
            caughtNameElem.innerText = bitingFish.name;
        }}

        resultModal.classList.add('show');
        overlayText.innerText = "🎉 GIỰT CÂU THÀNH CÔNG!";
        overlayText.style.background = "#388e3c";

        setTimeout(() => {{
            if(bitingFish) bitingFish.isCaught = false;
            gameState = 'IDLE';
            initFishes();
        }}, 800);
    }}
}});

// Vòng lặp vẽ đồ họa
function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Bầu trời & Bờ hồ
    ctx.fillStyle = '#87CEEB';
    ctx.fillRect(0, 0, canvas.width, 140);
    ctx.fillStyle = '#1E88E5';
    ctx.fillRect(0, 140, canvas.width, canvas.height - 140);

    // 2. Cần thủ & Cần câu
    ctx.font = '45px Arial';
    ctx.fillText('🧑‍🌾', 40, 120);

    ctx.strokeStyle = '#5D4037';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(80, 95);
    ctx.lineTo(floatX, 55);
    ctx.stroke();

    // Di chuyển vị trí phao êm ái
    floatY += (targetFloatY - floatY) * 0.2;

    // 3. Dây câu & Phao
    let currentFloatY = floatY;
    if (gameState === 'BITING') {{
        // Cá đớp làm phao giật mạnh chìm nổi
        currentFloatY += Math.sin(Date.now() / 30) * 9;
        
        // Tạo bọt khí khi cá đớp
        if (Math.random() < 0.4) {{
            bubbles.push({{
                x: floatX + (Math.random() - 0.5) * 20,
                y: currentFloatY + 10,
                r: Math.random() * 4 + 2,
                alpha: 1
            }});
        }}
    }}

    ctx.strokeStyle = 'rgba(255,255,255,0.85)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(floatX, 55);
    ctx.lineTo(floatX, currentFloatY);
    ctx.stroke();

    // Vẽ bọt khí
    bubbles.forEach((b, idx) => {{
        ctx.fillStyle = `rgba(255, 255, 255, ${{b.alpha}})`;
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
        ctx.fill();
        b.y -= 1;
        b.alpha -= 0.03;
        if (b.alpha <= 0) bubbles.splice(idx, 1);
    }});

    // Vẽ phao
    ctx.fillStyle = gameState === 'BITING' ? '#FF0000' : '#FFFFFF';
    ctx.beginPath();
    ctx.arc(floatX, currentFloatY, 7, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#FF0000';
    ctx.stroke();

    // 4. Vẽ danh sách Cá
    fishes.forEach(fish => {{
        if (fish.isCaught) {{
            // Khi bị giựt lên: Cá di chuyển thẳng lên phao
            fish.x = floatX;
            fish.y = currentFloatY + 20;
        }} else if (fish.isBiting) {{
            // Cá đớp câu: Bơi gấp đến vi trí phao và há miệng đớp dây
            let dx = floatX - fish.x;
            let dy = (currentFloatY + 10) - fish.y;
            fish.x += dx * 0.25;
            fish.y += dy * 0.25;
            fish.speedX = dx >= 0 ? 1 : -1;
        }} else {{
            // Cá bơi bình thường
            fish.x += fish.speedX;
            if (fish.x > canvas.width + 60) fish.x = -60;
            if (fish.x < -60) fish.x = canvas.width + 60;
        }}

        ctx.save();
        ctx.translate(fish.x, fish.y);
        
        // Quay hướng cá theo hướng bơi
        if (fish.speedX < 0) ctx.scale(-1, 1);

        // Vẽ thân cá
        ctx.fillStyle = fish.color;
        ctx.beginPath();
        ctx.ellipse(0, 0, 32, 15, 0, 0, Math.PI * 2);
        ctx.fill();

        // Vẽ đuôi cá
        ctx.beginPath();
        ctx.moveTo(-28, 0);
        ctx.lineTo(-42, -10);
        ctx.lineTo(-42, 10);
        ctx.closePath();
        ctx.fill();

        // Mắt cá & Miệng há đớp
        ctx.fillStyle = '#FFF';
        ctx.beginPath();
        ctx.arc(18, -4, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(19, -4, 2, 0, Math.PI * 2);
        ctx.fill();

        if (fish.isBiting) {{
            // Há miệng đớp phao
            ctx.fillStyle = '#333';
            ctx.beginPath();
            ctx.arc(28, 2, 5, 0, Math.PI);
            ctx.fill();
        }}

        ctx.restore();

        // Tên cá hiển thị trên đầu
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(fish.name, fish.x, fish.y - 20);
    }});

    requestAnimationFrame(draw);
}}

draw();
</script>
</body>
</html>
"""

components.html(detailed_fishing_html, height=400)
