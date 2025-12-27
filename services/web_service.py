# services/web_service.py
import webbrowser
import requests

class WebService:
    def search(self, slots: dict, **kwargs) -> str:
        query = slots.get("query")
        if not query:
            return "What should I search for?"
        
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return f"Searching for {query}"
    
    def open_site(self, slots: dict, **kwargs) -> str:
        target = slots.get("target", "")
        if not target:
            return "Which site should I open?"
        
        if "." in target or "http" in target:
            url = target if target.startswith("http") else f"https://{target}"
        else:
            if "gmail" in target:
                url = "https://mail.google.com"
            elif "youtube" in target:
                url = "https://www.youtube.com"
            else:
                url = f"https://{target}.com"
        
        webbrowser.open(url)
        return f"Opening {target}"
    
    def play_music(self, slots: dict, **kwargs) -> str:
        song = slots.get("song")
        if not song:
            return "What should I play?"
        
        webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
        return f"Playing {song}"
    
    def define_word(self, slots: dict, **kwargs) -> str:
        word = slots.get("word")
        if not word:
            return "Which word should I define?"
        
        try:
            response = requests.get(
                f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}",
                timeout=6
            ).json()
            meaning = response[0]["meanings"][0]["definitions"][0]["definition"]
            return meaning
        except:
            return "I couldn't find that definition."
    
    def get_joke(self, slots: dict, **kwargs) -> str:
        try:
            url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
            data = requests.get(url, timeout=6).json()
            
            if data.get("type") == "single":
                return data.get("joke")
            else:
                return f"{data.get('setup')} ... {data.get('delivery')}"
        except:
            return "I couldn't get a joke right now."