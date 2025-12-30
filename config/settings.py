import os
from pathlib import Path

GROQ_API_KEY = "<GROQ_API_KEY>"
OPENWEATHER_API_KEY = "<OPENWEATHER_API_KEY>"

AUDIO_TEMP_FILE = "temp_nex_audio.mp3"
WAKE_WORDS = {"nex", "next", "necks", "neks", "lex", "nacks", "neck", "nek"}

BASE_DIR = Path(__file__).parent.parent
REMINDERS_FILE = BASE_DIR / "data" / "reminders.json"

BASE_DIR.joinpath("data").mkdir(exist_ok=True)

DEBUG = True
