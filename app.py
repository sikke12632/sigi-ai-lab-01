import streamlit as st
from google import genai
from google.genai import types

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="식이쌤의 AI 실험실", page_icon="🤖", layout="centered")

st.title("🤖 식이쌤의 AI 실험실")
st.caption("5학년 9반 친구들을 위한 안전하고 재미있는 프롬프트 연습 공간입니다.")
st.markdown("---")

# 2. 안전하게 숨겨둔 API 키 불러오기 및 최신 클라이언트 선언
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("오류: 시스템에 API 키가 설정되지 않았습니다.")
    st.stop()

# 3. 대화 기록을 저장할 공간 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 화면에 이전 대화 기록 예쁘게 보여주기
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. 학생 입력창 및 최신 API 엔진 처리
if prompt := st.chat_input("AI에게 명령을 내려보세요! (예: 너는 300년 뒤 미래에서 온 로봇이야...)"):
    # 학생 입력 화면에 표시 및 저장
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # AI 답변 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("AI가 생각하고 있어요..."):
            try:
                # 이전 대화 맥락을 최신 규격에 맞게 변환하여 기억력 유지
                chat_history = []
                for msg in st.session_state.messages[:-1]:
                    chat_history.append(
                        types.Content(
                            role="user" if msg["role"] == "user" else "model",
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )
                
                # [수정] 구글 서버 과부하를 피하기 위해 가장 검증되고 안정적인 1.5-flash 모델로 변경
                chat = client.chats.create(
                    model="gemini-1.5-flash",
                    history=chat_history,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "너는 초등학교 5학년 학생들을 위한 다정하고 똑똑한 AI 선생님이야. "
                            "학생들이 프롬프트(명령어)를 어떻게 넣느냐에 따라 답변이 달라지는 원리를 학습하고 있어. "
                            "1. 항상 초등학생 눈높이에 맞게 쉽고 다정하게 격려하는 말투(~요, ~체)로 대답해줘. "
                            "2. 학생들이 특정 역할(예: 동화작가, 역사학자, 과학자)을 너에게 부여하면, 그 역할에 깊이 몰입해서 대답해줘. "
                            "3. 비속어, 유해한 내용, 장난스러운 공격성 프롬프트가 들어오면 답변을 거부하고 '바른 말을 사용해 주세요'라고 정중히 안내해줘."
                        )
                    )
                )
                
                # 답변 받아오기
                response = chat.send_message(prompt)
                ai_response = response.text
                
                # 화면 표시 및 저장
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error("앗, 너무 많은 친구들이 동시에 질문했나봐요! 10초만 기다렸다가 다시 해볼까요?")
                st.warning(f"🔍 에러 상세 원인: {e}")
