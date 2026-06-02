import requests
import json
from utils.logger import get_logger

logger = get_logger()

class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "meta-llama/llama-3-8b-instruct:free"
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def query(self, prompt: str, history: list = None) -> str:
        if not self.api_key:
            return "OpenRouter API key is not configured. Please add it in settings."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Jarvis AI Assistant"
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
                    logger.error(f"Error parsing OpenRouter response: {e}. Raw response: {result}")
                    return "Sorry, I could not parse the response from OpenRouter."
            else:
                logger.error(f"OpenRouter API returned status code {response.status_code}: {response.text}")
                return f"OpenRouter API error (Status {response.status_code})."
        except Exception as e:
            logger.error(f"Exception querying OpenRouter: {e}")
            return "Failed to connect to OpenRouter service."
