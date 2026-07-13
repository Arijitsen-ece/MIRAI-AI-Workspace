"""
Helper functions for token estimation, word counts, and chat exports.
"""
import json
from typing import List, Dict

def estimate_tokens(text: str) -> int:
    """Estimates tokens based on the character count / 4 rule."""
    if not text:
        return 0
    return len(text) // 4

def count_words(text: str) -> int:
    """Counts the number of words in a text string."""
    if not text:
        return 0
    return len(text.split())

def count_characters(text: str) -> int:
    """Counts the total characters in a text string."""
    if not text:
        return 0
    return len(text)

def export_chat_txt(chat_history: List[Dict]) -> str:
    """Formats chat history into a plain text string."""
    lines = []
    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "AI"
        lines.append(f"{role}:\n{msg['content']}\n")
    return "\n".join(lines)

def export_chat_md(chat_history: List[Dict]) -> str:
    """Formats chat history into a Markdown string."""
    lines = ["# AI Multiverse - Chat Export\n"]
    for msg in chat_history:
        role = "**User**" if msg["role"] == "user" else "**AI**"
        lines.append(f"{role}:\n\n{msg['content']}\n\n---\n")
    return "\n".join(lines)

def export_chat_json(chat_history: List[Dict]) -> str:
    """Formats chat history into a JSON string."""
    return json.dumps(chat_history, indent=4)