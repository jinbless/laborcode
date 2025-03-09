import streamlit as st
import openai

# OpenAI API 키 설정
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# OpenAI 클라이언트 생성 (1.0.0 버전 방식)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# 좌측 상단에 설정값 고정 표시
st.sidebar.header("⚙️ 설정 (고정)")
st.sidebar.write("📌 모델: **gpt-4o**")
st.sidebar.write("📌 Temperature: **0.0** (가장 논리적인 응답)")
st.sidebar.write("📌 최대 토큰 수: **1024**")

# 시스템 프롬프트 입력란 (더 넓게 설정)
st.markdown("### 📝 시스템 프롬프트 설정")
system_prompt = st.text_area(
    "지식데이터를 붙여넣으세요.",
    height=150  # 높이를 더 크게 설정
)

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

    # GPT API 호출 (고정된 설정값 사용)
    with st.spinner("GPT가 답변을 생성 중입니다..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # 고정
                messages=st.session_state.messages,
                temperature=0.0,  # 고정 (논리적인 응답)
                max_tokens=1024  # 고정 (최대 1024 토큰)
            )
            bot_reply = response.choices[0].message.content

            # 대화 기록에 GPT 응답 추가
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.chat_message("assistant").write(bot_reply)
        except Exception as e:
            st.error(f"오류 발생: {str(e)}")

# 🗑️ 대화 기록 초기화 버튼 (위치 유지)
if st.sidebar.button("🗑️ 대화 기록 초기화"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.experimental_rerun()
