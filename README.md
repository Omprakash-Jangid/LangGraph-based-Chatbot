# 🤖 LangGraph Chatbot

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.49.0-orange)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A **stateful chatbot** built using **Google Gemini LLM** with **LangGraph** for conversation state management.  
It uses a **Streamlit frontend** for interactive chat and a **backend** for handling AI responses, conversation state, and SQLite-based persistence.

---

## 🌟 Features

- **Stateful conversations**: Supports multiple chat threads and resumes previous sessions.  
- **Google Gemini LLM integration** via `langchain-google-genai`.  
- **SQLite database** stores chat threads persistently.  
- **Streamlit frontend**: Modern chat interface with styled message bubbles.  
- **Secure API management** using `.env` for environment variables.  
- Modular backend and frontend for easy extension.

---

## 🗂 Project Structure

