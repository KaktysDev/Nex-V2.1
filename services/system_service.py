# services/system_service.py
import os

class SystemService:
    def control(self, slots: dict, **kwargs) -> str:
        target = slots.get("target", "") or ""
        t = target.lower().strip()
        
        if any(k in t for k in ("exit", "quit", "stop", "goodbye")):
            return "EXIT"
        
        if "calculator" in t:
            os.system("gnome-calculator &")
            return "Opening calculator."
        elif "terminal" in t or "console" in t:
            os.system("gnome-terminal &")
            return "Opening terminal."
        elif "code" in t or "vscode" in t:
            os.system("code &")
            return "Opening VS Code."
        else:
            return "I can't do that system action yet."