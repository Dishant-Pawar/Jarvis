from ai.openrouter_client import OpenRouterClient

class ChatGPTConnector:
    def __init__(self, api_key: str):
        self.client = OpenRouterClient(api_key)

    def query(self, prompt: str, history: list = None) -> str:
        return self.client.query(prompt, history)
