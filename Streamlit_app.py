import streamlit as st
import streamlit.components.v1 as components

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Flappy Bird Deluxe - B Ray Spotify Edition",
    page_icon="🐤",
    layout="wide"
)

st.title("🐤 Flappy Bird Deluxe - Spotify Edition")
st.caption("🎵 Bài hát: **Vùng An Toàn - B Ray (ft. V#)**")

# Chia bố cục thành 2 cột: Cột trái chơi Game, Cột phải trình phát Spotify & Hướng dẫn
col_game, col_spotify = st.columns([2, 1])

with col_spotify:
    st.subheader("🎧 Trình phát Spotify")
    st.info("💡 **Hướng dẫn:** Bấm nút **Play (▶️)** trên khung Spotify bên dưới để nghe bài hát gốc **'Vùng An Toàn'** chính thức khi chơi game!")
    
    # Nhúng Spotify Embed Player chính thức
    # Lưu ý: Bạn có thể thay đổi ID track nếu muốn phát album hoặc playlist khác
    spotify_embed_code = """
    <iframe style="border-radius:12px" 
            src="https://open.spotify.com/embed/search/V%C3%B9ng%20An%20To%C3%A0n%20B%20Ray?utm_source=generator&theme=0" 
            width="100%" 
            height="152" 
            frameBorder="0" 
            allowfullscreen="" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            loading="lazy">
    </iframe>
    """
    components.html(spotify_embed_code, height=160)

    st.markdown("""
    ---
    ### 🎮 Hướng dẫn chơi:
    - **Phím Spacebar** hoặc **Click chuột**: Điều khiển chim bay lên.
    - **Chọn mức độ**: Dễ, Vừa, Khó ở Màn hình chờ.
    - **Nút 🔊/🔇**: Bật/Tắt âm thanh hiệu ứng (hoặc phím **M**).
    """)

with col_game:
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

    <!-- FILE ÂM THANH NHẠC NỀN DỰ PHÒNG CÓ THỂ MUTE/UNMUTE -->
    <audio id="bgMusic" loop preload="auto">
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">
    </audio>

    <script>
    const canvas = document.getElementById("birdCanvas");
    const ctx = canvas.getContext("2d");
    const bgMusic = document.getElementById("bgMusic");

    // TRẠNG THÁI GAME
    let gameState = 'START';
    let difficulty = 'MEDIUM';
    let isMuted = false;

    // Nút Bật/Tắt hiệu ứng góc trên phải
    const musicBtn = { x: 345, y: 15, w: 40, h: 40 };

    const settings = {
        EASY: { gravity: 0.22, jump: -5.8, speed: 2.0, gap: 160, spawnRate: 110 },
        MEDIUM: { gravity: 0.28, jump: -6.3, speed: 3.2, gap: 135, spawnRate: 90 },
        HARD: { gravity: 0.35, jump: -7.0, speed: 4.6, gap: 115, spawnRate: 70 }
    };

    let bird = { x: 80, y: 280, radius: 14, velocity: 0, rotation: 0 };
    let pipes = [];
    let frameCount = 0;
    let score = 0;
    let highScore = 0;

    function toggleMusic() {
        isMuted = !isMuted;
        bgMusic.muted = isMuted;
        if (!isMuted && bgMusic.paused) {
            bgMusic.play().catch(e => console.log("Cần tương tác để phát nhạc"));
        }
    }

    function playAudio() {
        if (!isMuted && bgMusic.paused) {
            bgMusic.play().catch(e => console.log("Chờ tương tác người dùng"));
        }
    }

    window.addEventListener("keydown", function(e) {
        if (e.code === "KeyM") {
            toggleMusic();
        } else if (e.code === "Space") {
            e.preventDefault();
            playAudio();
            handleInput();
        }
    });

    canvas.addEventListener("click", function(e) {
        const rect = canvas.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const clickY = e.clientY - rect.top;

        if (clickX >= musicBtn.x && clickX <= musicBtn.x + musicBtn.w &&
            clickY >= musicBtn.y && clickY <= musicBtn.y + musicBtn.h) {
            toggleMusic();
            return;
        }

        playAudio();

        if (gameState === 'START') {
            const btnY = 320, btnW = 90, btnH = 36;
            
            if (clickY >= btnY && clickY <= btnY + btnH) {
                if (clickX >= 40 && clickX <= 40 + btnW) difficulty = 'EASY';
                if (clickX >= 155 && clickX <= 155 + btnW) difficulty = 'MEDIUM';
                if (clickX >= 270 && clickX <= 270 + btnW) difficulty = 'HARD';
            }

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

    function drawMusicButton() {
        ctx.save();
        ctx.beginPath();
        ctx.roundRect(musicBtn.x, musicBtn.y, musicBtn.w, musicBtn.h, 10);
        ctx.fillStyle = isMuted ? "rgba(244, 67, 54, 0.85)" : "rgba(76, 175, 80, 0.85)";
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.fillStyle = "#ffffff";
        ctx.font = "20px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(isMuted ? "🔇" : "🔊", musicBtn.x + musicBtn.w / 2, musicBtn.y + musicBtn.h / 2);
        ctx.restore();
    }

    function drawDetailedPipe(x, topHeight, bottomY) {
        const pipeWidth = 58, capHeight = 24, capOutset = 5;

        let bodyGradient = ctx.createLinearGradient(x, 0, x + pipeWidth, 0);
        bodyGradient.addColorStop(0, "#2e7d32");
        bodyGradient.addColorStop(0.2, "#4caf50");
        bodyGradient.addColorStop(0.5, "#81c784");
        bodyGradient.addColorStop(0.8, "#388e3c");
        bodyGradient.addColorStop(1, "#1b5e20");

        let capGradient = ctx.createLinearGradient(x - capOutset, 0, x + pipeWidth + capOutset, 0);
        capGradient.addColorStop(0, "#1b5e20");
        capGradient.addColorStop(0.3, "#66bb6a");
        capGradient.addColorStop(0.7, "#388e3c");
        capGradient.addColorStop(1, "#0d5316");

        ctx.lineWidth = 2;
        ctx.strokeStyle = "#0a3a0a";

        ctx.fillStyle = bodyGradient;
        ctx.fillRect(x, 0, pipeWidth, topHeight - capHeight);
        ctx.strokeRect(x, 0, pipeWidth, topHeight - capHeight);
        ctx.fillStyle = capGradient;
        ctx.fillRect(x - capOutset, topHeight - capHeight, pipeWidth + capOutset * 2, capHeight);
        ctx.strokeRect(x - capOutset, topHeight - capHeight, pipeWidth + capOutset * 2, capHeight);

        ctx.fillRect(x - capOutset, bottomY, pipeWidth + capOutset * 2, capHeight);
        ctx.strokeRect(x - capOutset, bottomY, pipeWidth + capOutset * 2, capHeight);
        ctx.fillStyle = bodyGradient;
        ctx.fillRect(x, bottomY + capHeight, pipeWidth, canvas.height - (bottomY + capHeight));
        ctx.strokeRect(x, bottomY + capHeight, pipeWidth, canvas.height - (bottomY + capHeight));
    }

    function drawBird() {
        ctx.save();
        ctx.translate(bird.x, bird.y);
        bird.rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, bird.velocity * 0.08));
        ctx.rotate(bird.rotation);

        ctx.fillStyle = "#ffeb3b";
        ctx.beginPath(); ctx.arc(0, 0, bird.radius, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = "#f57f17"; ctx.lineWidth = 2; ctx.stroke();

        ctx.fillStyle = "#ffffff";
        ctx.beginPath(); ctx.arc(6, -5, 5, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = "#000000";
        ctx.beginPath(); ctx.arc(8, -5, 2, 0, Math.PI * 2); ctx.fill();

        ctx.fillStyle = "#ff5722";
        ctx.beginPath(); ctx.moveTo(10, 0); ctx.lineTo(18, 3); ctx.lineTo(10, 7); ctx.closePath(); ctx.fill();

        ctx.fillStyle = "#fbc02d";
        ctx.beginPath(); ctx.ellipse(-5, 2, 7, 4, Math.PI / 6, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
    }

    function drawStartScreen() {
        ctx.fillStyle = "#70c5ce";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#fff";
        ctx.font = "900 36px 'Segoe UI', sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("FLAPPY BIRD", canvas.width / 2, 100);
        ctx.fillStyle = "#fbc02d";
        ctx.fillText("DELUXE", canvas.width / 2, 145);

        ctx.fillStyle = "#01579b";
        ctx.font = "italic 13px sans-serif";
        ctx.fillText("🎵 Spotify: Vùng An Toàn - B Ray", canvas.width / 2, 175);

        bird.y = 215 + Math.sin(Date.now() / 200) * 6;
        drawBird();

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 15px sans-serif";
        ctx.fillText("CHỌN MỨC ĐỘ KHÓ:", canvas.width / 2, 295);

        const btnY = 320, btnW = 90, btnH = 36;
        const diffs = [
            { key: 'EASY', label: 'DỄ', x: 40, color: '#4caf50' },
            { key: 'MEDIUM', label: 'VỪA', x: 155, color: '#ff9800' },
            { key: 'HARD', label: 'KHÓ', x: 270, color: '#f44336' }
        ];

        diffs.forEach(d => {
            ctx.beginPath(); ctx.roundRect(d.x, btnY, btnW, btnH, 8);
            ctx.fillStyle = (difficulty === d.key) ? d.color : "#e0e0e0";
            ctx.fill();
            ctx.fillStyle = (difficulty === d.key) ? "#ffffff" : "#616161";
            ctx.font = "bold 14px sans-serif";
            ctx.fillText(d.label, d.x + btnW / 2, btnY + 23);
        });

        let startBtnGradient = ctx.createLinearGradient(100, 410, 300, 465);
        startBtnGradient.addColorStop(0, "#81c784");
        startBtnGradient.addColorStop(1, "#388e3c");

        ctx.beginPath(); ctx.roundRect(100, 410, 200, 55, 28);
        ctx.fillStyle = startBtnGradient; ctx.fill();

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 20px 'Segoe UI', sans-serif";
        ctx.fillText("BẮT ĐẦU PLAY 🚀", canvas.width / 2, 445);
    }

    function drawGameOverScreen() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 32px sans-serif"; ctx.textAlign = "center";
        ctx.fillText("GAME OVER", canvas.width / 2, 230);
        ctx.font = "20px sans-serif";
        ctx.fillText("Điểm số: " + score, canvas.width / 2, 280);
        ctx.fillStyle = "#ffeb3b"; ctx.font = "16px sans-serif";
        ctx.fillText("Nhấn SPACE hoặc CLICK để thử lại", canvas.width / 2, 390);
    }

    function loop() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (gameState === 'START') {
            drawStartScreen();
        } else if (gameState === 'PLAYING') {
            const cfg = settings[difficulty];
            ctx.fillStyle = "#70c5ce"; ctx.fillRect(0, 0, canvas.width, canvas.height);

            bird.velocity += cfg.gravity;
            bird.y += bird.velocity;

            if (bird.y + bird.radius >= canvas.height - 40 || bird.y - bird.radius <= 0) {
                gameState = 'GAMEOVER';
            }

            frameCount++;
            if (frameCount % cfg.spawnRate === 0) {
                const minHeight = 50;
                const maxHeight = canvas.height - 40 - cfg.gap - minHeight;
                const topHeight = Math.floor(Math.random() * (maxHeight - minHeight + 1)) + minHeight;
                pipes.push({ x: canvas.width, top: topHeight, bottom: topHeight + cfg.gap, passed: false });
            }

            for (let i = 0; i < pipes.length; i++) {
                let p = pipes[i];
                p.x -= cfg.speed;
                drawDetailedPipe(p.x, p.top, p.bottom);

                if (bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + 58 &&
                    (bird.y - bird.radius < p.top || bird.y + bird.radius > p.bottom)) {
                    gameState = 'GAMEOVER';
                }

                if (!p.passed && p.x + 58 < bird.x) {
                    p.passed = true;
                    score++;
                }
            }

            pipes = pipes.filter(p => p.x > -80);
            drawBird();

            ctx.fillStyle = "#ded895"; ctx.fillRect(0, canvas.height - 40, canvas.width, 40);
            ctx.fillStyle = "#ffffff"; ctx.font = "900 36px sans-serif"; ctx.textAlign = "center";
            ctx.fillText(score, canvas.width / 2, 60);
        } else if (gameState === 'GAMEOVER') {
            drawGameOverScreen();
        }

        drawMusicButton();

        requestAnimationFrame(loop);
    }

    loop();
    </script>
    </body>
    </html>
    """

    components.html(game_code, height=630)
  
