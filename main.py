import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목
st.title("🌍 MBTI 유형별 국가 Top 10 분석")

# CSV 데이터 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 데이터 변환 (wide → long)
    df_melted = df.melt(id_vars=["Country"], var_name="MBTI", value_name="Proportion")

    # MBTI 선택
    mbti_list = df_melted["MBTI"].unique()
    selected_mbti = st.selectbox("MBTI 유형을 선택하세요", mbti_list)

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
    ax.set_xlabel("Proportion")
    ax.set_ylabel("Country")
    ax.invert_yaxis()

    st.pyplot(fig)
