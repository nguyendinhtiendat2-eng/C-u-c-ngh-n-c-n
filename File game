import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Game Đua Vịt Siêu Cúp",
    page_icon="🦆",
    layout="wide"
)

st.title("🏆 ĐƯỜNG ĐUA VỊT VÔ ĐỊCH 🏆")
st.caption("Game đua vịt sôi nổi tích hợp âm thanh, hiệu ứng bước chạy và pháo hoa ăn mừng!")

# Mã HTML/CSS/JS của Game Đua Vịt
duck_race_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    * { box-sizing: border-box; }

    body {
      font-family: 'Fredoka One', cursive, sans-serif;
      background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
      margin: 0;
      padding: 15px;
      display: flex;
      flex-direction: column;
      align-items: center;
      color: #fff;
      overflow-x: hidden;
    }

    .controls {
      margin-bottom: 20px;
      display: flex;
      gap: 15px;
    }

    button {
      font-family: 'Fredoka One', cursive;
      padding: 12px 28px;
      font-size: 18px;
      color: white;
      background: linear-gradient(180deg, #ff7675, #d63031);
      border: 3px solid #fff;
      border-radius: 30px;
      cursor: pointer;
      box-shadow: 0 6px 0 #b22222, 0 10px 15px rgba(0,0,0,0.4);
      transition: all 0.1s ease;
      text-shadow: 1px 1px 2px #000;
    }

    button:hover { transform: translateY(-2px); box-shadow: 0 8px 0 #b22222, 0 12px 18px rgba(0,0,0,0.5); }
    button:active { transform: translateY(4px); box-shadow: 0 2px 0 #b22222, 0 4px 6px rgba(0,0,0,0.3); }
    button:disabled { background: #b2bec3; box-shadow: 0 4px 0 #636e72; cursor: not-allowed; transform: none; }

    #track-container {
      width: 100%;
      max-width: 800px;
      background: #48dbfb;
      border: 6px solid #fff;
      border-radius: 20px;
      box-shadow: 0 15px 35px rgba(0,0,0,0.5);
      position: relative;
      overflow: hidden;
    }

    .lane {
      position: relative;
      height: 80px;
      border-bottom: 4px dashed rgba(255, 255, 255, 0.8);
      background: repeating-linear-gradient(90deg, #1dd1a1 0px, #1dd1a1 25px, #10ac84 25px, #10ac84 50px);
      background-size: 50px 100%;
    }

    .lane.racing { animation: moveTrack 0.2s linear infinite; }
    @keyframes moveTrack { 0% { background-position-x: 0px; } 100% { background-position-x: -50px; } }
    .lane:last-child { border-bottom: none; }

    .finish-line {
      position: absolute; right: 50px; top: 0; bottom: 0; width: 16px;
      background: repeating-linear-gradient(0deg, #000, #000 12px, #fff 12px, #fff 24px);
      z-index: 1; box-shadow: 0 0 15px #fff, 0 0 25px #fbc531;
    }

    .duck-wrapper {
      position: absolute; left: 10px; top: 8px; z-index: 2;
      transition: left 0.08s linear; display: flex; align-items: center; justify-content: center;
    }

    .duck { font-size: 45px; display: inline-block; user-select: none; filter: drop-shadow(3px 5px 2px rgba(0,0,0,0.3)); }
    .duck-wrapper.running .duck { animation: duckRun 0.18s infinite alternate; }

    @keyframes duckRun {
      0% { transform: scale(1, 0.9) rotate(5deg) translateY(0); }
      100% { transform: scale(0.95, 1.05) rotate(-10deg) translateY(-8px); }
    }

    .duck-wrapper.winner-duck { z-index: 10; }
    .duck-wrapper.winner-duck .duck {
      animation: victoryDance 0.5s infinite alternate ease-in-out !important;
      filter: drop-shadow(0 0 15px #fbc531) drop-shadow(0 0 30px #ff9f43) !important;
    }

    .duck-wrapper.winner-duck::before {
      content: '👑'; position: absolute; top: -25px; font-size: 28px;
      animation: crownFloat 0.5s infinite alternate ease-in-out; filter: drop-shadow(0 0 8px #fff);
    }

    @keyframes victoryDance {
      0% { transform: translateY(0) scale(1.2) rotate(-10deg); }
      100% { transform: translateY(-15px) scale(1.3) rotate(10deg); }
    }

    @keyframes crownFloat {
      0% { transform: translateY(0) rotate(-5deg); }
      100% { transform: translateY(-6px) rotate(5deg); }
    }

    .duck-number {
      font-size: 13px; position: absolute; top: -2px; right: -2px; background: #ff4757;
      color: #fff; border: 2px solid #fff; border-radius: 50%; width: 20px; height: 20px;
      display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }

    #fx-canvas {
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 999;
    }

    #winner-banner {
      position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0);
      background: linear-gradient(145deg, #ffffff, #f1f2f6); border: 6px solid #fbc531;
      padding: 25px 45px; border-radius: 30px; text-align: center;
      box-shadow: 0 20px 60px rgba(0,0,0,0.7), 0 0 40px rgba(251, 197, 49, 0.6); z-index: 1000;
      transition: transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }

    #winner-banner.show { transform: translate(-50%, -50%) scale(1); }
    #winner-banner .trophy { font-size: 55px; margin-bottom: 5px; animation: trophyBounce 0.8s infinite alternate ease-in-out; }
    @keyframes trophyBounce { 0% { transform: scale(1) rotate(-5deg); } 100% { transform: scale(1.2) rotate(5deg); } }
    #winner-banner h2 { margin: 0 0 10px 0; color: #ff4757; font-size: 32px; text-shadow: 2px 2px 0px #fbc531; }
    #winner-banner p { margin: 0; font-size: 20px; color: #2f3542; }
  </style>
</head>
<body>

  <div class="controls">
    <button id="start-btn" onclick="startRace()">🚀 BẮT ĐẦU ĐUA</button>
    <button onclick="resetRace()">🔄 LÀM MỚI</button>
  </div>

  <div id="track-container">
    <div class="finish-line"></div>
    <div class="lane"><div class="duck-wrapper" id="duck1"><span class="duck">🦆</span><span class="duck-number">1</span></div></div>
    <div class="lane"><div class="duck-wrapper" id="duck2"><span class="duck">🦆</span><span class="duck-number">2</span></div></div>
    <div class="lane"><div class="duck-wrapper" id="duck3"><span class="duck">🦆</span><span class="duck-number">3</span></div></div>
    <div class="lane"><div class="duck-wrapper" id="duck4"><span class="duck">🦆</span><span class="duck-number">4</span></div></div>
  </div>

  <div id="winner-banner">
    <div class="trophy">🏆</div>
    <h2 id="winner-title">QUÁN QUÂN XUẤT HIỆN!</h2>
    <p id="winner-text">Chú vịt số 1 đã chiến thắng!</p>
  </div>

  <canvas id="fx-canvas"></canvas>

  <script>
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playQuackSound() {
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(320, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(140, audioCtx.currentTime + 0.12);
      gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.12);
    }

    function playVictorySound() {
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const notes = [261.63, 329.63, 392.00, 523.25, 659.25, 783.99, 1046.50]; 
      notes.forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime + i * 0.09);
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime + i * 0.09);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + i * 0.09 + 0.3);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(audioCtx.currentTime + i * 0.09);
        osc.stop(audioCtx.currentTime + i * 0.09 + 0.3);
      });
    }

    const ducks = [
      { id: 'duck1', pos: 10, num: 1 },
      { id: 'duck2', pos: 10, num: 2 },
      { id: 'duck3', pos: 10, num: 3 },
      { id: 'duck4', pos: 10, num: 4 }
    ];

    let raceInterval = null;
    let isRacing = false;

    function startRace() {
      if (isRacing) return;
      resetRace();
      isRacing = true;
      document.getElementById('start-btn').disabled = true;

      document.querySelectorAll('.lane').forEach(lane => lane.classList.add('racing'));
      document.querySelectorAll('.duck-wrapper').forEach(duck => duck.classList.add('running'));

      const trackWidth = document.getElementById('track-container').offsetWidth - 100;

      raceInterval = setInterval(() => {
        ducks.forEach(duck => {
          const step = Math.random() * 9 + 2;
          duck.pos += step;

          if (Math.random() < 0.08) playQuackSound();

          const el = document.getElementById(duck.id);
          el.style.left = duck.pos + 'px';

          if (duck.pos >= trackWidth && isRacing) {
            isRacing = false;
            clearInterval(raceInterval);
            finishGame(duck);
          }
        });
      }, 70);
    }

    function finishGame(winnerDuck) {
      document.querySelectorAll('.lane').forEach(lane => lane.classList.remove('racing'));
      document.querySelectorAll('.duck-wrapper').forEach(duck => duck.classList.remove('running'));

      const winnerEl = document.getElementById(winnerDuck.id);
      winnerEl.classList.add('winner-duck');

      playVictorySound();
      
      const banner = document.getElementById('winner-banner');
      document.getElementById('winner-text').innerText = `Chú vịt số ${winnerDuck.num} đã đoạt vương miện vô địch!`;
      banner.classList.add('show');
    }

    function resetRace() {
      clearInterval(raceInterval);
      isRacing = false;
      document.getElementById('start-btn').disabled = false;
      document.getElementById('winner-banner').classList.remove('show');
      document.querySelectorAll('.lane').forEach(lane => lane.classList.remove('racing'));
      document.querySelectorAll('.duck-wrapper').forEach(duck => {
        duck.classList.remove('running');
        duck.classList.remove('winner-duck');
      });

      ducks.forEach(duck => {
        duck.pos = 10;
        document.getElementById(duck.id).style.left = '10px';
      });
    }
  </script>
</body>
</html>
"""

# Hiển thị Game lên ứng dụng Streamlit
components.html(duck_race_html, height=600, scrolling=False)
