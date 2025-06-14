def seconds_to_timestamp(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02}:{secs:02}"

def timestamp_to_seconds(timestamp):
    mins, secs = map(int, timestamp.split(':'))
    return mins * 60 + secs

def to_frame_number(ts):
    total_frames = int(round(ts * 30))
    second = total_frames // 30
    frame = total_frames % 30
    return f"{second}.{frame}"