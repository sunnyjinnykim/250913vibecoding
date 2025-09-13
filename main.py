import streamlit as st
from typing import Dict, List
import random
import time
from datetime import date

# ============ 기본 설정 ============ #
st.set_page_config(
    page_title="MBTI 공부법 추천 🍀",
    page_icon="🧠",
    layout="centered"
)

# CSS (살짝 깔끔 + 미세 애니메이션)
st.markdown("""
<style>
/* 부드러운 카드 애니메이션 */
.reco-card {
  border-radius: 18px;
  padding: 18px 18px 6px 18px;
  background: linear-gradient(180deg, #ffffff 0%, #fafcff 100%);
  box-shadow: 0 6px 24px rgba(0,0,0,0.06);
  margin: 8px 0 18px;
  animation: floatIn 480ms ease-out both;
}
@keyframes floatIn { from {opacity:0; transform: translateY(6px)} to {opacity:1; transform: translateY(0)} }

.pill {
  display:inline-block; padding:6px 10px; border-radius:999px; margin:4px 6px 4px 0;
  background:#f2f6ff; border:1px solid #e7eeff; font-size:0.9rem;
}

.badge {
  display:inline-flex; align-items:center; gap:6px;
  background:#fff6e8; border:1px solid #ffe4bd;
  padding:6px 10px; border-radius:10px; font-weight:600; margin-right:8px;
}

.footer-note { color:#7b8899; font-size:0.86rem; margin-top:8px }
.small { font-size:0.9rem; color:#5b697a }

h1, h2, h3 { letter-spacing: -0.2px }
</style>
""", unsafe_allow_html=True)

# ============ 데이터 ============ #
MBTI_GROUP = {
    "NF(직관-감정) 🌈": ["INFP", "ENFP", "INFJ", "ENFJ"],
    "NT(직관-사고) 🧪": ["INTP", "ENTP", "INTJ", "ENTJ"],
    "SJ(감각-판단) 🗂️": ["ISTJ", "ESTJ", "ISFJ", "ESFJ"],
    "SP(감각-인식) 🎮": ["ISTP", "ESTP", "ISFP", "ESFP"],
}

# 각 유형별 핵심 추천 (간결·실전 위주)
RECO: Dict[str, Dict[str, List[str]]] = {
    "INFP": {
        "title": "스토리로 연결하고 가치에 몰입하기 ✨",
        "core": [
            "공부 주제를 ‘나의 가치/관심’에 연결해 학습 몰입 💡",
            "짧은 몰입(25분) + 감정 리셋(5분) ‘포모도로’ 권장 ⏱️",
            "요약은 ‘비유/메타포’로: 추상→이미지로 변환 🎨",
        ],
        "routine": [
            "1) 25분 몰입 → 5분 쉬기 × 3 세트",
            "2) 감정기록 1줄(오늘 배움이 나에게 준 의미)",
            "3) 슬로우 리뷰(핵심 키워드 5개만) 📝",
        ],
        "tools": ["Notion 템플릿 🧱", "루틴 타이머(포모도로) ⏲️", "마인드맵 ✏️"],
        "dont": ["완벽주의로 시작 미루기 🚫", "감정 과몰입으로 공부 회피 🙅‍♀️"],
        "quote": "완벽보다 ‘진행’이 더 큰 선물. 오늘 1cm라도 전진하기.",
    },
    "ENFP": {
        "title": "다채로움은 유지, 산만함은 줄이기 🌈",
        "core": [
            "과목별 ‘퀘스트 보드’로 미션 게임화 🎮",
            "동기 높일 보상 미니챌린지(스티커/이모지) 🏅",
            "협업·스터디로 에너지 업(설명하며 배우기) 🔁",
        ],
        "routine": [
            "1) 오늘 미션 3개만 선택",
            "2) 30분 집중 → 10분 리프레시(산책/스트레칭) 🚶",
            "3) 배운 내용 60초 스피치로 요약 🎤",
        ],
        "tools": ["칸반 보드 🗂️", "퀴즈 앱 ❓", "공부 브이로그✍️(셀프 피드백)"],
        "dont": ["계획 과다/변경 과다 📉", "잡다한 도구 수집만 하다 시간 소모 ⌛"],
        "quote": "흥미는 점화제, 루틴은 추진력. 둘을 함께 켜두기.",
    },
    "INFJ": {
        "title": "조용한 심층 몰입 + 구조적 정리 🧘",
        "core": [
            "개념-맥락-의미 층위로 노트 설계(3단 노트) 📚",
            "예측질문을 먼저 만들고 텍스트를 읽기 🔍",
            "주 1회 ‘관계도 업데이트’(개념 연결선 그리기) 🕸️",
        ],
        "routine": [
            "1) 45분 딥워크 → 10분 정리",
            "2) 예상문제 3개 생성 → 답안 골격만 쓰기",
            "3) 잠들기 전 5분 개념관계 리콜 💤",
        ],
        "tools": ["Obsidian/Notion 링크드 노트 🔗", "Anki SRS 🧠", "독서 타이머 ⏲️"],
        "dont": ["과정 지나친 내적검열 ❌", "과도한 장기계획만 세우고 실행 지연 🐢"],
        "quote": "깊이는 디테일에서 나오고, 디테일은 루틴에서 온다.",
    },
    "ENFJ": {
        "title": "사람과 함께 설계하고 이끌며 배우기 🤝",
        "core": [
            "스몰 그룹에 역할 부여(발표/질문/정리) 👥",
            "티칭백(teach-back)으로 개념 고정 🎯",
            "주간 ‘피드백 데이’ 지정하여 루틴 점검 🔁",
        ],
        "routine": [
            "1) 핵심 개념 3개 선택",
            "2) 30분 정리 → 10분 가르치기 스크립트 작성",
            "3) 모의 발표 or 녹음 🎙️",
        ],
        "tools": ["공유 칸반/미러 보드 🪞", "발표 타이머 ⏲️", "피드백 폼 📄"],
        "dont": ["타인 일정에 과몰입해 자기 루틴 붕괴 🫠"],
        "quote": "리더십은 먼저 배우고, 나눌 때 더 단단해진다.",
    },
    "INTP": {
        "title": "문제기반 탐구 + 실험적 메모 🧪",
        "core": [
            "‘왜?’로 시작하는 질문 리스

