import streamlit as st
import random
import time

st.set_page_config(
    page_title="Game Câu Cá May Mắn",
    page_icon="🎣",
    layout="centered"
)

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
if "last_catch" not in st.session_state:
    st.session_state.last_catch = {"name": "Sẵn sàng thả câu", "icon": "🌊", "rarity": "Bắt đầu"}

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

st.title("🎣 Game May Rủi: Câu Cá Đổi Thưởng")

col1, col2, col3 = st.columns(3)
col1.metric("💰 Xu", f"{st.session_state.money}")
col2.metric("🎣 Cần", ROD_UPGRADES[st.session_state.rod_level]["name"])
col3.metric("🐟 Số lần", f"{st.session_state.total_catches}")

st.divider()

tab_play, tab_shop, tab_inventory = st.tabs(["🎮 Câu cá", "🛒 Cửa hàng", "🎒 Túi đồ"])

with tab_play:
    st.subheader("🏞️ Khu vực Bờ Sông & Dưới Nước")
    st.info(f"🧑‍🌾 **Trên bờ:** Đang thả cần câu 🎣\n\n🌊 **Dưới nước (🐟 🐠 🦈):** {st.session_state.last_catch['icon']} Vừa bắt được: **{st.session_state.last_catch['name']}**")
    
    if st.button("🎣 THẢ CÂU NGAY (Tốn 5 xu)", use_container_width=True, type="primary"):
        if st.session_state.money < 5:
            st.error("Không đủ xu! Hãy bán cá trong túi đồ.")
        else:
            st.session_state.money -= 5
            with st.spinner("Đang chờ cá cắn câu... 🌊"):
                time.sleep(1)
            
            luck = ROD_UPGRADES[st.session_state.rod_level]["luck_bonus"]
            weights = [f["weight"] + (luck/4 if f["rarity"]!="Rác" else 0) for f in FISH_TYPES]
            caught = random.choices(FISH_TYPES, weights=weights, k=1)[0]
            
            st.session_state.total_catches += 1
            st.session_state.inventory[caught["name"]] = st.session_state.inventory.get(caught["name"], 0) + 1
            st.session_state.last_catch = caught
            
            if caught["rarity"] in ["Cực hiếm", "Huyền thoại"]:
                st.balloons()
                st.success(f"🎉 TRÚNG LỚN! Bắt được **{caught['name']}** {caught['icon']}")
            elif caught["rarity"] == "Rác":
            
                st.warning(f"😅 Xui xẻo! Vớt phải {caught['name']} {caught['icon']}")
            else:
                st.info(f"✨ Bắt được **{caught['name']}** {caught['icon']}")
            st.rerun()

    st.subheader("📜 Nhật ký")
    for log in st.session_state.logs[:3]:
        st.write(log)

with tab_shop:
    st.subheader("Cửa hàng nâng cấp")
    next_level = st.session_state.rod_level + 1
    if next_level in ROD_UPGRADES:
        info = ROD_UPGRADES[next_level]
        st.write(f"Nâng cấp lên **{info['name']}** - Giá: {info['cost']} xu")
        if st.button("Mua ngay"):
            if st.session_state.money >= info["cost"]:
                st.session_state.money -= info["cost"]
                st.session_state.rod_level = next_level
                st.success("Nâng cấp thành công!")
                st.rerun()
            else:
                st.error("Không đủ xu!")
    else:
        st.success("Đã đạt cấp tối đa!")

with tab_inventory:
    st.subheader("Túi đồ của bạn")
    if not st.session_state.inventory:
        st.write("Túi trống.")
    else:
        total_sell = 0
        for item, count in st.session_state.inventory.items():
            price = next(f["price"] for f in FISH_TYPES if f["name"] == item)
            icon = next(f["icon"] for f in FISH_TYPES if f["name"] == item)
            st.write(f"{icon} **{item}**: {count} con ({price * count} xu)")
            total_sell += price * count
        
        if st.button("💰 Bán tất cả lấy xu", type="primary"):
            st.session_state.money += total_sell
            st.session_state.inventory = {}
            st.success(f"Thu về {total_sell} xu!")
            st.rerun()
