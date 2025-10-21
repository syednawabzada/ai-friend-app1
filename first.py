import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="AI Friend Chat", page_icon="🤖")

st.title("🤖 AI Friend Chat (Powered by Gemini)")

# Configure Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Use the stable model
model = genai.GenerativeModel("gemini-1.5-pro")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display previous messages safely
for msg in st.session_state.chat.history:
    role = msg.get("role", "assistant")
    content = msg["parts"][0] if isinstance(msg["parts"][0], str) else msg["parts"][0].text
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(content)

# Chat input
if prompt := st.chat_input("Say something..."):
    st.chat_message("user").write(prompt)
    st.session_state.chat.history.append({"role": "user", "parts": [prompt]})

    try:
        # Generate response from Gemini
        response = st.session_state.chat.send_message(prompt)
        reply = response.text

        st.chat_message("assistant").write(reply)
        st.session_state.chat.history.append({"role": "assistant", "parts": [reply]})

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
