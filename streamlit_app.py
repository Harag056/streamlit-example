# import streamlit as st
# import requests
# import os

# Generate API key and endpoint ID
# api_key = "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O"
# endpoint_id = "456de868-464d-45e3-8f6a-8d9a8e1301ab"

import streamlit as st
import requests

# Define the curl command
curl_command = "curl --location --request POST 'https://predict.app.landing.ai/inference/v1/predict?endpoint_id=5bc96d69-6328-410f-83e2-eb3b5d97ad29' \
     --header 'Content-Type: multipart/form-data' \
     --header 'apikey: YOUR_APIKEY' \
     --form 'file=@\"YOUR_IMAGE\"'"

# Execute the curl command
response = requests.get(curl_command)

# Print the response
st.write(response.text)


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
