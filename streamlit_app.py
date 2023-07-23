import streamlit as st
import requests

url = "https://predict.app.landing.ai/inference/v1/predict?endpoint_id=456de868-464d-45e3-8f6a-8d9a8e1301ab"

payload = {}
files=[
  ('file',('1644269774_vehicles.jpg',open('og9uHBD8X/1644269774_vehicles.jpg','rb'),'image/jpeg'))
]
headers = {
  'apikey': 'land_sk_0EJDSLM53NDshwkFBKbuYzIKv2g7oaUeQ1zXLhBC2AeQKXLj0O'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
