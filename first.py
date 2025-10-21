import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Friend Chat", page_icon="🤖")

st.title("🤖 AI Friend Chat (Powered by Gemini)")

# Configure Gemini API key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use a stable model name (supported in free & paid keys)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display chat history
for msg in st.session_state.chat.history:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        if isinstance(msg["parts"][0], str):
            st.markdown(msg["parts"][0])
        else:
            st.markdown(str(msg["parts"][0]))

# Input field for user
if prompt := st.chat_input("Say something..."):
    # Display user message
    st.chat_message("user").write(prompt)
    st.session_state.chat.history.append({"role": "user", "parts": [prompt]})

    try:
        # Generate AI response
        response = st.session_state.chat.send_message(prompt)
        reply = response.text

        # Display AI reply
        st.chat_message("assistant").write(reply)
        st.session_state.chat.history.append({"role": "assistant", "parts": [reply]})

    except Exception as e:
        st.error(f"❌ Error: {e}")
