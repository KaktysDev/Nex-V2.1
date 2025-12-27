# core/coordinator.py
from core.event_bus import EventBus, Event, EventType
from core.intent_processor import IntentProcessor
from services.action_service import ActionService
from services.speech_service import SpeechService

class Coordinator:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.intent_processor = IntentProcessor()
        self.action_service = ActionService()
        self.speech_service = SpeechService()
        
        # Subscribe to events
        self.event_bus.subscribe(EventType.VOICE_INPUT, self._handle_voice_input)
        self.event_bus.subscribe(EventType.CHAT_INPUT, self._handle_chat_input)
        self.event_bus.subscribe(EventType.INTENT_DETECTED, self._handle_intent)
    
    def start(self):
        """Initialize services"""
        self.speech_service.initialize()
    
    def _handle_voice_input(self, event: Event):
        """Process voice input and trigger intent detection"""
        text = event.data.get("text", "")
        if not text:
            return
        
        intent_result = self.intent_processor.detect(text)
        self.event_bus.publish(Event(
            EventType.INTENT_DETECTED,
            {"intent": intent_result, "source": "voice", "original_text": text}
        ))
    
    def _handle_chat_input(self, event: Event):
        """Process chat input and trigger intent detection"""
        text = event.data.get("text", "")
        if not text:
            return
        
        intent_result = self.intent_processor.detect(text)
        self.event_bus.publish(Event(
            EventType.INTENT_DETECTED,
            {"intent": intent_result, "source": "chat", "original_text": text}
        ))
    
    def _handle_intent(self, event: Event):
        """Route intent to appropriate action"""
        intent_data = event.data.get("intent", {})
        source = event.data.get("source", "unknown")
        
        # Execute action
        response = self.action_service.execute(intent_data, source=source)
        
        # Publish response based on source
        if source == "voice":
            self.event_bus.publish(Event(
                EventType.SPEAK_RESPONSE,
                {"text": response, "original_text": event.data.get("original_text")}
            ))
        elif source == "chat":
            self.event_bus.publish(Event(
                EventType.CHAT_RESPONSE,
                {"text": response, "original_text": event.data.get("original_text")}
            ))