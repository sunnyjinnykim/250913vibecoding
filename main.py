import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("🌍 MBTI 유형별 국가 Top 10 분석")

# 기본 파일 경로 (앱과 같은 폴더에 있다고 가정)
default_file = "countriesMBTI_16types.csv"

df = None

# 1️⃣ 같은 폴더에 데이터가 있으면 자동 로드
if os.path.exists(default_file):
    st.info(f"📂 기본 데이터 파일을 사용합니다: {default_file}")
    df = pd.read_csv(default_file)

# 2️⃣ 없으면 업로드 기능 제공
else:
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
    if uploaded_file is not None:
        st.success("✅ 업로드된 파일을 사용합니다")
        df = pd.read_csv(uploaded_file)

if df is not None:
    # 데이터 변환 (wide → long)
    df_melted = df.melt(id_vars=["Country"], var_name="MBTI", value_name="Proportion")

    # MBTI 선택
    mbti_list = df_melted["MBTI"].unique()
    selected_mbti = st.selectbox("MBTI 유형을 선택하세요", sorted(mbti_list))

    # 선택한 MBTI의 상위 10개 국가
    subset = (
        df_melted[df_melted["MBTI"] == selected_mbti]
        .sort_values("Proportion", ascending=False)
        .head(10)
    )

    # 시각화
    fig, ax = plt.subplots(figsize=(10,6))
    ax.barh(subset["Country"], subset["Proportion"], color="skyblue")
    ax.set_title(f"Top 10 Countries with Highest {selected_mbti} Proportion")
    ax.set_xlabel("Proportion")_
