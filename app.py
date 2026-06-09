import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="내일의 나: 고등학생 진로 상담소", page_icon="🌱", layout="centered")
st.title("🌱 내일의 나: 진로 상담 챗봇")
st.caption("아직 하고 싶은 일을 찾지 못해 고민인가요? 함께 이야기 나누며 길을 찾아봐요.")

# 2. Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
try:
    # streamlit 공식 가이드에 따라 st.secrets에서 키를 가져옵니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("🔑 Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 설정 후 다시 시도해주세요.")
    st.stop()

# 3. 세션 상태(Session State)로 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 이전 대화 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 받기
if prompt := st.chat_input("고민이나 관심사가 있다면 편하게 말해주세요. (예: 어떤 과목을 좋아해, 요즘 관심 있는 것 등)"):
    
    # 사용자 메시지 화면에 표시 및 세션 저장
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 6. Gemini 모델을 통한 답변 생성 및 예외 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # 모델 설정 및 페르소나(System Instruction) 부여
        config = types.GenerateContentConfig(
            system_instruction=(
                "당신은 진로가 없어 고민하는 고등학생을 돕는 따뜻하고 공감 능력이 뛰어난 진로 상담사입니다. "
                "학생의 말에 깊이 공감해주고, 다정하며 친근한 말투(해요체)를 사용하세요. "
                "직업을 바로 정해주기보다는 학생이 좋아하는 과목, 취미, 관심사, 사소한 습관 등을 질문하며 "
                "스스로 장점과 흥미를 발견할 수 있도록 대화를 유도해주세요. 절대 다그치거나 딱딱하게 답변하지 마세요."
            ),
            temperature=0.7,
        )
        
        # 이전 대화 맥락을 Gemini가 이해할 수 있는 형태로 변환
        contents = []
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
        
        try:
            with st.spinner("생각 중... 🌱"):
                # 최신 대화 답변 요청 (gemini-2.5-flash-lite 사용)
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=contents,
                    config=config
                )
                
                # 결과 출력 및 세션 저장
                assistant_response = response.text
                message_placeholder.markdown(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                
        except APIError as e:
            # Gemini API 관련 오류 처리
            error_msg = f"⚠️ Gemini API 오류가 발생했습니다: {e.message}"
            message_placeholder.markdown(error_msg)
        except Exception as e:
            # 기타 일반 오류 처리
            error_msg = f"⚠️ 알 수 없는 오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_msg)
