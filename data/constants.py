import os

DEFAULT_EVENT_THRESHOLD = 0.9  # Default threshold for event detection
DEFAULT_EVENT_COOLDOWN = 1
INIT_COOLDOWN_VALUE = 9999  # Initial cooldown value for events

CLIP_DURATION = 10  # seconds
GAME_SEARCH_FRAME_STEP = 30  # Search every 30 frames

CONFIDENCE_PRECISION = 3  # Decimal places for confidence scores

GAME_EVENT_MIN = 30*60

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
# Folder paths
CROPS_DIR =     os.path.join("data", "events", "crops")
EXTRACTS_DIR =  os.path.join("data", "events", "extracts")
MASKS_DIR =     os.path.join("data", "events", "masks")

TEMPLATES_UNIQUE_DIR = os.path.join("data", "events", "templates", "unique")
TEMPLATES_SWITCH_DIR = os.path.join("data", "events", "templates", "switch")

FSM_DIR =       os.path.join("data", "fsm")

LOGS_DIR =      os.path.join("data", "logs")

RAW_VIDEO_DIR = os.path.join("data","raw_videos")

OUT_DF_DIR =    os.path.join("data","out","dataframes")

CLIPS_DIR =  os.path.join("data","out","clips")

# File paths
EVENTS_JSON_PATH = os.path.join("data","events","events.json")


"""
Which custom extract file for which event

default: sgt, src, brc

batch_01: ag, death, defeat, loadout, match_end, main_menu, podium, spawn_troop, splash, vaincu, desktop

batch_02: game_menu, victory, respawn, quit, scoreboard

batch_03 (2025-06-15 15-39-57): "assault", "heavy", "officer", "sniper", "aerial", "executor", "commando", "win"
"""
