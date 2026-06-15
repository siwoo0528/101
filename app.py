import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="AI 융합 탐구 주제 설계소",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI 융합 탐구 주제 설계소")
st.markdown(
    """
관심사를 여러 개 입력하면 AI가 이를 융합하여  
고등학교 생활기록부에 활용 가능한 탐구 주제를 제안합니다.
"""
)

# API 설정
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API 설정 오류: {e}")
    st.stop()

# 입력 영역
interest_text = st.text_area(
    "관심사를 쉼표(,)로 구분하여 입력하세요",
    placeholder="예: 인공지능, 심리학, 환경, 스포츠"
)

departments = [
    "자유 선택",
    "컴퓨터공학과",
    "의예과",
    "심리학과",
    "경영학과",
    "교육학과",
    "법학과",
    "경제학과",
    "생명과학과",
    "기계공학과",
    "전자공학과",
    "화학과",
    "물리학과",
    "간호학과",
    "미디어학과",
    "디자인학과"
]

department = st.selectbox(
    "희망 학과 선택",
    departments
)

difficulty = st.selectbox(
    "탐구 수준",
    ["고등학교 1학년", "고등학교 2학년", "고등학교 3학년"]
)

generate = st.button("🚀 탐구 주제 생성")

if generate:

    if not interest_text.strip():
        st.warning("관심사를 입력해주세요.")
        st.stop()

    interests = [
        x.strip()
        for x in interest_text.split(",")
        if x.strip()
    ]

    interest_string = ", ".join(interests)

    prompt = f"""
너는 대한민국 고등학교 진로·진학 전문 탐구 설계 AI이다.

학생 관심사:
{interest_string}

희망 학과:
{department}

학생 수준:
{difficulty}

조건:

1. 관심사를 모두 반영한다.
2. 학과와 연계한다.
3. 고등학교 생활기록부에 적합해야 한다.
4. 실제 수행 가능한 탐구여야 한다.
5. 너무 추상적이면 안 된다.
6. 창의적인 융합형 주제를 제안한다.

다음 형식으로 작성하라.

# 탐구 주제

# 주제 선정 이유

# 연구 질문

# 탐구 방법

# 기대 효과

# 진로 연계성

추가로

# 확장 탐구 아이디어

도 제안하라.
"""

    try:
        model = genai.GenerativeModel(
            "gemini-2.5-flash-lite"
        )

        response = model.generate_content(prompt)

        st.success("탐구 주제가 생성되었습니다.")

        st.markdown(response.text)

    except Exception as e:
        st.error("AI 생성 중 오류가 발생했습니다.")
        st.exception(e)

st.divider()

st.subheader("💡 입력 예시")

st.markdown(
"""
- 인공지능, 환경, 스포츠
- 심리학, 게임, 데이터분석
- 경제, 기후변화, 정책
- 의학, AI, 생명과학
- 교육, 메타버스, 심리학
"""
)
