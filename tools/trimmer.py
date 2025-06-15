import cv2
import os
from tkinter import Tk, filedialog

# Ask user for trim duration in minutes
try:
    minutes = float(input("⏱️ Enter duration to trim (in minutes): "))
except ValueError:
    print("❌ Invalid input. Please enter a number.")
    exit()

DURATION_SECONDS = int(minutes * 60)

# Open file dialog to choose video
Tk().withdraw()  # Hide the root window
video_path = filedialog.askopenfilename(
    title="Select a video to trim",
    initialdir="data/raw_videos",
    filetypes=[("MP4 files", "*.mp4")]
)

if not video_path:
    print("❌ No video selected.")
    exit()

# Prepare output file path
video_file = os.path.basename(video_path)
file_stem, file_ext = os.path.splitext(video_file)
parent_dir = os.path.dirname(video_path)
output_path = os.path.join(parent_dir, f"{file_stem}_trimmed{file_ext}")

# Setup video capture and writer
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
frame_limit = int(fps * DURATION_SECONDS)

print(f"✂️ Trimming first {DURATION_SECONDS} seconds from {video_file.name}")

frame_count = 0
while frame_count < frame_limit:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Reached end of video.")
        break
    out.write(frame)
    frame_count += 1

cap.release()
out.release()
print(f"✅ Trimmed clip saved to {OUTPUT_PATH}")
