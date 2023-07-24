import streamlit as st
import requests

# Replace 'YOUR_LANDING_AI_API_KEY' with your actual Landing AI API key
LANDING_AI_API_KEY = 'land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O'

LANDING_AI_UPLOAD_URL = 'https://predict.app.landing.ai/inference/v1/predict?endpoint_id=5bc96d69-6328-410f-83e2-eb3b5d97ad29'

def upload_image_to_landing_ai(image_path):
    headers = {
        'Authorization': f'ApiKey {LANDING_AI_API_KEY}',
    }

    files = {'file': open(image_path, 'rb')}

    response = requests.post(LANDING_AI_UPLOAD_URL, headers=headers, files=files)

    return response.json()

def main():
    st.title("Upload Image to Landing AI")

    # File uploader to choose an image file from the local machine
    image_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if image_file is not None:
        # Save the uploaded image to a temporary file
        with open('temp_image.jpg', 'wb') as f:
            f.write(image_file.read())

        st.image(image_file, caption="Uploaded Image", use_column_width=True)

        # Upload the image to Landing AI
        response_data = upload_image_to_landing_ai('temp_image.jpg')
        response_data
        # Process the response from Landing AI and display the result
        if 'prediction' in response_data:
            st.write("Prediction results from Landing AI:")
            for prediction in response_data['prediction']:
                st.write(f"Label: {prediction['label']}, Confidence: {prediction['confidence']:.2f}")

if __name__ == "__main__":
    main()
