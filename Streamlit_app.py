import streamlit as st

st.set_page_config(page_title="Flappy Bird Âm Thanh Streamlit", page_icon="🎵", layout="centered")

st.title("🎵 Flappy Bird (Có Âm Thanh) trên Streamlit")
st.write("Sử dụng **Phím Space (Dấu cách)** hoặc **Click chuột** để chơi. Âm thanh sẽ tự phát khi bạn tương tác lần đầu.")

# Mã HTML/JS với Web Audio API để phát âm thanh mượt mà không cần tải file ngoài
flappy_code_audio = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            background-color: #0e1117;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        #game-container {
            position: relative;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            border-radius: 8px;
            overflow: hidden;
        }
        canvas {
            display: block;
            background-color: #70c5ce;
        }
    </style>
</head>
<body>
<div id="game-container">
    <canvas id="birdCanvas" width="360" height="640"></canvas>
</div>

<script>
const canvas = document.getElementById('birdCanvas');
const ctx = canvas.getContext('2d');

// --- TẠO HỆ THỐNG ÂM THANH (WEB AUDIO API) ---
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new AudioContext();
    }
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
}

// Âm thanh khi vỗ cánh (Flap Sound)
function playFlapSound() {
    if (!audioCtx) return;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(400, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.1);
    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.1);
}

// Âm thanh khi cộng điểm (Score Sound)
function playScoreSound() {
    if (!audioCtx) return;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(523.25, audioCtx.currentTime); // Phím C5
    osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.08); // Phím E5
    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.25);
}

// Âm thanh khi thua (Hit / GameOver Sound)
function playHitSound() {
    if (!audioCtx) return;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(300, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(80, audioCtx.currentTime + 0.3);
    gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.3);
}

// --- LOGIC GAME ---
let gameState = 'START';
let score = 0;
let highScore = localStorage.getItem('flappy_highscore_st') || 0;
let frames = 0;

const bird = {
    x: 60,
    y: 250,
    radius: 12,
    gravity: 0.25,
    jump: 4.6,
    velocity: 0,
    draw() {
        ctx.fillStyle = '#ffeb3b';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#d7ccc8';
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(this.x + 4, this.y - 4, 2, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ff9800';
        ctx.beginPath();
        ctx.moveTo(this.x + 8, this.y);
        ctx.lineTo(this.x + 16, this.y + 2);
        ctx.lineTo(this.x + 8, this.y + 6);
        ctx.closePath();
        ctx.fill();
    },
    update() {
        this.velocity += this.gravity;
        this.y += this.velocity;
        if (this.y + this.radius >= canvas.height - 80) {
            this.y = canvas.height - 80 - this.radius;
            gameOver();
        }
        if (this.y - this.radius <= 0) {
            this.y = this.radius;
            this.velocity = 0;
        }
    },
    flap() {
        this.velocity = -this.jump;
        playFlapSound(); // Phát âm thanh khi vỗ cánh
    },
    reset() { this.y = 250; this.velocity = 0; }
};

const pipes = {
    position: [],
    width: 52,
    gap: 120,
    dx: 2,
    draw() {
        for (let i = 0; i < this.position.length; i++) {
            let p = this.position[i];
            ctx.fillStyle = '#2e7d32';
            ctx.strokeStyle = '#1b5e20';
            ctx.lineWidth = 2;
            ctx.fillRect(p.x, 0, this.width, p.y);
            ctx.strokeRect(p.x, 0, this.width, p.y);
            ctx.fillRect(p.x, p.y + this.gap, this.width, canvas.height - (p.y + this.gap) - 80);
            ctx.strokeRect(p.x, p.y + this.gap, this.width, canvas.height - (p.y + this.gap) - 80);
        }
    },
    update() {
        if (frames % 120 === 0) {
            let maxPos = canvas.height - 80 - this.gap - 50;
            this.position.push({
                x: canvas.width,
                y: Math.floor(Math.random() * (maxPos - 50)) + 50,
                passed: false
            });
        }
        for (let i = 0; i < this.position.length; i++) {
            let p = this.position[i];
            if (bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.width) {
                if (bird.y - bird.radius < p.y || bird.y + bird.radius > p.y + this.gap) {
                    gameOver();
                }
            }
            if (p.x + this.width < bird.x && !p.passed) {
                score++;
                p.passed = true;
                playScoreSound(); // Phát âm thanh khi ghi điểm
                if (score > highScore) {
                    highScore = score;
                    localStorage.setItem('flappy_highscore_st', highScore);
                }
            }
            p.x -= this.dx;
            if (p.x + this.width <= 0) {
                this.position.shift();
                i--;
            }
        }
    },
    reset() { this.position = []; }
};

function drawGround() {
    ctx.fillStyle = '#ded895';
    ctx.fillRect(0, canvas.height - 80, canvas.width, 80);
    ctx.fillStyle = '#73bf2e';
    ctx.fillRect(0, canvas.height - 80, canvas.width, 15);
}

function handleInput() {
    initAudio(); // Khởi tạo AudioContext sau lần nhấp/bấm phím đầu tiên
    if (gameState === 'START' || gameState === 'PLAYING') {
        if (gameState === 'START') gameState = 'PLAYING';
        bird.flap();
    } else if (gameState === 'GAMEOVER') {
        pipes.reset();
        bird.reset();
        score = 0;
        frames = 0;
        gameState = 'PLAYING';
    }
}

window.addEventListener('keydown', (e) => { if (e.code === 'Space') { e.preventDefault(); handleInput(); } });
canvas.addEventListener('click', handleInput);

function gameOver() {
    if (gameState !== 'GAMEOVER') {
        playHitSound(); // Phát âm thanh thua cuộc
    }
    gameState = 'GAMEOVER';
}

function drawUI() {
    ctx.fillStyle = '#fff';
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    if (gameState === 'PLAYING') {
        ctx.font = 'bold 35px sans-serif';
        ctx.fillText(score, canvas.width / 2 - 10, 50);
        ctx.strokeText(score, canvas.width / 2 - 10, 50);
    } else if (gameState === 'START') {
        ctx.font = '20px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('NHẤN DẤU CÁCH / CLICK', canvas.width / 2, canvas.height / 2 - 20);
        ctx.fillText('ĐỂ BẮT ĐẦU VÀ BẬT ÂM THANH', canvas.width / 2, canvas.height / 2 + 10);
    } else if (gameState === 'GAMEOVER') {
        ctx.textAlign = 'center';
        ctx.font = 'bold 30px sans-serif';
        ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2 - 50);
        ctx.font = '20px sans-serif';
        ctx.fillText(`Điểm: ${score}`, canvas.width / 2, canvas.height / 2);
        ctx.fillText(`Kỷ lục: ${highScore}`, canvas.width / 2, canvas.height / 2 + 30);
        ctx.font = '16px sans-serif';
        ctx.fillText('Nhấn để chơi lại', canvas.width / 2, canvas.height / 2 + 80);
    }
    ctx.textAlign = 'start';
}

function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (gameState === 'PLAYING') {
        bird.update();
        pipes.update();
        frames++;
    }
    pipes.draw();
    drawGround();
    bird.draw();
    drawUI();
    requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

st.components.v1.html(flappy_code_audio, height=700)
