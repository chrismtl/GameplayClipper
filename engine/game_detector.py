import os
import cv2
import json
from data.constants import EVENTS_JSON_PATH, GAME_SEARCH_FRAME_STEP, FULL_GAME_NAME
from matchers.matcher_registry import MATCH_FUNCTIONS
from tools.frame_extractor import iterate_video

def detect_game_from_video(video_path):
    """
    Detect the game from the video filename by searching for *_splash templates.

    Args:
        video_path (str): Path to the video file.

    Returns:
        str: Game identifier (e.g., "bf2", "fn").
    """
    video_file_name = os.path.basename(video_path)
    if not video_file_name.endswith(".mp4"):
        raise ValueError("❌ Video file must be .mp4")
    video_file_name = video_file_name[:-4]  # Remove .mp4 extension
    
    # Load splash events from event definitions
    with open(EVENTS_JSON_PATH, "r") as f:
        event_defs = json.load(f)

    splash_events = {
        name: data for name, data in event_defs.items()
        if name.endswith("_splash")
    }

    if not splash_events:
        raise ValueError("No splash events defined in event JSON.")

    detected_games = set()
    for frame_id, frame, _ in iterate_video(video_path):
        if frame_id % GAME_SEARCH_FRAME_STEP: continue

        for name, data in splash_events.items():
            roi = data["roi"]
            match_fn = MATCH_FUNCTIONS.get(data["match"])
            threshold = data.get("threshold", 0.95)

            if match_fn is None:
                continue

            x1, y1, x2, y2 = roi
            crop = frame[y1:y2, x1:x2]
            matched, score = match_fn(crop, name, video_file_name, threshold)
            if matched:
                matched_game_name = name.split("_")[0]
                detected_games.add(matched_game_name)

        if len(detected_games) > 1:
            raise ValueError(f"Multiple splash screens detected in the same frame: {detected_games}")
        elif len(detected_games) == 1:
            game_name = detected_games.pop()
            print(f"✅ Game detected: {FULL_GAME_NAME.get(game_name, game_name)}")
            return game_name, frame_id

    raise ValueError("❌ No game splash screen detected in video.")
