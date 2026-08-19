# Import libraries
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st

# Load env variables
load_dotenv()

# Streamlit page setup
st.set_page_config(
    page_title = "💬 Chatbot",
    page_icon = "🤖",
    layout = "centered"
)
st.title("💬 Generative AI Chatbot")

# Initiate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Define the LLM
llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    temperature = 0
)

# Input box
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    response = llm.invoke(
        input = [{"role": "system", "content": "You are a helpful assistant."}, *st.session_state.chat_history]
    )
    assistant_response = response.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# Here's how the code above works

# user query
# display user query
# save query to chat history
# send the chat history to llm
# get response from llm
# save response in chat history
# display llm response

# Replace llm.invoke() with llm.stream() and use st.write_stream() which Streamlit built specifically for this:
# if user_prompt:
#     st.chat_message("user").markdown(user_prompt)
#     st.session_state.chat_history.append({"role": "user", "content": user_prompt})

#     with st.chat_message("assistant"):
#         response = st.write_stream(
#             llm.stream(
#                 input=[{"role": "system", "content": "You are a helpful assistant."}, *st.session_state.chat_history]
#             )
#         )

#     st.session_state.chat_history.append({"role": "assistant", "content": response})
# What changed
# 	Before	After
# Method	llm.invoke()	llm.stream()
# Display	st.markdown()	st.write_stream()
# Returns	Full response at once	Chunks as they arrive
# Key points
# llm.stream() returns a generator that yields chunks as the LLM produces them
# st.write_stream() consumes that generator, displays each chunk in real time, and returns the full assembled string when done — so you can directly append it to history
# The with st.chat_message("assistant") wraps both the streaming display and keeps it inside the assistant bubble

# You can wrap the stream in a custom generator that adds a delay between chunks:
# import time

# def stream_with_delay(stream, delay=0.004):
#     for chunk in stream:
#         yield chunk
#         time.sleep(delay)

# if user_prompt:
#     st.chat_message("user").markdown(user_prompt)
#     st.session_state.chat_history.append({"role": "user", "content": user_prompt})

#     with st.chat_message("assistant"):
#         response = st.write_stream(
#             stream_with_delay(
#                 llm.stream(
#                     input=[{"role": "system", "content": "You are a helpful assistant."}, *st.session_state.chat_history]
#                 )
#             )
#         )

#     st.session_state.chat_history.append({"role": "assistant", "content": response})
# st.write_stream() accepts any generator, so wrapping the stream with your own generator that sleeps between chunks works perfectly. The delay is per chunk not per character though — if you want per character:
# def stream_with_delay(stream, delay=0.004):
#     for chunk in stream:
#         for char in chunk:
#             yield char
#             time.sleep(delay)
