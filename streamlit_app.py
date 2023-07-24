import streamlit as st
import snowflake.connector
from PIL import Image
import io
import cv2
import tempfile
import numpy as np
import os
import requests
import json

landingai_api_key=""
landinai_endpoint_id=""

def Connection():
    st.title("Connection App")
    st.write("Snowflake Connection Details")
    #Input fields for Snowflake connection parameters
    snowflake_account = st.text_input("Snowflake Account", "rz20203.central-india.azure")
    snowflake_username = st.text_input("User", "TESTUSER")
    snowflake_password = st.text_input("Password", "Test@123", type="password")
    snowflake_warehouse = st.text_input("Warehouse", "COMPUTE_WH")
    snowflake_database = st.text_input("Database", "LandingAI_DB")
    snowflake_schema = st.text_input("Schema", "Raw")
    st.write("LandingAI Connection Details")
    landingai_api_key = st.text_input("Api Key", "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O", type="password")
    landinai_endpoint_id = st.text_input("EndpointId", "5bc96d69-6328-410f-83e2-eb3b5d97ad29")
    # Function to connect to Snowflake
    def connect_to_snowflake():
        conn = snowflake.connector.connect(
            user=snowflake_username,
            password=snowflake_password,
            account=snowflake_account,
            warehouse=snowflake_warehouse,
            database=snowflake_database,
            schema=snowflake_schema
        )
        
    if st.button("Connect"):
        try:
            conn = connect_to_snowflake()
            st.success("Connected to Snowflake")
            #conn.close()
        except Exception as e:
            st.error(f"Error connecting to Snowflake: {str(e)}")
            return

    # Close the Snowflake connection when the app is closed
    

    
def upload(video_file, fps):
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



def inference(image_path):
        # Replace 'YOUR_LANDING_AI_API_KEY' with your actual Landing AI API key
    LANDING_AI_API_KEY = "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O"
    LANDING_AI_UPLOAD_URL = "https://predict.app.landing.ai/inference/v1/predict?endpoint_id=5bc96d69-6328-410f-83e2-eb3b5d97ad29"

    headers = {
        'apikey': LANDING_AI_API_KEY
    }
    payload = {}
    files = {'file': (image_path,open(image_path,'rb'),'image/jpeg')}
    
    image_path
    response = requests.request("POST", LANDING_AI_UPLOAD_URL, headers=headers, data=payload, files=files)
    
    print(response.text)
    #response = requests.post(LANDING_AI_UPLOAD_URL, headers=headers, files=files)

    return response.json()

def main():

    # Create a sidebar with menu options
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("", ("Connections Details", "Upload Image", "Run Inference"))

    if menu == "Connections Details":
        Connection()
    elif menu == "Upload Image":
        # File uploader to choose a video file from the local machine
        video_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mkv"])
    
        if video_file is not None:
            # Get desired frames per second using a slider
            desired_fps = st.slider("Select frames per second:", min_value=1, max_value=30, value=10)
    
            # Convert the video to frames and store them in an array
            frames = upload(video_file, desired_fps)
    
            st.write(f"Number of frames extracted: {len(frames)}")
            # Display the frames one by one
            for i, frame in enumerate(frames):
                st.image(frame, caption=f"Frame {i+1}", use_column_width=True)

    
    elif menu == "Run Inference":
        # File uploader to choose an image file from the local machine
        image_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        if image_file is not None:
            # Save the uploaded image to a temporary file
            with open('temp_image.jpg', 'wb') as f:
                f.write(image_file.read())
    
            st.image(image_file, caption="Uploaded Image", use_column_width=True)
    
            # Upload the image to Landing AI
            response_data = inference('temp_image.jpg')
            response_data
            # Set the confidence threshold using a slider
            confidence_threshold = st.slider("Set Confidence Threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
            filtered_predictions = [ pred for pred in response_data["backbonepredictions"].values() if pred["score"] >= confidence_threshold]
            #filtered_predictions = [prediction["score"] for prediction in response_data["backbonepredictions"].values() if prediction["score"] >= confidence_threshold]
    
            filtered_predictions
    
            if len(filtered_predictions) > 0:
                st.write("Predictions meeting the confidence threshold:")
                for pred in filtered_predictions:
                    st.write(f"Label: {pred['labelName']}, Confidence: {pred['score']:.2f}")
            else:
                st.write("No predictions meet the confidence threshold.")
if __name__ == "__main__":
    main()

# import os

# # Set the environment variable to prevent graphical backend usage in OpenCV
# os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = str(2**64)
# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "protocol_whitelist;file,rtp,udp"

# # Import the other necessary libraries after setting the environment variables

# import streamlit as st
# import numpy as np
# from PIL import Image
# #import cv2 

# def convert_video_to_binary(video_file):
#     binary_data = video_file.read()
#     return binary_data

# def get_video_frames(binary_data):
#     # Convert binary data to numpy array
#     np_array = np.frombuffer(binary_data, dtype=np.uint8)

#     # Read the video from the numpy array
#     video = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)

#     # Get frames per second (FPS) of the video
#     fps = video.get(cv2.CAP_PROP_FPS)

#     # Extract one frame per second
#     frame_interval = int(fps)  # Retrieve one frame per second
#     frames = [Image.fromarray(frame) for i, frame in enumerate(video) if i % frame_interval == 0]

#     return frames

# def main():
#     st.title("Video to Frames Converter")

#     # File uploader to choose a video file from the local machine
#     video_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mkv"])

#     if video_file is not None:
#         # Convert the video to binary data
#         binary_data = convert_video_to_binary(video_file)

#         # Get frames from the video
#         frames = get_video_frames(binary_data)

#         # Display the frames
#         for i, frame in enumerate(frames):
#             st.image(frame, caption=f"Frame {i+1}", use_column_width=True)

# if __name__ == "__main__":
#     main()
