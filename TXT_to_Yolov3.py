import xml.etree.ElementTree as element_tree
import os
import glob
import re

regex = re.compile(".*?\((.*?)\)")
project_path = os.getcwd()
data_dir = '/data'
Detection_label_path = 'data/classes.txt'
Dataset_train = "data/train.txt"
Dataset_test = "data/test.txt"
is_subfolder = True

detection_label = []

def ParseTXT(img_folder, file):
    for file_name in os.listdir(img_folder):
        if file_name.endswith('.txt'):
            # Create txt folder
            txt_folder_path = img_folder+'/txt'
            if not os.path.exists(txt_folder_path):
                os.makedirs(txt_folder_path) 
                print(txt_folder_path)

    # Extract content from TXT lines
    for txt_files in glob.glob(img_folder+'/*.txt'):
        txt_file_name = os.path.basename(txt_files)
        txt_file_path = os.path.dirname(os.path.abspath(txt_files))
        txt_file_relpath = os.path.relpath(txt_file_path, project_path) +'/'+txt_file_name
        yolo_format_txt_file = txt_folder_path+'/'+txt_file_name

        # Bounding box for object N "class_name" (Xmin, Ymin) - (Xmax, Ymax) : (101, 26) - (206, 323)
        with open(txt_files, 'r') as txt_file_pascal:
            with open(yolo_format_txt_file, 'w') as txt_file:
                lines = txt_file_pascal.readlines()
                txt_content = ''
                object_name = ''
                img_height = ''
                img_width = ''
                xywh = ''
                obj_index = ''
                for i, line in enumerate(lines):
                    # Image size (X x Y x C) : 396 x 397 x 3
                    if 'Image size' in line:
                        size_line = line.split(":")[1]
                        numbers = re.findall("[0-9.]+", line)
                        w_h = [i for i in numbers[:-1]]
                        img_width = w_h[0]
                        img_height = w_h[1]

                    #Original label for object N "class_name" : "class_name"
                    if 'Original label for object' in line:
                        label_ = line.split(":")[0]
                        label = re.search('"(.*)"', label_)
                        object_name = str(label.group(1))
                        if not object_name == '':
                            if not object_name in detection_label:
                                detection_label.append(object_name)
                                obj_index = detection_label.index(object_name)
                                object_name = str(detection_label[obj_index])
                                print("{} : {}".format(obj_index, object_name))
                                obj_index = ''

                    #Bounding box for object N "class_name" (Xmin, Ymin) - (Xmax, Ymax) : (228, 158) - (370, 436)
                    if 'Bounding box for object' in line:
                        xyxy = line.split(":")[1]
                        xyxy1 = re.findall(regex, xyxy)
                        x1 = float(xyxy1[0].split(", ")[0])
                        y1 = float(xyxy1[0].split(", ")[1])
                        x2 = float(xyxy1[1].split(", ")[0])
                        y2 = float(xyxy1[1].split(", ")[1])

                        x = ((x2-x1)/2+x1)/img_width
                        y = ((y2-y1)/2+y1)/img_height
                        w = (x2-x1)/ img_width
                        h = (y2-y1)/img_height

                        xywh = (str(x)+' '+str(y)+' '+str(w)+' '+str(h))

                    if not object_name == '' and not xywh == '':
                        txt_content = object_name +' '+ xywh +"\n"
                        #print(txt_content)  
                        txt_file.write(txt_content) 
                        txt_content = ''
                        object_name = ''
                        xywh = ''   

def run_TXT_to_YOLOv3():
    with open(Dataset_train, "w") as file:
        print(os.getcwd()+data_dir)
        img_path = os.path.join(os.getcwd()+data_dir)
        if is_subfolder:
            for directory in os.listdir(img_path):
                if not directory.endswith('.txt'):
                    xml_path = os.path.join(img_path, directory)
                    ParseTXT(xml_path, file)
        else:
            ParseTXT(img_path, file)

    print("Dectection_labels:", detection_label)
    with open(Detection_label_path, 'w') as lbl_file:
        for i in range(len(detection_label)):
            lbl_file.write(detection_label[i]+ '\n')

run_TXT_to_YOLOv3()