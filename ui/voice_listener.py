# ui/voice_listener.py
import threading
import time
from core.event_bus import event_bus, Event, EventType
from services.speech_service import SpeechService
from config.settings import DEBUG, WAKE_WORDS

class VoiceListener:
    def __init__(self):
        self.speech_service = SpeechService()
        self.is_running = False
        self.thread = None
    
    def start(self):
        """Start voice listening thread"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("[VoiceListener] Voice listening started")
        
        # Test speech to confirm audio works
        self.speech_service.speak("Voice system initialized")
    
    def stop(self):
        """Stop voice listening"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1)
        print("[VoiceListener] Voice listening stopped")
    
    def _listen_loop(self):
        """Main voice listening loop"""
        while self.is_running:
            try:
                # Listen continuously for ANY speech
                if DEBUG:
                    print("[VoiceListener] Listening for speech...")
                
                audio = self.speech_service.listen(timeout=1, phrase_time_limit=5)
                if not audio:
                    continue
                
                if DEBUG:
                    print(f"[VoiceListener] Raw speech detected: {audio}")
                
                # Check for wake word in the detected speech
                command = self.speech_service.extract_after_wake(audio)
                
                if command is not None:
                    print(f"[VoiceListener] Wake word detected! Command: {command}")
                    
                    # Publish voice input event
                    event_bus.publish(Event(
                        EventType.VOICE_INPUT,
                        {"text": command}
                    ))
                    
                    # Small delay to prevent rapid firing
                    time.sleep(0.5)
                else:
                    if DEBUG:
                        print("[VoiceListener] No wake word found")
                
            except Exception as e:
                print(f"[VoiceListener] Error: {e}")
                time.sleep(1)