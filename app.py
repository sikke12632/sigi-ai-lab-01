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
    st.error("오류: API 키가 설정되지 않았습니다.")
    st.stop()

# 3. [핵심] 사용 가능한 모델 자동 검색
try:
    # 생성 가능한 모델 중 가장 적합한 1.5-flash 계열을 자동으로 찾음
    models = [m for m in genai.list_models() if 'generateContent' in m.supported_methods and 'gemini-1.5-flash' in m.name]
    if not models:
        st.error("모델을 찾을 수 없습니다. API 키를 다시 확인해주세요.")
        st.stop()
    selected_model = models[0].name
    model = genai.GenerativeModel(
        model_name=selected_model,
        system_instruction="너는 초등학교 5학년 학생들을 위한 다정하고 똑똑한 AI 선생님이야. 항상 초등학생 눈높이에 맞게 쉽고 다정하게 격려하는 말투(~요, ~체)로 대답해줘."
    )
except Exception as e:
    st.error(f"모델 설정 오류: {e}")
    st.stop()

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 4. 대화 기록 표시
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# 5. 학생 입력창
if prompt := st.chat_input("AI에게 명령을 내려보세요!"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("AI가 생각하고 있어요..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error("앗, 오류가 발생했어요. 잠시 후 다시 시도해 주세요.")
                st.warning(f"🔍 에러 상세 원인: {e}")
