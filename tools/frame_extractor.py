import cv2
import utils.time_utils as time_utils

def iterate_video(path, frame_rate=None):
    cap = cv2.VideoCapture(path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    step = 1 if frame_rate is None else max(1, int(fps // frame_rate))

    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id % step == 0:
            timestamp_str = time_utils.timestamp(frame_id, fps)
            yield frame_id, frame, timestamp_str
        frame_id += 1

    cap.release()
