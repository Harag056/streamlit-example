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
        return None

def main():
    st.title("Binary File to Images Converter")
    uploaded_file = st.file_uploader("Upload a binary file", type=["bin"])

    if uploaded_file is not None:
        # Read binary data from the uploaded file
        binary_data = uploaded_file.getvalue()

        # Convert binary data to images
        images = convert_bin_to_images(binary_data)

        # Display the images if conversion is successful
        if images:
            for i, image in enumerate(images):
                st.image(image, caption=f"Image {i+1}", use_column_width=True)

if __name__ == "__main__":
    main()
