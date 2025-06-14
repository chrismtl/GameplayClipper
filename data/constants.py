from pathlib import Path

CLIP_DURATION = 10  # seconds

GAME_SEARCH_FRAME_STEP = 30  # Search every 30 frames

# =============== PATHS ===============
RAW_VIDEO_DIR = "data/raw_videos"
OUT_DATAFRAMES_DIR = "data/out/dataframes"
CLIPS_FOLDER = "data/out/clips"
EVENTS_JSON_PATH = Path("data/events/events.json")

# =============== DISPLAY NAME ===============
FULL_GAME_NAME = {
    "bf2": "Star Wars Battlefront II",
    "fn": "Fortnite",
    "lol": "League of Legends",
    "r6": "Rainbow Six Siege",
    "valo": "Valorant"
}