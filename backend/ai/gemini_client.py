import requests
import json
from utils.logger import get_logger

logger = get_logger()

class GeminiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Default modern fast model
        self.model = "gemini-2.5-flash"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

    def query(self, prompt: str, history: list = None) -> str:
        if not self.api_key:
            return "Gemini API key is not configured. Please add it in settings."

        headers = {
            "Content-Type": "application/json"
        }

        # Build contents array with conversation history
        contents = []
        if history:
            for item in history:
                role = "user" if item["role"] == "user" else "model"
                contents.append({
                    "role": role,
                    "parts": [{"text": item["content"]}]
                })
        
        # Add the current prompt
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        payload = {
            "contents": contents
        }

        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                try:
                    # Parse the standard response structure
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    return text.strip()
                except (KeyError, IndexError) as e:
                    logger.error(f"Error parsing Gemini response: {e}. Raw response: {result}")
                    return "Sorry, I could not parse the response from Gemini."
            else:
                logger.error(f"Gemini API returned status code {response.status_code}: {response.text}")
                return f"Gemini API error (Status {response.status_code})."
        except Exception as e:
            logger.error(f"Exception querying Gemini: {e}")
            return "Failed to connect to Gemini service."
