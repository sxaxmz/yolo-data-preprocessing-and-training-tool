import cv2
import numpy as np
import glob
import re
    
'''
# Traditional yolov3 detection
def detect_rectangles(detection, img):
    print(detection[0], detection[1], detection[2], detection[3])
    img = cv2.imread(img)
    height, width, channels = img.shape
    obj_x_center = int(detection[0] * width)
    obj_y_center = int(detection[1] * height)
    w = int(detection[2] * width)
    h = int(detection[3] * height)
    x = int(obj_x_center - w / 2) # Top Left
    y = int(obj_y_center -  h / 2) # Top Left
    print(x, y, w, h)
    return [x, y, w, h]
'''

# Modified based on pascal to yolo conversion
def detect_rectangles(detection, img):
    img = cv2.imread(img)
    height, width, channels = img.shape
    x = int(detection[0] * width)
    y = int(detection[1] * height)
    w = int(detection[2] * width)
    h = int(detection[3] * height)
    return [x, y, w, h]  

white_color = (255, 255, 255)
black_color = (0, 0, 0)
blue_color = (260, 0, 0)
green_color = (0, 260, 0)
yellow_color = (255, 211, 67)
red_color = (0, 0, 260)

list_imgs_path = glob.glob(r"data/images/*.png", recursive=True)
list_txt_path = glob.glob(r"data/Annotation/txt/*.txt", recursive=True)

detect_accuracies = []
detect_objects = []
detected_rectangles = [[]]

classes = []
with open('vehicle.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
print(classes)

for i, file in enumerate(list_txt_path):
        detected_rectangles.append([])
        with open(file, "r") as img_txt:
            lines = img_txt.readlines()
            for line in lines:
                object_name = re.findall('[aA-zZ]+', line)
                rx = re.compile(r"\d[\d().]+")
                numbers = rx.findall(line)
                numbers = [float(number) for number in numbers]
                if object_name[0] in classes:
                    detect_objects.append(classes.index(object_name[0]))
                    detection = [numbers[0], numbers[1], numbers[2], numbers[3]]
                    detected_rectangles[i].append(detect_rectangles(detection, list_imgs_path[i]))

'''
for i in range(len(detected_rectangles)):
    if i in unique_detected_objects:
        # Detection Accuracy Color Labeling      
        if 90 < detect_accuracies[i]:
            detection_color = green_color
        if 70 < detect_accuracies[i] < 90:
            detection_color = yellow_color
        if 50 < detect_accuracies[i] < 70:
            detection_color = red_color     
'''   
for i, img in enumerate(list_imgs_path): 
    if i == 3:
        break  
    else:
        img = cv2.imread(img)
        for j in range(len(detected_rectangles[i])):
            x, y, w, h = detected_rectangles[i][j]
            detected_label = classes[detect_objects[i]]
            cv2.putText(img, "{}".format(detected_label), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, green_color)
            cv2.rectangle(img, (x, y), (x + w, y + h), green_color, 2)
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()      