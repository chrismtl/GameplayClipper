import os
import time
import glob
import shutil
import pandas as pd
from engine.detectors.game_detector import detect_game_from_video
from engine.matchers.matcher_registry import MATCH_FUNCTIONS
from engine.matchers.match_utils import reset_match_template_id
from tools.frame_extractor import iterate_video
import utils.json_cacher as js
import utils.constants as cst

def load_fsm_for_game(game_name, event_defs):
    """
    Load the FSM configuration for a given game name.

    Args:
        game_name (str): Game identifier (e.g., "bf2", "csgo")
        event_defs (dict): Dictionary of all event definitions

    Returns:
        dict: FSM dictionary mapping states to allowed events

    Raises:
        FileNotFoundError: If the FSM file does not exist.
        ValueError: If the FSM refers to unknown states or events (excluding 'start').
    """
    fsm_file = os.path.join("data", game_name, f"fsm_{game_name}.json")
    if not os.path.exists(fsm_file):
        raise FileNotFoundError(f"❌ FSM file not found for game '{game_name}' at {fsm_file}")

    fsm_dict = js.load(fsm_file)

    known_events = set(event_defs.keys())
    
    for state, transitions in fsm_dict.items():
        # Skip validation for pseudo-state 'start'
        if state == "start":
            pass
        elif f"{game_name}_{state}" in known_events:
            pass
        elif state.startswith("fsm_"):
            pass
        else:
            raise ValueError(f"❌ FSM state '{state}' is not a valid event name.")

        for target_event in transitions:
            if f"{game_name}_{target_event}" in known_events:
                pass
            elif target_event.startswith("fsm_"):
                pass
            else:
                raise ValueError(f"❌ FSM transition from '{state}' targets unknown event '{target_event}'.")

    return fsm_dict

def detect_all_videos():
    print("🔍 Detecting events in all videos...\n")
    
    all_events = []
    for video_path in glob.glob(os.path.join(cst.MEDIA_DIR, "*.mp4")):
        filename = os.path.splitext(os.path.basename(video_path))[0]
        print(f"🎞 Processing {filename}...")
        
        game_name, first_frame = detect_game_from_video(video_path)
        if game_name==None:
            print(f"❌ Skipping detection for {filename}: could not detect game")
        
        event_path = os.path.join("data", game_name, f"{game_name}_events.json")
        event_defs = js.load(event_path)
        
        fsm_dict = load_fsm_for_game(game_name, event_defs)
        event_df = detect_events(game_name, video_path, event_defs, fsm_dict, first_frame)
        all_events.append(event_df)

        save_events_to_csv(event_df, filename)

    if not all_events:
        print("⚠️ No events detected.")


def detect_single_video():
    filename = input("Enter mp4 video file name (e.g. recording_1): ").strip()
    path = os.path.join(cst.MEDIA_DIR, filename + ".mp4")

    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return

    print(f"🔍 Detecting events in {filename}...\n")
    game_name, first_frame = detect_game_from_video(path)
    if game_name==None:
        game_name = input("Could not detect game, please provide it: ")
        first_frame_input = input("First frame:").strip()
        first_frame =int(first_frame_input) if first_frame_input else cst.GAME_EVENT_MIN
    
    event_path = os.path.join("data", game_name, f"{game_name}_events.json")
    event_defs = js.load(event_path)
    
    fsm_dict = load_fsm_for_game(game_name, event_defs)
    events_df = detect_events(game_name, path, event_defs, fsm_dict, first_frame)
    if not events_df.empty:
        print(f"✅ {len(events_df)} events detected.")
        save_events_to_csv(events_df, filename)
    else:
        print("⚠️ No events detected.")


def detect_events(game_name, video_path, event_defs, fsm_dict, first_frame, first_state="start"):
    start_time = time.time()
    video_file_name = os.path.basename(video_path)
    if not video_file_name.endswith(".mp4"):
        raise ValueError("❌ Video file must be .mp4")
    video_file_name = video_file_name[:-4]  # Remove .mp4 extension
    
    print(f"Detecting events for {video_file_name}")
    all_events = []
    
    if fsm_dict is None:
        raise ValueError("FSM dictionary is required for event detection.")
    
    delete_log_folder()
    
    current_state = first_state
    prefix = f"{game_name}_"
    
    # Filter event_defs to only include events for the current game
    filtered_event_defs = {
        name[len(prefix):]: data
        for name, data in event_defs.items()
        if name.startswith(prefix)
    }
    
    fsincelast = {}
    has_min_frames = set()

    for event, data in filtered_event_defs.items(): 
        fsincelast[event] = data.get("min_frames", cst.INIT_COOLDOWN_VALUE)
        if "min_frames" in data:
            has_min_frames.add(event)

    # Cache relevant event data
    events_cache = {
        name: {
            "roi": data["roi"],
            "match_fn": MATCH_FUNCTIONS.get(data["match"]),
            "threshold": data.get("threshold", 0.9),
            "trigger_interval": data.get("trigger_interval", 0),
            "fcooldown": data.get("fcooldown", 0)
        }
        for name, data in filtered_event_defs.items()
    }
    
    for frame_id, frame, timestamp in iterate_video(video_path):
        if frame_id < first_frame: continue
        
        # Get allowed events for the current state
        allowed_events = fsm_dict.get(current_state, [])
        if not allowed_events:
            raise ValueError(f"⚠️ DEAD END: No allowed events at {timestamp} for state '{current_state}' ⚠️")
        
        allowed_events[:] = [
            sub
            for e in allowed_events
            for sub in (fsm_dict.get(e, []) if e.startswith("fsm_") else [e])
        ]
        
        for event_name in allowed_events:
            data = events_cache[event_name]
            trigger_interval = data.get("trigger_interval",0)
            fcooldown = data.get("fcooldown",cst.DEFAULT_EVENT_COOLDOWN)
            
            since_last = fsincelast[event_name]

            # Trigger interval logic
            if trigger_interval and frame_id%trigger_interval:
                continue
            
            # Cooldown logic
            elif fcooldown and since_last < fcooldown:
                fsincelast[event_name] = since_last + 1
                continue
            
            match_fn = data["match_fn"]
            threshold = data.get("threshold",cst.DEFAULT_EVENT_THRESHOLD)
            x1, y1, x2, y2 = data["roi"]
            
            if match_fn is None:
                print(f"⚠️ Matcher not found for '{event_name}'. Skipping...")
                continue
            
            frame_crop = frame[y1:y2, x1:x2]
            glob_event_name = f"{game_name}_{event_name}"
            matched, score, final_event_name = match_fn(frame_crop, glob_event_name, video_file_name, threshold)
            
            # Min frames logic
            if event_name in has_min_frames:
                if matched:
                    fsincelast[event_name] += 1
                else:
                    fsincelast[event_name] = 0
                
                if fsincelast[event_name] < filtered_event_defs[event_name]["min_frames"]:
                    continue
            
            if matched:
                print(f"✅ Detected {final_event_name:<{cst.MAX_EVENT_NAME_LEN}} at {timestamp} with score {score:.2f}")
                fsincelast[event_name] = 0
                current_state = event_name
                all_events.append({
                    "game": game_name,
                    "event": final_event_name,
                    "timestamp": timestamp,
                    "confidence": round(score, cst.CONFIDENCE_PRECISION),
                    "video": video_file_name
                })
    
    reset_match_template_id()  # Reset global counter after processing
    end_time = time.time()
    print(f"⏱️  Runtime for {video_file_name}: {end_time - start_time:.3f} seconds")
    return pd.DataFrame(all_events)

def prompt_event_selection(event_defs):
    print("Events to detect (press Enter to finish):")
    selected_events = []
    while True:
        raw = input("> ").strip()
        if not raw:
            break
        if raw in event_defs:
            print(f"✅")
            selected_events.append(raw)
        else:
            print(f"❌ Invalid event name, try again")
    return selected_events

def delete_log_folder():
    if os.path.exists(cst.LOGS_DIR):
        shutil.rmtree(cst.LOGS_DIR)
        print("🗑️  Deleting previous logs")

def save_events_to_csv(df, filename):
    """
    Save the DataFrame to a CSV file. If the file already exists, append (1), (2), etc.

    Args:
        df (pd.DataFrame): Events DataFrame to save.
        filename (str): Base filename (without extension).
    """
    os.makedirs(cst.OUT_DF_DIR, exist_ok=True)

    output_path = os.path.join(cst.OUT_DF_DIR, f"{filename}.csv")
    
    counter = 1
    while os.path.exists(output_path):
        output_path = os.path.join(cst.OUT_DF_DIR, f"{filename}_{counter}.csv")
        counter += 1

    df.to_csv(output_path, index=False)
    print(f"\n✅ Events saved to {output_path}")
