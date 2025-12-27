# core/event_bus.py
from typing import Callable, Dict, List
from threading import Lock
from enum import Enum

class EventType(Enum):
    VOICE_INPUT = "voice_input"
    CHAT_INPUT = "chat_input"
    INTENT_DETECTED = "intent_detected"
    ACTION_RESPONSE = "action_response"
    SPEAK_RESPONSE = "speak_response"
    CHAT_RESPONSE = "chat_response"

class Event:
    def __init__(self, event_type: EventType, data: dict, source: str = None):
        self.type = event_type
        self.data = data
        self.source = source

class EventBus:
    def __init__(self):
        self._listeners: Dict[EventType, List[Callable]] = {}
        self._lock = Lock()
    
    def subscribe(self, event_type: EventType, callback: Callable):
        with self._lock:
            if event_type not in self._listeners:
                self._listeners[event_type] = []
            self._listeners[event_type].append(callback)
    
    def publish(self, event: Event):
        with self._lock:
            listeners = self._listeners.get(event.type, []).copy()
        
        for callback in listeners:
            try:
                callback(event)
            except Exception as e:
                print(f"[EventBus] Error in callback {callback}: {e}")

# Global event bus instance
event_bus = EventBus()