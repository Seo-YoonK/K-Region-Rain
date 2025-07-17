import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import re

st.set_page_config(layout="wide")
st.title("📌 지역별 강수량 지도 시각화 (Folium)")
st.write("깃허브에 업로드된 CSV를 자동으로 불러와 지도에 파란색 네모와 강수량을 표시합니다.")

# ✅ 깃허브 RAW CSV URL 입력 (사용자 정보에 맞게 수정하세요)
CSV_URL = "https://raw.githubusercontent.com/Seo-YoonK/K-Region-Rain/main/rn_20250717112859.csv"

# ✅ CSV 불러오기
try:
    df = pd.read_csv(CSV_URL, encoding="EUC-KR")
except:
    df = pd.read_csv(CSV_URL, encoding="utf-8-sig")

# ✅ 데이터 전처리
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
