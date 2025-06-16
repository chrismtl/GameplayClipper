import os
import cv2
from matchers.match_utils import increment_match_template_id, save_match_log
import utils.image_cacher as imgc
import utils.json_cacher as js
import data.constants as cst

def match_switch(frame_crop, glob_event_name, video_file_name, threshold=0.95):
    """
    Match a frame crop against multiple switch templates.

    Args:
        frame_crop (np.ndarray): RGB cropped frame region.
        event_name (str): Event name (must contain a 'switches' list).
        video_file_name (str): Video name for logging.
        threshold (float): Match threshold (default: 0.95).

    Returns:
        matched (bool): True if any switch match exceeds threshold.
        score (float): Best match score.
        event_name (str): Name of the best-matching switch.
    """
    # Get event name without the game prefix
    event_name = glob_event_name.split("_", 1)[1]
    
    # Load event definition
    event_defs = js.load(cst.EVENTS_JSON_PATH)

    event_info = event_defs.get(glob_event_name, {})
    switches = event_info.get("switches", [])
    
    # Reading error handling
    if not event_info:
        raise ValueError(f"❌ Event '{event_name}' not found in events.json")
    if not switches:
        raise ValueError(f"❌ No 'switches' defined for event '{event_name}'")

    # HERE MATCH IS A TABLE NOT A BOOL
    matched = []

    # Convert frame to grayscale once
    frame_gray = cv2.cvtColor(frame_crop, cv2.COLOR_BGR2GRAY)

    for switch in switches:
        template_path = os.path.join(cst.TEMPLATES_SWITCH_DIR, glob_event_name, f"{switch}_template.png")
        template_gray = imgc.load(template_path, cv2.IMREAD_GRAYSCALE)

        if template_gray is None:
            raise FileNotFoundError(f"❌ Template not found for switch '{switch}'")

        if frame_gray.shape != template_gray.shape:
            raise ValueError(f"❌ Frame crop shape {frame_gray.shape} does not match template shape {template_gray.shape} for switch '{switch}'")

        result = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_SQDIFF_NORMED)
        min_val, _, _, _ = cv2.minMaxLoc(result)
        score = 1.0 - min_val

        if score >= threshold:
            matched.append((score, switch))
    
    if matched:
        if len(matched)!=1: raise ValueError(f"❌ Cross match for '{event_name}':{[name for _,name in matched]}")
    
        save_match_log(frame_crop, event_name, video_file_name)
        increment_match_template_id()

    # Debug
    # if matched: print(f"🔍 Switch match results for '{event_name}': {matched}")
    final_score = matched[0][0] if matched else 0.0
    final_switch = matched[0][1] if matched else None
    
    return matched, final_score, final_switch
