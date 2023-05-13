import cv2
import numpy as np
import cv2
import math
import os
def find_bars(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper color range for the bars
    lower_color_range = np.array([0, 50, 50], dtype=np.uint8)
    upper_color_range = np.array([180, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_color_range, upper_color_range)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bars = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
#         print(area)
        if h > 0 and area > 0:
            bars.append((x, y, x + w, y + h))
    return bars 


data=[]
def draw_bounding_boxes(image_path, image, bars, label_gap=5, label_height=22):

    # Find the origin point of the chart
    origin_x = float('inf')
    origin_y = float('-inf')
    for bar in bars:
        x1, y1, x2, y2 = bar
        if x1 < origin_x:
            origin_x = x1
        if y2 > origin_y:
            origin_y = y2
    cv2.circle(image, (origin_x-6, origin_y), 5, (255, 0, 0), 5)

    # Initialize the output dictionary
    output_dict = {
        "categories": [],
        "annotations": [],
        "images": []
    }
    
    # Define the categories
    category_dict = {
        "supercategory": "bar",
        "id": 1,
        "name": "first bar",
        "keypoints": [
            "origin","y-axis", "top left","bottom right","bottom center ",
            "top left label", "bottom right label"
        ],
        "skeleton": [
            [1,2],[2,3],[3,4],[4,5],[5,6],[6,7]
        ]
    }
    output_dict["categories"].append(category_dict)

    # Draw bounding boxes, center point, and circles on each bar
    for i, bar in enumerate(bars):
        x1, y1, x2, y2 = bar
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        x_center = int((x1 + x2) / 2)
        y_center = int((y1 + y2) / 2)
        y_top = y1
        y_bottom = y2
        
        cv2.circle(image, (x_center, y_bottom), 2, (0, 0, 255), 3)
        cv2.circle(image, (origin_x - 7 , y_top), 2, (0, 0, 255), 3)

        # Draw circles on the top left and bottom right
        cv2.circle(image, (x1, y1), 3, (0, 0, 0), 3)
        cv2.circle(image, (x2, y2), 3, (0, 0, 0), 3)
        cv2.line(image, (x1, y_top), (x2, y2), (0, 0, 0), 1)  # top-right to bottom-left
        
        
        cv2.line(image, (origin_x-7, origin_y), (origin_x - 7 , y_top), (0, 0, 0), 1)
        cv2.line(image, (x1, y_top), (origin_x - 7 , y_top), (0, 0, 0),1 )
        cv2.line(image, (x_center, y_bottom), (x2, y2), (0, 0, 0),1 )

        
        
        label_x1 = x1 + label_gap
        label_y1 = y2 + label_gap
        label_x2 = x2 - label_gap
        label_y2 = label_y1 + label_height
        cv2.rectangle(image, (label_x1, label_y1), (label_x2, label_y2), (0,0, 255), 1)

        cv2.line(image, (x_center, y_bottom), (label_x1, label_y1), (0, 0, 0), 1)
        cv2.line(image, (label_x1, label_y1), (label_x2, label_y2), (0, 0, 0), 1)
#         cv2.line(image, (x1, y_top), (x2, y2), (255, 0, 0), 2)
        

        # Define the annotation
        annotation_dict = {
            "image_id":0 , # Set to 0 for simplicity
            "category_id": 1,
            "id": i+1,
            "bbox": [x1, y1, x2-x1, y2-y1],
            "area": (x2-x1)*(y2-y1),
            "iscrowd": 0,
            "keypoints": [
                origin_x -7, origin_y, # origin
                origin_x, y_top, # y-axis
                x1, y1, # top left
                x2, y2, # bottom right
                x_center, y_bottom, # bottom center
                x1+label_gap, y2+label_gap, # top left label
                x2-label_gap, y2+label_gap # bottom right label
            ],
            "num_keypoints": 7
        }
        output_dict["annotations"].append(annotation_dict)
        image_dict = {
            "id": 0,
            "width": image.shape[1],
            "height": image.shape[0],
            "file_name": image_path
        }
        output_dict["images"].append(image_dict)
    data.append(output_dict)
    with open('key_points.json', 'w') as f:
        json.dump(data, f)
    return image


image_folder = "C:/Users/A.Basit/Desktop/bar"
for image_name in os.listdir(image_folder):
    image_path = os.path.join(image_folder, image_name)
    print(image_path)
    image = cv2.imread(image_path)
    bars = find_bars(image)
    output_image = draw_bounding_boxes(image_path,image, bars)
    cv2.imwrite(f"output_{image_name}", output_image)