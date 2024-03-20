from openai import OpenAI
import streamlit as st

from prompt import IDEAS_PROMPT, STARTER_MESSAGE

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Fresh Ideas")

if "openai_model" not in st.session_state:
  st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
  st.session_state.messages = [{"role": "assistant", "content": STARTER_MESSAGE}]

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
  st.session_state.messages.append({"role": "user", "content": prompt})
  # Display user message in chat message container
  with st.chat_message("user"):
    st.markdown(prompt)
  # Display assitant message in chat message container
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""

    messages = [
      {"role": m["role"], "content": m["content"]}
      for m in st.session_state.messages
    ]
    messages.insert(0, {"role": "system", "content": IDEAS_PROMPT})
    # Simulate stream of response with milliseconds delay
    for response in client.chat.completions.create(
      model="gpt-4-turbo-preview",
      messages=messages,
      temperature=1.2,
      #will provide lively writing
      stream=True,
    ):
      #get content in response
      if response.choices[0].delta.content:
        full_response += response.choices[0].delta.content
      # Add a blinking cursor to simulate typing
      message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
  # Add assistant response to chat history
  st.session_state.messages.append({"role": "assistant", "content": full_response})