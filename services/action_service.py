# services/action_service.py
import os
import threading
from datetime import datetime, timedelta
import json
from config.settings import REMINDERS_FILE, OPENWEATHER_API_KEY, DEBUG
from services.weather_service import WeatherService
from services.web_service import WebService
from services.reminder_service import ReminderService
from services.system_service import SystemService

class ActionService:
    def __init__(self):
        self.weather_service = WeatherService(OPENWEATHER_API_KEY)
        self.web_service = WebService()
        self.reminder_service = ReminderService(REMINDERS_FILE)
        self.system_service = SystemService()
        
        # Action registry
        self.actions = {
            "weather": self.weather_service.get_weather,
            "time": self._get_time,
            "date": self._get_date,
            "joke": self.web_service.get_joke,
            "search": self.web_service.search,
            "open_site": self.web_service.open_site,
            "play_music": self.web_service.play_music,
            "define": self.web_service.define_word,
            "calculate": self._calculate,
            "reminder_set": self.reminder_service.set_reminder,
            "reminder_list": self.reminder_service.list_reminders,
            "timer": self.reminder_service.set_timer,
            "system_control": self.system_service.control,
            "small_talk": self._small_talk,
        }
    
    def execute(self, intent_data: dict, source: str = "unknown") -> str:
        """Execute action based on intent"""
        intent = intent_data.get("intent", "unknown")
        slots = intent_data.get("slots", {})
        
        if DEBUG:
            print(f"[ActionService] Executing {intent} with slots: {slots}")
        
        action = self.actions.get(intent)
        if not action:
            return "I don't know how to answer that, but I'm here."
        
        try:
            result = action(slots, source=source)
            return result or "Action completed."
        except Exception as e:
            if DEBUG:
                print(f"[ActionService] Error executing {intent}: {e}")
            return f"Sorry, I had trouble with that: {str(e)}"
    
    def _get_time(self, slots: dict, **kwargs) -> str:
        now = datetime.now().strftime("%I:%M %p")
        return f"The time is {now}"
    
    def _get_date(self, slots: dict, **kwargs) -> str:
        today = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}"
    
    def _calculate(self, slots: dict, **kwargs) -> str:
        expr = slots.get("expr", "")
        if not expr:
            return "What should I calculate?"
        
        # Simple evaluation (use with caution - production should use safer methods)
        try:
            # Replace words with operators
            expr = expr.replace("times", "*").replace("x", "*").replace("plus", "+")
            result = eval(expr, {"__builtins__": {}}, {})
            return f"The answer is {result}"
        except:
            return "I couldn't calculate that."
    
    def _small_talk(self, slots: dict, **kwargs) -> str:
        text = slots.get("text", "").lower()
        
        if any(word in text for word in ["hello", "hi", "hey"]):
            return "Hello! How can I help you?"
        elif "how are you" in text:
            return "I'm a program — always ready to assist!"
        return "I don't know how to answer that, but I'm here."