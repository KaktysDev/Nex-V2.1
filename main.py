import sys
from core.coordinator import Coordinator
from core.event_bus import event_bus, Event, EventType
from ui.chat_window import ChatWindow
from ui.voice_listener import VoiceListener
from services.speech_service import SpeechService
from config.settings import DEBUG

class NexAssistant:
    def __init__(self):
        self.coordinator = Coordinator(event_bus)
        self.chat_window = ChatWindow()
        self.voice_listener = VoiceListener()
        self.speech_service = SpeechService()
        
        event_bus.subscribe(EventType.VOICE_INPUT, self._debug_voice)
        event_bus.subscribe(EventType.INTENT_DETECTED, self._debug_intent)
        event_bus.subscribe(EventType.SPEAK_RESPONSE, self._handle_speak)
        
        event_bus.subscribe(EventType.ACTION_RESPONSE, self._check_shutdown)
    
    def _debug_voice(self, event: Event):
        print(f"[DEBUG] Voice input received: {event.data}")
    
    def _debug_intent(self, event: Event):
        print(f"[DEBUG] Intent detected: {event.data}")
    
    def _handle_speak(self, event: Event):
        """Handle TTS responses"""
        text = event.data.get("text", "")
        print(f"[DEBUG] Speaking: {text}")
        self.speech_service.speak(text)
    
    def _check_shutdown(self, event: Event):
        """Check for shutdown command"""
        if event.data.get("text") == "EXIT":
            print("Shutting down Nex...")
            self.shutdown()
    
    def start(self):
        """Start the assistant"""
        print("Starting Nex Assistant...")
        
        self.coordinator.start()
        
        self.voice_listener.start()
        
        # Test audio system
        if DEBUG:
            print("[Main] Testing audio system...")
            self.speech_service.speak("Audio test successful")
        
        self.speech_service.speak("Nex is ready")
        
        print("[Main] System ready.")
        print("[Main]")
        
        self.chat_window.run()
    
    def shutdown(self):
        """shutdown"""
        self.voice_listener.stop()
        self.speech_service.shutdown()
        self.chat_window.close()
        sys.exit(0)

if __name__ == "__main__":
    assistant = NexAssistant()
    try:
        assistant.start()
    except KeyboardInterrupt:
        assistant.shutdown()
    except Exception as e:
        print(f"Fatal error: {e}")
        assistant.shutdown()
