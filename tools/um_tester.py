import os
import cv2
from ..engine.matchers.unique_matcher import match_template_mask

mode = 1

if mode==0:
    # === CONFIG ===
    SAMPLE_FOLDER = "testing/unique_match/samples"
    GLOB_EVENT_NAME = "bf2_kill_brc"
    THRESHOLD = 0.95

    # === MAIN LOOP ===
    for filename in os.listdir(SAMPLE_FOLDER):
        if filename.lower().endswith(".png"):
            img_path = os.path.join(SAMPLE_FOLDER, filename)
            frame_crop = cv2.imread(img_path)

            if frame_crop is None:
                print(f"❌ Failed to load image: {filename}")
                continue

            matched, score, event_name = match_template_mask(frame_crop, GLOB_EVENT_NAME, filename, threshold=THRESHOLD , testing=True)

            print(f"🖼️ {filename:<25} | Matched: {str(matched):<5} | Score: {score:.3f} | Event: {event_name}")
            

elif mode==1:
    # Target frame index
    target_id = 21*60*30 + 12*30 + 5
    video_path = "media/Jakku.mp4"
    # Iterate until the desired frame is found
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_id)
    ret, frame = cap.read()
    x1, y1, x2, y2 = [905,485,1014,594]
    crop = frame[y1:y2, x1:x2]
    cv2.imshow("Crop", crop); cv2.waitKey(0); cv2.destroyAllWindows()

    matched, score, _ = match_template_mask(crop, "bf2_kill_brc", video_path, threshold=0.95, testing=True)
    print(f"🖼️ Matched: {str(matched):<5} | Score: {score:.3f} | Event: bf2_kill_brc")
    cap.release()


