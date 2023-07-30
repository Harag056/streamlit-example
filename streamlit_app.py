import os
import cv2
import json
import streamlit as st
import azure.ai.vision as sdk


output_image=""

    # Load the Azure AI Vision SDK service options
service_options = sdk.VisionServiceOptions(
        "https://bi3va.cognitiveservices.azure.com/",
        "6667acbd346846a4abb0a5e36219de60"
    )
analysis_options = sdk.ImageAnalysisOptions()
analysis_options.features = (sdk.ImageAnalysisFeature.TEXT,)
analysis_options.language = "en"
analysis_options.gender_neutral_caption = True

def annotated_path(input_path, new_folder="annotated"):
    folder_path, file_name = os.path.split(input_path)
    new_folder_path = os.path.join(folder_path, new_folder)
    new_file_path = os.path.join(new_folder_path, file_name)
    return new_file_path

def calculate_bounding_box(bounding_boxes):
    min_x = float('inf')
    min_y = float('inf')
    max_width = 0
    max_height = 0

    for box in bounding_boxes:
        x, y, width, height = box
        # Find the minimum x and y coordinates
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        # Find the maximum width and height
        max_width = max(max_width, width)
        max_height = max(max_height, height)

    return int(min_x), int(min_y), int(max_width), int(max_height)

def bounding_polygon_to_boxes(bounding_polygon):
    bounding_boxes = []
    num_points = len(bounding_polygon)

    for i in range(0, num_points, 2):
        x1, y1 = bounding_polygon[i], bounding_polygon[i + 1]

        if i + 2 < num_points:
            x2, y2 = bounding_polygon[i + 2], bounding_polygon[i + 3]
        else:
            # If the last point is reached, connect it to the first point to close the polygon
            x2, y2 = bounding_polygon[0], bounding_polygon[1]

        # Find the minimum and maximum coordinates for each axis
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)

        # Add the bounding box to the list
        bounding_boxes.append((min_x, min_y, max_x - min_x, max_y - min_y))

    return bounding_boxes

def draw_bounding_boxes_with_text(image_path, bounding_boxes, output_path):
    # Step 1: Load the image
    image = cv2.imread(image_path)

    for boxes, text in bounding_boxes:
        if len(boxes) > 0:
            # Draw the first bounding box in each element of the input_data array
            x, y, w, h = map(int, boxes[0])
            x, y, w, h = calculate_bounding_box(boxes)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Save the result
    cv2.imwrite(output_path, image)

json_out = []

# Function to process image and get bounding boxes with text
def process_image(image_path):
    vision_source = sdk.VisionSource(filename=image_path)
    image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)
    result = image_analyzer.analyze()

    if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
        st.write("Image height:", result.image_height)
        st.write("Image width:", result.image_width)
        st.write("Model version:", result.model_version)

        if result.objects is not None:
            st.write("Objects:")
            for obj in result.objects:
                st.write("   '{}', {}, Confidence: {:.4f}".format(obj.name, obj.bounding_box, obj.confidence))

        if result.tags is not None:
            st.write("Tags:")
            for tag in result.tags:
                st.write("   '{}', Confidence {:.4f}".format(tag.name, tag.confidence))

        if result.people is not None:
            st.write("People:")
            for person in result.people:
                st.write("   {}, Confidence {:.4f}".format(person.bounding_box, person.confidence))

        if result.caption is not None:
            st.write("Caption:")
            st.write("   '{}', Confidence {:.4f}".format(result.caption.content, result.caption.confidence))

        lst_bounding_boxes = []

        if result.text is not None:
            st.write("Text:")
            for line in result.text.lines:
                bounding_boxes = bounding_polygon_to_boxes(line.bounding_polygon)
                tuple_bounding_box = (bounding_boxes, line.content)
                lst_bounding_boxes.append(tuple_bounding_box)
                points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
                st.write("   Line: '{}', Bounding polygon {}".format(line.content, points_string))

                data = {
                    "image": image_path,
                    "detectedword": line.content,
                    "detectedpolygon": points_string
                }
                json_out.append(data)

                for word in line.words:
                    points_string = "{" + ", ".join([str(int(point)) for point in word.bounding_polygon]) + "}"
                    st.write("     Word: '{}', Bounding polygon {}, Confidence {:.4f}"
                             .format(word.content, points_string, word.confidence))

        output_image = annotated_path(image_path, "AI")
        st.write(lst_bounding_boxes)
        st.write("output_image::",output_image)
        draw_bounding_boxes_with_text(image_path, lst_bounding_boxes, output_image)
    else:
        error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
        st.write("Analysis failed.")
        st.write("Error reason:", error_details.reason)
        st.write("Error code:", error_details.error_code)
        st.write("Error message:", error_details.message)


# Function to iterate over images in a folder and process them
def iterate_images_in_folder(folder_path):
    # Check if the given path is a directory
    if not os.path.isdir(folder_path):
        st.write("Invalid directory path.")
        return

    # List all the files in the directory
    file_list = os.listdir(folder_path)

    # Filter files to get only image files (you can add more extensions if needed)
    image_files = [f for f in file_list if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Process each image
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        process_image(image_path)


def display_images():
    image_files = annotated_path(image_path, "AI")
    st.write(image_files)
    
    for image_file in image_files:
        if image_file.endswith(("png", "jpg", "jpeg", "gif")):
            st.write(image_file)
            image_path = os.path.join(folder_path, "AI", image_file)
            st.write(image_path)
            st.image(image_path,caption=image_file,use_column_width=True)

# Streamlit app code
def main():
    st.title("Image Analysis with Azure Vision API")

    # File uploader to select the folder with images
    folder_path = st.text_input("Select a folder", "C:\\Users\\HarishSankaranarayan\\Desktop\\test\\")
    #folder_path = st.file_uploader("Select a folder with images", type=["png", "jpg", "jpeg", "gif"])
        # Create a button to start image analysis
    if st.button("Analyze Images"):
        st.write("Processing images...")
        iterate_images_in_folder(folder_path)
        st.write("Image analysis completed!")

        # Save the JSON output to a file
        json_output_path = os.path.join(folder_path, "AI", "output.json")
        with open(json_output_path, "w") as json_file:
            json.dump(json_out, json_file)

        # Display the processed images
    display_images()
    # image_files = annotated_path(image_path, "AI")
    # st.write(image_files)
    
    # for image_file in image_files:
    #     if image_file.endswith(("png", "jpg", "jpeg", "gif")):
    #         st.write(image_file)
    #         image_path = os.path.join(folder_path, "AI", image_file)
    #         st.write(image_path)
    #         st.image(image_path,caption=image_file,use_column_width=True)
            #st.image("C:\\Users\\HarishSankaranarayan\\Desktop\\test\\1644269774_vehicles.jpg")

# Run the Streamlit app
if __name__ == "__main__":
    main()
