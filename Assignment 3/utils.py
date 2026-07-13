"""
Helper utilities for metrics calculation and data export.
"""
import json
from typing import List, Dict

def estimate_tokens(text: str) -> int:
    """Estimates tokens using a standard 4 characters per token ratio."""
    if not text:
        return 0
    return max(1, len(text) // 4)

def count_words(text: str) -> int:
    """Calculates the word count of a given string."""
    if not text:
        return 0
    return len(text.split())

def count_characters(text: str) -> int:
    """Calculates the character count of a given string."""
    if not text:
        return 0
    return len(text)

def export_chat_txt(messages: List[Dict]) -> str:
    """Exports the chat history to a plain text format."""
    lines = []
    for msg in messages:
        role = "User" if msg["role"] == "user" else "AI"
        lines.append(f"[{role}]:\n{msg['content']}\n")
    return "\n".join(lines)

def export_chat_md(messages: List[Dict]) -> str:
    """Exports the chat history to a Markdown format."""
    lines = ["# AI Multiverse - Memory Vault Export\n"]
    for msg in messages:
        role = "**🧑‍💻 User**" if msg["role"] == "user" else "**🤖 AI Assistant**"
        lines.append(f"{role}:\n\n{msg['content']}\n\n---\n")
    return "\n".join(lines)

def export_chat_json(messages: List[Dict]) -> str:
    """Exports the chat history to a JSON string."""
    return json.dumps(messages, indent=4)