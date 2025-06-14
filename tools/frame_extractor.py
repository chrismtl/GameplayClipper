import cv2

def iterate_video(path):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    step = 1

    frame_id = 0
    timestamp = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id % step == 0:
            yield frame_id, frame, timestamp
        frame_id += 1
        timestamp += 1 / fps

    cap.release()