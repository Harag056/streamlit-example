import streamlit as st
import cv2
from PIL import Image

uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])

# if uploaded_file is not None:
#     # Read the video file using OpenCV VideoCapture
#     video_capture = cv2.VideoCapture(uploaded_file)
    
#     # Check if the video is opened successfully
#     if not video_capture.isOpened():
#         st.error("Error: Unable to open the video file.")
#     else:
#         st.success("Video file opened successfully.")

#         # Read and display each frame of the video
#         while True:
#             ret, frame = video_capture.read()

#             if not ret:
#                 break

#             # Convert the frame from BGR to RGB
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             # Display the frame using Streamlit
#             st.image(frame_rgb, channels="RGB", use_column_width=True)

#     # Release the video capture object and close the video file
#     video_capture.release()

