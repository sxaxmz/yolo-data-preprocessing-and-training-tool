import xml.etree.ElementTree as element_tree
import os
import glob

data_dir = '/data/licenses-plate'
Detection_label_path = 'data/licenses-plate/classes.txt'
Dataset_train = "data/licenses-plate/train.txt"
Dataset_test = "data/licenses-plate/test.txt"
is_subfolder = True

detection_label = []

def ParseXML(img_folder, file):
    for file_name in os.listdir(img_folder):
        if file_name.endswith('.xml'):
            # Create txt folder
            txt_folder_path = img_folder+'/txt'
            if not os.path.exists(txt_folder_path):
                os.makedirs(txt_folder_path) 
                print(txt_folder_path)

    # Extract content from XML tags
    for xml_file in glob.glob(img_folder+'/*.xml'):
        tree = element_tree.parse(open(xml_file))
        root = tree.getroot()
        image_file_name = root.find('filename').text 
        xmlsize = root.find('size')
        img_width = int(xmlsize.find('width').text)
        img_height = int(xmlsize.find('height').text)
        image_name, image_extension = os.path.splitext(image_file_name)
        img_path = img_folder+'/'+image_file_name
        txt_file_name = txt_folder_path+'/'+image_name+'.txt'

        # Iterate each object
        for i, obj in enumerate(root.iter('object')):
            difficult = obj.find('difficult').text
            object_name = obj.find('name').text
            if object_name not in detection_label:
                detection_label.append(object_name)
            txt_content = object_name   
            object_id = detection_label.index(object_name)
            xmlbox = obj.find('bndbox') 
            x1 = int(float(xmlbox.find('xmin').text))
            y1 = int(float(xmlbox.find('ymin').text))
            x2 = int(float(xmlbox.find('xmax').text))
            y2 = int(float(xmlbox.find('ymax').text))
            x = ((x2-x1)/2+x1)/img_width
            y = ((y2-y1)/2+y1)/img_height
            w = (x2-x1)/ img_width
            h = (y2-y1)/img_height
            xyxy = (str(x)+' '+str(y)+' '+str(w)+' '+str(h)+' ')

            img_path += ' '+ xyxy
            txt_content += ' '+ xyxy

            with open(txt_file_name, 'a') as txt_file:
                txt_file.write(txt_content+'\n')

        file.write(img_path+'\n')

def run_XML_to_YOLOv3():
    for i, folder in enumerate(['train','test']):
        with open([Dataset_train,Dataset_test][i], "w") as file:
            print(os.getcwd()+data_dir+'/'+folder)
            img_path = os.path.join(os.getcwd()+data_dir+'/'+folder)
            if is_subfolder:
                for directory in os.listdir(img_path):
                    xml_path = os.path.join(img_path, directory)
                    ParseXML(xml_path, file)
            else:
                ParseXML(img_path, file)

    print("Dectection_labels:", detection_label)
    with open(Detection_label_path, 'w') as lbl_file:
        for i in range(len(detection_label)):
            lbl_file.write(detection_label[i]+ '\n')

run_XML_to_YOLOv3()