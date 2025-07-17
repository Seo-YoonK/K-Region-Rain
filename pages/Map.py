import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import re

st.set_page_config(layout="wide")
st.title("📌 지역별 강수량 지도 시각화 (Folium)")
st.write("CSV 파일을 업로드하면 지도에 파란색 네모와 강수량이 표시됩니다.")

# ✅ CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type=["csv"])

if uploaded_file is not None:
    # ✅ CSV 읽기 (EUC-KR → 실패 시 utf-8-sig로 재시도)
    try:
        df = pd.read_csv(uploaded_file, encoding="EUC-KR")
    except:
        df = pd.read_csv(uploaded_file, encoding="utf-8-sig")

    # ✅ 전처리
    df['지점정보'] = df['지점정보'].apply(lambda x: re.sub(r"\(.*?\)", "", str(x)).strip())
    df = df.rename(columns={"지점정보": "지역", "강수량(mm)": "강수량"})

    st.subheader("전처리된 데이터")
    st.dataframe(df)

    # ✅ 지도 생성
    center_lat = df['위도'].mean()
    center_lon = df['경도'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

    for _, row in df.iterrows():
        lat, lon = row['위도'], row['경도']
        rain = row['강수량']
        region = row['지역']

        delta = 0.05
        bounds = [
            [lat - delta, lon - delta],
            [lat + delta, lon + delta]
        ]

        folium.Rectangle(
            bounds=bounds,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.3,
            tooltip=f"{region} : {rain}mm"
        ).add_to(m)

        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size:11px;
                    color:blue;
                    background-color:rgba(255,255,255,0.7);
                    border:1px solid blue;
                    border-radius:3px;
                    padding:1px;
                    text-align:center;">
                    {rain}mm
                </div>
                """
            )
        ).add_to(m)

    st.subheader("지역별 강수량 지도")
    folium_static(m, width=1000, height=600)
else:
    st.info("⬆️ 먼저 CSV 파일을 업로드해주세요.")
