import cv2
import json
import os

def cropper(match_fn_names):
    """
    Extracts and saves a cropped image for a specific event class from a video frame.

    Args:
        event_class_name (str): Name of the event class (e.g., "kill", "flag_capture").
        video_file_stem (str): Video file name without extension (e.g., "kill_extract"), located in data/raw_videos/.
        frame_id (int): Frame index to extract from.
    """
    try:
        # Read inputs
        event_class_name = input("Enter event name (e.g. kill): ").strip()
        
        # Load ROI
        roi_path = os.path.join("data", "events", "events.json")
        with open(roi_path, "r") as f:
            roi_data = json.load(f)

        if event_class_name not in roi_data:
            raise ValueError(f"Event class '{event_class_name}' not found in event_roi.json.")

        x1, y1, x2, y2 = roi_data[event_class_name]["roi"]
        frame_id = roi_data[event_class_name]["frame_id"]
        
        # Open video file and read the specified frame
        file_name = input("🎥 Enter extract file name (press Enter to use default): ").strip()

        if not file_name:
            video_path = os.path.join("data", "events", "extracts", f"{event_class_name}_extract.mp4")
        else:
            video_path = os.path.join("data", "events", "extracts", f"{file_name}.mp4")

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video file: {video_path}")

        # Read the frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise ValueError(f"Could not read frame {frame_id} from {video_path}")

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
        
        if selected_fn == "fixtemplate_rgb":
            pass
        elif selected_fn == "fixtemplate_gray":
            is_template = True
            is_gray = True
        else:
            raise ValueError(f"❌ Missing crop export details for function for function:{selected_fn}")

        if is_template:
            save_dir = os.path.join("data", "events", "templates")
        else:
            save_dir = os.path.join("data", "events", "crop")

        # Convert to grayscale if needed
        if is_gray:
            print("Converting frame to grayscale...")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Crop
        cropped = frame[y1:y2, x1:x2]

        # Save selected match function in the event JSON
        roi_data[event_class_name]["match"] = selected_fn
        with open(roi_path, "w") as f:
            json.dump(roi_data, f, indent=2)
        print(f"💾 Match function '{selected_fn}' saved to event '{event_class_name}' in events.json.")

        # Save cropped image
        output_path = os.path.join(save_dir, f"{event_class_name}_{'template' if is_template else 'crop'}.png")
        os.makedirs(save_dir, exist_ok=True)
        cv2.imwrite(output_path, cropped)

        input(f"✅ Cropped image saved to: {output_path} ! Press Enter to continue...")

        
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to continue...")
    