import streamlit as st
import openai

st.set_page_config(
    page_title="AI노동법 지원단",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

PASSWORD = st.secrets["password"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    user_password = st.text_input("🔑 비밀번호를 입력하세요:", type="password")
    if st.button("로그인"):
        if user_password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.warning("❌ 비밀번호가 틀렸습니다. 다시 시도하세요.")
    st.stop()

st.write("✅ 인증되었습니다.")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)

with st.sidebar:
    st.header("⚙️ 설정")
    model = "gpt-4o"
    temperature = 0.0
    max_tokens = 1024
    system_prompt_input = st.text_area("🔹 시스템 프롬프트 입력", "", height=150, placeholder="여기에 지식데이터를 입력하세요.")
    if st.button("💾 저장"):
        if system_prompt_input.strip() == "":
            st.warning("⚠️ system_prompt에 지식데이터를 넣으세요!")
        else:
            st.session_state.system_prompt = system_prompt_input
            st.success("✅ 시스템 프롬프트가 저장되었습니다. 대화가 5회를 초과하면 강제 초기화 됩니다.")

st.title("🔬 AI노동법 지원단 GPT")

if "system_prompt" not in st.session_state or st.session_state.system_prompt.strip() == "":
    st.warning("⚠️ 먼저 사이드바에서 system_prompt를 입력하고 저장하세요!")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        elif message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])

    if user_input := st.chat_input("메시지를 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        if len(st.session_state.messages) > 10:  # 시스템 프롬프트 포함하여 5회 초과 시 초기화
            st.session_state.pop("messages", None)
            st.session_state.pop("system_prompt", None)
            st.rerun()

        with st.spinner("GPT가 답변을 생성 중입니다..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                bot_reply = response.choices[0].message.content
                
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                st.chat_message("assistant").write(bot_reply)
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")

if st.sidebar.button("🗑️ 대화 기록 초기화"):
    st.session_state.pop("messages", None)
    st.session_state.pop("system_prompt", None)
    st.rerun()
