import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

st.set_page_config(
    page_title="AI 안정직업 추천소",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI 안정직업 추천소")
st.caption("AI가 적성을 분석하여 사회적으로 안정적인 직업을 추천합니다.")

# Gemini 설정
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
except Exception:
    model = None

with st.sidebar:
    st.header("입력 정보")
    interests = st.text_area(
        "관심 분야",
        placeholder="예: IT, 경제, 의료"
    )

    activities = st.text_area(
        "좋아하는 활동",
        placeholder="예: 문제 해결, 사람 돕기"
    )

    personality = st.text_area(
        "성격",
        placeholder="예: 꼼꼼함, 책임감 강함"
    )

    strengths = st.text_area(
        "강점",
        placeholder="예: 분석력, 의사소통 능력"
    )

analyze = st.button("🔍 직업 추천 받기", type="primary")

if analyze:

    if not all([
        interests.strip(),
        activities.strip(),
        personality.strip(),
        strengths.strip()
    ]):
        st.warning("모든 항목을 입력해주세요.")
        st.stop()

    if model is None:
        st.error(
            "Gemini API가 설정되지 않았습니다. Secrets에 GEMINI_API_KEY를 등록해주세요."
        )
        st.stop()

    prompt = f"""
당신은 진로 컨설턴트입니다.

사용자 정보

관심 분야:
{interests}

좋아하는 활동:
{activities}

성격:
{personality}

강점:
{strengths}

요구사항

사회적으로 안정적인 직업 위주로 5개 추천.

반드시 아래 JSON만 출력.

[
  {{
    "직업":"",
    "안정성점수":90,
    "적합도점수":85,
    "추천이유":"",
    "미래전망":""
  }}
]
"""

    with st.spinner("AI가 적성을 분석하고 있습니다..."):

        try:
            response = model.generate_content(prompt)

            text = response.text.strip()

            if text.startswith("```json"):
                text = text.replace("```json", "")
                text = text.replace("```", "").strip()

            jobs = json.loads(text)

            st.success("분석 완료!")

            df = pd.DataFrame(jobs)

            st.subheader("📊 추천 직업 목록")
            st.dataframe(
                df[["직업", "안정성점수", "적합도점수"]],
                use_container_width=True
            )

            st.subheader("📋 상세 분석")

            for job in jobs:

                with st.expander(
                    f"{job['직업']} | 안정성 {job['안정성점수']}점 | 적합도 {job['적합도점수']}점"
                ):
                    st.write("### 추천 이유")
                    st.write(job["추천이유"])

                    st.write("### 미래 전망")
                    st.write(job["미래전망"])

        except json.JSONDecodeError:
            st.error(
                "AI 응답 형식 오류가 발생했습니다. 다시 시도해주세요."
            )

        except Exception as e:
            st.error(f"오류 발생: {str(e)}")

st.markdown("---")
st.markdown(
    """
### 사용 방법
1. 관심 분야 입력
2. 좋아하는 활동 입력
3. 성격 입력
4. 강점 입력
5. 직업 추천 받기 클릭
"""
)
