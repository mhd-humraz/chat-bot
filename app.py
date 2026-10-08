"""StudyBuddy AI - Streamlit user interface."""
import streamlit as st

import chatbot
import config

st.set_page_config(page_title=config.APP_TITLE, page_icon="🤖", layout="centered")

# Small, targeted CSS: header banner and rounded buttons only.
st.markdown(
    """
    <style>
    .hero {padding: 1.2rem 1.4rem; border-radius: 16px; margin-bottom: 1rem;
           background: linear-gradient(135deg, #6C63FF 0%, #8E7CFF 100%); color: white;}
    .hero h1 {margin: 0; font-size: 2rem; color: white;}
    .hero p {margin: .2rem 0 0 0; opacity: .95;}
    div.stButton > button {border-radius: 12px;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- state helpers ----------
def init_state() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("active_tool", None)
    st.session_state.setdefault("pending_prompt", None)


def queue_prompt(text: str) -> None:
    st.session_state.pending_prompt = text


def select_tool(key: str) -> None:
    # Clicking the active tool again turns it off.
    st.session_state.active_tool = None if st.session_state.active_tool == key else key


def clear_chat() -> None:
    st.session_state.messages = []
    st.session_state.active_tool = None
    st.session_state.pending_prompt = None


def api_history() -> list[dict]:
    """Messages to send to the API (skips failed turns and error notices)."""
    return [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if not m.get("failed") and not m.get("error")
    ]


# ---------- UI sections ----------
def render_sidebar() -> str:
    with st.sidebar:
        st.header("⚙️ Study Settings")
        mode = st.radio(
            "🎯 Response Mode",
            list(config.RESPONSE_MODES),
            format_func=lambda m: f"{m}  ·  {config.MODE_HELP[m]}",
            key="mode",
        )
        st.divider()
        st.subheader("🧰 Quick Tools")
        for key, (label, icon, _) in config.TOOLS.items():
            active = st.session_state.active_tool == key
            st.button(
                f"{icon} {label}", key=f"tool_{key}", use_container_width=True,
                type="primary" if active else "secondary",
                on_click=select_tool, args=(key,),
            )
        st.caption("Pick a tool, then type your topic below.")
        st.divider()
        st.button("🗑️ Clear Chat", use_container_width=True, on_click=clear_chat)
        if not config.get_api_key():
            st.warning("No API key found. Copy `.env.example` to `.env` and add your key.")
    return mode


def render_header() -> None:
    st.markdown(
        "<div class='hero'><h1>🤖 StudyBuddy AI</h1>"
        "<p><b>Your Personal AI Study Assistant</b><br>"
        "Learn smarter. Understand faster. Prepare better.</p></div>",
        unsafe_allow_html=True,
    )


def render_landing() -> None:
    st.markdown("### What would you like to learn today? 🚀")
    cols = st.columns(2)
    for i, (label, prompt) in enumerate(config.STARTER_PROMPTS):
        cols[i % 2].button(
            label, key=f"starter_{i}", use_container_width=True,
            on_click=queue_prompt, args=(prompt,),
        )


def render_history() -> None:
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            if msg.get("error"):
                st.warning(msg["content"])
            else:
                st.markdown(msg.get("display", msg["content"]))


def handle_prompt(prompt: str, mode: str) -> None:
    """Send one user message, stream the reply and store both in history."""
    tool = st.session_state.active_tool

    if tool:
        label, icon, _ = config.TOOLS[tool]
        user_msg = {
            "role": "user",
            "content": chatbot.build_tool_prompt(tool, prompt),
            "display": f"{icon} **{label}:** {prompt}",
        }
        st.session_state.active_tool = None
    else:
        user_msg = {"role": "user", "content": prompt}

    st.session_state.messages.append(user_msg)

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_msg.get("display", prompt))

    with st.chat_message("assistant", avatar="🤖"):
        try:
            placeholder = st.empty()
            reply = ""

            for chunk in chatbot.stream_reply(api_history(), mode):
                reply += str(chunk)
                placeholder.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except chatbot.ChatbotError as err:
            user_msg["failed"] = True
            st.session_state.messages.append({
                "role": "assistant",
                "content": str(err),
                "error": True
            })
            st.warning(str(err))


# ---------- main ----------
def main() -> None:
    init_state()
    mode = render_sidebar()
    render_header()

    tool = st.session_state.active_tool
    placeholder = config.TOOL_PLACEHOLDERS[tool] if tool else "Ask StudyBuddy anything..."
    typed = st.chat_input(placeholder)
    prompt = st.session_state.pending_prompt or typed
    st.session_state.pending_prompt = None

    if prompt is not None and not prompt.strip():
        st.info("Please type a question first. ✍️")
        prompt = None

    if tool:
        label, icon, _ = config.TOOLS[tool]
        st.info(f"{icon} **{label}** tool is active. {config.TOOL_PLACEHOLDERS[tool]}")

    if not st.session_state.messages and not prompt:
        render_landing()

    render_history()
    if prompt:
        handle_prompt(prompt.strip(), mode)


main()

