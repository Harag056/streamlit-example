import streamlit as st
import snowflake.connector
from PIL import Image
import io
import cv2


st.title("Snowflake Connection App")

# Input fields for Snowflake connection parameters
# snowflake_account = st.text_input("Snowflake Account", "")
# snowflake_user = st.text_input("User", "")
# snowflake_password = st.text_input("Password", "", type="password")
# snowflake_warehouse = st.text_input("Warehouse", "")
# snowflake_database = st.text_input("Database", "")
# snowflake_schema = st.text_input("Schema", "")

# snowflake_username = 'TESTUSER'
# snowflake_password = 'Test@123'
# snowflake_account = 'rz20203.central-india.azure'
# snowflake_warehouse = 'COMPUTE_WH'
# snowflake_database = 'LandingAI_DB'
# snowflake_schema = 'Raw'

# # Function to connect to Snowflake
# def connect_to_snowflake():
#     conn = snowflake.connector.connect(
#         user=snowflake_username,
#         password=snowflake_password,
#         account=snowflake_account,
#         warehouse=snowflake_warehouse,
#         database=snowflake_database,
#         schema=snowflake_schema
#     )
#     return conn

def convert_binary_to_video(binary_data):
    # Implement your binary to video conversion logic here
    # For example, if the binary_data is a video file in MP4 format, you can save it to a temporary file and return the file path.
    # In this example, we assume the binary_data is already in video format (e.g., MP4).

    # For demonstration purposes, we'll simply return the binary_data as is.
    return binary_data

# Function to execute a Snowflake query and return results
# def execute_query(conn, query):
#     cursor = conn.cursor()
#     cursor.execute(query)
#     results = cursor.fetchall()
#     cursor.close()
#     return results

# Streamlit app
def main():
     st.title("Binary to Video Converter")

    uploaded_file = st.file_uploader("Upload a binary video file", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        # Read the binary file and convert it to video
        video_binary_data = uploaded_file.read()
        converted_video = convert_binary_to_video(video_binary_data)

        # Display the converted video
        st.video(converted_video)
    st.title("Snowflake Data Viewer")
    
    # Connect to Snowflake
    # try:
    #     conn = connect_to_snowflake()
    #     st.success("Connected to Snowflake")
    # except Exception as e:
    #     st.error(f"Error connecting to Snowflake: {str(e)}")
    #     return
    
    # # Query input
    # query_input = st.text_area("Enter your Snowflake SQL query:")
    
    # if st.button("Run Query"):
    #     # Execute the query and display results
    #     try:
    #         results = execute_query(conn, query_input)
    #         if results:
    #             st.table(results)
    #         else:
    #             st.info("No results to display.")
    #     except Exception as e:
    #         st.error(f"Error executing query: {str(e)}")
    
    # # Close the Snowflake connection when the app is closed
    # st.experimental_rerun_on_finish(connect_to_snowflake)
    # conn.close()





   



if __name__ == "__main__":
    main()
