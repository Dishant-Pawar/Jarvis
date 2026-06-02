from config.settings_manager import SettingsManager
from ai.memory_manager import MemoryManager
from ai.gemini_client import GeminiClient
from ai.openrouter_client import OpenRouterClient
from ai.grok_client import GrokClient
from utils.logger import get_logger

logger = get_logger()

class AssistantRouter:
    def __init__(self, settings_manager: SettingsManager, memory_manager: MemoryManager):
        self.settings_manager = settings_manager
        self.memory_manager = memory_manager

    def query_assistant(self, prompt: str) -> str:
        # Load latest configurations
        self.settings_manager.load_config()
        provider = self.settings_manager.get_setting("default_provider", "gemini").lower()
        api_key = self.settings_manager.get_api_key(provider)

        logger.info(f"Routing query to AI provider: {provider}")

        # Fetch conversation context history (limit to 10 messages for speed)
        history = self.memory_manager.get_history(limit=10)

        # Select corresponding client
        response_text = ""
        if provider == "gemini":
            client = GeminiClient(api_key)
            response_text = client.query(prompt, history)
        elif provider == "openrouter":
            client = OpenRouterClient(api_key)
            response_text = client.query(prompt, history)
        elif provider == "grok":
            client = GrokClient(api_key)
            response_text = client.query(prompt, history)
        else:
            response_text = f"Unknown AI provider '{provider}' selected in configuration settings."

        # Save to memory logs if the request succeeded or returned normal text
        if response_text and not response_text.startswith("Error") and not "API key is not configured" in response_text:
            self.memory_manager.save_message("user", prompt)
            self.memory_manager.save_message("assistant", response_text)

        return response_text
