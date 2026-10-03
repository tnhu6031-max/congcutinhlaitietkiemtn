
import streamlit as st
st.image("logo.jpg")
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰APP TÍNH LÃI GỬI TIẾT KIỆM_BY TÂM NHƯ")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi.")

st.divider()

# =========================
# NHẬP THÔNG TIN
# =========================
so_tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0,
    value=100_000_000,
    step=1_000_000,
    format="%d"
)

ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

st.divider()

# =========================
# NÚT TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    # Lãi suất năm chuyển sang số thập phân
    lai_suat_nam = lai_suat / 100

    # =========================
    # TRƯỜNG HỢP NHẬN LÃI CUỐI KỲ
    # =========================
    if hinh_thuc == "Cuối kỳ":

        tong_lai = so_tien_gui * lai_suat_nam * ky_han / 12
        lai_dinh_ky = tong_lai

        tong_tien = so_tien_gui + tong_lai

        bang_chi_tiet = pd.DataFrame({
            "Kỳ nhận lãi": [f"Sau {ky_han} tháng"],
            "Tiền lãi": [lai_dinh_ky]
        })

    # =========================
    # TRƯỜNG HỢP NHẬN LÃI HÀNG THÁNG
    # =========================
    elif hinh_thuc == "Hàng tháng":

        lai_moi_thang = so_tien_gui * lai_suat_nam / 12

        tong_lai = lai_moi_thang * ky_han
        lai_dinh_ky = lai_moi_thang

        tong_tien = so_tien_gui + tong_lai

        bang_chi_tiet = pd.DataFrame({
            "Tháng": range(1, ky_han + 1),
            "Tiền lãi nhận được": [lai_moi_thang] * ky_han
        })

    # =========================
    # TRƯỜNG HỢP NHẬN LÃI HÀNG QUÝ
    # =========================
    else:

        lai_moi_quy = so_tien_gui * lai_suat_nam / 4

        so_quy = ky_han // 3
        thang_le = ky_han % 3

        tong_lai = lai_moi_quy * so_quy

        # Nếu kỳ hạn không chia hết cho 3 tháng,
        # tính thêm phần lãi của số tháng còn lại
        if thang_le > 0:
            lai_thang_le = so_tien_gui * lai_suat_nam * thang_le / 12
            tong_lai += lai_thang_le

        lai_dinh_ky = lai_moi_quy

        tong_tien = so_tien_gui + tong_lai

        ky_nhan_lai = []
        tien_lai = []

        for i in range(1, so_quy + 1):
            ky_nhan_lai.append(f"Quý {i}")
            tien_lai.append(lai_moi_quy)

        if thang_le > 0:
            ky_nhan_lai.append(f"{thang_le} tháng cuối")
            tien_lai.append(lai_thang_le)

        bang_chi_tiet = pd.DataFrame({
            "Kỳ nhận lãi": ky_nhan_lai,
            "Tiền lãi nhận được": tien_lai
        })

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Tính toán hoàn tất!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            f"{lai_dinh_ky:,.0f} VNĐ"
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            f"{tong_lai:,.0f} VNĐ"
        )

    with col3:
        st.metric(
            "💰 Tổng gốc + lãi",
            f"{tong_tien:,.0f} VNĐ"
        )

    st.divider()

    # =========================
    # THÔNG TIN KHOẢN GỬI
    # =========================
    st.subheader("📋 Thông tin khoản gửi")

    thong_tin = pd.DataFrame({
        "Thông tin": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Hình thức nhận lãi"
        ],
        "Giá trị": [
            f"{so_tien_gui:,.0f} VNĐ",
            f"{ky_han} tháng",
            f"{lai_suat:.2f}%/năm",
            hinh_thuc
        ]
    })

    st.table(thong_tin)

    # =========================
    # BẢNG CHI TIẾT LÃI
    # =========================
    st.subheader("📊 Chi tiết tiền lãi")

    # Format tiền VNĐ để hiển thị đẹp
    bang_hien_thi = bang_chi_tiet.copy()

    for cot in bang_hien_thi.columns:
        if "Tiền lãi" in cot:
            bang_hien_thi[cot] = bang_hien_thi[cot].apply(
                lambda x: f"{x:,.0f} VNĐ"
            )

    st.dataframe(
        bang_hien_thi,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # KẾT LUẬN
    # =========================
    st.info(
        f"💡 Với số tiền gửi {so_tien_gui:,.0f} VNĐ, "
        f"kỳ hạn {ky_han} tháng và lãi suất {lai_suat:.2f}%/năm, "
        f"bạn nhận được tổng cộng {tong_lai:,.0f} VNĐ tiền lãi."
    )

# =========================
# GHI CHÚ
# =========================
st.caption(
    "Lưu ý: Công cụ sử dụng phương pháp tính lãi đơn trên số tiền gốc, "
    "chưa tính trường hợp lãi được nhập gốc để tái tục."
)
