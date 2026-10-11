import random
import time
import streamlit as st
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Hồ Câu May Mắn - Random Picker 3.0",
    page_icon="🎣",
    layout="wide",  # Sử dụng chế độ rộng để hiển thị hồ cá tốt hơn
)

# --- CSS TÙY CHỈNH ĐỂ TẠO GIAO DIỆN HỒ CÁ & NGƯỜI CÂU ---
st.markdown(
    """
<style>
    /* Tổng thể */
    .stApp {
        background-color: #f0f8ff; /* Màu xanh nước biển nhạt */
    }

    /* Tiêu đề chính */
    .main-title {
        text-align: center;
        color: #0056b3;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        text-shadow: 2px 2px 4px #aaa;
    }

    /* --- Khu vực Người Câu --- */
    .fisherman-container {
        text-align: center;
        padding: 10px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
    }
    .fisherman-img {
        max-width: 150px;
        height: auto;
    }

    /* --- Khu vực Hồ Cá --- */
    .lake-container {
        background-color: #0077be; /* Màu xanh đậm của nước */
        border: 5px solid #0056b3;
        border-radius: 20px;
        padding: 20px;
        min-height: 400px;
        position: relative;
        overflow: hidden; /* Để cá không bơi ra ngoài */
    }

    .lake-title {
        color: white;
        text-align: center;
        margin-bottom: 20px;
        font-size: 1.5rem;
    }

    /* --- Định dạng Chú Cá (Chứa Tên) --- */
    .fish-wrapper {
        display: inline-block;
        margin: 10px;
        position: relative; /* Dùng cho hiệu ứng bơi nếu muốn nâng cấp */
        transition: transform 0.2s;
    }
    
    .fish-wrapper:hover {
        transform: scale(1.1); /* Phóng to nhẹ khi di chuột vào */
    }

    .fish-icon {
        width: 80px; /* Độ rộng ảnh con cá */
        height: auto;
    }

    .fish-name {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-45%, -50%); /* Căn chỉnh tên vào giữa thân cá */
        color: #333;
        font-weight: bold;
        font-size: 0.85rem;
        white-space: nowrap; /* Không cho xuống dòng */
        overflow: hidden;
        text-overflow: ellipsis; /* Nếu tên quá dài */
        max-width: 60px; /* Giới hạn độ dài tên hiển thị */
    }
    
    /* Hiệu ứng "đang câu" */
    .fishing-spinner {
        text-align: center;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: 20px;
    }

</style>
""",
    unsafe_allow_html=True,
)


# --- KHỞI TẠO SESSION STATE ---
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

if "last_action" not in st.session_state:
    st.session_state.last_action = None


# --- HÀM TRỢ GIÚP ĐỂ HIỂN THỊ HÌNH ẢNH CÁ ---
def get_fish_html(name, fish_img_path="fish_icon.png"):
    """Tạo HTML cho một con cá chứa tên."""
    if os.path.exists(fish_img_path):
        # Sử dụng ảnh nếu tồn tại
        return f"""
        <div class="fish-wrapper">
            <img src="app/static/{fish_img_path}" class="fish-icon" alt="Cá">
            <div class="fish-name">{name}</div>
        </div>
        """
    else:
        # Sử dụng ký tự 🐟 nếu không có ảnh
        return f"""
        <div class="fish-wrapper" style="background:rgba(255,255,255,0.7); padding: 5px 10px; border-radius:15px;">
            <span style="font-size:1.2rem;">🐟</span> **{name}**
        </div>
        """


# --- TIÊU ĐỀ CHÍNH ---
st.markdown(
    '<h1 class="main-title">🎣 HỒ CÂU MAY MẮN 🎣</h1>', unsafe_allow_html=True
)
st.markdown("---")

# --- BỐ CỤC CHÍNH (MAIN LAYOUT) ---
col_game, col_history = st.columns([3, 1])

with col_game:
    # --- MÀN HÌNH CHÍNH (Người Câu + Hồ Cá) ---
    col_fisherman, col_lake = st.columns([1, 2])

    # 1. Màn hình hiển thị Người Câu
    with col_fisherman:
        st.markdown('<div class="fisherman-container">', unsafe_allow_html=True)
        st.subheader("🕵️‍♂️ Người Câu")

        # Hiển thị hình ảnh người câu (nếu có)
        fisherman_img_path = "fisherman.png"
        if os.path.exists(fisherman_img_path):
            st.image(fisherman_img_path, use_column_width=False, width=150)
        else:
            st.markdown(
                "<h1 style='text-align:center; font-size:5rem;'>👴</h1>",
                unsafe_allow_html=True,
            )

        st.markdown(f"**Số người trong hồ:** {len(st.session_state.participants)}")
        st.markdown("</div>", unsafe_allow_html=True)

        # Nút điều khiển
        st.markdown("---")
        remove_after_catch = st.checkbox(
            "Loại bỏ sau khi câu", value=True, help="Nếu chọn, người được câu sẽ bị xóa khỏi hồ."
        )

        if st.button("🎣 Quăng Cần!", type="primary", use_container_width=True):
            if not st.session_state.participants:
                st.warning("Hồ hết cá rồi! Vui lòng thêm người ở Sidebar.")
            else:
                st.session_state.fishing = True
                st.session_state.hooked_person = None
                st.rerun()

    # 2. Màn hình hiển thị Hồ Cá chứa tên
    with col_lake:
        st.markdown('<div class="lake-container">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="lake-title">🌊 Hồ Dữ Liệu ({len(st.session_state.participants)} chú cá) 🌊</div>',
            unsafe_allow_html=True,
        )

        # Hiển thị các con cá
        if st.session_state.participants:
            fish_html_content = ""
            for person in st.session_state.participants:
                fish_html_content += get_fish_html(person)

            st.markdown(
                f'<div style="text-align:center;">{fish_html_content}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<h3 style='text-align:center; color:white;'>Hồ trống rỗng...</h3>",
                unsafe_allow_html=True,
            )

        # Hiển thị trạng thái đang câu
        if st.session_state.fishing:
            st.markdown(
                '<div class="fishing-spinner">⌛ Đang thả mồi... Chờ chút... 🌊</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


# --- XỬ LÝ LOGIC CÂU CÁ (Khi đang câu) ---
if st.session_state.fishing:
    time.sleep(2)  # Tạo độ trễ 2 giây để hồi hộp

    # Chọn ngẫu nhiên
    chosen = random.choice(st.session_state.participants)
    st.session_state.hooked_person = chosen
    st.session_state.fishing = False

    # Thêm vào lịch sử
    st.session_state.history.insert(0, chosen)

    # Loại bỏ nếu cần
    if remove_after_catch:
        st.session_state.participants.remove(chosen)

    st.balloons()  # Hiệu ứng chúc mừng
    st.rerun()  # Cập nhật lại giao diện để hiển thị kết quả


# --- HIỂN THỊ KẾT QUẢ KHI CÂU ĐƯỢC ---
if st.session_state.hooked_person:
    st.success(
        f"🎉 TUYỆT VỜI! Bạn đã câu được: **{st.session_state.hooked_person}**!"
    )
    st.session_state.hooked_person = None  # Xóa để không hiển thị lại khi refresh


# --- CỘT LỊCH SỬ CÂU ---
with col_history:
    st.subheader("📋 Lịch sử câu")
    if st.session_state.history:
        for idx, person in enumerate(st.session_state.history[:15]):
            st.write(f"{idx + 1}. **{person}**")
    else:
        st.write("Chưa ai bị câu lên.")

    if st.button("🗑️ Xóa Lịch Sử"):
        st.session_state.history = []
        st.rerun()


# --- THANH BÊN (SIDEBAR) - CÀI ĐẶT DANH SÁCH ---
with st.sidebar:
    st.header("⚙️ Cài đặt Hồ Cá")
    st.markdown("---")

    input_mode = st.radio(
        "Cách nhập danh sách:", ("Hàng loạt (Nên dùng)", "Từng người một")
    )

    if input_mode == "Hàng loạt (Nên dùng)":
        bulk_input = st.text_area(
            "Nhập danh sách (mỗi tên một dòng):",
            value="\n".join(st.session_state.participants),
            height=300,
        )
        if st.button("🔄 Cập nhật Hồ Cá"):
            names = [
                n.strip() for n in bulk_input.split("\n") if n.strip()
            ]
            if names:
                st.session_state.participants = names
                st.success("Đã cập nhật hồ cá mới!")
                st.rerun()
            else:
                st.error("Danh sách không được trống.")
    else:
        with st.form("add_person_form", clear_on_submit=True):
            new_name = st.text_input("Tên người tham gia mới:")
            submitted = st.form_submit_button("Thêm chú cá")
            if submitted and new_name:
                if new_name not in st.session_state.participants:
                    st.session_state.participants.append(new_name)
                    st.success(f"Đã thêm cá: {new_name}")
                    st.rerun()
                else:
                    st.warning("Tên này đã có trong hồ!")

    st.markdown("---")
    st.warning("⚠️ Nhập danh sách mới sẽ thay thế danh sách hiện tại.")
      
