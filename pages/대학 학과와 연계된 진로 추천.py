import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="활동가 진로 탐색기",
    page_icon="🌍",
    layout="wide"
)

# -------------------------
# 데이터
# -------------------------

CAREERS = {
    "환경 활동가": {
        "major": [
            "환경공학과",
            "환경과학과",
            "생태학과",
            "기후에너지학과"
        ],
        "jobs": [
            "환경운동가",
            "환경컨설턴트",
            "탄소중립 전문가",
            "환경교육 강사",
            "환경 NGO 활동가"
        ],
        "tip": "환경 문제 해결 프로젝트와 봉사활동에 참여해 보세요."
    },

    "인권 활동가": {
        "major": [
            "법학과",
            "사회학과",
            "인권학과",
            "행정학과"
        ],
        "jobs": [
            "인권단체 활동가",
            "노동인권 상담사",
            "시민단체 기획자",
            "공익변호사",
            "정책연구원"
        ],
        "tip": "토론 활동과 사회 문제 분석 능력을 길러보세요."
    },

    "교육 활동가": {
        "major": [
            "교육학과",
            "평생교육학과",
            "청소년지도학과",
            "아동학과"
        ],
        "jobs": [
            "교육 NGO 활동가",
            "청소년 지도사",
            "교육기획자",
            "평생교육사",
            "교육 컨설턴트"
        ],
        "tip": "멘토링과 교육 봉사 경험을 쌓아 보세요."
    },

    "사회복지 활동가": {
        "major": [
            "사회복지학과",
            "상담심리학과",
            "아동복지학과",
            "노인복지학과"
        ],
        "jobs": [
            "사회복지사",
            "복지기관 기획자",
            "지역사회 활동가",
            "상담사",
            "복지정책 연구원"
        ],
        "tip": "사람을 돕는 봉사활동 경험을 늘려 보세요."
    },

    "정치·시민참여 활동가": {
        "major": [
            "정치외교학과",
            "행정학과",
            "언론정보학과",
            "공공인재학과"
        ],
        "jobs": [
            "시민단체 활동가",
            "정책기획자",
            "공공캠페인 전문가",
            "지방의회 보좌진",
            "공공기관 연구원"
        ],
        "tip": "사회 이슈를 꾸준히 공부하고 토론해 보세요."
    },

    "국제협력 활동가": {
        "major": [
            "국제학과",
            "국제개발협력학과",
            "국제관계학과",
            "영어영문학과"
        ],
        "jobs": [
            "국제 NGO 활동가",
            "국제개발 전문가",
            "국제기구 직원",
            "ODA 사업 담당자",
            "국제협력 코디네이터"
        ],
        "tip": "외국어 능력과 국제 이슈 이해도를 높여 보세요."
    }
}

QUESTIONS = [
    ("환경 보호를 위해 생활 습관을 바꾸는 편이다.", "환경 활동가"),
    ("기후 위기 문제에 관심이 많다.", "환경 활동가"),

    ("사회적 약자의 권리에 관심이 많다.", "인권 활동가"),
    ("불공정한 문제를 보면 개선하고 싶다.", "인권 활동가"),

    ("사람을 가르치거나 돕는 것이 즐겁다.", "교육 활동가"),
    ("교육을 통해 사회를 변화시킬 수 있다고 생각한다.", "교육 활동가"),

    ("타인의 어려움을 보면 돕고 싶다.", "사회복지 활동가"),
    ("복지 문제에 관심이 많다.", "사회복지 활동가"),

    ("사회 문제 해결을 위한 정책에 관심이 많다.", "정치·시민참여 활동가"),
    ("공공 문제를 토론하는 것을 좋아한다.", "정치·시민참여 활동가"),

    ("국제 문제와 세계 뉴스에 관심이 많다.", "국제협력 활동가"),
    ("다른 나라 사람들과 협력하는 일에 흥미가 있다.", "국제협력 활동가")
]

OPTIONS = {
    "전혀 아니다": 1,
    "아니다": 2,
    "보통": 3,
    "그렇다": 4,
    "매우 그렇다": 5
}

# -------------------------
# UI
# -------------------------

st.title("🌍 활동가 진로 탐색기")
st.markdown(
    """
    활동가 적성 검사를 통해

    ✔ 나에게 맞는 활동가 유형

    ✔ 추천 대학 학과

    ✔ 관련 직업

    을 확인해보세요.
    """
)

st.divider()

scores = {key: 0 for key in CAREERS.keys()}

with st.form("career_test"):

    st.subheader("적성 검사")

    answers = []

    for idx, (question, category) in enumerate(QUESTIONS, start=1):
        answer = st.radio(
            f"{idx}. {question}",
            list(OPTIONS.keys()),
            key=f"q{idx}"
        )
        answers.append((answer, category))

    submit = st.form_submit_button("결과 보기")

if submit:

    try:

        for answer, category in answers:
            scores[category] += OPTIONS[answer]

        result_type = max(scores, key=scores.get)

        result_data = CAREERS[result_type]

        st.success(f"당신에게 가장 적합한 활동가 유형은 **{result_type}** 입니다!")

        st.subheader("📊 적성 분석")

        chart_df = pd.DataFrame({
            "활동가 유형": list(scores.keys()),
            "점수": list(scores.values())
        })

        st.bar_chart(
            chart_df.set_index("활동가 유형")
        )

        st.subheader("🎓 추천 학과")

        for major in result_data["major"]:
            st.write(f"• {major}")

        st.subheader("💼 추천 직업")

        for job in result_data["jobs"]:
            st.write(f"• {job}")

        st.subheader("🚀 진로 준비 방법")
        st.info(result_data["tip"])

        st.subheader("📌 요약")

        st.write(f"추천 유형: **{result_type}**")
        st.write(
            f"추천 학과 수: {len(result_data['major'])}개"
        )
        st.write(
            f"추천 직업 수: {len(result_data['jobs'])}개"
        )

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
