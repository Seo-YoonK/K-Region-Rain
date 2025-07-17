import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import re

# 페이지 설정
st.set_page_config(layout="wide")
st.title("📌 지역별 강수량 지도 시각화 (Folium)")
st.write("깃허브에 업로드된 CSV를 자동으로 불러와 지도에 **파란빛 하늘색 정사각형**과 강수량을 표시합니다.")

# ✅ 깃허브 RAW CSV URL
CSV_URL = "https://raw.githubusercontent.com/Seo-YoonK/K-Region-Rain/main/rn_20250717112859.csv"

# ✅ CSV 불러오기 (EUC-KR → 실패 시 utf-8-sig)
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
m = folium.Map(location=[center_lat, center_lon], zoom_start=7, control_scale=True)

# ✅ 각 지역에 정사각형 + 강수량 표시
for _, row in df.iterrows():
    lat, lon = row['위도'], row['경도']
    rain = row['강수량']
    region = row['지역']

    delta = 0.05  # 정사각형 한 변의 절반 크기
    bounds = [
        [lat - delta, lon - delta],
        [lat + delta, lon + delta]
    ]

    # 파란빛 하늘색 정사각형
    folium.Rectangle(
        bounds=bounds,
        color="#5DADE2",        # 조금 더 파란색이 섞인 하늘색
        fill=True,
        fill_color="#5DADE2",
        fill_opacity=0.4,
        tooltip=f"{region} : {rain}mm"
    ).add_to(m)

    # 네모 중앙 강수량 표시 (흰색 글자 + 검정 테두리)
    folium.Marker(
        location=[lat, lon],
        icon=folium.DivIcon(
            html=f"""
            <div style="
                font-size:12px;
                font-weight:bold;
                color:white;
                text-shadow:
                    -1px -1px 0 black,
                    1px -1px 0 black,
                    -1px 1px 0 black,
                    1px 1px 0 black;
                background-color:rgba(0,0,0,0.2);
                border:1px solid #5DADE2;
                border-radius:3px;
                padding:2px;
                text-align:center;">
                {rain}mm
            </div>
            """
        )
    ).add_to(m)

st.subheader("🗺️ 지역별 강수량 지도")
folium_static(m, width=1000, height=600)
