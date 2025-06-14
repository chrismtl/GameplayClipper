import subprocess

def extract_clips(event_df, video_path, output_path, duration=10):
    for _, row in event_df.iterrows():
        ts = max(0, row["timestamp"] - duration / 2)
        cmd = f'ffmpeg -ss {ts:.2f} -i "{video_path}" -t {duration} -c copy "{output_path}"'
        subprocess.run(cmd, shell=True)
        
def extract_clips():
    input("🔜 Clip extraction feature is under development. Stay tuned!")