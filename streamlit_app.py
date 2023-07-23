import streamlit as st
import landingai as la

# Create a Landing AI client
client = la.Client(api_key="land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O")

# Classify the text
text = "This is a sentence."
classification = client.classify(text)

# Print the classification results
print(classification)
