# AI Multiverse — Memory Vault

> **Assignment 3 — The Memory Vault (Stateful Chatbot)**  
> **MirAI School of Technology | Virtual Summer Internship 2026 | AI Builder Track**

AI Multiverse — Memory Vault is a modern, stateful AI chatbot built with **Streamlit** and powered by **Google Gemini**. The application demonstrates persistent conversation memory using **`st.session_state`**, allowing users to continue natural conversations without losing context during Streamlit reruns.

---

## ✨ Highlights

- 🧠 **Stateful Conversation Memory** using `st.session_state`
- 🤖 **10 AI Personalities** with unique system prompts
- 💬 **Modern Chat Interface** using `st.chat_input()` and `st.chat_message()`
- ⚡ **Google Gemini API** integration with streaming responses
- 📊 **Live Conversation Metrics**
  - Response Time
  - Word Count
  - Character Count
  - Estimated Tokens
  - Message Counter
- 🔄 **Persistent Chat History** across Streamlit reruns
- 🔀 **Persona Switching** while preserving conversation history
- 📁 **Export Conversations** as TXT, Markdown, or JSON
- 🎨 **Cyber Aurora UI** with a modern glassmorphism design
- 🛡️ **Robust Error Handling** for API and network issues

---

## 🚀 Technologies Used

- Python 3.10+
- Streamlit
- Google Gemini API
- Google Generative AI SDK
- python-dotenv

---

## 🧠 Assignment Objective

This project upgrades a traditional stateless chatbot into a **stateful conversational assistant** by implementing Streamlit Session State.

The chatbot preserves conversation history, renders previous messages after every rerun, and delivers a seamless ChatGPT-style experience using Streamlit's native chat components.

---

## 🔐 Environment Variable

Create a `.env` file in the project root and add your Google Gemini API key.

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📸 Preview

Application preview is available in:

```
demo/memory-vault-preview.png
```

---

## 📌 Key Learning Outcomes

- Streamlit Session State
- Stateful Chat Applications
- ChatGPT-style User Interface
- Google Gemini API Integration
- Prompt Engineering
- Modular Python Development
- Conversation Memory Management

---

## 👨‍💻 Developer

**Arijit Sen**

B.Tech — Electronics & Communication Engineering (ECE)

MirAI School of Technology — AI Builder Internship 2026

---

## 📄 License

This project is developed for educational purposes as part of the **MirAI School of Technology AI Builder Internship 2026**.