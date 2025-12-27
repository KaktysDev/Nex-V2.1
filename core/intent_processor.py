# core/intent_processor.py
import json
from groq import Groq
from config.settings import GROQ_API_KEY, DEBUG

class IntentProcessor:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.system_prompt = """You are Nex's intent extraction agent. Return ONLY a JSON object with this exact format:
{
  "intent": "weather|time|date|reminder_set|reminder_list|timer|joke|search|open_site|play_music|define|calculate|system_control|small_talk|unknown",
  "slots": {"city": "...", "query": "...", "song": "...", "word": "...", "expr": "...", "amount": "...", "unit": "...", "datetime": "...", "target": "..."}
}
Extract any slots from the user's message. Do not include any commentary or markdown."""
    
    def detect(self, text: str) -> dict:
        """Detect intent using Groq with robust fallback"""
        if not text:
            return {"intent": "unknown", "slots": {}}
        
        try:
            # Try Groq first
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text}
                ],
                max_tokens=150,
                temperature=0.1,
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean up response (remove markdown if present)
            content = content.replace("```json", "").replace("```", "").strip()
            
            parsed = json.loads(content)
            
            # Validate structure
            if "intent" in parsed and "slots" in parsed:
                if DEBUG:
                    print(f"[IntentProcessor] Detected: {parsed}")
                return parsed
            
        except json.JSONDecodeError as e:
            if DEBUG:
                print(f"[IntentProcessor] JSON parse error: {e}")
                print(f"[IntentProcessor] Raw content: {content}")
        except Exception as e:
            if DEBUG:
                print(f"[IntentProcessor] Groq error: {e}")
        
        # Fallback to keyword matching
        if DEBUG:
            print("[IntentProcessor] Falling back to keywords")
        return self._keyword_fallback(text)
    
    def _keyword_fallback(self, text: str) -> dict:
        """Simple keyword-based intent detection"""
        t = text.lower()
        
        # Weather
        if any(word in t for word in ["weather", "temperature", "temp", "forecast", "rain", "snow"]):
            city = self._extract_after(t, "in")
            return {"intent": "weather", "slots": {"city": city}}
        
        # Time
        if any(word in t for word in ["time", "what time", "clock"]):
            return {"intent": "time", "slots": {}}
        
        # Date
        if any(word in t for word in ["date", "what day", "today", "day is it"]):
            return {"intent": "date", "slots": {}}
        
        # Joke
        if "joke" in t:
            return {"intent": "joke", "slots": {}}
        
        # Search
        if any(word in t for word in ["search", "look up", "find"]):
            query = text.replace("search", "").replace("look up", "").strip()
            return {"intent": "search", "slots": {"query": query}}
        
        # Open site
        if any(word in t for word in ["open", "go to"]):
            target = text.replace("open", "").replace("go to", "").strip()
            return {"intent": "open_site", "slots": {"target": target}}
        
        # Play music
        if any(word in t for word in ["play", "song", "music"]):
            song = text.replace("play", "").strip()
            return {"intent": "play_music", "slots": {"song": song}}
        
        # Define
        if any(word in t for word in ["define", "definition", "what does"]):
            word = text.replace("define", "").strip()
            return {"intent": "define", "slots": {"word": word}}
        
        # Calculate
        if any(char in t for char in ["+", "-", "*", "/"]) or "calculate" in t:
            expr = text.replace("calculate", "").strip()
            return {"intent": "calculate", "slots": {"expr": expr}}
        
        # Reminder
        if "remind" in t:
            return {"intent": "reminder_set", "slots": {}}
        
        # Timer
        if "timer" in t:
            return {"intent": "timer", "slots": {}}
        
        # Small talk
        if any(word in t for word in ["hello", "hi", "hey", "how are you"]):
            return {"intent": "small_talk", "slots": {}}
        
        return {"intent": "unknown", "slots": {}}
    
    def _extract_after(self, text: str, keyword: str) -> str:
        """Extract text after a keyword"""
        parts = text.split(keyword)
        if len(parts) > 1:
            return parts[1].strip()
        return ""