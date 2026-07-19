"""
Handles URL construction and API requests to the Pollinations AI Image service.
"""
import requests
import urllib.parse
import random
from typing import Optional, Tuple

def build_image_url(
    prompt: str, 
    style: str, 
    width: int, 
    height: int, 
    enhance: bool, 
    magic_prompt: str, 
    style_prompts: dict
) -> str:
    """
    Constructs the exact Pollinations API URL based on user parameters.
    """
    # Base prompt construction
    full_prompt = prompt.strip()
    
    # Append Magic Enhance if checked
    if enhance:
        full_prompt += f", {magic_prompt}"
        
    # Append Art Style modifiers
    if style in style_prompts:
        full_prompt += f", {style_prompts[style]}"
        
    # Encode prompt for URL safety
    encoded_prompt = urllib.parse.quote(full_prompt)
    
    # Generate random seed to ensure unique images for identical prompts
    seed = random.randint(1, 999999)
    
    # Construct final URL
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"
    
    return url

def fetch_image(url: str, timeout: int = 30) -> Tuple[bool, Optional[bytes], str]:
    """
    Fetches the image bytes from the generated URL safely.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return True, response.content, "Success"
        
    except requests.exceptions.Timeout:
        return False, None, "The request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return False, None, "Network error. Please check your internet connection."
    except requests.exceptions.RequestException as e:
        return False, None, f"API error occurred: {str(e)}"
    except Exception as e:
        return False, None, f"An unexpected error occurred: {str(e)}"