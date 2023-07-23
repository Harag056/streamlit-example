# import streamlit as st
# import requests
# import os

# Generate API key and endpoint ID
# api_key = "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O"
# endpoint_id = "456de868-464d-45e3-8f6a-8d9a8e1301ab"
import streamlit as st
import numpy as np
from PIL import Image

def convert_bin_to_images(binary_data):
    try:
        # Convert binary data to a numpy array
        np_array = np.frombuffer(binary_data, dtype=np.uint8)

        # Assuming the data represents images, you can reshape it to a suitable shape (e.g., [num_images, height, width, channels])
        # Replace 'num_images', 'height', 'width', and 'channels' with the actual values based on your binary data format.
        # For example, if it's a single image with shape (height, width, channels), you can use np_array.reshape((height, width, channels))
        images = np_array.reshape([num_images, height, width, channels])

        # Convert numpy arrays to PIL images
        pil_images = [Image.fromarray(image) for image in images]

        return pil_images
    except Exception as e:
        st.error(f"Error occurred: {e}")

def main():
    st.title("Binary File to Images Converter")
    uploaded_file = st.file_uploader("Upload a binary file", type=["bin"])

    if uploaded_file is not None:
        # Read binary data from the uploaded file
        binary_data = uploaded_file.getvalue()

        # Convert binary data to images
        images = convert_bin_to_images(binary_data)

        # Display the images
        for i, image in enumerate(images):
            st.image(image, caption=f"Image {i+1}", use_column_width=True)

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
