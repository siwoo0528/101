import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 설정
st.set_page_config(page_title="꿈을 찾는 진로상담소", page_icon="🎓", layout="centered")
st.title("🎓 꿈을 찾는 진로상담소")
st.caption("학과 선택, 직업 고민, 역량 개발 등 진로에 대한 무엇이든 물어보세요. (Gemini 2.5 Flash-Lite 구동)")

# Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 설정 후 다시 시도해주세요.")
    st.stop()

# 세션 상태(Chat History) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "content": "안녕하세요! 당신의 적성과 꿈을 함께 찾아갈 진로 상담사입니다. 현재 어떤 진로 고민을 가지고 계시나요? 😊"
        }
    ]

# 기존 채팅 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 사용자 입력 받기
if user_input := st.chat_input("진로, 학과, 취업 등 고민을 입력하세요..."):
    # 1. 사용자 메시지 화면에 표시 및 세션 저장
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 2. 챗봇 답변 생성
    with st.chat_message("model"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 진로 고민을 분석하고 해결책을 생각 중입니다...")
        
        try:
            # API 호출용 대화 기록 포맷 변환 (Gemini SDK 표준에 맞춤)
            history = []
            for msg in st.session_state.messages[:-1]: # 방금 넣은 user_input 제외 과거 기록
                history.append(
                    types.Content(
                        role="user" if msg["role"] == "user" else "model",
                        parts=[types.Part.from_text(text=msg["content"])]
                    )
                )

            # 진로 상담에 특화된 페르소나 부여 (System Instruction)
            config = types.GenerateContentConfig(
                system_instruction=(
                    "당신은 구직자와 학생들을 대상으로 하는 따뜻하고 전문적인 진로/진학 전문 상담사입니다. "
                    "질문자의 상황에 깊이 공감해주되, 객관적인 데이터나 현실적인 조언을 균형 있게 제공하세요. "
                    "막연한 위로보다는 구체적인 학과 추천, 직업 트렌드, 필요한 역량 및 자격증, 구체적인 커리어 로드맵을 제안해 주세요. "
                    "친근감을 주기 위해 답변에 적절한 이모지를 섞어서 가독성 좋게 작성해 주세요."
                ),
                temperature=0.7,
            )

            # Gemini 2.5 Flash-Lite 모델 호출
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=history + [types.Content(role="user", parts=[types.Part.from_text(text=user_input)])],
                config=config
            )
            
            # 결과 출력 및 세션 저장
            ai_response = response.text
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "model", "content": ai_response})

        except APIError as e:
            # Gemini API 관련 오류 처리
            message_placeholder.empty()
            st.error(f"Gemini API 오류가 발생했습니다: {e.message}")
        except Exception as e:
            # 기타 일반 오류 처리
            message_placeholder.empty()
            st.error(f"알 수 없는 오류가 발생했습니다: {str(e)}")
