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

import azure.ai.vision as sdk

# Azure Cognitive Services setup
service_options = sdk.VisionServiceOptions(
    "https://bi3va.cognitiveservices.azure.com/",
    "6667acbd346846a4abb0a5e36219de60"
)

analysis_options = sdk.ImageAnalysisOptions()
analysis_options.features = (sdk.ImageAnalysisFeature.TEXT,)
analysis_options.language = "en"
analysis_options.gender_neutral_caption = True

# Helper functions
def calculate_bounding_box(bounding_boxes):
    min_x = float('inf')
    min_y = float('inf')
    max_width = 0
    max_height = 0
    for box in bounding_boxes:
        x, y, width, height = box
        # Find the minimum x and y coordinates
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        # Find the maximum width and height
        max_width = max(max_width, width)
        max_height = max(max_height, height)
    return int(min_x), int(min_y), int(max_width), int(max_height)

def bounding_polygon_to_boxes(bounding_polygon):
        bounding_boxes = []
        num_points = len(bounding_polygon)
    
        for i in range(0, num_points, 2):
            x1, y1 = bounding_polygon[i], bounding_polygon[i + 1]
    
            if i + 2 < num_points:
                x2, y2 = bounding_polygon[i + 2], bounding_polygon[i + 3]
            else:
                # If the last point is reached, connect it to the first point to close the polygon
                x2, y2 = bounding_polygon[0], bounding_polygon[1]
    
            # Find the minimum and maximum coordinates for each axis
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            min_y = min(y1, y2)
            max_y = max(y1, y2)
    
            # Add the bounding box to the list
            bounding_boxes.append((min_x, min_y, max_x - min_x, max_y - min_y))

        return bounding_boxes

def draw_bounding_boxes_with_text(image, bounding_boxes):
    # Step 1: Load the image
    image = cv2.imread(image_path)
    
    for boxes, text in bounding_boxes:
        if len(boxes) > 0:
            # Draw the first bounding box in each element of the input_data array
            x, y, w, h = map(int, boxes[0])
            x, y, w, h = calculate_bounding_box(boxes)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    # Save the result
    cv2.imwrite(output_path, image)
    
    json_out=[]


# Streamlit app
def process_image(image_path):
    vision_source = sdk.VisionSource(filename=image_path)
    image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)

    result = image_analyzer.analyze()


    if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
        print("Image height: {}".format(result.image_height))
        print("Image width: {}".format(result.image_width))
        print("Model version: {}".format(result.model_version))

        if result.objects is not None:
            print("Objects:")
            for obj in result.objects:
                print("   '{}', {}, Confidence: {:.4f}".format(obj.name, obj.bounding_box, obj.confidence))

        if result.tags is not None:
            print("Tags:")
            for tag in result.tags:
                print("   '{}', Confidence {:.4f}".format(tag.name, tag.confidence))

        if result.people is not None:
            print("People:")
            for person in result.people:
                print("   {}, Confidence {:.4f}".format(person.bounding_box, person.confidence))

        if result.caption is not None:
            print("Caption:")
            print("   '{}', Confidence {:.4f}".format(result.caption.content, result.caption.confidence))

        lst_bounding_boxes = []

        if result.text is not None:
            print("Text:")
            for line in result.text.lines:
                bounding_boxes = bounding_polygon_to_boxes(line.bounding_polygon)
                tuple_bounding_box = (bounding_boxes, line.content)
                lst_bounding_boxes.append(tuple_bounding_box)
                points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
                print("   Line: '{}', Bounding polygon {}".format(line.content, points_string))

                data = {
                    "image": image_path,
                    "detectedword": line.content,
                    "detectedpolygon": points_string
                }
                json_out.append(data)

                for word in line.words:
                    points_string = "{" + ", ".join([str(int(point)) for point in word.bounding_polygon]) + "}"
                    print("     Word: '{}', Bounding polygon {}, Confidence {:.4f}"
                          .format(word.content, points_string, word.confidence))

        outputimage = annoated_path(image_path, "AI")
        print(lst_bounding_boxes)
        print(outputimage)
        draw_bounding_boxes_with_text(image_path, lst_bounding_boxes, outputimage)
    else:
        error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
        print("Analysis failed.")
        print("   Error reason: {}".format(error_details.reason))
        print("   Error code: {}".format(error_details.error_code))
        print("   Error message: {}".format(error_details.message))



def main():
    st.title("Azure Cognitive Services Vision API Image Analysis")

    # Folder selection
    folder_path = st.text_input("Enter the path to the folder containing images:", "C:\\Users\\HarishSankaranarayan\\Desktop\\test\\")
    if not os.path.isdir(folder_path):
        isdir = os.path.isdir(folder_path)
        st.error(isdir)
        return

    if st.button("Analyze Images"):
        # Process each image in the folder
        st.text("Processing images... Please wait.")
        for image_file in os.listdir(folder_path):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(folder_path, image_file)
                process_image(image_path)
        st.text("Image analysis completed.")

        # Save output JSON
        with open(os.path.join(folder_path, "AI", "output.json"), "w") as json_file:
            json.dump(json_out, json_file)

if __name__ == "__main__":
    main()

# landingai_api_key=""
# landinai_endpoint_id=""

# def Connection():
#     st.title("Connection App")
#     st.write("Snowflake Connection Details")
#     #Input fields for Snowflake connection parameters
#     snowflake_account = st.text_input("Snowflake Account", "rz20203.central-india.azure")
#     snowflake_username = st.text_input("User", "TESTUSER")
#     snowflake_password = st.text_input("Password", "Test@123", type="password")
#     snowflake_warehouse = st.text_input("Warehouse", "COMPUTE_WH")
#     snowflake_database = st.text_input("Database", "LandingAI_DB")
#     snowflake_schema = st.text_input("Schema", "Raw")
#     st.write("LandingAI Connection Details")
#     landingai_api_key = st.text_input("Api Key", "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O", type="password")
#     landinai_endpoint_id = st.text_input("EndpointId", "5bc96d69-6328-410f-83e2-eb3b5d97ad29")
#     # Function to connect to Snowflake
#     def connect_to_snowflake():
#         conn = snowflake.connector.connect(
#             user=snowflake_username,
#             password=snowflake_password,
#             account=snowflake_account,
#             warehouse=snowflake_warehouse,
#             database=snowflake_database,
#             schema=snowflake_schema
#         )
        
#     if st.button("Connect"):
#         try:
#             conn = connect_to_snowflake()
#             st.success("Connected to Snowflake")
#             #conn.close()
#         except Exception as e:
#             st.error(f"Error connecting to Snowflake: {str(e)}")
#             return

#     # Close the Snowflake connection when the app is closed
    

    
# def upload(video_file, fps):
#     temp_file = tempfile.NamedTemporaryFile(delete=False)
#     temp_file.write(video_file.read())
#     temp_file.close()

#     video = cv2.VideoCapture(temp_file.name)

#     # Get frames per second (FPS) of the video
#     original_fps = video.get(cv2.CAP_PROP_FPS)

#     # Calculate frame interval to get desired FPS
#     frame_interval = int(original_fps / fps)

#     frames = []
#     frame_count = 0

#     while True:
#         ret, frame = video.read()

#         if not ret:
#             break

#         if frame_count % frame_interval == 0:
#             frames.append(frame)

#         frame_count += 1

#     video.release()
#     os.unlink(temp_file.name)
#     return frames



# def inference(image_path):
#         # Replace 'YOUR_LANDING_AI_API_KEY' with your actual Landing AI API key
#     LANDING_AI_API_KEY = "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O"
#     LANDING_AI_UPLOAD_URL = "https://predict.app.landing.ai/inference/v1/predict?endpoint_id=5bc96d69-6328-410f-83e2-eb3b5d97ad29"

#     headers = {
#         'apikey': LANDING_AI_API_KEY
#     }
#     payload = {}
#     files = {'file': (image_path,open(image_path,'rb'),'image/jpeg')}
    
#     image_path
#     response = requests.request("POST", LANDING_AI_UPLOAD_URL, headers=headers, data=payload, files=files)
    
#     print(response.text)
#     #response = requests.post(LANDING_AI_UPLOAD_URL, headers=headers, files=files)

#     return response.json()

# def main():

#     # Create a sidebar with menu options
#     st.sidebar.title("Menu")
#     menu = st.sidebar.radio("", ("Connections Details", "Upload Image", "Run Inference"))

#     if menu == "Connections Details":
#         Connection()
#     elif menu == "Upload Image":
#         # File uploader to choose a video file from the local machine
#         video_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mkv"])
    
#         if video_file is not None:
#             # Get desired frames per second using a slider
#             desired_fps = st.slider("Select frames per second:", min_value=1, max_value=30, value=10)
    
#             # Convert the video to frames and store them in an array
#             frames = upload(video_file, desired_fps)
    
#             st.write(f"Number of frames extracted: {len(frames)}")
#             # Display the frames one by one
#             for i, frame in enumerate(frames):
#                 st.image(frame, caption=f"Frame {i+1}", use_column_width=True)

    
#     elif menu == "Run Inference":
#         # File uploader to choose an image file from the local machine
#         image_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
#         if image_file is not None:
#             # Save the uploaded image to a temporary file
#             with open('temp_image.jpg', 'wb') as f:
#                 f.write(image_file.read())
    
#             st.image(image_file, caption="Uploaded Image", use_column_width=True)
    
#             # Upload the image to Landing AI
#             response_data = inference('temp_image.jpg')
#             # Set the confidence threshold using a slider
#             confidence_threshold = st.slider("Set Confidence Threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
#             filtered_predictions = [ pred for pred in response_data["backbonepredictions"].values() if pred["score"] >= confidence_threshold]
#             #filtered_predictions = [prediction["score"] for prediction in response_data["backbonepredictions"].values() if prediction["score"] >= confidence_threshold]
    
#             filtered_predictions
    
#             if len(filtered_predictions) > 0:
#                 st.write("Predictions meeting the confidence threshold:")
#                 for pred in filtered_predictions:
#                     st.write(f"Label: {pred['labelName']}, Confidence: {pred['score']:.2f}")
#             else:
#                 st.write("No predictions meet the confidence threshold.")
# if __name__ == "__main__":
#     main()

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
