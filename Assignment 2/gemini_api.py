"""
Handles Google Gemini API initialization and stream generation.
"""
import os
import google.generativeai as genai
from typing import List, Dict, Generator
from dotenv import load_dotenv

def init_api() -> bool:
    """Loads the environment variables and configures the API key."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True

def generate_chat_stream(
    prompt: str, 
    history: List[Dict], 
    system_instruction: str, 
    temperature: float, 
    max_tokens: int
) -> Generator[str, None, None]:
    """
    Connects to the Gemini API and yields the response as a stream.
    Safely handles exceptions and rate limits.
    """
    if not init_api():
        yield "⚠️ **Error:** `GEMINI_API_KEY` not found. Please add it to your `.env` file."
        return

    try:
        # Initialize model with persona parameters
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        )

        # Format history for Gemini (Requires strictly alternating user/model roles)
        formatted_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg["content"]]})

        # Start chat and stream response
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(prompt, stream=True)

        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        error_msg = str(e).lower()
        if "quota" in error_msg or "rate" in error_msg:
            yield "⚠️ **Error:** API Rate limit or quota exceeded. Please wait a moment and try again."
        elif "api key" in error_msg:
            yield "⚠️ **Error:** Invalid API Key provided."
        elif "network" in error_msg or "connection" in error_msg:
            yield "⚠️ **Error:** Network connection failed. Please check your internet."
        else:
            yield f"⚠️ **Unexpected Error:** {str(e)}"