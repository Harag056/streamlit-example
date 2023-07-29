import os
import cv2
from PIL import Image
import json
import streamlit as st
import azure.ai.vision as sdk

# Azure Cognitive Services setup
service_options = sdk.VisionServiceOptions(
    "https://bi3va.cognitiveservices.azure.com/",
    "6667acbd346846a4abb0a5e36219de60"
)

analysis_options = sdk.ImageAnalysisOptions()
analysis_options.features = (sdk.ImageAnalysisFeature.TEXT,)
analysis_options.language = "en"
analysis_options.gender_neutral_caption = True

# Helper functions
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

def draw_bounding_boxes_with_text(image, bounding_boxes):
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
    
    json_out=[]


# Streamlit app
def process_image(image_path):
    vision_source = sdk.VisionSource(filename=image_path)
    image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)

    result = image_analyzer.analyze()


    if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
        print("Image height: {}".format(result.image_height))
        print("Image width: {}".format(result.image_width))
        print("Model version: {}".format(result.model_version))

        if result.objects is not None:
            print("Objects:")
            for obj in result.objects:
                print("   '{}', {}, Confidence: {:.4f}".format(obj.name, obj.bounding_box, obj.confidence))

        if result.tags is not None:
            print("Tags:")
            for tag in result.tags:
                print("   '{}', Confidence {:.4f}".format(tag.name, tag.confidence))

        if result.people is not None:
            print("People:")
            for person in result.people:
                print("   {}, Confidence {:.4f}".format(person.bounding_box, person.confidence))

        if result.caption is not None:
            print("Caption:")
            print("   '{}', Confidence {:.4f}".format(result.caption.content, result.caption.confidence))

        lst_bounding_boxes = []

        if result.text is not None:
            print("Text:")
            for line in result.text.lines:
                bounding_boxes = bounding_polygon_to_boxes(line.bounding_polygon)
                tuple_bounding_box = (bounding_boxes, line.content)
                lst_bounding_boxes.append(tuple_bounding_box)
                points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
                print("   Line: '{}', Bounding polygon {}".format(line.content, points_string))

                data = {
                    "image": image_path,
                    "detectedword": line.content,
                    "detectedpolygon": points_string
                }
                json_out.append(data)

                for word in line.words:
                    points_string = "{" + ", ".join([str(int(point)) for point in word.bounding_polygon]) + "}"
                    print("     Word: '{}', Bounding polygon {}, Confidence {:.4f}"
                          .format(word.content, points_string, word.confidence))

        outputimage = annoated_path(image_path, "AI")
        print(lst_bounding_boxes)
        print(outputimage)
        draw_bounding_boxes_with_text(image_path, lst_bounding_boxes, outputimage)
    else:
        error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
        print("Analysis failed.")
        print("   Error reason: {}".format(error_details.reason))
        print("   Error code: {}".format(error_details.error_code))
        print("   Error message: {}".format(error_details.message))



def main():
    st.title("Azure Cognitive Services Vision API Image Analysis")

    # Folder selection
    folder_path = st.text_input("Enter the path to the folder containing images:", "C:\\Users\\HarishSankaranarayan\\Desktop\\test")
    if not os.path.isdir(folder_path):
        st.error("Invalid directory path.")
        return

    if st.button("Analyze Images"):
        # Process each image in the folder
        st.text("Processing images... Please wait.")
        for image_file in os.listdir(folder_path):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(folder_path, image_file)
                process_image(image_path)
        st.text("Image analysis completed.")

        # Save output JSON
        with open(os.path.join(folder_path, "AI", "output.json"), "w") as json_file:
            json.dump(json_out, json_file)

if __name__ == "__main__":
    main()
