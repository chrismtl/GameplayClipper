import cv2

def format_timestamp_from_frame(frame_id, fps):
    hours = frame_id // (3600 * fps)
    minutes = (frame_id // (60 * fps)) % 60
    seconds = (frame_id // fps) % 60
    frames = frame_id % fps
    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

def iterate_video(path):
    cap = cv2.VideoCapture(path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    step = 1

    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id % step == 0:
            timestamp_str = format_timestamp_from_frame(frame_id, fps)
            yield frame_id, frame, timestamp_str
        frame_id += 1

    cap.release()
