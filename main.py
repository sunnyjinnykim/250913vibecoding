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
            "‘왜?’로 시작하는 질문 리스트업 📝",
            "예제 변형/경계 케이스 실험 🧩",
            "노트는 공식보다 ‘아이디어 로그’ 중심 🔍",
        ],
        "routine": [
            "1) 질문 5개 작성",
            "2) 40분 실험/코딩/문제 변형",
            "3) 10분 결론/한계/다음 실험 메모",
        ],
        "tools": ["Jupyter/Colab 📓", "LaTeX/수식 노트 ➕", "Anki SRS 🧠"],
        "dont": ["토픽 점프/딴 길 탐험으로 본선수업 이탈 🌀"],
        "quote": "탐구는 자유롭게, 출력은 간결하게.",
    },
    "ENTP": {
        "title": "논쟁·아이디어 폭발을 구조화하기 ⚡",
        "core": [
            "논쟁형 노트(찬반/가정/반례) 🥊",
            "속도 있는 브레인라이팅 → 수렴 단계 명확화 ✍️",
            "프로젝트·경진대회로 ‘마감’을 만들어 추진 ⏳",
        ],
        "routine": [
            "1) 20분 아이디어 폭발",
            "2) 20분 수렴/선정",
            "3) 20분 결과물 초안 만들기",
        ],
        "tools": ["화이트보드/포스트잇 🧻", "타이머 ⏱️", "프레젠테이션 툴 📽️"],
        "dont": ["완결 없는 확장만 반복 🔁"],
        "quote": "아이디어는 많다. 승패는 끝까지 만든 사람에게.",
    },
    "INTJ": {
        "title": "거꾸로 설계(시험→전략) + 시스템화 ♟️",
        "core": [
            "목표 점수 역산 → 역량 모듈별 학습 RTM 📐",
            "지식 그래프/시스템 체크리스트 🔗",
            "피드백 루프 자동화(모의고사→오답 DB) ♻️",
        ],
        "routine": [
            "1) 데일리 KPI 3개",
            "2) 50분 집중 → 10분 리뷰",
            "3) 주간 리포트(지표/보틀넥) 작성",
        ],
        "tools": ["스프레드시트 KPI 📊", "Anki/오답노트 DB", "타스크 자동화 🔁"],
        "dont": ["완벽주의 최적화→실행 지연 🧊"],
        "quote": "전략이 실행을 이기지 못한다면, 전략을 더 단순하게.",
    },
    "ENTJ": {
        "title": "목표-자원-일정 정렬, 고강도 실행 🚀",
        "core": [
            "OKR/SMART 목표로 자원 배치 🎯",
            "블록 스케줄링(딥워크 블록) 📆",
            "성과 리뷰 후 과감한 피봇/위임 🔧",
        ],
        "routine": [
            "1) 오늘의 임팩트 태스크 3개",
            "2) 60분 딥워크 × 2",
            "3) EOD 리뷰(주요 성과/리스크)",
        ],
        "tools": ["OKR 보드 📌", "캘린더 블록 ⏰", "성과 대시보드 📈"],
        "dont": ["과적/번아웃, 관계 케어 소홀 🧯"],
        "quote": "속도와 지속가능성의 균형이 장기 승리를 만든다.",
    },
    "ISTJ": {
        "title": "체크리스트-기반 정밀 학습 📏",
        "core": [
            "교과서-기출 체크박스화 ✅",
            "규칙적 루틴(시간·장소 고정) 🕰️",
            "정리노트는 ‘사전’처럼 색인 📇",
        ],
        "routine": [
            "1) 45분 집중 → 10분 정리",
            "2) 체크리스트 10칸 채우기",
            "3) 하루 마지막 5분 파일링",
        ],
        "tools": ["체크리스트 앱 ☑️", "색인 포스트잇 🏷️", "기출 분석표 📄"],
        "dont": ["예외 상황 오면 계획 경직 ❄️"],
        "quote": "꾸준함은 언제나 ‘특수 능력’이다.",
    },
    "ESTJ": {
        "title": "표준 절차로 안정적 성과 내기 🏗️",
        "core": [
            "표준 학습 프로세스(SOP) 문서화 📘",
            "타임박싱·산출물 명확화 📦",
            "주간 성과 회고(숫자로 말하기) 🔢",
        ],
        "routine": [
            "1) 오늘 SOP 2회전",
            "2) 진척률 70% 넘기기",
            "3) 주간 그래프 업데이트",
        ],
        "tools": ["SOP 문서 📄", "간트/버전관리 📊", "체크리스트 ☑️"],
        "dont": ["절차가 목적이 되지 않게 주의 ⚠️"],
        "quote": "규율은 자유를 위해 존재한다.",
    },
    "ISFJ": {
        "title": "조용한 규칙성 + 따뜻한 보상 🌿",
        "core": [
            "작은 목표를 매일 달성 → 신뢰감 축적 🧩",
            "오답은 ‘원인-처방’ 카드화 💊",
            "환경 정돈(책상/디지털 폴더) 🧺",
        ],
        "routine": [
            "1) 30분 집중 × 2",
            "2) 오답 카드 3장 업데이트",
            "3) 스몰 보상(티/산책) ☕",
        ],
        "tools": ["플래시카드 📇", "미니 캘린더 ✅", "정리 체크리스트 🗂️"],
        "dont": ["타인 요청에 학습시간 침식 🙇‍♀️"],
        "quote": "작고 확실한 성취가 큰 자신감을 만든다.",
    },
    "ESFJ": {
        "title": "함께해서 더 잘되는 루틴 🤗",
        "core": [
            "짝스터디/소그룹 리듬 만들기 👭",
            "서로의 강점 분담(가르침/정리/퀴즈) 🧩",
            "감정 리듬 체크인(짧은 공유) 💬",
        ],
        "routine": [
            "1) 30분 공동 학습",
            "2) 10분 퀴즈/피드백",
            "3) 오늘의 칭찬 1개씩 🌟",
        ],
        "tools": ["공유 노트 📝", "퀴즈 폼 ❓", "그룹 캘린더 📅"],
        "dont": ["관계 조율에 과에너지 사용 🔋"],
        "quote": "서로의 성장에 불을 붙이는 사람이 되기.",
    },
    "ISTP": {
        "title": "손으로 풀며 배우기(메이킹/실습) 🔧",
        "core": [
            "예제보다 ‘제작/실험’ 먼저 🎯",
            "짧고 빈번한 피드백 사이클 ♻️",
            "장비/도구 세팅 체크리스트 🧰",
        ],
        "routine": [
            "1) 20분 설계",
            "2) 30분 제작/코딩",
            "3) 10분 문제 해결 로그",
        ],
        "tools": ["실습 키트 🧪", "버전관리(Git) 🔀", "체크리스트 ☑️"],
        "dont": ["설명서 안 읽고 바로 돌입 → 시간 손실 ⛔"],
        "quote": "직접 만져보면 이해 속도가 달라진다.",
    },
    "ESTP": {
        "title": "스피드-피드백-승부감으로 밀어붙이기 🏁",
        "core": [
            "짧은 모의전 → 즉시 피드백 🔥",
            "경쟁/기록 갱신 요소 도입 🏅",
            "현실 문제에 적용해 결과보기 💼",
        ],
        "routine": [
            "1) 20분 요약",
            "2) 20분 문제/퀴즈",
            "3) 20분 실전 시뮬",
        ],
        "tools": ["타이머 ⏱️", "랭킹보드/스코어카드 🧾", "퀴즈앱 ❓"],
        "dont": ["단기 성과만 추구해 기초 빈약 📉"],
        "quote": "속도는 좋다. 기초를 잃지 않을 때 더 좋다.",
    },
    "ISFP": {
        "title": "감각적 몰입 + 잔잔한 꾸준함 🎧",
        "core": [
            "미니 환경 연출(좋아하는 음악/향) 🎵",
            "예쁜 요약/그림노트로 재미 유지 🖍️",
            "체크인: 오늘의 기분 색상 고르기 🎨",
        ],
        "routine": [
            "1) 25분 집중 × 3",
            "2) 체크리스트 5칸",
            "3) 셀프 칭찬 1개 💚",
        ],
        "tools": ["타스커/체크리스트 ☑️", "그림노트/태블릿 ✏️", "화이트 노이즈 🔊"],
        "dont": ["감정 기복으로 루틴 끊김 ⚠️"],
        "quote": "조용하지만 꾸준한 빛이 먼 길을 비춘다.",
    },
    "ESFP": {
        "title": "즐거움-성과 동시추구 🎉",
        "core": [
            "학습을 ‘챌린지’로 만들고 기록 공유 📸",
            "퀴즈/게임 요소로 집중 끌어올리기 🎲",
            "현장감 있는 사례/영상 학습 🎬",
        ],
        "routine": [
            "1) 20분 요약",
            "2) 20분 퀴즈/게임",
            "3) 20분 발표/리뷰",
        ],
        "tools": ["챌린지 스티커 📌", "퀴즈앱 ❓", "간단 리포트 양식 🧾"],
        "dont": ["계획 없이 즉흥으로만 진행 💨"],
        "quote": "재미는 연료, 루틴은 엔진.",
    },
}

# 16유형 누락 없도록 나머지 자동 채우기(동일 그룹 패턴 활용)
BASE_CLONE = {
    "core": ["핵심 개념을 작게 쪼개 꾸준히 반복 🔁",
             "오답·약점은 원인-처방으로 기록 💊",
             "짧은 집중 블록과 리프레시 교차 ⏱️"],
    "routine": ["1) 30~45분 집중", "2) 5~10분 정리", "3) 데일리 체크 ✅"],
    "tools": ["타이머 ⏱️", "노트/마인드맵 📝", "SRS/플래시카드 🧠"],
    "dont": ["한 번의 완벽을 노리다 시작 못함 ⛔"],
    "quote": "꾸준함이 모든 유형을 이긴다.",
    "title": "맞춤 루틴으로 꾸준히 전진하기 🧭"
}

ALL_TYPES = sum(MBTI_GROUP.values(), [])  # 16개
for t in ALL_TYPES:
    if t not in RECO:
        RECO[t] = {k: (v if k == "title" else list(v)) for k, v in BASE_CLONE.items()}

# ============ 사이드바 ============ #
with st.sidebar:
    st.header("🔎 MBTI 선택")
    group = st.selectbox("기질 그룹", list(MBTI_GROUP.keys()))
    mbti = st.selectbox("MBTI 유형", MBTI_GROUP[group])
    intensity = st.slider("오늘의 강도(난이도) 💪", 1, 5, 3)
    spark = st.radio("효과", ["🎈 축하 풍선", "❄️ 눈 내리기", "✨ 조용히"])
    st.markdown("---")
    st.caption("Tip: 유형은 참고용! 나에게 맞는 루틴을 조금씩 커스터마이즈하면 가장 좋아요 😊")

# ============ 본문 ============ #
st.title("MBTI 맞춤 공부법 추천 🧠✨")
st.subheader("한 번의 클릭으로 오늘의 공부 레시피 완성! 🍱")

# 재미있는 준비 애니메이션
with st.status("개인화 레시피 조리 중... 🍳", expanded=False) as status:
    for i in range(0, 101, random.choice([17, 23, 29])):
        st.progress(min(i, 100))
        time.sleep(0.12)
    status.update(label="완료! 맛있게 드세요 😋", state="complete")

if spark == "🎈 축하 풍선":
    st.balloons()
elif spark == "❄️ 눈 내리기":
    try:
        st.snow()
    except Exception:
        pass

data = RECO[mbti]
st.markdown(f"### {mbti} — {data.get('title','맞춤 루틴')}")
st.markdown(
    f"<div class='badge'>📅 {date.today().strftime('%Y.%m.%d')}</div>"
    f"<div class='badge'>🎯 강도 Lv.{intensity}</div>"
    f"<div class='badge'>🧩 그룹: {group}</div>",
    unsafe_allow_html=True
)

# 추천 카드
def bullet(items: List[str]) -> str:
    return "".join([f"- {x}\n" for x in items])

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("#### 🔥 핵심 전략")
    st.markdown(f"<div class='reco-card'>{bullet(data['core'])}</div>", unsafe_allow_html=True)
    st.markdown("#### 🧭 루틴 템플릿")
    st.markdown(f"<div class='reco-card'>{bullet(data['routine'])}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("#### 🛠️ 추천 도구")
    st.markdown(f"<div class='reco-card'>{' '.join([f'<span class=\"pill\">{x}</span>' for x in data['tools']])}</div>", unsafe_allow_html=True)
    st.markdown("#### ⚠️ 피해야 할 함정")
    st.markdown(f"<div class='reco-card'>{bullet(data['dont'])}</div>", unsafe_allow_html=True)

st.success(f"💬 오늘의 한 줄: *{data['quote']}*")

# ============ 1시간 개인화 플랜 생성기 ============ #
st.markdown("---")
st.header("⏰ 오늘의 1시간 플랜 만들기")

# 강도에 따라 시간 배분 가중치
weights = {
    1: (15, 10, 20, 15),  # 워밍업, 집중, 문제/응용, 리뷰(분)
    2: (10, 20, 20, 10),
    3: (8, 25, 20, 7),
    4: (5, 30, 20, 5),
    5: (3, 35, 18, 4),
}[intensity]

# 유형 기질에 따라 미니 임무 추천
mini_tasks = {
    "NF": ["의미 연결 한 줄 쓰기 ✍️", "핵심 개념 3개를 비유로 설명하기 🎨", "60초 스피치 녹음 🎤"],
    "NT": ["반례 찾기 🔎", "가정 바꿔보기 🧪", "공식 유도 과정 요약 📐"],
    "SJ": ["체크리스트 10칸 채우기 ✅", "오답 원인-처방 기록 💊", "색인/폴더 정돈 🗂️"],
    "SP": ["실습 성공 영상 찍기 🎥", "기록 갱신 도전 🏅", "현실 사례에 적용해보기 🔧"],
}
key = group.split("(")[0]  # NF/NT/SJ/SP 키 추출
tasks = mini_tasks["NF" if "NF" in group else "NT" if "NT" in group else "SJ" if "SJ" in group else "SP"]

segments = [
    ("워밍업", weights[0], random.choice([
        "오늘 목표 2가지 적기 📝", "지난 오답 3개 훑기 📄", "책상/파일 3분 정리 🧺"
    ])),
    ("집중학습", weights[1], random.choice([
        "핵심 개념 요약 정리", "예제 5문제 풀기", "강의 1개 시청/필기"
    ])),
    ("문제·응용", weights[2], random.choice(tasks)),
    ("리뷰·정리", weights[3], random.choice([
        "오늘 배운 3줄 요약 ✍️", "내일 과제 1개 예약 📌", "핵심 키워드 5개 리콜 🧠"
    ])),
]

st.markdown("### 📒 추천 타임테이블 (60분)")
for name, mins, action in segments:
    st.info(f"**{name}** — {mins}분 | {action}")

# 텍스트 묶어서 다운로드
plan_text = "\n".join([f"{name} — {mins}분 | {action}" for name, mins, action in segments])
st.download_button(
    label="📝 플랜 텍스트 다운로드",
    data=(f"[{mbti}] 오늘의 1시간 플랜\n\n" + plan_text).encode("utf-8"),
    file_name=f"{mbti}_study_plan.txt",
    mime="text/plain"
)

# ============ 가벼운 체크리스트 ============ #
st.markdown("---")
st.header("✅ 오늘의 체크리스트")
checks = [
    "공부 공간 깔끔하게 정리했나요? 🧽",
    "포모도로/타이머 준비 완료? ⏲️",
    "핵심 목표 2가지 메모했나요? 🎯",
    "오답/약점 1개는 반드시 처리! 💊",
]
for c in checks:
    st.checkbox(c)

st.caption("✨ 팁: 유형은 시작점일 뿐, ‘나만의 변형’이 최고의 최적화예요.")
st.markdown("<div class='footer-note'>© 2025 MBTI Study Chef — made with ❤️ & Streamlit</div>", unsafe_allow_html=True)
