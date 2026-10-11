import streamlit as st
import random
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Game Câu Cá May Mắn",
    page_page_icon="🎣",
    layout="centered"
)

# --- KHỞI TẠO STATE ---
if "money" not in st.session_state:
    st.session_state.money = 100
if "rod_level" not in st.session_state:
    st.session_state.rod_level = 1
if "inventory" not in st.session_state:
    st.session_state.inventory = {}
if "total_catches" not in st.session_state:
    st.session_state.total_catches = 0
if "logs" not in st.session_state:
    st.session_state.logs = []

# --- DỮ LIỆU CÁ & CẦN CÂU ---
FISH_TYPES = [
    {"name": "Rác / Giày cũ", "price": 0, "rarity": "Rác", "weight": 35, "icon": "👞"},
    {"name": "Cá Chép", "price": 20, "rarity": "Phổ thông", "weight": 35, "icon": "🐟"},
    {"name": "Cá Hồi", "price": 50, "rarity": "Hiếm", "weight": 18, "icon": "🐠"},
    {"name": "Cá Ngừ", "price": 120, "rarity": "Cực hiếm", "weight": 9, "icon": "🐡"},
    {"name": "Cá Mập Vàng", "price": 500, "rarity": "Huyền thoại", "weight": 3, "icon": "🦈"},
]

ROD_UPGRADES = {
    1: {"name": "Cần Trúc", "cost": 0, "luck_bonus": 0},
    2: {"name": "Cần Máy", "cost": 200, "luck_bonus": 5},
    3: {"name": "Cần Carbon", "cost": 600, "luck_bonus": 12},
}

# --- PHẦN PHÁT ÂM THANH (Web Audio API) ---
def play_sound(sound_type):
    if sound_type == "catch":
        # Âm thanh bắt được cá
        js = """
        <script>
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.connect(gain); gain.connect(ctx.destination);
        osc.frequency.setValueAtTime(440, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.3, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
        osc.start(); osc.stop(ctx.currentTime + 0.3);
        </script>
        """
    else:
        # Âm thanh thả câu
        js = """
        <script>
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.connect(gain); gain.connect(ctx.destination);
        osc.frequency.setValueAtTime(200, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(100, ctx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2);
        osc.start(); osc.stop(ctx.currentTime + 0.2);
        </script>
        """
    st.components.v1.html(js, height=0)

# --- HÀM XỬ LÝ CÂU CÁ ---
def cast_line():
    # Điều chỉnh tỷ lệ may rủi dựa trên cấp cần câu
    luck = ROD_UPGRADES[st.session_state.rod_level]["luck_bonus"]
    weights = []
    for fish in FISH_TYPES:
        w = fish["weight"]
        if fish["rarity"] != "Rác":
            w += luck / 4
        weights.append(max(w, 1))

    # Quay số may rủi chọn loại cá
    caught_fish = random.choices(FISH_TYPES, weights=weights, k=1)[0]
    
    # Cập nhật thông số
    st.session_state.total_catches += 1
    fish_name = caught_fish["name"]
    st.session_state.inventory[fish_name] = st.session_state.inventory.get(fish_name, 0) + 1
    
    log_entry = f"{caught_fish['icon']} Bạn đã câu được **{fish_name}** ({caught_fish['rarity']}) - Trị giá: {caught_fish['price']} xu"
    st.session_state.logs.insert(0, log_entry)
    
    return caught_fish

# --- GIAO DIỆN CHÍNH ---
st.title("🎣 Game May Rủi: Câu Cá Đổi Thưởng")

# Hiển thị chỉ số
col1, col2, col3 = st.columns(3)
col1.metric("💰 Xu hiện có", f"{st.session_state.money} xu")
col2.metric("🎣 Cần câu", ROD_UPGRADES[st.session_state.rod_level]["name"])
col3.metric("🐟 Số lần đã câu", f"{st.session_state.total_catches}")

st.divider()

# TAB CHỨC NĂNG
tab_play, tab_shop, tab_inventory = st.tabs(["🎮 Bắt đầu câu", "🛒 Cửa hàng", "🎒 Túi đồ"])

with tab_play:
    st.write("Nhấn nút bên dưới để thử vận may của bạn!")
    if st.button("🎣 THẢ CÂU (Tốn 5 xu)", use_container_width=True, type="primary"):
        if st.session_state.money < 5:
            st.error("Bạn không đủ xu để thả câu! Hãy bán bớt cá trong túi đồ.")
        else:
            st.session_state.money -= 5
            play_sound("cast")
            
            # Hiệu ứng chờ may rủi
            with st.spinner("Đang chờ cá cắn câu..."):
                time.sleep(1.2)
            
            caught = cast_line()
            play_sound("catch")
            
            if caught["rarity"] in ["Cực hiếm", "Huyền thoại"]:
                st.balloons()
                st.success(f"🎉 TRÚNG LỚN! Bạn đã câu được **{caught['name']}** {caught['icon']}")
            elif caught["rarity"] == "Rác":
                st.warning(f"😅 Xui xẻo rồi! Bạn chỉ câu được {caught['name']} {caught['icon']}")
            else:
                st.info(f"✨ Bạn câu được **{caught['name']}** {caught['icon']}")

    # Nhật ký câu cá
    st.subheader("📜 Nhật ký vận may")
    for log in st.session_state.logs[:5]:
        st.markdown(log)

with tab_shop:
    st.subheader("Nâng cấp cần câu để tăng may mắn!")
    next_level = st.session_state.rod_level + 1
    if next_level in ROD_UPGRADES:
        info = ROD_UPGRADES[next_level]
        st.write(f"**{info['name']}**")
        st.write(f"- Giá: {info['cost']} xu")
        st.write(f"- Tăng tỉ lệ gặp cá hiếm/huyền thoại: +{info['luck_bonus']}%")
        
        if st.button(f"Mua {info['name']}", key="buy_rod"):
            if st.session_state.money >= info["cost"]:
                st.session_state.money -= info["cost"]
                st.session_state.rod_level = next_level
                st.success(f"Chúc mừng bạn đã nâng cấp thành công lên {info['name']}!")
                st.rerun()
            else:
                st.error("Bạn không có đủ xu!")
    else:
        st.success("🥇 Bạn đã sở hữu Cần câu cấp tối đa!")

with tab_inventory:
    st.subheader("Các loại cá bạn đang sở hữu")
    if not st.session_state.inventory:
        st.write("Túi đồ trống.")
    else:
        total_sell = 0
        for item, count in st.session_state.inventory.items():
            price = next(f["price"] for f in FISH_TYPES if f["name"] == item)
            icon = next(f["icon"] for f in FISH_TYPES if f["name"] == item)
            st.write(f"{icon} **{item}**: {count} con (Tổng giá trị: {price * count} xu)")
            total_sell += price * count
        
        if st.button("💰 Bán tất cả lấy Xu", type="primary"):
            st.session_state.money += total_sell
            st.session_state.inventory = {}
            st.success(f"Đã bán toàn bộ thu về {total_sell} xu!")
            st.rerun()
