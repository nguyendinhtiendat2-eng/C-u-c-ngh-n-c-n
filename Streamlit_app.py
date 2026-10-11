import streamlit as st
import random
import time

st.set_page_config(page_title="Game Câu Cá", page_icon="🎣")

if "started" not in st.session_state:
    st.session_state.started = False
if "money" not in st.session_state:
    st.session_state.money = 100
if "rod" not in st.session_state:
    st.session_state.rod = 1
if "bag" not in st.session_state:
    st.session_state.bag = {}
if "total" not in st.session_state:
    st.session_state.total = 0
if "logs" not in st.session_state:
    st.session_state.logs = []
if "last" not in st.session_state:
    st.session_state.last = "Chưa có gì"

FISH = [
    ("Rác", 0, "Rác", 40, "👞"),
    ("Cá Chép", 20, "Thường", 35, "🐟"),
    ("Cá Hồi", 50, "Hiếm", 17, "🐠"),
    ("Cá Ngừ", 120, "Cực hiếm", 6, "🐡"),
    ("Cá Mập", 500, "Huyền thoại", 2, "🦈")
]

RODS = {
    1: ("Cần Trúc", 0, 0),
    2: ("Cần Máy", 200, 5),
    3: ("Cần Carbon", 600, 12)
}

if not st.session_state.started:
    st.title("🎣 GAME CÂU CÁ MAY MẮN")
    st.write("Săn cá đổi thưởng ngay trên điện thoại!")
    st.info("Bắt đầu với 100 xu. Mỗi lần câu tốn 5 xu.")
    if st.button("🚀 BẮT ĐẦU CHƠI", use_container_width=True, type="primary"):
        st.session_state.started = True
        st.rerun()
else:
    st.title("🎣 Câu Cá Đổi Thưởng")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Xu", st.session_state.money)
    c2.metric("🎣 Cần", RODS[st.session_state.rod][0])
    c3.metric("🐟 Số lần", st.session_state.total)
    
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["🎮 Câu cá", "🛒 Cửa hàng", "🎒 Túi đồ"])
    
    with tab1:
        st.write(f"🏞️ **Trạng thái:** {st.session_state.last}")
        
        if st.button("🎣 THẢ CÂU (5 xu)", use_container_width=True, type="primary"):
            if st.session_state.money < 5:
                st.error("Bạn hết xu rồi! Hãy bán cá trong túi đồ.")
            else:
                st.session_state.money -= 5
                with st.spinner("Đang chờ cá cắn câu..."):
                    time.sleep(1)
                
                bonus = RODS[st.session_state.rod][2]
                weights = [w + (bonus if r != "Rác" else 0) for _, _, r, w, _ in FISH]
                
                caught = random.choices(FISH, weights=weights, k=1)[0]
                name, price, rarity, _, icon = caught
                
                st.session_state.total += 1
                st.session_state.bag[name] = st.session_state.bag.get(name, 0) + 1
                st.session_state.last = f"{icon} Bắt được {name} ({rarity})"
                
                if rarity == "Huyền thoại":
                    st.balloons()
                    st.success(f"🎉 TRÚNG LỚN! {icon} {name}")
                elif rarity == "Rác":
                    st.warning(f"😅 Xui xẻo! Vớt phải {icon} {name}")
                else:
                    st.info(f"✨ Bắt được {icon} {name}")
                st.rerun()
        
        st.subheader("📜 Nhật ký")
        for l in st.session_state.logs[:3]:
            st.write(l)
            
    with tab2:
        st.subheader("Nâng cấp cần câu")
        next_r = st.session_state.rod + 1
        if next_r in RODS:
            r_name, r_cost, _ = RODS[next_r]
            st.write(f"Nâng lên **{r_name}** - Giá: {r_cost} xu")
            if st.button("Mua nâng cấp"):
                if st.session_state.money >= r_cost:
                    st.session_state.money -= r_cost
                    st.session_state.rod = next_r
                    st.success("Nâng cấp thành công!")
                    st.rerun()
                else:
                    st.error("Không đủ xu!")
        else:
            st.success("Đã đạt cấp tối đa!")
            
    with tab3:
        st.subheader("Túi cá của bạn")
        if not st.session_state.bag:
            st.write("Túi đang trống.")
        else:
            total_val = 0
            for name, count in st.session_state.bag.items():
                price = next(p for n, p, _, _, _ in FISH if n == name)
                icon = next(i for n, _, _, _, i in FISH if n == name)
                st.write(f"{icon} **{name}**: {count} con ({price * count} xu)")
                total_val += price * count
  
