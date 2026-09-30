import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Game Câu Tên Hoành Tráng", page_icon="🎉", layout="centered"
)

st.title("🎣 Game Câu Tên May Mắn & Pháo Giấy 🎊")

# Nhập danh sách tên
default_names = "An\nBình\nCường\nDung\nHoàng\nLan\nMinh\nPhúc"
names_input = st.text_area(
    "📝 Danh sách tên dưới hồ (mỗi tên 1 dòng):",
    value=default_names,
    height=80,
)
names_list = [n.strip() for n in names_input.split("\n") if n.strip()]
names_json = str(names_list)

# Code HTML5 Canvas + Web Audio API (Nhạc/SFX) + Confetti Particle Engine
ultimate_fishing_html = f"""
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
        height: 390px;
        margin: 0 auto;
        border-radius: 12px;
        overflow: hidden;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(0,0,0,0.35);
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
        z-index: 30;
        color: white;
        text-align: center;
    }}
    #startBtn {{
        background: #ff9800;
        color: white;
        border: none;
        padding: 14px 35px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 30px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(255,152,0,0.5);
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
        z-index: 10;
    }}
    /* Modal chúc mừng hoành tráng */
    #resultModal {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.75);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.25s ease-in-out;
        z-index: 20;
    }}
    #resultModal.show {{
        opacity: 1;
        pointer-events: auto;
    }}
    .celebration-box {{
        background: linear-gradient(135deg, #ffffff, #f0f3f8);
        padding: 25px 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        transform: scale(0.5);
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 3px solid #ffcc00;
    }}
    #resultModal.show .celebration-box {{
        transform: scale(1);
    }}
    .winner-title {{
        font-size: 16px;
        color: #666;
        margin: 0;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .winner-name {{
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(45deg, #FF1493, #FF8C00, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
        text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.3);
        animation: pulse 1s infinite alternate;
    }}
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        100% {{ transform: scale(1.08); }}
    }}
</style>
</head>
<body>

<div id="gameContainer">
    <!-- Màn hình Bắt đầu -->
    <div id="startScreen">
        <h1 style="margin: 0; font-size: 32px;">🎣 CÂU TÊN MAY MẮN 🎊</h1>
        <p style="margin-top: 8px; opacity: 0.9;">Nhìn cá đớp phao, giựt lên để xem tên chiến thắng nổi to!</p>
        <button id="startBtn">▶ BẮT ĐẦU CHƠI</button>
    </div>

    <canvas id="fishCanvas"></canvas>
    <div id="overlayText">CLICK VÀO MÀN HÌNH ĐỂ THẢ CẦN!</div>
    
    <!-- Modal Chúc mừng + Nổi tên to -->
    <div id="resultModal">
        <div class="celebration-box">
            <div class="winner-title">🎉 CHÚC MỪNG BẠN ĐÃ CÂU ĐƯỢC 🎉</div>
            <div class="winner-name" id="caughtName">TÊN</div>
            <p style="margin:0; color:#888; font-size:13px;">Click vào màn hình để tiếp tục câu!</p>
        </div>
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
canvas.height = 390;

const names = {names_json};
const colors = ['#FF5722', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4', '#4CAF50', '#FFEB3B'];

let gameStarted = false;

// Web Audio API giả lập hiệu ứng âm thanh (SFX) sinh động
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playSound(type) {{
    if (audioCtx.state === 'suspended') {{
        audioCtx.resume();
    }}
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    if (type === 'splash') {{
        // Âm thanh thả phao/cá đớp
        osc.type = 'sine';
        osc.frequency.setValueAtTime(300, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(80, audioCtx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.2);
    }} else if (type === 'bite') {{
        // Âm thanh cảnh báo cắn câu
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(600, audioCtx.currentTime);
        osc.frequency.linearRampToValueAtTime(900, audioCtx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
    }} else if (type === 'win') {{
        // Âm thanh chiến thắng chúc mừng
        const now = audioCtx.currentTime;
        const notes = [261.63, 329.63, 392.00, 523.25]; // C E G C
        notes.forEach((freq, index) => {{
            const noteOsc = audioCtx.createOscillator();
            const noteGain = audioCtx.createGain();
            noteOsc.connect(noteGain);
            noteGain.connect(audioCtx.destination);
            noteOsc.frequency.setValueAtTime(freq, now + index * 0.1);
            noteGain.gain.setValueAtTime(0.2, now + index * 0.1);
            noteGain.gain.exponentialRampToValueAtTime(0.001, now + index * 0.1 + 0.3);
            noteOsc.start(now + index * 0.1);
            noteOsc.stop(now + index * 0.1 + 0.3);
        }});
    }}
}}

startBtn.addEventListener('click', (e) => {{
    e.stopPropagation();
    startScreen.style.display = 'none';
    overlayText.style.display = 'block';
    gameStarted = true;
    playSound('splash');
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
            y: Math.random() * 100 + 230,
            speedX: (Math.random() * 2 + 1.5) * (Math.random() < 0.5 ? 1 : -1),
            color: colors[i % colors.length],
            isBiting: false,
            isCaught: false
        }});
    }}
}}
initFishes();

// Hệ thống hạt Pháo giấy (Confetti Engine)
let confetti = [];
function createConfetti() {{
    confetti = [];
    const colors = ['#FF1493', '#00BFFF', '#FFD700', '#32CD32', '#FF4500', '#9400D3'];
    for (let i = 0; i < 100; i++) {{
        confetti.push({{
            x: canvas.width / 2,
            y: canvas.height / 2 - 40,
            vx: (Math.random() - 0.5) * 12,
            vy: (Math.random() - 0.7) * 12,
            size: Math.random() * 8 + 4,
            color: colors[Math.floor(Math.random() * colors.length)],
            rotation: Math.random() * 360,
            vRot: (Math.random() - 0.5) * 10
        }});
    }}
}}

let gameState = 'IDLE';
let floatX = 260;
let floatY = 120;
let targetFloatY = 120;
let bitingFish = null;
let bubbles = [];

function getWaterHeight(x, time) {{
    const waterLevel = 140;
    const wave1 = Math.sin(x * 0.02 + time * 0.003) * 6;
    const wave2 = Math.sin(x * 0.04 - time * 0.005) * 3;
    return waterLevel + wave1 + wave2;
}}

// Click Tương Tác
document.getElementById('gameContainer').addEventListener('click', () => {{
    if (!gameStarted) return;

    if (gameState === 'IDLE') {{
        gameState = 'WAITING';
        targetFloatY = 140;
        resultModal.classList.remove('show');
        overlayText.innerText = "⏳ Phao nhấp nhô... Chờ cá tiến lại đớp!";
        overlayText.style.background = "rgba(0,0,0,0.7)";
        playSound('splash');

        setTimeout(() => {{
            if (gameState === 'WAITING') {{
                gameState = 'BITING';
                bitingFish = fishes[Math.floor(Math.random() * fishes.length)];
                bitingFish.isBiting = true;
                overlayText.innerText = "🚨 CÁ ĐÃ ĐỚP DÂY CÂU! GIỰT LÊN NGAY!";
                overlayText.style.background = "#FF0000";
                playSound('bite');
            }}
        }}, 1200 + Math.random() * 1300);

    }} else if (gameState === 'WAITING') {{
        gameState = 'IDLE';
        targetFloatY = 120;
        overlayText.innerText = "❌ Giựt quá sớm! Cá giật mình bơi mất.";
        overlayText.style.background = "#d32f2f";

    }} else if (gameState === 'BITING') {{
        gameState = 'CAUGHT';
        targetFloatY = 70;

        if (bitingFish) {{
            bitingFish.isBiting = false;
            bitingFish.isCaught = true;
            caughtNameElem.innerText = bitingFish.name;
        }}

        playSound('win');
        createConfetti();
        resultModal.classList.add('show');
        overlayText.innerText = "🎉 CÂU THÀNH CÔNG!";
        overlayText.style.background = "#388e3c";

    }} else if (gameState === 'CAUGHT') {{
        // Reset sau khi xem kết quả
        resultModal.classList.remove('show');
        if(bitingFish) bitingFish.isCaught = false;
        gameState = 'IDLE';
        initFishes();
        overlayText.innerText = "CLICK VÀO MÀN HÌNH ĐỂ THẢ CẦN!";
        overlayText.style.background = "rgba(0,0,0,0.7)";
    }}
}});

function draw() {{
    const time = Date.now();
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Bầu trời
    ctx.fillStyle = '#87CEEB';
    ctx.fillRect(0, 0, canvas.width, 140);

    // 2. Thủy cung bên dưới
    ctx.fillStyle = '#1E88E5';
    ctx.fillRect(0, 140, canvas.width, canvas.height - 140);

    // 3. Cần thủ & Cần câu
    ctx.font = '45px Arial';
    ctx.fillText('🧑‍🌾', 40, 120);

    ctx.strokeStyle = '#5D4037';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(80, 95);
    ctx.lineTo(floatX, 55);
    ctx.stroke();

    floatY += (targetFloatY - floatY) * 0.2;
    let currentWaterY = getWaterHeight(floatX, time);
    let currentFloatY = floatY;

    if (gameState === 'WAITING') {{
        currentFloatY = currentWaterY;
    }} else if (gameState === 'BITING') {{
        currentFloatY = currentWaterY + 12 + Math.sin(time / 20) * 8;
        if (Math.random() < 0.5) {{
            bubbles.push({{
                x: floatX + (Math.random() - 0.5) * 22,
                y: currentFloatY + 5,
                r: Math.random() * 4 + 2,
                alpha: 1
            }});
        }}
    }}

    // 4. Dây câu & Phao
    ctx.strokeStyle = 'rgba(255,255,255,0.85)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(floatX, 55);
    ctx.lineTo(floatX, currentFloatY);
    ctx.stroke();

    // Bọt khí
    bubbles.forEach((b, idx) => {{
        ctx.fillStyle = `rgba(255, 255, 255, ${{b.alpha}})`;
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
        ctx.fill();
        b.y -= 1;
        b.alpha -= 0.03;
        if (b.alpha <= 0) bubbles.splice(idx, 1);
    }});

    // Phao
    ctx.fillStyle = gameState === 'BITING' ? '#FF0000' : '#FFFFFF';
    ctx.beginPath();
    ctx.arc(floatX, currentFloatY, 7, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#FF0000';
    ctx.stroke();

    // 5. Mặt nước sóng sánh chông chênh
    ctx.fillStyle = 'rgba(13, 71, 161, 0.5)';
    ctx.beginPath();
    ctx.moveTo(0, canvas.height);
    for (let x = 0; x <= canvas.width; x += 10) {{
        ctx.lineTo(x, getWaterHeight(x, time + 500) - 3);
    }}
    ctx.lineTo(canvas.width, canvas.height);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = 'rgba(30, 136, 229, 0.8)';
    ctx.beginPath();
    ctx.moveTo(0, canvas.height);
    for (let x = 0; x <= canvas.width; x += 10) {{
        ctx.lineTo(x, getWaterHeight(x, time));
    }}
    ctx.lineTo(canvas.width, canvas.height);
    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let x = 0; x <= canvas.width; x += 10) {{
        ctx.lineTo(x, getWaterHeight(x, time));
    }}
    ctx.stroke();

    // 6. Vẽ danh sách Cá
    fishes.forEach(fish => {{
        if (fish.isCaught) {{
            fish.x = floatX;
            fish.y = currentFloatY + 20;
        }} else if (fish.isBiting) {{
            let dx = floatX - fish.x;
            let dy = (currentFloatY + 10) - fish.y;
            fish.x += dx * 0.25;
            fish.y += dy * 0.25;
            fish.speedX = dx >= 0 ? 1 : -1;
        }} else {{
            fish.x += fish.speedX;
            if (fish.x > canvas.width + 60) fish.x = -60;
            if (fish.x < -60) fish.x = canvas.width + 60;
        }}

        ctx.save();
        ctx.translate(fish.x, fish.y);
        if (fish.speedX < 0) ctx.scale(-1, 1);

        ctx.fillStyle = fish.color;
        ctx.beginPath();
        ctx.ellipse(0, 0, 32, 15, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(-28, 0);
        ctx.lineTo(-42, -10);
        ctx.lineTo(-42, 10);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#FFF';
        ctx.beginPath();
        ctx.arc(18, -4, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(19, -4, 2, 0, Math.PI * 2);
        ctx.fill();

        if (fish.isBiting) {{
            ctx.fillStyle = '#333';
            ctx.beginPath();
            ctx.arc(28, 2, 5, 0, Math.PI);
            ctx.fill();
        }}

        ctx.restore();

        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(fish.name, fish.x, fish.y - 20);
    }});

    // 7. Vẽ Pháo giấy (Confetti Particles)
    confetti.forEach((p, idx) => {{
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate((p.rotation * Math.PI) / 180);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
        ctx.restore();

        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.2; // Trọng lực
        p.rotation += p.vRot;

        if (p.y > canvas.height) confetti.splice(idx, 1);
    }});

    requestAnimationFrame(draw);
}}

draw();
</script>
</body>
</html>
"""

components.html(ultimate_fishing_html, height=410)
