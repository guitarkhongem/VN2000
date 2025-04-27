import streamlit as st
import pandas as pd
import re
import os
from streamlit_folium import st_folium

from functions.parser import parse_coordinates
from functions.converter import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao
from functions.mapgen import df_to_kml, generate_map
from functions.background import set_background
from functions.footer import show_footer
from analytics.logger import log_visit

# Xác định đường dẫn tuyệt đối
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Setup
st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="wide")
log_visit()
set_background(os.path.join(CURRENT_DIR, "assets", "background.png"))

# Hàm hỗ trợ chuyển decimal degree thành độ phút
def decimal_to_dms_lon0(decimal_deg):
    degrees = int(decimal_deg)
    minutes = int(round((decimal_deg - degrees) * 60))
    return f"{degrees}°{minutes}'"

# Danh sách kinh tuyến trục kèm tỉnh
lon0_choices = {
    104.5: "Kiên Giang, Cà Mau",
    104.75: "Lào Cai, Phú Thọ, Nghệ An, An Giang",
    105.0: "Vĩnh Phúc, Hà Nam, Ninh Bình, Thanh Hóa, Đồng Tháp, TP. Cần Thơ, Hậu Giang, Bạc Liêu",
    105.5: "Hà Giang, Bắc Ninh, Hải Dương, Hưng Yên, Nam Định, Thái Bình, Hà Tĩnh, Tây Ninh, Vĩnh Long, Trà Vinh",
    105.75: "TP. Hải Phòng, Bình Dương, Long An, Tiền Giang, Bến Tre, TP. Hồ Chí Minh",
    106.0: "Tuyên Quang, Hòa Bình, Quảng Bình",
    106.25: "Quảng Trị, Bình Phước",
    106.5: "Bắc Kạn, Thái Nguyên",
    107.0: "Bắc Giang, Thừa Thiên – Huế",
    107.25: "Lạng Sơn",
    107.5: "Kon Tum",
    107.75: "TP. Đà Nẵng, Quảng Nam, Đồng Nai, Bà Rịa – Vũng Tàu, Lâm Đồng",
    108.0: "Quảng Ngãi",
    108.25: "Bình Định, Khánh Hòa, Ninh Thuận",
    108.5: "Gia Lai, Đắk Lắk, Đắk Nông, Phú Yên, Bình Thuận"
}

# Header
col1, col2 = st.columns([1, 5])
with col1:
    logo_path = os.path.join(CURRENT_DIR, "assets", "logo.jpg")
    if os.path.exists(logo_path):
        st.image(logo_path, width=90)
    else:
        st.warning("⚠️ Không tìm thấy file logo.jpg trong thư mục assets.")
with col2:
    st.title("VN2000 ⇄ WGS84 Converter")
    st.markdown("### BẤT ĐỘNG SẢN HUYỆN HƯỚNG HÓA")

# Tabs
tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    # Combobox chọn kinh tuyến trục
    lon0_display = [f"{decimal_to_dms_lon0(lon)} – {province}" for lon, province in lon0_choices.items()]
    default_index = list(lon0_choices.keys()).index(106.25)

    selected_display = st.selectbox(
        "🧭 Chọn kinh tuyến trục (độ phút chính xác)",
        options=lon0_display,
        index=default_index,
        key="lon0_vn2000"
    )
    selected_lon0 = list(lon0_choices.keys())[lon0_display.index(selected_display)]

    coords_input = st.text_area("📝 Nhập toạ độ VN2000 (X Y H hoặc mã hiệu E/N)", height=180)
    if st.button("🔁 Chuyển sang WGS84"):
        parsed = parse_coordinates(coords_input)
        if parsed:
            df = pd.DataFrame(
                [vn2000_to_wgs84_baibao(x, y, h, selected_lon0) for x, y, h in parsed],
                columns=["Vĩ độ (Lat)", "Kinh độ (Lon)", "H (m)"]
            )
            st.session_state.df = df
            st.success(f"✅ Đã xử lý {len(df)} điểm.")
        else:
            st.error("⚠️ Không có dữ liệu hợp lệ!")

with tab2:
    # Combobox chọn kinh tuyến trục
    lon0_display = [f"{decimal_to_dms_lon0(lon)} – {province}" for lon, province in lon0_choices.items()]
    default_index = list(lon0_choices.keys()).index(106.25)

    selected_display = st.selectbox(
        "🧭 Chọn kinh tuyến trục (độ phút chính xác)",
        options=lon0_display,
        index=default_index,
        key="lon0_wgs84"
    )
    selected_lon0 = list(lon0_choices.keys())[lon0_display.index(selected_display)]

    coords_input = st.text_area("📝 Nhập toạ độ WGS84 (Lat Lon H)", height=180, key="wgs84input")
    if st.button("🔁 Chuyển sang VN2000"):
        tokens = re.split(r'\s+', coords_input.strip())
        coords = []
        i = 0
        while i < len(tokens):
            chunk = []
            for _ in range(3):
                if i < len(tokens):
                    try:
                        chunk.append(float(tokens[i].replace(",", ".")))
                    except:
                        break
                    i += 1
            if len(chunk) == 2:
                chunk.append(0.0)
            if len(chunk) == 3:
                coords.append(chunk)
            else:
                i += 1
        if coords:
            df = pd.DataFrame(
                [wgs84_to_vn2000_baibao(lat, lon, h, selected_lon0) for lat, lon, h in coords],
                columns=["X (m)", "Y (m)", "h (m)"]
            )
            st.session_state.df = df
            st.success(f"✅ Đã xử lý {len(df)} điểm.")
        else:
            st.error("⚠️ Không có dữ liệu hợp lệ!")

# Show output
if "df" in st.session_state:
    df = st.session_state.df
    st.dataframe(df)

    if {"Vĩ độ (Lat)", "Kinh độ (Lon)"}.issubset(df.columns):
        m = generate_map(df)
        st_folium(m, width="100%", height=550)

        kml = df_to_kml(df)
        if kml:
            st.download_button(
                label="📥 Tải xuống file KML",
                data=kml,
                file_name="converted_points.kml",
                mime="application/vnd.google-earth.kml+xml"
            )

show_footer()
