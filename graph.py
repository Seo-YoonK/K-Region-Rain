import streamlit as st
import pandas as pd
import re

# ------------------------
# ✅ CSV 직접 불러오기
# ------------------------
file_path = "rn_20250717112859.csv"  # 같은 폴더에 위치해야 함
df = pd.read_csv(file_path, encoding="EUC-KR")

# ------------------------
# ✅ 데이터 전처리
# ------------------------
# 지역명에서 괄호와 숫자 제거 (예: "속초(90)" → "속초")
df['지점정보'] = df['지점정보'].apply(lambda x: re.sub(r"\(.*?\)", "", str(x)).strip())

# 컬럼명 변경 (Streamlit에서 보기 쉽게)
df = df.rename(columns={"지점정보": "지역", "강수량(mm)": "강수량"})

# ------------------------
# ✅ Streamlit UI
# ------------------------
st.title("📊 지역별 강수량 시각화")
st.write("이 앱은 CSV 데이터를 이용해 지역별 강수량을 시각화합니다.")

# ✅ 전처리된 데이터 표시
st.subheader("전처리된 데이터")
st.dataframe(df)

# ✅ 강수량 선 그래프
st.subheader("지역별 강수량 선 그래프")
df_graph = df.set_index('지역')[['강수량']]
st.line_chart(df_graph)
