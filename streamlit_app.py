import streamlit as st
import numpy as np
import landingai

# Generate API key and endpoint ID
api_key = "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O"
endpoint_id = "5bc96d69-6328-410f-83e2-eb3b5d97ad29"

# Create predictor object
predictor = landingai.Predictor(api_key=api_key, endpoint_id=endpoint_id)

# Load image
image = np.asarray(Image.open("1644269774_vehicles.jpg"))

# Make prediction
prediction = predictor.predict(image)

# Print prediction
st.write(prediction)
