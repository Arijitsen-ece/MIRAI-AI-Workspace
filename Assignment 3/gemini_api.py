"""
Handles Google Gemini API initialization and streaming interactions.
"""
import os
import google.generativeai as genai
from typing import List, Dict, Generator
from dotenv import load_dotenv

def init_api() -> bool:
    """Loads the API key from .env and configures the SDK."""
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
    Connects to Gemini, passes the unified history, and yields a streaming response.
    Gracefully catches and yields error messages without crashing.
    """
    if not init_api():
        yield "⚠️ **System Error:** `GEMINI_API_KEY` is missing from the environment. Please configure your `.env` file."
        return

    try:
        # Construct the model with current persona settings
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        )

        # Map generic message format to Gemini's expected format
        formatted_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg["content"]]})

        # Start the chat session
        chat = model.start_chat(history=formatted_history)
        
        # Stream the response
        response = chat.send_message(prompt, stream=True)

        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        error_msg = str(e).lower()
        if "quota" in error_msg or "rate limit" in error_msg:
            yield "⚠️ **API Error:** Rate limit or quota exceeded. Please try again later."
        elif "api key" in error_msg:
            yield "⚠️ **Authentication Error:** Invalid API Key provided."
        elif "network" in error_msg or "connection" in error_msg:
            yield "⚠️ **Network Error:** Failed to connect to Google servers."
        else:
            yield f"⚠️ **Unexpected Error:** {str(e)}"