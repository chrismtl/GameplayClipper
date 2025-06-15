import os

DEFAULT_EVENT_THRESHOLD = 0.9  # Default threshold for event detection
INIT_COOLDOWN_VALUE = 9999  # Initial cooldown value for events

CLIP_DURATION = 10  # seconds
GAME_SEARCH_FRAME_STEP = 30  # Search every 30 frames

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
TEMPLATES_DIR = os.path.join("data", "events", "templates")

FSM_DIR =       os.path.join("data", "fsm")

LOGS_DIR =      os.path.join("data", "logs")

RAW_VIDEO_DIR = os.path.join("data","raw_videos")

OUT_DF_DIR =    os.path.join("data","out","dataframes")

CLIPS_DIR =  os.path.join("data","out","clips")

# File paths
EVENTS_JSON_PATH = os.path.join("data","events","events.json")