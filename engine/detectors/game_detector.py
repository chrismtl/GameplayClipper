import os
import utils.constants as cst
from engine.matchers.matcher_registry import MATCH_FUNCTIONS
from tools.frame_extractor import iterate_video
import utils.json_cacher as js

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
    
    # Load starter events from each game folder
    starter_events = {}
    for game_name in os.listdir("data"):
        game_folder = os.path.join("data", game_name)
        starter_path = os.path.join(game_folder, "starter.json")

        starter_list = js.load(starter_path)
        event_path = os.path.join(game_folder, f"{game_name}_events.json")

        event_defs = js.load(event_path)
        for event_name in starter_list:
            event_name = f"{game_name}_{event_name}"
            if event_name in event_defs:
                starter_events[event_name] = event_defs[event_name]
            else:
                raise ValueError(f"❌ {event_name} is not an event for {game_name}")

    if not starter_events:
        raise ValueError("❌ No starter events found")

    detected_games = set()
    for frame_id, frame, _ in iterate_video(video_path, cst.GAME_SEARCH_FRAME_STEP):
        if frame_id > cst.GAME_EVENT_MIN:
            print(f"❌ No game detected within the first {cst.GAME_EVENT_MIN/30} frames.")
            return None, None

        for name, data in starter_events.items():
            roi = data["roi"]
            match_fn = MATCH_FUNCTIONS.get(data["match"])
            threshold = data.get("threshold", 0.95)

            if match_fn is None:
                continue

            x1, y1, x2, y2 = roi
            crop = frame[y1:y2, x1:x2]
            matched, _, _ = match_fn(crop, name, video_file_name, threshold)
            if matched:
                matched_game_name = name.split("_")[0]
                detected_games.add(matched_game_name)

        if len(detected_games) > 1:
            raise ValueError(f"Multiple splash screens detected in the same frame: {detected_games}")
        elif len(detected_games) == 1:
            game_name = detected_games.pop()
            print(f"✅ Game detected: {cst.FULL_GAME_NAME.get(game_name, game_name)}")
            return game_name, frame_id

    raise ValueError(f"❌ No game starter event detected in {video_file_name}.")
