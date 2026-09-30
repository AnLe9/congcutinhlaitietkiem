import streamlit as st
st.image("IMG_0423.jpeg")

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Ứng dụng tính lãi gửi tiết kiệm")
st.write("Tính tiền lãi theo **lãi đơn** và **lãi kép**.")

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================
# NHẬP DỮ LIỆU
# =========================

st.subheader("📌 Thông tin gửi tiết kiệm")

# Số tiền gửi
tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

# Kỳ hạn
ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

# Hình thức gửi
hinh_thuc_gui = st.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

# Hình thức nhận lãi
hinh_thuc_nhan_lai = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# Lãi suất
lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=5.0,
    step=0.1
)

# =========================
# TÍNH TOÁN
# =========================

if st.button("🧮 Tính lãi", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
    elif lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
    else:

        # Lãi suất dạng thập phân
        r = lai_suat / 100

        # Thời gian gửi tính theo năm
        so_nam = ky_han / 12

        # -------------------------
        # LÃI ĐƠN
        # -------------------------
        if hinh_thuc_gui == "Lãi đơn":

            tong_tien_lai = tien_gui * r * so_nam
            tong_tien = tien_gui + tong_tien_lai

        # -------------------------
        # LÃI KÉP
        # -------------------------
        else:

            # Số lần nhập lãi:
            # Theo tháng = 12 lần/năm
            # Theo quý = 4 lần/năm
            # Cuối kỳ = 1 lần/kỳ hạn
            if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
                so_lan_nhap_lai_moi_nam = 12

            elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
                so_lan_nhap_lai_moi_nam = 4

            else:
                so_lan_nhap_lai_moi_nam = 1

            # Trường hợp cuối kỳ:
            # Lãi được tính một lần sau toàn bộ kỳ hạn
            if hinh_thuc_nhan_lai == "Lãnh lãi cuối kỳ":
                tong_tien = tien_gui * (1 + r) ** so_nam

            else:
                tong_tien = tien_gui * (
                    1 + r / so_lan_nhap_lai_moi_nam
                ) ** (
                    so_lan_nhap_lai_moi_nam * so_nam
                )

            tong_tien_lai = tong_tien - tien_gui

        # =========================
        # TÍNH LÃI ĐỊNH KỲ
        # =========================

        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

            # Lãi định kỳ theo tháng
            lai_dinh_ky = tien_gui * r / 12

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

            # Lãi định kỳ theo quý
            lai_dinh_ky = tien_gui * r / 4

        else:

            # Lãnh cuối kỳ
            lai_dinh_ky = tong_tien_lai

        # =========================
        # HIỂN THỊ KẾT QUẢ
        # =========================

        st.success("✅ Tính toán thành công!")

        st.subheader("📊 Kết quả")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Tiền lãi định kỳ",
                dinh_dang_tien(lai_dinh_ky)
            )

        with col2:
            st.metric(
                "Tổng tiền lãi",
                dinh_dang_tien(tong_tien_lai)
            )

        with col3:
            st.metric(
                "Tổng gốc + lãi",
                dinh_dang_tien(tong_tien)
            )

        # =========================
        # THÔNG TIN CHI TIẾT
        # =========================

        st.divider()

        st.write("### 📋 Thông tin khoản gửi")

        st.write(f"**Số tiền gửi:** {dinh_dang_tien(tien_gui)}")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Hình thức tính:** {hinh_thuc_gui}")
        st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")
