# ui/chat_window.py
import tkinter as tk
from core.event_bus import event_bus, Event, EventType

class ChatWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nex Chat")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Position window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - 420
        y = screen_height - 550
        self.root.geometry(f"+{x}+{y}")
        
        # Setup UI
        self._setup_ui()
        
        # Subscribe to chat responses
        event_bus.subscribe(EventType.CHAT_RESPONSE, self._display_response)
    
    def _setup_ui(self):
        """Setup chat interface"""
        self.chat_log = tk.Text(self.root, state="disabled", wrap="word", height=20)
        self.chat_log.pack(padx=10, pady=(10, 5), fill="both", expand=True)
        
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(padx=10, pady=(0, 10), fill="x", side="bottom")
        
        self.entry = tk.Entry(entry_frame, font=("Arial", 11))
        self.entry.pack(side="left", fill="x", expand=True)
        
        send_btn = tk.Button(entry_frame, text="Send", command=self._send_message)
        send_btn.pack(side="right", padx=(5, 0))
        
        self.entry.bind("<Return>", self._send_message)
    
    def _send_message(self, event=None):
        """Send chat message"""
        user_text = self.entry.get().strip()
        if not user_text:
            return
        
        self.entry.delete(0, "end")
        self._display_message("You", user_text)
        
        # Publish chat input event
        event_bus.publish(Event(
            EventType.CHAT_INPUT,
            {"text": user_text}
        ))
    
    def _display_message(self, sender: str, text: str):
        """Add message to chat log"""
        self.chat_log.config(state="normal")
        self.chat_log.insert("end", f"{sender}: {text}\n")
        self.chat_log.see("end")
        self.chat_log.config(state="disabled")
    
    def _display_response(self, event: Event):
        """Display assistant response"""
        text = event.data.get("text", "Sorry, I couldn't process that.")
        self._display_message("Nex", text)
    
    def run(self):
        """Start GUI event loop"""
        self.root.mainloop()
    
    def close(self):
        """Close window"""
        self.root.destroy()