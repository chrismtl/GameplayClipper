import os
import cv2
import utils.json_cacher as js
import data.constants as cst

def cropper(match_fn_names):
    """
    Extracts and saves a cropped image for a specific event class from a video frame.

    Args:
        event_class_name (str): Name of the event class (e.g., "kill", "flag_capture").
        video_file_stem (str): Video file name without extension (e.g., "kill_extract"), located in data/raw_videos/.
        frame_id (int): Frame index to extract from.
    """
    # Refresh json cache
    js.refresh(cst.EVENTS_JSON_PATH)
    
    # Read inputs
    event_class_name = input("Enter event name (e.g. kill): ").strip()
    
    # Load ROI
    event_defs = js.load(cst.EVENTS_JSON_PATH)

    if event_class_name not in event_defs:
        raise ValueError(f"Event class '{event_class_name}' not found in event_roi.json.")

    x1, y1, x2, y2 = event_defs[event_class_name]["roi"]
    frame_id = event_defs[event_class_name]["frame_id"]
    
    # Open video file and read the specified frame
    file_name = input("🎥 Enter extract file name (press Enter to use default): ").strip()

    if not file_name:
        video_path = os.path.join(cst.EXTRACTS_DIR, f"{event_class_name}_extract.mp4")
    else:
        video_path = os.path.join(cst.EXTRACTS_DIR, f"{file_name}.mp4")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise FileNotFoundError(f"❌ Cannot open video file: {video_path}")

    # Read the frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise ValueError(f"❌ Could not read frame {frame_id} from {video_path}")

    # Prompt user for match function
    print("\n🔍 Choose a match function:")
    for i, name in enumerate(match_fn_names, 1):
        print(f"{i}) {name}")

    while True:
        choice = input(">> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(match_fn_names):
            selected_fn = match_fn_names[int(choice) - 1]
            break
        print("❌ Invalid selection. Try again.")

    # Determine mode and path
    is_template = False
    is_gray = False
    is_switch = False
    
    if selected_fn == "fixtemplate_rgb":
        pass
    elif selected_fn == "fixtemplate_gray":
        is_template = True
        is_gray = True
        is_switch = False
    elif selected_fn == "switch":
        is_template = False
        is_gray = True
        is_switch = True
    else:
        raise ValueError(f"❌ Missing crop export details for function for function:{selected_fn}")

    if is_template:
        save_dir = cst.TEMPLATES_UNIQUE_DIR
    elif is_switch:
        save_dir = os.path.join(cst.TEMPLATES_SWITCH_DIR,event_class_name)
    else:
        save_dir = cst.CROPS_DIR

    # Convert to grayscale if needed
    if is_gray:
        print("Converting frame to grayscale...")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)            
    
    # Crop
    cropped = frame[y1:y2, x1:x2]

    event_defs[event_class_name]["match"] = selected_fn
    # Save selected match function in the event JSON
    js.update(cst.EVENTS_JSON_PATH, event_defs)

    # Save cropped image
    if is_template:
        filename = f"{event_class_name}_template"
    elif is_switch:
        filename = f"{frame_id}_template"
    else:
        filename = f"{event_class_name}_crop"
        
    output_path = os.path.join(save_dir, f"{filename}.png")
    os.makedirs(save_dir, exist_ok=True)
    cv2.imwrite(output_path, cropped)

    input(f"✅ Cropped image saved to: {output_path} ! Press Enter to continue...")
    