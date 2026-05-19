import streamlit as st
import google.generativeai as genai

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="식이쌤의 AI 실험실", page_icon="🤖", layout="centered")

st.title("🤖 식이쌤의 AI 실험실")
st.caption("5학년 9반 친구들을 위한 안전하고 재미있는 프롬프트 연습 공간입니다.")
st.markdown("---")

# 2. 안전하게 숨겨둔 API 키 불러오기
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("오류: 시스템에 API 키가 설정되지 않았습니다.")
    st.stop()

# 3. 5학년 맞춤형 AI 설정
if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "너는 초등학교 5학년 학생들을 위한 다정하고 똑똑한 AI 선생님이야. "
            "학생들이 프롬프트(명령어)를 어떻게 넣느냐에 따라 답변이 달라지는 원리를 학습하고 있어. "
            "1. 항상 초등학생 눈높이에 맞게 쉽고 다정하게 격려하는 말투(~요, ~체)로 대답해줘. "
            "2. 학생들이 특정 역할(예: 동화작가, 역사학자, 과학자)을 너에게 부여하면, 그 역할에 깊이 몰입해서 대답해줘. "
            "3. 비속어, 유해한 내용, 장난스러운 공격성 프롬프트가 들어오면 답변을 거부하고 '바른 말을 사용해 주세요'라고 정중히 안내해줘."
        )
    )
    st.session_state.chat = model.start_chat(history=[])

# 4. 화면에 이전 대화 기록 보여주기
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. 학생 입력창 및 생성 처리
if prompt := st.chat_input("AI에게 명령을 내려보세요! (예: 너는 300년 뒤 미래에서 온 로봇이야...)"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("AI가 생각하고 있어요..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                message_placeholder.markdown(response.text)
            except Exception as e:
                # 화면에는 다정하게 안내하고, 검은색 로그창에 진짜 원인을 출력합니다.
                st.error("앗, 너무 많은 친구들이 동시에 질문했나봐요! 10초만 기다렸다가 다시 해볼까요?")
                print(f"❌ [진짜 에러 발견]: {e}")
