import requests
import json
from utils.logger import get_logger

logger = get_logger()

class GrokClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Default active x.ai grok model
        self.model = "grok-2"
        self.url = "https://api.x.ai/v1/chat/completions"

    def query(self, prompt: str, history: list = None) -> str:
        if not self.api_key:
            return "Grok API key is not configured. Please add it in settings."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Build messages payload
        messages = []
        if history:
            for item in history:
                messages.append({
                    "role": item["role"],
                    "content": item["content"]
                })
        
        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": self.model,
            "messages": messages
        }

        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                try:
                    text = result["choices"][0]["message"]["content"]
                    return text.strip()
                except (KeyError, IndexError) as e:
                    logger.error(f"Error parsing Grok response: {e}. Raw response: {result}")
                    return "Sorry, I could not parse the response from Grok."
            else:
                logger.error(f"Grok API returned status code {response.status_code}: {response.text}")
                return f"Grok API error (Status {response.status_code})."
        except Exception as e:
            logger.error(f"Exception querying Grok: {e}")
            return "Failed to connect to Grok service."
