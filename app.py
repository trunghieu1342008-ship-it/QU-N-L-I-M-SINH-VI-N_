import pandas as pd
import streamlit as st

# Cấu hình trang
st.set_page_config(
    page_title="Quản Lý Điểm Sinh Viên", page_icon="🎓", layout="centered"
)

# 1. Tiêu đề ứng dụng
st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'>QUẢN LÝ ĐIỂM SINH VIÊN</h1>",
    unsafe_allow_html=True,
)
st.write("---")

# Dữ liệu mẫu 10 sinh viên
# Trọng số: Chuyên cần (10%), Giữa kỳ (30%), Cuối kỳ (60%)
data = {
    "MSSV": [
        "SV001",
        "SV002",
        "SV003",
        "SV004",
        "SV005",
        "SV006",
        "SV007",
        "SV008",
        "SV009",
        "SV010",
    ],
    "Họ tên": [
        "Nguyễn Văn An",
        "Trần Thị Bích",
        "Lê Hoàng Cường",
        "Phạm Thị Dung",
        "Hoàng Văn Em",
        "Vũ Thị Phương",
        "Đỗ Minh Giang",
        "Bùi Thị Hoa",
        "Ngô Văn Hùng",
        "Dương Thị Kim",
    ],
    "Chuyên cần": [8.0, 9.0, 7.0, 10.0, 6.5, 8.5, 9.0, 5.0, 7.5, 8.0],
    "Giữa kỳ": [7.5, 8.0, 6.0, 9.0, 5.5, 7.0, 8.5, 4.0, 6.5, 7.5],
    "Cuối kỳ": [8.0, 8.5, 6.5, 9.5, 6.0, 7.5, 9.0, 4.5, 7.0, 8.0],
}

df = pd.DataFrame(data)

# Tính điểm tổng kết (Chuyên cần * 0.1 + Giữa kỳ * 0.3 + Cuối kỳ * 0.6)
df["Tổng kết"] = (
    df["Chuyên cần"] * 0.1 + df["Giữa kỳ"] * 0.3 + df["Cuối kỳ"] * 0.6
).round(2)


# Hàm xếp loại
def xep_loai(diem):
  if diem >= 8.5:
    return "Giỏi"
  elif diem >= 7.0:
    return "Khá"
  elif diem >= 5.0:
    return "Trung bình"
  else:
    return "Yếu"


df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# 2. Hiển thị bảng điểm của 10 sinh viên
st.subheader("📋 Bảng điểm chi tiết")
st.dataframe(df, use_container_width=True)

# 3, 4, 5. Các thông tin thống kê
st.subheader("📊 Thống kê lớp học")
diem_tb_lop = df["Tổng kết"].mean()
sv_cao_nhat = df.loc[df["Tổng kết"].idxmax()]
sv_thap_nhat = df.loc[df["Tổng kết"].idxmin()]
so_sv_dat = len(df[df["Tổng kết"] >= 5.0])

col1, col2 = st.columns(2)
with col1:
  st.metric(label="Điểm trung bình lớp", value=f"{diem_tb_lop:.2f}")
  st.metric(label="Số sinh viên đạt (>= 5.0)", value=f"{so_sv_dat}/10")

with col2:
  st.markdown(
      f"🏆 **Cao nhất:** {sv_cao_nhat['Họ tên']} ({sv_cao_nhat['Tổng kết']})"
  )
  st.markdown(
      f"⚠️ **Thấp nhất:** {sv_thap_nhat['Họ tên']} ({sv_thap_nhat['Tổng kết']})"
  )

st.write("---")

# 6 & 7. Danh sách xổ xuống chọn sinh viên và xem thông tin chi tiết
st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_student = st.selectbox(
    "Chọn sinh viên để xem chi tiết:", df["Họ tên"].tolist()
)

# Lấy dữ liệu của sinh viên được chọn
student_info = df[df["Họ tên"] == selected_student].iloc[0]

c1, c2, c3 = st.columns(3)
c1.metric("Điểm Chuyên cần", student_info["Chuyên cần"])
c2.metric("Điểm Giữa kỳ", student_info["Giữa kỳ"])
c3.metric("Điểm Cuối kỳ", student_info["Cuối kỳ"])

c4, c5 = st.columns(2)
c4.metric("Điểm Tổng kết", student_info["Tổng kết"])
c5.metric("Xếp loại", student_info["Xếp loại"])

st.write("---")

# 8. Biểu đồ cột điểm tổng kết của 10 sinh viên
st.subheader("📈 Biểu đồ điểm tổng kết")
chart_data = df.set_index("Họ tên")[["Tổng kết"]]
st.bar_chart(chart_data)

st.write("---")

# 9. Thông tin người tạo ứng dụng (chữ nhỏ ở cuối trang)
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 12px;'>"
    "Người tạo: Nguyễn Trung Hiếu - MSSV: 045208006328<br>"
    "Ứng dụng Quản lý Điểm Sinh Viên - Xây dựng bằng Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
