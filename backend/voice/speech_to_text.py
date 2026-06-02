import speech_recognition as sr
from utils.logger import get_logger

logger = get_logger()

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_and_transcribe(self, timeout: int = 4, phrase_time_limit: int = 5, language: str = "en-US") -> str:
        """
        Listens from the default microphone and transcribes speech using Google Speech Recognition.
        """
        with sr.Microphone() as source:
            logger.info("Calibrating microphone for ambient noise...")
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                logger.info("Microphone ready. Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
                logger.info("Transcribing speech...")
                text = self.recognizer.recognize_google(audio, language=language)
                logger.info(f"Transcribed Text: {text}")
                return text.strip()
            except sr.WaitTimeoutError:
                logger.info("Listening timed out. No speech detected.")
                return ""
            except sr.UnknownValueError:
                logger.info("Speech recognition could not understand audio.")
                return ""
            except sr.RequestError as e:
                logger.error(f"Could not request speech recognition results: {e}")
                return ""
            except Exception as e:
                logger.error(f"Unexpected error in speech recognition: {e}")
                return ""
                
    def voice_typing_stream(self, callback, language: str = "en-US"):
        """
        Listens continuously in a loop and calls callback(text) for live voice typing.
        """
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio, language=language)
                    if text:
                        callback(text)
                except (sr.WaitTimeoutError, sr.UnknownValueError):
                    continue
                except Exception as e:
                    logger.error(f"Voice typing error: {e}")
                    break
