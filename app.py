import sys
import os
sys.path.append(os.path.dirname(__file__))  # 👈 Thêm dòng này vào
import streamlit as st
import pandas as pd
import re
import os
from streamlit_folium import st_folium
import logger
logger.log_visit()
from functions.background import set_background
from functions.parse import parse_coordinates
from functions.kml import df_to_kml
from functions.footer import show_footer
from functions.converter import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao
from functions.mapgen import generate_map

# Setup
st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="wide")

set_background("assets/background.png")

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.jpg", width=90)
with col2:
    st.title("VN2000 ⇄ WGS84 Converter")
    st.markdown("### BẤT ĐỘNG SẢN HUYỆN HƯỚNG HÓA")

# Tabs
tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    st.markdown("#### 📝 Nhập toạ độ VN2000 (X Y H hoặc mã hiệu E/N)")
    coords_input = st.text_area("Mỗi dòng một điểm", height=180)
    if st.button("🔁 Chuyển sang WGS84"):
        parsed = parse_coordinates(coords_input)
        if parsed:
            df = pd.DataFrame(
                [vn2000_to_wgs84_baibao(x, y, h, 106.25) for x, y, h in parsed],
                columns=["Vĩ độ (Lat)", "Kinh độ (Lon)", "H (m)"]
            )
            st.session_state.df = df
            st.success(f"✅ Đã xử lý {len(df)} điểm.")
        else:
            st.error("⚠️ Không có dữ liệu hợp lệ!")

with tab2:
    st.markdown("#### 📝 Nhập toạ độ WGS84 (Lat Lon H)")
    coords_input = st.text_area("Mỗi dòng một điểm", height=180, key="wgs84input")
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
                [wgs84_to_vn2000_baibao(lat, lon, h, 106.25) for lat, lon, h in coords],
                columns=["X (m)", "Y (m)", "h (m)"]
            )
            st.session_state.df = df
            st.success(f"✅ Đã xử lý {len(df)} điểm.")
        else:
            st.error("⚠️ Không có dữ liệu hợp lệ!")

# Show results
if "df" in st.session_state:
    df = st.session_state.df
    st.markdown("### 📊 Kết quả")
    st.dataframe(df)

    if {"Vĩ độ (Lat)", "Kinh độ (Lon)"}.issubset(df.columns):
        st.markdown("### 🌍 Bản đồ vệ tinh")
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
