import streamlit as st

def convert_video_to_binary(video_file):
    with open(video_file, 'rb') as file:
        binary_data = file.read()
    return binary_data

def main():
    st.title("Video to Binary File Converter")

    # File uploader to choose a video file from the local machine
    video_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mkv"])

    if video_file is not None:
        # Convert the video to binary data
        binary_data = convert_video_to_binary(video_file)

        # Provide a link to download the binary file
        st.markdown(get_binary_file_download_link(binary_data), unsafe_allow_html=True)

def get_binary_file_download_link(binary_data):
    # Function to create a download link for binary data
    href = f'<a href="data:video/mp4;base64,{binary_data}" download="video_binary_file.bin">Download Binary File</a>'
    return href

if __name__ == "__main__":
    main()
