import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Friend Chat", page_icon="🤖")

st.title("🤖 AI Friend Chat (Powered by Gemini)")

# Configure Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Model
model = genai.GenerativeModel("gemini-1.5-flash")

# Chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display chat history
for msg in st.session_state.chat.history:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["parts"][0].text)

# Input field
if prompt := st.chat_input("Say something..."):
    st.chat_message("user").write(prompt)
    st.session_state.chat.history.append({"role": "user", "parts": [prompt]})

    # Generate AI response
    response = st.session_state.chat.send_message(prompt)
    reply = response.text

    st.chat_message("assistant").write(reply)
    st.session_state.chat.history.append({"role": "assistant", "parts": [reply]})
