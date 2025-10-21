import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="AI Friend Chat", page_icon="🤖")

st.title("🤖 AI Friend Chat (Powered by Gemini)")

# Configure Gemini API key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use the latest Gemini model
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display previous chat messages
for msg in st.session_state.chat.history:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        if isinstance(msg["parts"][0], str):
            st.markdown(msg["parts"][0])
        else:
            st.markdown(msg["parts"][0].text)

# User input
if prompt := st.chat_input("Say something..."):
    # Display user message
    st.chat_message("user").write(prompt)
    st.session_state.chat.history.append({"role": "user", "parts": [prompt]})

    # Get AI response
    response = st.session_state.chat.send_message(prompt)
    reply = response.text

    # Display AI response
    st.chat_message("assistant").write(reply)
    st.session_state.chat.history.append({"role": "assistant", "parts": [reply]})
