import streamlit as st
import requests

# Replace 'YOUR_LANDING_AI_API_KEY' with your actual Landing AI API key
LANDING_AI_API_KEY = 'land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O'

#LANDING_AI_UPLOAD_URL = 'https://predict.app.landing.ai/inference/v1/predict?endpoint_id=5bc96d69-6328-410f-83e2-eb3b5d97ad29'
LANDING_AI_UPLOAD_URL = "https://predict.app.landing.ai/inference/v1/predict?endpoint_id=5bc96d69-6328-410f-83e2-eb3b5d97ad29"

def upload_image_to_landing_ai(image_path):
    headers = {
        'apikey': 'land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O'
    }
    payload = {}
    files = {'file': (image_path,open(image_path,'rb'),'image/jpeg')}
    
    image_path
    response = requests.request("POST", LANDING_AI_UPLOAD_URL, headers=headers, data=payload, files=files)
    
    print(response.text)
    #response = requests.post(LANDING_AI_UPLOAD_URL, headers=headers, files=files)

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
        # Parse the JSON data
        parsed_data = json.loads(response_data)
        # Set the confidence threshold using a slider
        confidence_threshold = st.slider("Set Confidence Threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
        filtered_predictions = [prediction["score"] for prediction in parsed_data["backbonepredictions"] >= confidence_threshold]
        filtered_predictions

        if len(filtered_predictions) > 0:
            st.write("Predictions meeting the confidence threshold:")
            for pred in filtered_predictions:
                st.write(f"Label: {pred['label']}, Confidence: {pred['confidence']:.2f}")
        else:
            st.write("No predictions meet the confidence threshold.")

        # Process the response from Landing AI and display the result
        # if 'prediction' in response_data:
        #     st.write("Prediction results from Landing AI:")
        #     for prediction in response_data['prediction']:
        #         st.write(f"Label: {prediction['label']}, Confidence: {prediction['confidence']:.2f}")

if __name__ == "__main__":
    main()
