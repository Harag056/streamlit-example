# import streamlit as st
# import requests
# import os

# Generate API key and endpoint ID
# api_key = "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O"
# endpoint_id = "456de868-464d-45e3-8f6a-8d9a8e1301ab"
import os

# Set the environment variable to prevent graphical backend usage in OpenCV
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = str(2**64)
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "protocol_whitelist;file,rtp,udp"

# Import the other necessary libraries after setting the environment variables

import streamlit as st
import numpy as np
from PIL import Image
import cv2 

def convert_video_to_binary(video_file):
    binary_data = video_file.read()
    return binary_data

def get_video_frames(binary_data):
    # Convert binary data to numpy array
    np_array = np.frombuffer(binary_data, dtype=np.uint8)

    # Read the video from the numpy array
    video = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)

    # Get frames per second (FPS) of the video
    fps = video.get(cv2.CAP_PROP_FPS)

    # Extract one frame per second
    frame_interval = int(fps)  # Retrieve one frame per second
    frames = [Image.fromarray(frame) for i, frame in enumerate(video) if i % frame_interval == 0]

    return frames

def main():
    st.title("Video to Frames Converter")

    # File uploader to choose a video file from the local machine
    video_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mkv"])

    if video_file is not None:
        # Convert the video to binary data
        binary_data = convert_video_to_binary(video_file)

        # Get frames from the video
        frames = get_video_frames(binary_data)

        # Display the frames
        for i, frame in enumerate(frames):
            st.image(frame, caption=f"Frame {i+1}", use_column_width=True)

if __name__ == "__main__":
    main()


# LANDING_AI_API_KEY = "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O"
# LANDING_AI_API_ENDPOINT = "https://predict.app.landing.ai/inference/v1/predict?endpoint_id=456de868-464d-45e3-8f6a-8d9a8e1301ab"  # Replace this with the actual API endpoint URL

# def landing_ai_api_request(api_endpoint, headers, data):
#     try:
#         response = requests.post(api_endpoint, headers=headers, data=data)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error during API request: {e}")
#         return None

# st.title("Landing AI API Usage")

# # Your Streamlit app UI to accept user inputs or images for processing with the API

# # Example: Upload an image using file_uploader
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

# if uploaded_file is not None:
#     # Save the uploaded image to a temporary location
#     image_path = f"temp_{uploaded_file.name}"
#     with open(image_path, "wb") as f:
#         f.write(uploaded_file.read())
#     st.success("Image uploaded successfully.")

#     # Prepare headers and data for the API request
#     headers = {
#         "Authorization": f"Bearer {LANDING_AI_API_KEY}",
#         # Add any other required headers based on the API documentation
#     }

#     data = {
#         # Add any required data or parameters based on the API documentation
#     }

#     # Use the API to process the image
#     api_response = landing_ai_api_request(LANDING_AI_API_ENDPOINT, headers=headers, data=data)

#     # Process and display the API response as needed
#     if api_response:
#         st.write("API Response:")
#         st.write(api_response)

#     # Remove the temporary image file after processing
#     os.remove(image_path)
