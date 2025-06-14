import json
import os

def get_event_roi(event_name):
    json_path = os.path.join("data", "events", "events.json")
    with open(json_path, "r") as f:
        data = json.load(f)

    if event_name not in data:
        raise ValueError(f"ROI for event '{event_name}' not found in events.json")

    return tuple(map(int, data[event_name]))
