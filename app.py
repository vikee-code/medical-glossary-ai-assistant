import streamlit as st
from modules.gemini_client import get_gemini_response

st.set_page_config(
    page_title="Medical Image Analyzer Assistant",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Medical Image Analyzer Assistant")

st.markdown("""
### Welcome

This assistant helps healthcare professionals:

- Analyze medical images
- Generate observations
- Explain medical findings
- Assist image interpretation

⚠️ This tool is intended for decision support and educational purposes only.
""")

st.divider()

api_key = st.text_input(
    "Enter your Gemini API Key",
    type="password",
    placeholder="AIza..."
)

if api_key:
    st.success("API Key loaded successfully!")

if st.button(
    "Start Assistant",
    disabled=not bool(api_key)
):
    st.session_state["started"] = True

if st.session_state.get("started", False):

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": """
Hello Doctor 👋

I can help you:

• Analyze medical images
• Explain findings
• Generate observations
• Assist image interpretation

Upload a medical image or ask a question to get started.
"""
            }
        ]

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input(
    "Ask a medical imaging question..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    try:

        response = get_gemini_response(
            api_key,
            prompt
        )

    except Exception as e:

        response = f"Error: {str(e)}"

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()