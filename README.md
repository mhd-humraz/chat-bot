# 🤖 StudyBuddy AI

**Your Personal AI Study Assistant.** *Learn smarter. Understand faster. Prepare better.*

StudyBuddy AI is a Streamlit chatbot for college students. It explains concepts, makes study notes, builds quizzes and structures answers for exam revision, and it remembers the conversation so follow-up questions just work.

## ✨ Features

- 💬 Modern chat interface with streaming replies (`st.chat_message`, `st.chat_input`)
- 🧠 Conversation memory using Streamlit session state
- 🎯 Three response modes: **Simple**, **Detailed**, **Exam**
- 🧰 Quick tools: **Explain**, **Notes**, **Exam Prep**, **Quiz**, **Summarize**
- 🚀 Starter prompts on the landing screen (one click sends them)
- 🗑️ Clear chat button
- 🛡️ Friendly handling of missing/invalid keys, rate limits, network and API errors
- 🔐 API key kept in environment variables, never in source code

## 🛠️ Tech Stack

Python · Streamlit · OpenAI-compatible API (`openai` SDK) · `python-dotenv`

## 📸 Screenshots

> Add your own screenshots to `assets/` (for example `assets/demo.png`) and link them here:
>
> `![StudyBuddy AI](assets/demo.png)`

## 🏗️ Project Structure

```text
studybuddy-ai/
├── app.py            # Streamlit UI: sidebar, chat, landing screen
├── chatbot.py        # Prompt building, API call, streaming, error handling
├── config.py         # Settings, response modes, tools, starter prompts
├── requirements.txt
├── .env.example      # Template for your API key
├── .gitignore
├── assets/           # Put screenshots here
└── .streamlit/
    └── config.toml   # Theme
```

## 🚀 Installation

```bash
git clone <repository-url>
cd studybuddy-ai

python -m venv venv
```

Activate the environment.

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your `.env` file (copy `.env.example`) and add your key:

```env
OPENAI_API_KEY=your_api_key_here
```

Run:

```bash
streamlit run app.py
```

**Optional settings** in `.env`: `OPENAI_MODEL` (default `gpt-4o-mini`) and `OPENAI_BASE_URL` (to use any OpenAI-compatible provider).

## 🧠 How It Works

```text
User
 ↓
Streamlit UI
 ↓
Chatbot Logic
 ↓
AI Model
 ↓
Response
 ↓
Chat Interface
```

1. The UI collects the message and the selected mode (and an optional quick tool).
2. `chatbot.py` builds a system prompt = base persona + mode instructions, adds the recent chat history, and calls the API with streaming.
3. The reply streams into the chat and is saved in `st.session_state` for the next turn.

## 🎯 Approach

The project uses an **AI API-based chatbot** approach: it calls a hosted language model rather than training a model from scratch. The "intelligence" of the study features comes from prompt design. Modes and tools change the instructions sent to the same model.

## 💡 What Makes It Unique

- **Student-focused design**: built around studying, not just chatting
- **Exam Mode**: Definition → Key Points → Example → Exam Tip → Remember
- **Study tools**: notes, quizzes, summaries and exam prep in one click
- **Conversation memory**: follow-ups like "give me an example" work
- **Beginner-friendly explanations** by default

## 🧩 Challenges Faced

| Challenge | How it was solved |
|---|---|
| Managing conversation history | Stored in `st.session_state`; only the last 20 messages are sent; failed turns are excluded |
| Designing useful prompts | One base persona plus swappable mode instructions; tools wrap input in task templates |
| Handling API failures | All SDK errors are mapped to short friendly messages in one place (`chatbot.py`) |
| Keeping credentials secure | Key read from `.env`; `.env` is git-ignored; `.env.example` is committed instead |
| Clean chat interface | Native Streamlit chat components, a theme in `config.toml`, and only a few lines of CSS |

## 🚀 Future Improvements

- PDF/document Q&A
- RAG over course material
- Voice input
- Flashcard generation
- Better quiz generation (interactive, scored)
- User accounts
- Study progress tracking
- Multiple AI models

## 👨‍💻 Author

**Muhammed Humraz H**
