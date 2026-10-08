"""Central configuration: environment variables, modes, tools and prompts."""
import os

from dotenv import load_dotenv

load_dotenv()  # reads .env if present (never committed to git)

APP_TITLE = "StudyBuddy AI"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
BASE_URL = os.getenv("OPENAI_BASE_URL") or None  # for OpenAI-compatible providers
MAX_HISTORY_MESSAGES = 20  # keeps requests small and cheap

PLACEHOLDER_KEYS = {"", "your_api_key_here"}


def get_api_key() -> str:
    """Return the API key, or an empty string if it is missing/placeholder."""
    key = os.getenv("OPENAI_API_KEY", "").strip()
    return "" if key in PLACEHOLDER_KEYS else key


BASE_PROMPT = (
    "You are StudyBuddy AI, a helpful academic assistant designed for college "
    "students. Explain technical and academic topics clearly and accurately. "
    "Adapt your explanation according to the selected response mode. Avoid "
    "unnecessarily complicated language. Use examples whenever useful. If you "
    "are unsure about a fact, clearly state the uncertainty instead of "
    "inventing information. Use the earlier conversation to resolve follow-ups "
    "such as 'give me an example'."
)

# Response modes: name -> extra instructions appended to the system prompt
RESPONSE_MODES = {
    "Simple": (
        "MODE: Simple. Use beginner-friendly language and short sentences. "
        "Prefer everyday analogies. Keep answers brief (a short paragraph or "
        "a few bullets) and avoid jargon unless you define it."
    ),
    "Detailed": (
        "MODE: Detailed. Give a thorough answer with these sections: "
        "Explanation, Examples, Important Concepts, Practical Applications. "
        "Use Markdown headings and bullets."
    ),
    "Exam": (
        "MODE: Exam. Structure every answer exactly like this, in Markdown:\n"
        "📚 **Definition**\n\n🔑 **Key Points** (numbered list)\n\n"
        "📝 **Example**\n\n⭐ **Exam Tip**\n\n💡 **Remember** (one-line takeaway)\n"
        "Be precise and concise, as in a good revision sheet."
    ),
}

MODE_HELP = {
    "Simple": "Beginner-friendly, short answers",
    "Detailed": "Explanation, examples, applications",
    "Exam": "Definition, key points, tips",
}

# Quick tools: key -> (button label, icon, instruction template)
TOOLS = {
    "explain": (
        "Explain", "📚",
        "Explain this concept simply, as if to a first-year student, with one "
        "clear example:\n\n{text}",
    ),
    "notes": (
        "Notes", "📝",
        "Turn this topic into concise, well-organised study notes (headings, "
        "bullets, key terms in bold):\n\n{text}",
    ),
    "exam": (
        "Exam Prep", "🎯",
        "Prepare me for an exam on this topic. Cover likely questions, key "
        "points to memorise, common mistakes and a quick revision checklist:"
        "\n\n{text}",
    ),
    "quiz": (
        "Quiz", "❓",
        "Create a short 5-question multiple-choice quiz on this topic. Give "
        "four options (A-D) per question. Put the answer key with one-line "
        "explanations at the end, after a divider:\n\n{text}",
    ),
    "summarize": (
        "Summarize", "🔄",
        "Summarize the following text into a short summary followed by 3-5 "
        "key takeaways:\n\n{text}",
    ),
}

TOOL_PLACEHOLDERS = {
    "explain": "Which concept should I explain?",
    "notes": "Which topic should I make notes on?",
    "exam": "Which topic are you preparing for?",
    "quiz": "Which topic should the quiz cover?",
    "summarize": "Paste the text you want summarized...",
}

STARTER_PROMPTS = [
    ("📡 Explain OSI Model", "Explain the OSI model."),
    ("🧠 Learn Machine Learning", "Explain Machine Learning in simple terms."),
    ("🐍 Generate Python Notes", "Make concise study notes on Python basics."),
    (
        "🎯 Prepare me for an exam",
        "I have an exam coming up. Help me prepare. Ask me which subject and "
        "topics I need to cover.",
    ),
]
