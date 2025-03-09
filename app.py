import streamlit as st
import openai

# OpenAI API 키 설정
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# OpenAI 클라이언트 생성 (1.0.0 버전 방식)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# 웹앱 제목
st.title("🔬 OpenAI Playground (Streamlit 버전)")

# 🌟 사이드바에서 설정 옵션 추가
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 모델 선택 옵션
    model = st.selectbox("모델 선택", ["gpt-4o", "gpt-4o-mini"])

    # Temperature 설정 (창의적 or 논리적 답변 조절)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

    # 최대 토큰 제한
    max_tokens = st.slider("최대 토큰 수", 100, 4096, 1024, 100)

    # 시스템 프롬프트 입력 (사용자 역할 설정)
    system_prompt = st.text_area("🔹 시스템 프롬프트", "You are a helpful assistant.")

# 세션 상태에서 대화 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 채팅 기록 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 받기
if user_input := st.chat_input("메시지를 입력하세요..."):
    # 대화 기록에 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # GPT API 호출
    with st.spinner("GPT가 답변을 생성 중입니다..."):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            bot_reply = response.choices[0].message.content

            # 대화 기록에 GPT 응답 추가
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.chat_message("assistant").write(bot_reply)
        except Exception as e:
            st.error(f"오류 발생: {str(e)}")

# 🔄 대화 리셋 버튼 추가
if st.sidebar.button("🗑️ 대화 기록 초기화"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.experimental_rerun()
