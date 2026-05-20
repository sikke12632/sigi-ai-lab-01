import streamlit as st
from google import genai

# 1. 페이지 설정
st.set_page_config(page_title="식이쌤의 AI 실험실", page_icon="🤖")
st.title("🤖 식이쌤의 AI 실험실")

# 2. 클라이언트 초기화
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API 키를 설정해주세요.")
    st.stop()

# 3. 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 화면 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. 입력 및 응답 (모델명을 'gemini-1.5-flash'로 고정)
if prompt := st.chat_input("질문을 입력하세요"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("AI가 생각 중..."):
            try:
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"오류 발생: {e}")
