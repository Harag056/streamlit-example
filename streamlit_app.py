import streamlit as st
import cv2
import numpy as np
import tempfile
import os

def read_video_frames(binary_data, fps):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(binary_data)
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

    # Binary uploader to choose a video file in binary format
    binary_file = st.file_uploader("Choose a video file in binary format", type=["bin"])

    if binary_file is not None:
        # Get desired frames per second using a slider
        desired_fps = st.slider("Select frames per second:", min_value=1, max_value=30, value=10)

        # Convert the binary file to frames and store them in an array
        binary_data = binary_file.getvalue()
        frames = read_video_frames(binary_data, desired_fps)

        # Display the frames one by one
        for i, frame in enumerate(frames):
            st.image(frame, caption=f"Frame {i+1}", use_column_width=True)

if __name__ == "__main__":
    main()
