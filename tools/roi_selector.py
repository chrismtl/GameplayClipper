import os
import cv2
import utils.json_cacher as js
import data.constants as cst

def roi_selector_gui(video_path: str, event_name: str, initial_frame_index: int = 0, draw_roi: tuple[int, int, int, int] = None):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"❌ Cannot open video: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # ===== Mouse Callback State =====
    click_start = [None]
    zoom_roi = [None]
    frame_index = [initial_frame_index]
    roi = [draw_roi]
    scroll_step = 10

    cv2.namedWindow("ROI Preview", cv2.WINDOW_NORMAL)

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            click_start[0] = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            if click_start[0] is not None:
                x1, y1 = click_start[0]
                x2, y2 = x, y
                if zoom_roi[0]:
                    zx1, zy1, _, _ = zoom_roi[0]
                    x1 += zx1
                    x2 += zx1
                    y1 += zy1
                    y2 += zy1
                x1, x2 = sorted((x1, x2))
                y1, y2 = sorted((y1, y2))
                roi[0] = (x1, y1, x2, y2)
                print(f"[ROI Selected] ({x1}, {y1}) to ({x2}, {y2})")
                click_start[0] = None
        elif event == cv2.EVENT_RBUTTONDOWN:
            click_start[0] = (x, y)
        elif event == cv2.EVENT_RBUTTONUP:
            if click_start[0] is not None:
                x1, y1 = click_start[0]
                x2, y2 = x, y
                x1, x2 = sorted((x1, x2))
                y1, y2 = sorted((y1, y2))

                frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                aspect_ratio = frame_w / frame_h

                crop_w = x2 - x1
                crop_h = y2 - y1
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                if crop_w / crop_h > aspect_ratio:
                    new_h = int(crop_w / aspect_ratio)
                    y1 = cy - new_h // 2
                    y2 = cy + new_h // 2
                else:
                    new_w = int(crop_h * aspect_ratio)
                    x1 = cx - new_w // 2
                    x2 = cx + new_w // 2

                # Clamp within image bounds
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(frame_w, x2)
                y2 = min(frame_h, y2)

                zoom_roi[0] = (x1, y1, x2, y2)
                print(f"[Zoom ROI Set] ({x1}, {y1}) to ({x2}, {y2})")
                click_start[0] = None

        elif event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0 and frame_index[0] < total_frames - scroll_step:
                frame_index[0] += scroll_step
            elif flags < 0 and frame_index[0] > scroll_step:
                frame_index[0] -= scroll_step
            frame_index[0] = max(0, min(frame_index[0], total_frames - 1))
            print(f"[Frame] {frame_index[0]}")

    cv2.setMouseCallback("ROI Preview", mouse_callback)

    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index[0])
        ret, frame = cap.read()

        if not ret:
            print(f"⚠️ Failed to read frame {frame_index[0]}")
            break

        if zoom_roi[0]:
            x1, y1, x2, y2 = zoom_roi[0]
            display = frame[y1:y2, x1:x2].copy()
        else:
            display = frame.copy()

        if roi[0]:
            x1, y1, x2, y2 = roi[0]
            if zoom_roi[0]:
                zx1, zy1, _, _ = zoom_roi[0]
                rx1, ry1, rx2, ry2 = x1 - zx1, y1 - zy1, x2 - zx1, y2 - zy1
                if 0 <= rx1 < display.shape[1] and 0 <= ry1 < display.shape[0]:
                    cv2.rectangle(display, (rx1, ry1), (rx2, ry2), (0, 255, 0), 1)
            else:
                cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 1)

        cv2.imshow("ROI Preview", display)

        key = cv2.waitKey(20) & 0xFF
        if key == ord('q') and frame_index[0] > 0:
            frame_index[0] -= 1
            print(f"[Frame] {frame_index[0]}")
        elif key == ord('d') and frame_index[0] < total_frames - 1:
            frame_index[0] += 1
            print(f"[Frame] {frame_index[0]}")
        elif key == ord('r'):
            zoom_roi[0] = None
            click_start[0] = None
            print("[Zoom Reset]")
        elif key == ord('a'):
            scroll_step = max(10, scroll_step - 10)
            print(f"[Scroll Step] Decreased to {scroll_step}")
        elif key == ord('e'):
            scroll_step += 10
            print(f"[Scroll Step] Increased to {scroll_step}")

        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    if roi[0]:
        print(f"\n✅ Final ROI: {roi[0]}")
        print(f"✅ Final Frame Index: {frame_index[0]}")

        confirm = input(f"\n💾 Save this ROI as '{event_name}'? [y/N]: ").strip().lower()
        if confirm == "y":
            save_event_data(event_name, roi[0], frame_index[0])
        else:
            print("❌ Save aborted.")
    else:
        print("⚠️ No ROI selected.")

def save_event_data(event_name: str, roi: tuple, frame_id: int):
    # Load existing data
    if os.path.exists(cst.EVENTS_JSON_PATH):
        event_defs = js.load(cst.EVENTS_JSON_PATH)
    else:
        raise ValueError("⚠️ cst.EVENTS_JSON_PATH does not exist.")

    if event_name not in event_defs:
        event_defs[event_name] = {}

    event_defs[event_name].update({
        "roi": list(roi),
        "frame_id": frame_id
    })
    
    js.update(cst.EVENTS_JSON_PATH, event_defs)
    
    print("✅ New event created in events.json.")

def roi_selector():
    event_name = input("🏷️  Enter new event name: ").strip()
    file_name = input("🎥 Enter extract filename (press Enter to use default): ").strip()

    if not file_name:
        full_path = f"data/events/extracts/{event_name}_extract.mp4"
    else:
        full_path = f"data/events/extracts/{file_name}.mp4"


    if not os.path.exists(full_path):
        input(f"❌ File not found: {full_path}")
        return

    roi_selector_gui(full_path, event_name)
    input("Press Enter to continue...")

