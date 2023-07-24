import streamlit as st
import snowflake.connector
from PIL import Image
import io
import cv2
import tempfile



def Connection():
    st.title("Connection App")

    #Input fields for Snowflake connection parameters
    snowflake_account = st.text_input("Snowflake Account", "rz20203.central-india.azure")
    snowflake_username = st.text_input("User", "TESTUSER")
    snowflake_password = st.text_input("Password", "Test@123", type="password")
    snowflake_warehouse = st.text_input("Warehouse", "COMPUTE_WH")
    snowflake_database = st.text_input("Database", "LandingAI_DB")
    snowflake_schema = st.text_input("Schema", "Raw")

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
    


def upload():
    def save_uploaded_file(uploaded_file):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            return temp_file.name
        
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        temp_video_path = save_uploaded_file(uploaded_file)
        
        # Read the video file using OpenCV VideoCapture
        video_capture = cv2.VideoCapture(temp_video_path)
        
        # Check if the video is opened successfully
        if not video_capture.isOpened():
            st.error("Error: Unable to open the video file.")
        else:
            st.success("Video file opened successfully.")
    
            # Read and display each frame of the video
            while True:
                ret, frame = video_capture.read()
    
                if not ret:
                    break
    
                # Convert the frame from BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
                # Display the frame using Streamlit
                st.image(frame_rgb, channels="RGB", use_column_width=True)
    
    #     # Release the video capture object and close the video file
    #     video_capture.release()



def inference():
    st.title("Contact Us")
    st.write("This is the Contact Us page content.")

def main():

    # Create a sidebar with menu options
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("", ("Connections Details", "Upload Image", "Run Inference"))

    if menu == "Connections Details":
        Connection()
    elif menu == "Upload Image":
        upload()
    elif menu == "Run Inference":
        inference()

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
