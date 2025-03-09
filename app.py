import streamlit as st
import openai

# OpenAI API 키 설정
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# OpenAI 클라이언트 생성 (1.0.0 버전 방식)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# 사이드바에서 설정 옵션 추가
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 모델 선택 옵션 (고정값)
    model = "gpt-4o"

    # Temperature 설정 (고정값)
    temperature = 0.0

    # 최대 토큰 제한 (고정값)
    max_tokens = 1024

    # 시스템 프롬프트 입력란 (사이드바에서 입력)
    system_prompt_input = st.text_area("🔹 시스템 프롬프트 입력", "", height=150, placeholder="여기에 지식데이터를 입력하세요.")

    # 저장 버튼 (누르면 세션 상태에 저장됨)
    if st.button("💾 저장"):
        if system_prompt_input.strip() == "":
            st.warning("⚠️ system_prompt에 지식데이터를 넣으세요!")  # 팝업 알람 띄우기
        else:
            st.session_state.system_prompt = system_prompt_input
            st.success("✅ 시스템 프롬프트가 저장되었습니다.")

# 웹앱 제목
st.title("🔬 AI노동법 지원단")

# 사용자가 시스템 프롬프트를 저장하지 않았다면 경고 메시지 표시
if "system_prompt" not in st.session_state or st.session_state.system_prompt.strip() == "":
    st.warning("⚠️ 먼저 사이드바에서 system_prompt를 입력하고 저장하세요!")
else:
    # 세션 상태에서 대화 기록 유지
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]

    # 사용자 입력 받기 (프롬프트가 입력된 경우에만 활성화)
    if user_input := st.chat_input("메시지를 입력하세요..."):
        # 대화 기록에 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # GPT API 호출 (고정된 설정값 사용, 저장된 시스템 프롬프트 반영)
        with st.spinner("GPT가 답변을 생성 중입니다..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": st.session_state.system_prompt}] + st.session_state.messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                bot_reply = response.choices[0].message.content

                # 대화 기록에 GPT 응답 추가
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                st.chat_message("assistant").write(bot_reply)
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")

# 대화 리셋 버튼 추가
if st.sidebar.button("🗑️ 대화 기록 초기화"):
    st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]
    st.rerun()