import os
import cv2
import data.constants as cst

# Match template ID for logging
match_template_id = 1

def reset_match_template_id():
    global match_template_id
    match_template_id = 1
    
def increment_match_template_id():
    global match_template_id
    match_template_id += 1

# Save match log for successful matches
def save_match_log(frame_crop, event_name, video_file_name):
    os.makedirs(f"data/logs/{video_file_name}", exist_ok=True)
    log_path = os.path.join(cst.LOGS_DIR, video_file_name, f"{event_name}_{match_template_id}.png")
    cv2.imwrite(log_path, frame_crop)
