import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from backend.langgraph_database_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# **************************************** Utility Functions *************************

def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])


# **************************************** Session Setup *****************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])


# **************************************** Sidebar UI ********************************

st.sidebar.markdown("## 💬 LangGraph Chatbot")

if st.sidebar.button('➕ New Chat'):
    reset_chat()

st.sidebar.markdown("### 📂 My Conversations")
for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(f"🗨️ {str(thread_id)[:8]}..."):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []
        for msg in messages:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages


# **************************************** Main UI ***********************************

st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🤖 LangGraph Chat Assistant</h2>", unsafe_allow_html=True)

# Show conversation history with styled full-width chat bubbles
for message in st.session_state['message_history']:
    if message['role'] == "user":
        st.markdown(
            f"""
            <div style='width: 100%; background-color: #DCF8C6; 
            color: black; padding: 12px; border-radius: 10px; 
            margin: 5px 0;'>
                <b>You:</b> {message['content']}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='width: 100%; background-color: #F1F0F0; 
            color: black; padding: 12px; border-radius: 10px; 
            margin: 5px 0;'>
                <b>Bot:</b> {message['content']}
            </div>
            """,
            unsafe_allow_html=True
        )

# Input handler
user_input = st.chat_input('Type your message...')

if user_input:
    # Add user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    st.markdown(
        f"""
        <div style='width: 100%; background-color: #DCF8C6; 
        color: black; padding: 12px; border-radius: 10px; 
        margin: 5px 0;'>
            <b>You:</b> {user_input}
        </div>
        """,
        unsafe_allow_html=True
    )

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.spinner("🤔 Thinking..."):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

    # Bot reply bubble
    st.markdown(
        f"""
        <div style='width: 100%; background-color: #F1F0F0; 
        color: black; padding: 12px; border-radius: 10px; 
        margin: 5px 0;'>
            <b>Bot:</b> {ai_message}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
