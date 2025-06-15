def timestamp(frame_id, fps):
    hours = frame_id // (3600 * fps)
    minutes = (frame_id // (60 * fps)) % 60
    seconds = (frame_id // fps) % 60
    frames = frame_id % fps
    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"