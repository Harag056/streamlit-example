import streamlit as st
import requests

LANDING_AI_API_KEY = "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O"
LANDING_AI_ENDPOINT_ID = "5bc96d69-6328-410f-83e2-eb3b5d97ad29"
LANDING_AI_API_URL = "https://predict.app.landing.ai/inference/v1/predict?endpoint_id=456de868-464d-45e3-8f6a-8d9a8e1301ab"  # Replace this with the actual API URL

def upload_image(image_path):
    try:
        headers = {
            "Authorization": f"Bearer {LANDING_AI_API_KEY}",
        }

        files = {
            "file": open(image_path, "rb"),
        }

        data = {
            "endpoint_id": LANDING_AI_ENDPOINT_ID,
            # Add any other required parameters based on the API documentation
        }

        response = requests.post(LANDING_AI_API_URL, headers=headers, files=files, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error occurred during API request: {e}")
        return None

st.title("Landing AI Image Upload")

# File uploader widget to select an image for upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Save the uploaded image to a temporary location
    image_path = f"temp_{uploaded_file.name}"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("Image uploaded successfully.")

    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Use the API to process the image (if Landing AI API is available)
    if st.button("Process Image"):
        result = upload_image(image_path)
        if result:
            # Process and display the API response as needed
            st.write("API Response:")
            st.write(result)

    # Remove the temporary image file after processing
    os.remove(image_path)
