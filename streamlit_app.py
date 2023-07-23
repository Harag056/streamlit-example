import streamlit as st
import landingai as la

# Get the API key from Landing AI
api_key = "land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O"

# Create a Landing AI client
client = la.Client(api_key=api_key)

# Create a text field
text_input = st.text_input("Enter some text")

# Classify the text
if text_input:
    classification = client.classify(text_input)
    st.write(classification)
