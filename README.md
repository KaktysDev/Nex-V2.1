# Nex-V2.1

Nex is your intelligent voice assistant that makes computer interaction effortless through natural voice commands and chat interface.
What Nex Does: 

Nex listens for your voice commands and helps you:

    Get instant information: Weather, time, definitions, calculations
    Control your system: Open apps, websites, perform searches
    Stay organized: Set reminders and timers
    Stay entertained: Tell jokes, play music

Key Features
  Voice Activation: Say "Hey Nex" followed by your command
  Chat Interface: Type commands in the GUI window
  Smart Understanding: Uses Groq AI to understand natural language
  Concurrent Operation: Voice and chat work simultaneously
  Extensible: Easy to add new commands and capabilities
  
Quick Start

Install dependencies:

    pip install groq speechrecognition gTTS pygame tk

Configure API keys in config/settings.py:


    GROQ_API_KEY = "your_groq_key_here" 
    OPENWEATHER_API_KEY = "your_weather_key_here"  # Optional 


Run Nex: 

    python main.py

Start talking: Say "Hey Nex" followed by commands like:

        "What's the weather in New York?"
        What's the time right now?
        "Tell me a joke"
        "Open YouTube"

Architecture:

Nex uses an event-driven architecture that cleanly separates concerns:

    Core: Event bus and coordinator for message passing
    Services: Speech recognition, LLM processing, action execution
    UI: Voice listener and chat window interfaces

Examples

Voice Commands:


"Hey Nex what's the weather"
"Hey Nex set a reminder for 3 PM"
"Hey Nex search for Python tutorials"
"Hey Nex what time is it"

Chat Commands:
Type the same commands without "Hey Nex" in the GUI window.
Requirements

    Python 3.8+
    Microphone for voice commands
    Internet connection for web services

License

MIT License - feel free to modify and extend Nex for your needs.
