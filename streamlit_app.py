import streamlit as st
import cv2
import numpy as np
import tempfile
import os

def read_video_frames(video_file, fps):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(video_file.read())
    temp_file.close()

    video = cv2.VideoCapture(temp_file.name)

    # Get frames per second (FPS) of the video
    original_fps = video.get(cv2.CAP_PROP_FPS)

    # Calculate frame interval to get desired FPS
    frame_interval = int(original_fps / fps)

    frames = []
    frame_count = 0

    while True:
        ret, frame = video.read()

        if not ret:
            break

        if frame_count % frame_interval == 0:
            frames.append(frame)

        frame_count += 1

    video.release()
    os.unlink(temp_file.name)
    return frames

def main():
    st.title("Video to Frames Converter")

    # File uploader to choose a video file from the local machine
    video_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mkv"])

    if video_file is not None:
        # Get desired frames per second using a slider
        desired_fps = st.slider("Select frames per second:", min_value=1, max_value=30, value=10)

        # Convert the video to frames and store them in an array
        frames = read_video_frames(video_file, desired_fps)

        st.write(f"Number of frames extracted: {len(frames)}")

        # You can now use the frames as desired (e.g., display them, process them, etc.)

if __name__ == "__main__":
    main()
