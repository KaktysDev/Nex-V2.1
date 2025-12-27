# services/speech_service.py
import os
import time
import threading
import contextlib
import io
from typing import Optional
import speech_recognition as sr
from gtts import gTTS
import pygame
from config.settings import AUDIO_TEMP_FILE, DEBUG, WAKE_WORDS

class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_speaking = threading.Event()
        self.is_speaking.set()  # Start ready to speak
        self._shutdown = threading.Event()
        
    def initialize(self):
        """Initialize audio system"""
        with contextlib.redirect_stdout(io.StringIO()):
            pygame.mixer.init()
    
    def speak(self, text: str, block: bool = True):
        """Text-to-Speech with thread safety"""
        if not text or self._shutdown.is_set():
            return
        
        # Wait for any current speech to finish
        self.is_speaking.wait()
        self.is_speaking.clear()
        
        try:
            tts = gTTS(text=str(text), lang="en")
            tts.save(AUDIO_TEMP_FILE)
            
            pygame.mixer.music.load(AUDIO_TEMP_FILE)
            pygame.mixer.music.play()
            
            if block:
                while pygame.mixer.music.get_busy() and not self._shutdown.is_set():
                    time.sleep(0.1)
            
            # Cleanup in background
            threading.Thread(target=self._cleanup_audio, daemon=True).start()
            
        except Exception as e:
            print(f"[SpeechService] TTS error: {e}")
        finally:
            self.is_speaking.set()
    
    def _cleanup_audio(self):
        """Clean up audio file after delay"""
        time.sleep(0.3)
        try:
            if os.path.exists(AUDIO_TEMP_FILE):
                os.remove(AUDIO_TEMP_FILE)
        except Exception:
            pass
    
    def listen(self, timeout: Optional[int] = 5, phrase_time_limit: int = 8) -> str:
        """Speech-to-Text"""
        if self._shutdown.is_set():
            return ""
        
        with sr.Microphone() as source:
            if DEBUG:
                print("[SpeechService] Listening...")
            
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            except sr.WaitTimeoutError:
                return ""
            
            try:
                text = self.recognizer.recognize_google(audio)
                if DEBUG:
                    print(f"[SpeechService] Recognized: {text}")
                return text.lower()
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return ""
    
    def extract_after_wake(self, text: str) -> Optional[str]:
        """Extract command after wake word"""
        if not text:
            return None
        
        text_lower = text.lower()
        words = text_lower.split()
        
        if DEBUG:
            print(f"[SpeechService] Checking wake words in: {words}")
        
        for i, w in enumerate(words):
            if w.strip() in WAKE_WORDS:
                if i == len(words) - 1:
                    return ""  # Just wake word, no command
                return " ".join(words[i+1:]).strip()
        
        return None  # No wake word found
    
    def shutdown(self):
        """Graceful shutdown"""
        self._shutdown.set()
        self.is_speaking.set()
        pygame.mixer.quit()