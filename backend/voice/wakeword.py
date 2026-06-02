class WakeWordDetector:
    def __init__(self, wakeword: str = "hey jarvis"):
        self.wakeword = wakeword.lower()

    def check_wakeword(self, text: str) -> bool:
        """
        Returns True if the transcribed text contains the wake word.
        """
        if not text:
            return False
        
        normalized_text = text.lower()
        # Accept minor variations or direct substring matches
        if self.wakeword in normalized_text or "jarvis" in normalized_text:
            return True
            
        return False
