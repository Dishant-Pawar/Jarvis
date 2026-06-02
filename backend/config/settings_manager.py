import os
import json

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

class SettingsManager:
    def __init__(self):
        self.config = {}
        self.load_config()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            # Create default config if missing
            self.config = {
                "openrouter_api_key": "",
                "grok_api_key": "",
                "gemini_api_key": "",
                "default_provider": "gemini",
                "voice_settings": {
                    "rate": 180,
                    "volume": 1.0,
                    "voice_id": ""
                },
                "language_settings": {
                    "stt_lang": "en-US",
                    "tts_lang": "en"
                },
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "smtp_email": "",
                "smtp_password": ""
            }
            self.save_config()
        else:
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception:
                self.config = {}

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception:
            return False

    def get_setting(self, key, default=None):
        return self.config.get(key, default)

    def set_setting(self, key, value):
        self.config[key] = value
        self.save_config()

    def get_api_key(self, provider):
        provider = provider.lower()
        if provider == "gemini":
            return self.config.get("gemini_api_key", "")
        elif provider == "openrouter":
            return self.config.get("openrouter_api_key", "")
        elif provider == "grok":
            return self.config.get("grok_api_key", "")
        return ""
