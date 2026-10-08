"""Chatbot logic: prompt building and communication with the AI API."""
from typing import Iterator

import openai
from openai import OpenAI

import config


class ChatbotError(Exception):
    """An error whose message is safe and friendly to show to the user."""


def build_system_prompt(mode: str) -> str:
    """Combine the base persona with the instructions of the chosen mode."""
    mode_text = config.RESPONSE_MODES.get(mode, config.RESPONSE_MODES["Simple"])
    return f"{config.BASE_PROMPT}\n\n{mode_text}"


def build_tool_prompt(tool_key: str, user_text: str) -> str:
    """Wrap the user's text in the instruction for a quick tool."""
    template = config.TOOLS[tool_key][2]
    return template.format(text=user_text)


def _friendly_message(exc: Exception) -> str:
    """Translate API exceptions into messages for students."""
    if isinstance(exc, openai.AuthenticationError):
        return "🔑 The API key looks invalid. Please check `OPENAI_API_KEY` in your `.env` file."
    if isinstance(exc, openai.RateLimitError):
        return "⏳ Rate limit or quota reached. Please wait a moment (or check your plan) and try again."
    if isinstance(exc, openai.APIConnectionError):  # includes timeouts
        return "🌐 Could not reach the AI service. Please check your internet connection and try again."
    if isinstance(exc, openai.NotFoundError):
        return f"🤖 The model `{config.MODEL}` was not found. Check `OPENAI_MODEL` in your `.env` file."
    return (
        "⚠️ Something went wrong while contacting the AI service.\n\n"
        "Please check your API configuration and try again."
    )


def stream_reply(history: list[dict], mode: str) -> Iterator[str]:
    """Yield the assistant's reply in chunks.

    `history` is a list of {"role": ..., "content": ...} dicts (the
    conversation so far, ending with the newest user message).
    Raises ChatbotError with a friendly message on any failure.
    """
    api_key = config.get_api_key()
    if not api_key:
        raise ChatbotError(
            "🔑 No API key found. Copy `.env.example` to `.env`, add your "
            "`OPENAI_API_KEY`, then restart the app."
        )

    # Keep only recent turns, and never start the list with an assistant turn.
    recent = history[-config.MAX_HISTORY_MESSAGES:]
    while recent and recent[0]["role"] != "user":
        recent = recent[1:]
    messages = [{"role": "system", "content": build_system_prompt(mode)}, *recent]

    try:
        client = OpenAI(api_key=api_key, base_url=config.BASE_URL, timeout=60)
        stream = client.chat.completions.create(
            model=config.MODEL, messages=messages, stream=True, temperature=0.4
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except openai.OpenAIError as exc:
        raise ChatbotError(_friendly_message(exc)) from exc
    except Exception as exc:  # never show a raw traceback to the user
        raise ChatbotError(_friendly_message(exc)) from exc
