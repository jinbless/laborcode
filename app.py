import streamlit as st
import openai

# OpenAI API 키 입력 (직접 입력보다는 환경 변수 사용 권장)
OPENAI_API_KEY = "your_openai_api_key"

# 웹앱 제목
st.title("💬 ChatGPT 웹앱 (Streamlit)")

# 세션 상태에서 대화 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 받기
if user_input := st.chat_input("질문을 입력하세요"):
    # 사용자 입력 저장 및 출력
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # GPT API 호출
    with st.spinner("GPT가 답변을 생성 중입니다..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=st.session_state.messages,
                api_key=OPENAI_API_KEY,
            )
            bot_reply = response["choices"][0]["message"]["content"]

            # GPT 응답 저장 및 출력
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.chat_message("assistant").write(bot_reply)
        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
