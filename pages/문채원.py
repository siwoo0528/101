import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="AI 진로 상담소",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI 진로 상담소")
st.write("성격, 관심사, 잘하는 과목을 입력하면 AI가 어울리는 직업을 추천해드립니다.")

# API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# 입력
personality = st.text_area(
    "😊 성격",
    placeholder="예: 사람들과 이야기하는 것을 좋아하고 책임감이 강함"
)

interest = st.text_area(
    "🎨 관심사",
    placeholder="예: 아이들, 그림 그리기, 음악"
)

subject = st.text_area(
    "📚 잘하는 과목",
    placeholder="예: 국어, 영어, 미술"
)

dream = st.text_input(
    "🌟 관심 있는 직업 (선택)"
)

if st.button("진로 분석하기"):

    if not personality or not interest or not subject:
        st.warning("성격, 관심사, 잘하는 과목을 모두 입력해주세요.")
        st.stop()

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
당신은 고등학생 전문 진로상담사입니다.

학생 정보

성격:
{personality}

관심사:
{interest}

잘하는 과목:
{subject}

관심 직업:
{dream}

다음 형식으로 자세하게 답변하세요.

1. 학생 성향 분석

2. 추천 직업 TOP 5
- 직업명
- 추천 이유

3. 추천 학과

4. 고등학생이 지금 준비하면 좋은 활동

5. 한 줄 조언

답변은 친절하고 이해하기 쉽게 작성하세요.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        st.success("분석 완료!")

        st.markdown(response.text)

    except Exception as e:
        st.error(f"AI 분석 중 오류가 발생했습니다.\n\n{e}")
