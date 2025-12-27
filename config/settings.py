# config/settings.py
import os
from pathlib import Path

# API Keys
GROQ_API_KEY = "<GROQ_API_KEY>"
OPENWEATHER_API_KEY = "<OPENWEATHER_API_KEY>"

# Audio Settings
AUDIO_TEMP_FILE = "temp_nex_audio.mp3"
WAKE_WORDS = {"nex", "next", "necks", "neks", "lex", "nacks", "neck", "nek"}

# Paths
BASE_DIR = Path(__file__).parent.parent
REMINDERS_FILE = BASE_DIR / "data" / "reminders.json"

# Create data directory
BASE_DIR.joinpath("data").mkdir(exist_ok=True)

# Debug Mode
DEBUG = True