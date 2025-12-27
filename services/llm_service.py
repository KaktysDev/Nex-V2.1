# services/llm_service.py
from groq import Groq
from config.settings import GROQ_API_KEY, DEBUG
import json

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.system_prompt = """You are Nex's intent extraction agent. Return ONLY a JSON object with this exact format:
{
  "intent": "weather|time|date|reminder_set|reminder_list|timer|joke|search|open_site|play_music|define|calculate|system_control|small_talk|unknown",
  "slots": {"city": "...", "query": "...", "song": "...", "word": "...", "expr": "...", "amount": "...", "unit": "...", "datetime": "...", "target": "..."}
}
Extract any slots from the user's message. Do not include any commentary or markdown."""

    def extract_intent(self, text: str) -> dict:
        """Extract intent using Groq API"""
        if not text:
            return {"intent": "unknown", "slots": {}}
        
        try:
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
            content = content.replace("```json", "").replace("```", "").strip()
            
            parsed = json.loads(content)
            
            if "intent" in parsed and "slots" in parsed:
                if DEBUG:
                    print(f"[LLMService] Extracted intent: {parsed}")
                return parsed
                
        except json.JSONDecodeError as e:
            if DEBUG:
                print(f"[LLMService] JSON parse error: {e}")
        except Exception as e:
            if DEBUG:
                print(f"[LLMService] Groq error: {e}")
        
        return None  # Signal fallback needed