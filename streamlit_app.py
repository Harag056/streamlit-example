import streamlit as st
import landingai

def upload_images():
    # Get the images from the user.
    images = st.file_uploader("Upload images", multiple=True)

    # Upload the images to Landing AI.
    for image in images:
        landingai.upload_image(image)

# Create a button to upload the images.
st.button("Upload Images", on_click=upload_images)

# Run the Streamlit app.
if __name__ == "__main__":
    st.run()
