import streamlit as st
import streamlit.components.v1 as components

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Flappy Bird Streamlit Edition",
    page_icon="🐤",
    layout="centered"
)

# --- THANH BÊN: CÀI ĐẶT ÂM THANH & HƯỚNG DẪN ---
st.sidebar.title("🎵 Cài đặt Game")
audio_file = st.sidebar.file_uploader("Tải nhạc nền (MP3, WAV):", type=["mp3", "wav", "ogg"])

if audio_file is not None:
    st.sidebar.audio(audio_file, format="audio/mp3", loop=True)
else:
    st.sidebar.info("💡 Bạn có thể tải file MP3 yêu thích từ máy để làm nhạc nền game!")

st.sidebar.markdown("""
---
### 🎮 Hướng dẫn chơi:
- **Phím Cách (Spacebar)** hoặc **Click chuột** vào màn hình để chim bay lên.
- Tránh va chạm vào các cột xanh và mép màn hình.
""")

st.title("🐤 Flappy Bird Deluxe")

# --- MÃ HTML5 / CANVAS GAME INTERACTIVE ---
game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #111;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            width: 400px;
            height: 600px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border-radius: 12px;
            overflow: hidden;
        }
        canvas {
            display: block;
            background: #70c5ce;
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="birdCanvas" width="400" height="600"></canvas>
</div>

<script>
const canvas = document.getElementById("birdCanvas");
const ctx = canvas.getContext("2d");

// Trạng thái game: 'START', 'PLAYING', 'GAMEOVER'
let gameState = 'START';

// Cài đặt mức độ khó
let difficulty = 'MEDIUM'; // EASY, MEDIUM, HARD
const settings = {
    EASY: { gravity: 0.22, jump: -5.8, speed: 2.0, gap: 160, spawnRate: 110 },
    MEDIUM: { gravity: 0.28, jump: -6.3, speed: 3.2, gap: 135, spawnRate: 90 },
    HARD: { gravity: 0.35, jump: -7.0, speed: 4.6, gap: 115, spawnRate: 70 }
};

// Đối tượng Chim
let bird = {
    x: 80,
    y: 280,
    radius: 14,
    velocity: 0,
    rotation: 0
};

// Mảng chứa các Cột
let pipes = [];
let frameCount = 0;
let score = 0;
let highScore = 0;

// Bắt sự kiện điều khiển
window.addEventListener("keydown", function(e) {
    if (e.code === "Space") {
        e.preventDefault();
        handleInput();
    }
});

canvas.addEventListener("click", function(e) {
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    if (gameState === 'START') {
        // Kiểm tra click chọn độ khó
        const btnY = 320;
        const btnW = 90;
        const btnH = 36;
        
        if (clickY >= btnY && clickY <= btnY + btnH) {
            if (clickX >= 40 && clickX <= 40 + btnW) difficulty = 'EASY';
            if (clickX >= 155 && clickX <= 155 + btnW) difficulty = 'MEDIUM';
            if (clickX >= 270 && clickX <= 270 + btnW) difficulty = 'HARD';
        }

        // Kiểm tra click nút "BẮT ĐẦU PLAY"
        if (clickX >= 100 && clickX <= 300 && clickY >= 410 && clickY <= 465) {
            startGame();
        }
    } else {
        handleInput();
    }
});

function handleInput() {
    if (gameState === 'PLAYING') {
        bird.velocity = settings[difficulty].jump;
    } else if (gameState === 'GAMEOVER') {
        gameState = 'START';
    }
}

function startGame() {
    gameState = 'PLAYING';
    bird.y = 250;
    bird.velocity = 0;
    pipes = [];
    score = 0;
    frameCount = 0;
}

// --- VẼ CHI TIẾT CỘT 3D VỚI KHỚP NỐI & ĐỔ BÓNG ---
function drawDetailedPipe(x, topHeight, bottomY) {
    const pipeWidth = 58;
    const capHeight = 24;
    const capOutset = 5;

    // Gradient thân cột (Hiệu ứng ống tròn 3D)
    let bodyGradient = ctx.createLinearGradient(x, 0, x + pipeWidth, 0);
    bodyGradient.addColorStop(0, "#2e7d32");
    bodyGradient.addColorStop(0.2, "#4caf50");
    bodyGradient.addColorStop(0.5, "#81c784");
    bodyGradient.addColorStop(0.8, "#388e3c");
    bodyGradient.addColorStop(1, "#1b5e20");

    // Gradient đầu cột (Cap)
    let capGradient = ctx.createLinearGradient(x - capOutset, 0, x + pipeWidth + capOutset, 0);
    capGradient.addColorStop(0, "#1b5e20");
    capGradient.addColorStop(0.3, "#66bb6a");
    capGradient.addColorStop(0.7, "#388e3c");
    capGradient.addColorStop(1, "#0d5316");

    ctx.lineWidth = 2;
    ctx.strokeStyle = "#0a3a0a";

    // 1. Cột trên
    // Thân
    ctx.fillStyle = bodyGradient;
    ctx.fillRect(x, 0, pipeWidth, topHeight - capHeight);
    ctx.strokeRect(x, 0, pipeWidth, topHeight - capHeight);
    
    // Đầu cột trên
    ctx.fillStyle = capGradient;
    ctx.fillRect(x - capOutset, topHeight - capHeight, pipeWidth + capOutset * 2, capHeight);
    ctx.strokeRect(x - capOutset, topHeight - capHeight, pipeWidth + capOutset * 2, capHeight);

    // 2. Cột dưới
    // Đầu cột dưới
    ctx.fillRect(x - capOutset, bottomY, pipeWidth + capOutset * 2, capHeight);
    ctx.strokeRect(x - capOutset, bottomY, pipeWidth + capOutset * 2, capHeight);
    
    // Thân
    ctx.fillStyle = bodyGradient;
    ctx.fillRect(x, bottomY + capHeight, pipeWidth, canvas.height - (bottomY + capHeight));
    ctx.strokeRect(x, bottomY + capHeight, pipeWidth, canvas.height - (bottomY + capHeight));

    // Điểm nhấn đường viền sáng dọc cột
    ctx.fillStyle = "rgba(255, 255, 255, 0.2)";
    ctx.fillRect(x + 8, 0, 4, topHeight - capHeight);
    ctx.fillRect(x + 8, bottomY + capHeight, 4, canvas.height - bottomY);
}

// --- VẼ CHIM CHI TIẾT ---
function drawBird() {
    ctx.save();
    ctx.translate(bird.x, bird.y);
    
    // Xoay góc chim theo vận tốc
    bird.rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, bird.velocity * 0.08));
    ctx.rotate(bird.rotation);

    // Thân chim
    ctx.fillStyle = "#ffeb3b";
    ctx.beginPath();
    ctx.arc(0, 0, bird.radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#f57f17";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Mắt
    ctx.fillStyle = "#ffffff";
    ctx.beginPath();
    ctx.arc(6, -5, 5, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#000000";
    ctx.beginPath();
    ctx.arc(8, -5, 2, 0, Math.PI * 2);
    ctx.fill();

    // Mỏ
    ctx.fillStyle = "#ff5722";
    ctx.beginPath();
    ctx.moveTo(10, 0);
    ctx.lineTo(18, 3);
    ctx.lineTo(10, 7);
    ctx.closePath();
    ctx.fill();

    // Cánh
    ctx.fillStyle = "#fbc02d";
    ctx.beginPath();
    ctx.ellipse(-5, 2, 7, 4, Math.PI / 6, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
}

// --- MÀN HÌNH CHỜ (START SCREEN / LOBBY) ---
function drawStartScreen() {
    // Phông nền trời & mây
    ctx.fillStyle = "#70c5ce";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Đám mây trang trí
    ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
    ctx.beginPath(); ctx.arc(80, 100, 30, 0, Math.PI * 2); ctx.arc(110, 90, 40, 0, Math.PI * 2); ctx.arc(140, 100, 30, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(280, 150, 25, 0, Math.PI * 2); ctx.arc(305, 140, 35, 0, Math.PI * 2); ctx.arc(330, 150, 25, 0, Math.PI * 2); ctx.fill();

    // Tiêu đề Game
    ctx.shadowColor = "rgba(0,0,0,0.3)";
    ctx.shadowBlur = 8;
    ctx.fillStyle = "#fff";
    ctx.font = "900 36px 'Segoe UI', sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("FLAPPY BIRD", canvas.width / 2, 110);
    
    ctx.fillStyle = "#fbc02d";
    ctx.fillText("DELUXE", canvas.width / 2, 155);
    ctx.shadowBlur = 0;

    // Chim hoạt ảnh nhẹ tại màn hình chờ
    bird.y = 210 + Math.sin(Date.now() / 200) * 6;
    drawBird();

    // Khung chọn Mức Độ Khó
    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 16px sans-serif";
    ctx.fillText("CHỌN MỨC ĐỘ KHÓ:", canvas.width / 2, 295);

    const btnY = 320;
    const btnW = 90;
    const btnH = 36;

    const diffs = [
        { key: 'EASY', label: 'DỄ', x: 40, color: '#4caf50' },
        { key: 'MEDIUM', label: 'VỪA', x: 155, color: '#ff9800' },
        { key: 'HARD', label: 'KHÓ', x: 270, color: '#f44336' }
    ];

    diffs.forEach(d => {
        ctx.beginPath();
        ctx.roundRect(d.x, btnY, btnW, btnH, 8);
        if (difficulty === d.key) {
            ctx.fillStyle = d.color;
            ctx.shadowColor = d.color;
            ctx.shadowBlur = 10;
        } else {
            ctx.fillStyle = "#e0e0e0";
            ctx.shadowBlur = 0;
        }
        ctx.fill();
        ctx.shadowBlur = 0;

        ctx.fillStyle = (difficulty === d.key) ? "#ffffff" : "#616161";
        ctx.font = "bold 14px sans-serif";
        ctx.fillText(d.label, d.x + btnW / 2, btnY + 23);
    });

    // NÚT "BẮT ĐẦU PLAY"
    let startBtnGradient = ctx.createLinearGradient(100, 410, 300, 465);
    startBtnGradient.addColorStop(0, "#81c784");
    startBtnGradient.addColorStop(1, "#388e3c");

    ctx.beginPath();
    ctx.roundRect(100, 410, 200, 55, 28);
    ctx.fillStyle = startBtnGradient;
    ctx.shadowColor = "rgba(56, 142, 60, 0.5)";
    ctx.shadowBlur = 12;
    ctx.fill();
    ctx.shadowBlur = 0;

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 20px 'Segoe UI', sans-serif";
    ctx.fillText("BẮT ĐẦU PLAY 🚀", canvas.width / 2, 445);

    // Điểm cao nhất
    ctx.fillStyle = "#333";
    ctx.font = "14px sans-serif";
    ctx.fillText("Điểm cao nhất: " + highScore, canvas.width / 2, 530);
}

// --- MÀN HÌNH GAME OVER ---
function drawGameOverScreen() {
    ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 32px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("GAME OVER", canvas.width / 2, 230);

    ctx.font = "20px sans-serif";
    ctx.fillText("Điểm số: " + score, canvas.width / 2, 280);
    ctx.fillText("Điểm kỷ lục: " + highScore, canvas.width / 2, 315);

    ctx.fillStyle = "#ffeb3b";
    ctx.font = "16px sans-serif";
    ctx.fillText("Nhấn SPACE hoặc CLICK để thử lại", canvas.width / 2, 390);
}

// --- VÒNG LẶP CHÍNH (GAME LOOP) ---
function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameState === 'START') {
        drawStartScreen();
    } else if (gameState === 'PLAYING') {
        const cfg = settings[difficulty];

        // 1. Nền & Mặt đất
        ctx.fillStyle = "#70c5ce";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // 2. Xử lý Vịt/Chim
        bird.velocity += cfg.gravity;
        bird.y += bird.velocity;

        // Va chạm đất hoặc trần
        if (bird.y + bird.radius >= canvas.height - 40 || bird.y - bird.radius <= 0) {
            gameState = 'GAMEOVER';
        }

        // 3. Xử lý Cột
        frameCount++;
        if (frameCount % cfg.spawnRate === 0) {
            const minHeight = 50;
            const maxHeight = canvas.height - 40 - cfg.gap - minHeight;
            const topHeight = Math.floor(Math.random() * (maxHeight - minHeight + 1)) + minHeight;
            
            pipes.push({
                x: canvas.width,
                top: topHeight,
                bottom: topHeight + cfg.gap,
                passed: false
            });
        }

        for (let i = 0; i < pipes.length; i++) {
            let p = pipes[i];
            p.x -= cfg.speed;

            // Vẽ cột chi tiết
            drawDetailedPipe(p.x, p.top, p.bottom);

            // Kiểm tra va chạm cột
            const pipeWidth = 58;
            if (
                bird.x + bird.radius > p.x &&
                bird.x - bird.radius < p.x + pipeWidth &&
                (bird.y - bird.radius < p.top || bird.y + bird.radius > p.bottom)
            ) {
                gameState = 'GAMEOVER';
            }

            // Tính điểm
            if (!p.passed && p.x + pipeWidth < bird.x) {
                p.passed = true;
                score++;
                if (score > highScore) highScore = score;
            }
        }

        // Xóa cột đã đi qua màn hình
        pipes = pipes.filter(p => p.x > -80);

        // Vẽ Chim
        drawBird();

        // 4. Vẽ Mặt đất
        ctx.fillStyle = "#ded895";
        ctx.fillRect(0, canvas.height - 40, canvas.width, 40);
        ctx.fillStyle = "#73bf2e";
        ctx.fillRect(0, canvas.height - 40, canvas.width, 10);

        // 5. Vẽ Điểm số realtime
        ctx.fillStyle = "#ffffff";
        ctx.strokeStyle = "#000000";
        ctx.lineWidth = 3;
        ctx.font = "900 36px 'Segoe UI', sans-serif";
        ctx.textAlign = "center";
        ctx.strokeText(score, canvas.width / 2, 60);
        ctx.fillText(score, canvas.width / 2, 60);

    } else if (gameState === 'GAMEOVER') {
        drawGameOverScreen();
    }

    requestAnimationFrame(loop);
}

// Bắt đầu vòng lặp game
loop();
</script>
</body>
</html>
"""

components.html(game_code, height=630)
