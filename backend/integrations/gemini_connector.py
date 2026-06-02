from ai.gemini_client import GeminiClient

class GeminiConnector:
    def __init__(self, api_key: str):
        self.client = GeminiClient(api_key)

    def query(self, prompt: str, history: list = None) -> str:
        return self.client.query(prompt, history)
