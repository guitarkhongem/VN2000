import streamlit as st
import datetime

def show_footer():
    year = datetime.datetime.now().year
    st.markdown("---")
    st.markdown(
        f"📌 Tác giả: **Trần Trường Sinh**  \n"
        "📞 0917.750.555"
    )
    st.markdown(
        "🔍 **Nguồn công thức**: Bài báo khoa học: **CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG UAV**  \n"
        "_Hội nghị KH Quốc gia về Công nghệ Địa không gian_"
    )
    st.markdown(
        f"© {year} Trần Trường Sinh."
    )
