import streamlit as st
import openai

# OpenAI API 키 설정
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# OpenAI 클라이언트 생성 (1.0.0 이상 버전 방식)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Streamlit 웹앱 제목
st.title("💬 ChatGPT 웹앱 (OpenAI 1.0.0 버전 대응)")

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

    # GPT API 호출 (OpenAI 1.0.0 방식)
    with st.spinner("GPT가 답변을 생성 중입니다..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
            )
            bot_reply = response.choices[0].message.content

            # GPT 응답 저장 및 출력
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.chat_message("assistant").write(bot_reply)
        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
