# services/reminder_service.py
import json
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

class ReminderService:
    def __init__(self, reminders_file: Path):
        self.reminders_file = reminders_file
        self.active_timers = []
    
    def set_reminder(self, slots: dict, **kwargs) -> str:
        text = slots.get("text")
        when = slots.get("datetime")
        
        if not text:
            return "What should I remind you about?"
        
        reminder = {
            "text": text,
            "when": when or datetime.now().isoformat(),
            "created": datetime.now().isoformat()
        }
        
        reminders = self._load_reminders()
        reminders.append(reminder)
        self._save_reminders(reminders)
        
        return f"Reminder set: {text}"
    
    def list_reminders(self, slots: dict, **kwargs) -> str:
        reminders = self._load_reminders()
        
        if not reminders:
            return "You have no reminders."
        
        lines = []
        for r in reminders:
            when = r.get("when", "")
            lines.append(f"- {r.get('text')} at {when}")
        
        return "\n".join(lines)
    
    def set_timer(self, slots: dict, **kwargs) -> str:
        try:
            amount = int(slots.get("amount", 0))
            unit = slots.get("unit", "seconds")
            label = slots.get("label", "Timer")
            
            if unit.startswith("min"):
                amount *= 60
            elif unit.startswith("hour"):
                amount *= 3600
            
            timer = threading.Timer(amount, self._timer_callback, args=[label])
            timer.daemon = True
            timer.start()
            self.active_timers.append(timer)
            
            return f"Timer set for {amount} seconds."
        except:
            return "Timer cancelled."
    
    def _timer_callback(self, label: str):
        from services.speech_service import SpeechService
        # Create temporary instance for TTS
        speech = SpeechService()
        speech.speak(f"{label} done.")
    
    def _load_reminders(self) -> List[Dict]:
        try:
            if self.reminders_file.exists():
                return json.loads(self.reminders_file.read_text())
        except:
            pass
        return []
    
    def _save_reminders(self, reminders: List[Dict]):
        try:
            self.reminders_file.write_text(json.dumps(reminders, indent=2, default=str))
        except Exception as e:
            print(f"Failed to save reminders: {e}")