import os

DEFAULT_EVENT_THRESHOLD = 0.9  # Default threshold for event detection
DEFAULT_EVENT_COOLDOWN = 1
INIT_COOLDOWN_VALUE = 9999  # Initial cooldown value for events

CLIP_DURATION = 10  # seconds
GAME_SEARCH_FRAME_STEP = 30  # Search every 30 frames

CONFIDENCE_PRECISION = 4  # Decimal places for confidence scores

GAME_EVENT_MIN = 10*60*30

MAX_EVENT_NAME_LEN = 12

# =============== DICTIONARIES ===============
FULL_GAME_NAME = {
    "bf2": "Star Wars Battlefront II",
    "fn": "Fortnite",
    "lol": "League of Legends",
    "r6": "Rainbow Six Siege",
    "valo": "Valorant"
}

# =============== PATHS ===============
LOGS_DIR = os.path.join("generated", "logs")

MEDIA_DIR = "media"

OUT_DF_DIR = os.path.join("generated","dataframes")

CLIPS_DIR = os.path.join("generated","clips")

CROPS_DIR = os.path.join("assets","crops")
TEMPLATES_SWITCH_DIR = os.path.join("assets","templates","switch")
TEMPLATES_UNIQUE_DIR = os.path.join("assets","templates","unique")
MASKS_DIR = os.path.join("assets","masks")

"""
Which custom extract file for which event

default: sgt, src, brc

batch_01: ag, death, defeat, loadout, match_end, main_menu, podium, spawn_troop, splash, vaincu, desktop

batch_02: game_menu, victory, respawn, quit, scoreboard

batch_03 (2025-06-15 15-39-57): "assault", "heavy", "officer", "sniper", "aerial", "executor", "commando", "win"
"""
