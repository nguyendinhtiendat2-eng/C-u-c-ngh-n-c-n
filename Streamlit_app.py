<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flappy Bird Mini</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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

// Trạng thái game: 'START', 'PLAYING', 'GAMEOVER'
let gameState = 'START';
let score = 0;
let highScore = localStorage.getItem('flappy_highscore') || 0;
let frames = 0;

// Đối tượng Chim
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

        // Mắt chim
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(this.x + 4, this.y - 4, 2, 0, Math.PI * 2);
        ctx.fill();

        // Mỏ chim
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

        // Va chạm với đất
        if (this.y + this.radius >= canvas.height - 80) {
            this.y = canvas.height - 80 - this.radius;
            gameOver();
        }

        // Tránh chim bay vượt quá trần nhà
        if (this.y - this.radius <= 0) {
            this.y = this.radius;
            this.velocity = 0;
        }
    },

    flap() {
        this.velocity = -this.jump;
    },

    reset() {
        this.y = 250;
        this.velocity = 0;
    }
};

// Quản lý Ống cống
const pipes = {
    position: [],
    width: 52,
    gap: 120,
    dx: 2,

    draw() {
        for (let i = 0; i < this.position.length; i++) {
            let p = this.position[i];
            let topY = p.y;
            let bottomY = p.y + this.gap;

            ctx.fillStyle = '#2e7d32';
            ctx.strokeStyle = '#1b5e20';
            ctx.lineWidth = 2;

            // Ống trên
            ctx.fillRect(p.x, 0, this.width, topY);
            ctx.strokeRect(p.x, 0, this.width, topY);

            // Ống dưới
            ctx.fillRect(p.x, bottomY, this.width, canvas.height - bottomY - 80);
            ctx.strokeRect(p.x, bottomY, this.width, canvas.height - bottomY - 80);
        }
    },

    update() {
        // Thêm ống mới mỗi 120 frames
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

            // Xử lý va chạm
            let topPipeBottom = p.y;
            let bottomPipeTop = p.y + this.gap;

            if (bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.width) {
                if (bird.y - bird.radius < topPipeBottom || bird.y + bird.radius > bottomPipeTop) {
                    gameOver();
                }
            }

            // Tăng điểm khi vượt qua ống
            if (p.x + this.width < bird.x && !p.passed) {
                score++;
                p.passed = true;
                if (score > highScore) {
                    highScore = score;
                    localStorage.setItem('flappy_highscore', highScore);
                }
            }

            // Di chuyển ống sang trái
            p.x -= this.dx;

            // Xóa ống đã đi ra khỏi màn hình
            if (p.x + this.width <= 0) {
                this.position.shift();
                i--;
            }
        }
    },

    reset() {
        this.position = [];
    }
};

// Vẽ mặt đất
function drawGround() {
    ctx.fillStyle = '#ded895';
    ctx.fillRect(0, canvas.height - 80, canvas.width, 80);
    ctx.fillStyle = '#73bf2e';
    ctx.fillRect(0, canvas.height - 80, canvas.width, 15);
}

// Xử lý sự kiện điều khiển
function handleInput() {
    switch (gameState) {
        case 'START':
            gameState = 'PLAYING';
            bird.flap();
            break;
        case 'PLAYING':
            bird.flap();
            break;
        case 'GAMEOVER':
            pipes.reset();
            bird.reset();
            score = 0;
            frames = 0;
            gameState = 'PLAYING';
            break;
    }
}

window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') handleInput();
});
canvas.addEventListener('click', handleInput);

function gameOver() {
    gameState = 'GAMEOVER';
}

// Hiển thị UI / Điểm số
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
        ctx.fillText('ĐỂ BẮT ĐẦU', canvas.width / 2, canvas.height / 2 + 10);
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

// Vòng lặp chính của Game
function loop() {
    // 1. Xóa màn hình
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 2. Cập nhật trạng thái
    if (gameState === 'PLAYING') {
        bird.update();
        pipes.update();
        frames++;
    }

    // 3. Vẽ lại các thành phần
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
