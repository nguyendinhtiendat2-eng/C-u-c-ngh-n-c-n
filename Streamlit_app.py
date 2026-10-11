import random
import time
import streamlit as st

# Thiết lập giao diện trang
st.set_page_config(
    page_title="Câu Cá May Mắn - Random Picker", page_icon="🎣", layout="centered"
)


# Khởi tạo Session State để lưu danh sách người và lịch sử
if "participants" not in st.session_state:
    st.session_state.participants = [
        "Nguyễn Văn A",
        "Trần Thị B",
        "Lê Văn C",
        "Phạm Thị D",
        "Hoàng Văn E",
    ]

if "history" not in st.session_state:
    st.session_state.history = []

if "hooked_person" not in st.session_state:
    st.session_state.hooked_person = None

if "fishing" not in st.session_state:
    st.session_state.fishing = False

# Tiêu đề game
st.title("🎣 Câu Cá May Mắn - Random Picker")
st.markdown(
    "Thả cần câu xuống dòng sông dữ liệu và xem ai sẽ là người 'cắn câu' ngẫu nhiên nhé!"
)

# --- THANH BÊN (SIDEBAR) ĐỂ CÀI ĐẶT DANH SÁCH ---
with st.sidebar:
    st.header("⚙️ Cài đặt danh sách")

    # Nhập danh sách mới
    input_mode = st.radio(
        "Cách nhập danh sách:", ("Nhập từng người", "Nhập danh sách hàng loạt")
    )

    if input_mode == "Nhập từng người":
        with st.form("add_person_form", clear_on_submit=True):
            new_name = st.text_input("Tên người tham gia:")
            submitted = st.form_submit_button("Thêm vào danh sách")
            if submitted and new_name:
                if new_name not in st.session_state.participants:
                    st.session_state.participants.append(new_name)
                    st.success(f"Đã thêm: {new_name}")
                else:
                    st.warning("Tên này đã có trong danh sách!")
    else:
        bulk_input = st.text_area(
            "Nhập danh sách (mỗi người một dòng):",
            value="\n".join(st.session_state.participants),
        )
        if st.button("Cập nhật danh sách"):
            names = [
                n.strip() for n in bulk_input.split("\n") if n.strip()
            ]
            if names:
                st.session_state.participants = names
                st.success("Đã cập nhật danh sách thành công!")
            else:
                st.error("Danh sách không được để trống.")

    st.markdown("---")
    if st.button("🗑️ Xóa toàn bộ lịch sử câu"):
        st.session_state.history = []
        st.success("Đã xóa lịch sử!")

# --- KHU VỰC HIỂN THỊ TRÒ CHƠI ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🌊 Hồ Câu Dữ Liệu")

    # Hiển thị số lượng người còn lại
    num_people = len(st.session_state.participants)
    st.info(f"Hiện có **{num_people}** người đang bơi lội trong hồ.")

    if num_people == 0:
        st.warning(
            "Hồ đã cạn cá (hết người)! Vui lòng thêm người ở thanh bên cạnh."
        )
    else:
        # Nút thả thính / câu cá
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            remove_after_catch = st.checkbox(
                "Bắt xong thả ra / Giữ lại trong hồ", value=True
            )
            # True: Bắt xong giữ lại trong hồ (cho phép lặp lại)
            # False: Bắt xong bỏ ra khỏi danh sách

        if st.button("🎣 Quăng cần câu ngay!", type="primary", use_container_width=True):
            if num_people > 0:
                st.session_state.fishing = True
                st.session_state.hooked_person = None

                # Hiệu ứng chờ câu cá
                with st.spinner("Đang thả mồi... Chờ cá cắn câu... 🌊🐟"):
                    time.sleep(1.5)  # Hiệu ứng hồi hộp

                # Chọn ngẫu nhiên
                chosen = random.choice(st.session_state.participants)
                st.session_state.hooked_person = chosen
                st.session_state.fishing = False

                # Thêm vào lịch sử
                st.session_state.history.insert(0, chosen)

                # Nếu cấu hình là loại bỏ người đã bắt khỏi danh sách (tùy chỉnh logic)
                # Ở đây dùng checkbox ngược lại: nếu không check giữ lại thì xóa
                if not remove_after_catch:
                    st.session_state.participants.remove(chosen)

                st.rerun()

        # Hiển thị kết quả câu được
        if st.session_state.hooked_person:
            st.success(
                f"🎉 Chúc mừng! Bạn đã câu được: **{st.session_state.hooked_person}** 🐟"
            )
            st.balloons()

with col2:
    st.subheader("📋 Lịch sử câu")
    if st.session_state.history:
        for idx, person in enumerate(
            st.session_state.history[:10]
        ):  # Hiển thị 10 lần gần nhất
            st.write(f"{idx + 1}. **{person}**")
    else:
        st.write("Chưa có ai cắn câu cả.")

# Hiển thị danh sách hiện tại trong hồ ở màn hình chính cho trực quan
with st.expander("👀 Xem danh sách người trong hồ hiện tại"):
    if st.session_state.participants:
        st.write(", ".join(st.session_state.participants))
    else:
        st.text("Hồ trống không.")
                                                         
