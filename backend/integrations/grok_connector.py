from ai.grok_client import GrokClient

class GrokConnector:
    def __init__(self, api_key: str):
        self.client = GrokClient(api_key)

    def query(self, prompt: str, history: list = None) -> str:
        return self.client.query(prompt, history)
