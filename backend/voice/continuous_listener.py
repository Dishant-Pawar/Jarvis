import threading
import time
from voice.speech_to_text import SpeechToText
from voice.wakeword import WakeWordDetector
from utils.logger import get_logger

logger = get_logger()

class ContinuousListener:
    def __init__(self, command_callback, settings_manager):
        self.command_callback = command_callback
        self.settings_manager = settings_manager
        self.stt = SpeechToText()
        self.detector = WakeWordDetector()
        self.is_listening = False
        self.thread = None

    def _listen_loop(self):
        logger.info("Continuous wake word listener thread started.")
        while self.is_listening:
            try:
                # Load settings dynamically
                self.settings_manager.load_config()
                lang = self.settings_manager.get_setting("language_settings", {}).get("stt_lang", "en-US")
                
                # Listen briefly for wake word
                text = self.stt.listen_and_transcribe(timeout=2, phrase_time_limit=3, language=lang)
                if text:
                    logger.info(f"Listener heard: {text}")
                    if self.detector.check_wakeword(text):
                        logger.info("Wake word detected! Activating voice assistant pipeline...")
                        
                        # Call command handler callback with the text after wake word
                        cleaned_command = self._clean_command(text)
                        self.command_callback(cleaned_command)
            except Exception as e:
                logger.error(f"Error in continuous listener loop: {e}")
                time.sleep(1)

    def _clean_command(self, text: str) -> str:
        text_lower = text.lower()
        wakewords = ["hey jarvis", "jarvis"]
        
        for ww in wakewords:
            if text_lower.startswith(ww):
                # Return the string after the wake word
                return text[len(ww):].strip()
                
        return text

    def start(self):
        if self.is_listening:
            return
        self.is_listening = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        logger.info("Continuous listener started.")

    def stop(self):
        self.is_listening = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("Continuous listener stopped.")
