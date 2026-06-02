import pyttsx3
import threading
from utils.logger import get_logger

logger = get_logger()

class TextToSpeech:
    def __init__(self, rate: int = 180, volume: float = 1.0, voice_id: str = None):
        self.rate = rate
        self.volume = volume
        self.voice_id = voice_id
        self._engine_lock = threading.Lock()

    def speak(self, text: str):
        """
        Speaks text in a background thread to prevent blocking the main process loop.
        """
        def speak_thread():
            import pythoncom
            pythoncom.CoInitialize()
            with self._engine_lock:
                try:
                    engine = pyttsx3.init()
                    engine.setProperty("rate", self.rate)
                    engine.setProperty("volume", self.volume)
                    
                    if self.voice_id:
                        engine.setProperty("voice", self.voice_id)
                    
                    engine.say(text)
                    engine.runAndWait()
                    # Clean up engine resources
                    del engine
                except Exception as e:
                    logger.error(f"Error executing pyttsx3 text-to-speech: {e}")
                finally:
                    pythoncom.CoUninitialize()

        thread = threading.Thread(target=speak_thread)
        thread.start()

    def get_available_voices(self):
        voices_list = []
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty("voices")
            for voice in voices:
                voices_list.append({
                    "id": voice.id,
                    "name": voice.name,
                    "languages": voice.languages,
                    "gender": voice.gender
                })
            del engine
        except Exception as e:
            logger.error(f"Failed to get pyttsx3 voices: {e}")
        return voices_list
