import time
import random
import streamlit as st

st.set_page_config(
    page_title="Câu Cá & Đua Vịt Chọn Tên", page_icon="🎣", layout="centered"
)

st.title("🎣 Minigame: Câu Cá & Đua Vịt Chọn Tên 🦆")
st.write(
    "Kết hợp hoàn hảo: Câu cá tích lũy kỹ năng/điểm số, sau đó đưa danh sách tên vào đường đua vịt để tìm ra người chiến thắng!"
)

# Khởi tạo Session State để lưu trữ điểm số và trạng thái game câu cá
if "score" not in st.session_state:
    st.session_state.score = 0
if "fish_count" not in st.session_state:
    st.session_state.fish_count = 0
if "fishing_status" not in st.session_state:
    st.session_state.fishing_status = "idle"  # idle, waiting, biting
if "bite_time" not in st.session_state:
    st.session_state.bite_time = 0

st.markdown("---")

# ================= PHẦN 1: CÂU CÁ =================
st.subheader("Giai đoạn 1: Sân Câu Cá 🌊")

col1, col2, col3 = st.columns(3)
col1.metric("Điểm thưởng", st.session_state.score)
col2.metric("Số cá bắt được", st.session_state.fish_count)
col3.metric(
    "Trạng thái",
    (
        "Đang rảnh"
        if st.session_state.fishing_status == "idle"
        else ("Chờ cá..." if st.session_state.fishing_status == "waiting" else "⚠️ CÁ CẮN CÂU!")
    ),
)

fishing_message = st.empty()

# Nút điều khiển câu cá
c1, c2 = st.columns(2)

with c1:
    if st.button("🎣 Thả cần câu"):
        if st.session_state.fishing_status == "idle":
            st.session_state.fishing_status = "waiting"
            st.session_state.bite_time = (
                time.time() + random.uniform(1.5, 3.5)
            )  # Thời gian cá cắn ngẫu nhiên
            st.rerun()

with c2:
    pull_btn = st.button("⚡ KÉO CẦN NGAY!")

# Xử lý logic thời gian chờ cá cắn
if st.session_state.fishing_status == "waiting":
    if time.time() >= st.session_state.bite_time:
        st.session_state.fishing_status = "biting"
        st.rerun()
    else:
        fishing_message.info(
            "⏳ Phao đang nổi bập bềnh... Chờ cá cắn câu nhé..."
        )
        time.sleep(0.5)
        st.rerun()
elif st.session_state.fishing_status == "biting":
    fishing_message.warning(
        "🚨 **CÁ CẮN CÂU RỒI! BẤM 'KÉO CẦN NGAY' LẬP TỨC!**"
    )

# Xử lý sự kiện kéo cần
if pull_btn:
    if st.session_state.fishing_status == "biting":
        st.session_state.score += 10
        st.session_state.fish_count += 1
        st.session_state.fishing_status = "idle"
        fishing_message.success(
            "🎉 Chúc mừng! Bạn đã câu thành công 1 chú cá (+10 điểm)!"
        )
        st.rerun()
    elif st.session_state.fishing_status == "waiting":
        st.session_state.fishing_status = "idle"
        fishing_message.error("❌ Bạn kéo quá sớm! Cá chưa kịp cắn đã sợ chạy mất.")
        st.rerun()
    else:
        fishing_message.info("⚠️ Bạn chưa thả cần câu mà!")

st.markdown("---")

# ================= PHẦN 2: ĐUA VỊT CHỌN TÊN =================
st.subheader("Giai đoạn 2: Đua Vịt Chọn Tên 🏁")

default_names = "An\nBình\nCường\nDung\nHoàng"
names_input = st.text_area(
    "Nhập danh sách tên cần chọn (mỗi tên một dòng):", value=default_names, height=100
)

if st.button("🚀 Bắt đầu Cuộc Đua Vịt!"):
    names = [n.strip() for n in names_input.split("\n") if n.strip()]

    if len(names) < 2:
        st.warning("Vui lòng nhập ít nhất 2 tên để tổ chức cuộc đua!")
    else:
        # Khởi tạo vị trí ban đầu của các chú vịt (từ 0 đến 100)
        positions = {name: 0 for name in names}
        finish_line = 100
        winner = None

        progress_container = st.empty()
        status_container = st.empty()

        status_container.info(
            "🏁 Tiếng còi vang lên! Đàn vịt đang bơi hết tốc lực..."
        )

        # Mô phỏng quá trình đua vịt theo từng bước
        while not winner:
            chart_data = {}
            for name in names:
                # Tăng bước nhảy ngẫu nhiên cho từng chú vịt
                positions[name] += random.randint(5, 15)
                if positions[name] >= finish_line:
                    positions[name] = finish_line
                    winner = name
                chart_data[name] = positions[name]

            # Hiển thị biểu đồ thanh mô phỏng đường đua
            with progress_container.container():
                st.bar_chart(chart_data)

            if winner:
                break
            time.sleep(0.15)

        status_container.success(
            f"🏆 **CHÚC MỪNG!** Vịt mang tên **[ {winner} ]** đã về đích đầu tiên và giành chiến thắng tuyệt đối! 🎉"
  )
