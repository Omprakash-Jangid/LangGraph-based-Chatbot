# 🤖 LangGraph Chatbot

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.49.0-orange)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A **stateful chatbot** powered by **Google Gemini LLM** and **LangGraph**, designed to demonstrate tool-augmented, multi-turn conversational AI with persistent context.  
The project includes a backend built with LangGraph and SQLite checkpointing, and an optional Streamlit UI for interactive chat.

---

## 🌟 Features

- **Stateful conversations** — each thread is tracked and restorable across sessions.  
- **Tool-augmented reasoning** — includes web search, calculator, and stock price tools.  
- **LangGraph orchestration** — manages chat and tool nodes with conditional transitions.  
- **SQLite checkpointing** — persists chat state and tool execution history.  
- **Gemini-2.5-Flash-Lite integration** via `langchain-google-genai`.  
- **Environment variable security** through `.env`.  
- Modular and easily extensible structure.

---

## 🗂 Project Structure

```text
LangGraph_Chatbot/
├── backend/
│   └── langgraph_database_backend.py
├── frontend/
│   └── chatbot_ui.py
├── assets/
│   └── chatbot_ui_screenshot.png
├── .env     # API keys and environment variables
├── .gitignore
├── requirements.txt
└── README.md
```
## 🧠 Tools Integrated

| 🧩 Tool Name | ⚙️ Description |
|--------------|----------------|
| **DuckDuckGo Search** | Fetches real-time web results using the DuckDuckGo API. |
| **Calculator** | Performs arithmetic operations — addition, subtraction, multiplication, and division. |
| **Stock Price Fetcher** | Retrieves live stock market data using the Alpha Vantage API. |

---

## 🧰 Tech Stack

| 🧱 Component | 📝 Description |
|--------------|----------------|
| **Python 3.10+** | Core programming language used. |
| **LangGraph** | For graph-based LLM orchestration and managing chat flow. |
| **LangChain** | Framework connecting tools, LLMs, and chains together. |
| **Google Gemini API** | LLM powering the chatbot’s reasoning and responses. |
| **SQLite** | Local database for checkpointing conversation state. |
| **dotenv** | Secure management of API keys and environment variables. |
| **Requests** | Used for making external API calls to fetch live data. |

---

## 🖼 User Interface

Here’s how the LangGraph Chatbot looks in action:

<p align="center">
  <img src="assets/chatbot_ui_screenshot.png" alt="Chatbot UI" width="600"/>
</p>

> Full-width chat bubbles for user and bot messages, with a sidebar to manage multiple chat threads.

---

## ⚙️ Setup Instructions

```bash
1. **Clone the repository**
git clone https://github.com/yourusername/LangGraph_Chatbot.git
cd LangGraph_Chatbot

2. **Create and activate a virtual environment**
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

3. **Install dependencies**
pip install -r requirements.txt

4. **Add your Google API key**
Create a .env file in the project root:
GOOGLE_API_KEY=your_google_api_key_here

5. **Run the frontend UI**
streamlit run frontend/chatbot_ui.py
```

---

## 🚀 Future Enhancements

- [ ] Add **user authentication** and personalized chat sessions.  
- [ ] Integrate **multiple LLM providers** (OpenAI, Anthropic Claude).  
- [ ] Implement **logging and analytics dashboard** for insights.  
- [ ] Add **export to PDF/Markdown** feature for chat history.  

---

## 🪪 License

This project is licensed under the **MIT License**.  
You are free to **use, modify, and distribute** the code with proper attribution.
