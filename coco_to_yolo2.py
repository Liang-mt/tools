import json
import os
import numpy as np
from copy import deepcopy
import cv2


def xywh2yolo(rect,landmarks_sort,imageheight,imagewidth):
    h = imageheight
    w = imagewidth

    rect[0] = 0
    rect[1] = 0
    rect[2] = w
    rect[3] = h
    annotation = np.zeros((1, 7))
    annotation[0, 0] = (rect[0] + rect[2] / 2) / w  # cx
    annotation[0, 1] = (rect[1] + rect[3] / 2) / h  # cy
    annotation[0, 2] = rect[2] / w  # w
    annotation[0, 3] = rect[3] / h  # h

    annotation[0, 4] = landmarks_sort[0][0] / w  # l0_x
    annotation[0, 5] = landmarks_sort[0][1] / h  # l0_y
    annotation[0, 6] = 2.0000


    return annotation




if __name__ == "__main__":
    pic_file = r"C:/Users/28645/Desktop/keypoints/val"
    file_path = r"C:/Users/28645/Desktop/keypoints/val"
    save_small_path = r"C:/Users/28645/Desktop/keypoints/labels"
    #label_file = ['no_red', 'no_blue']
    label_file = ['KPT']
    for root, dirs, files in os.walk(pic_file):
            for file in files:
                if file.endswith(".png"):
                    image_file = os.path.join(root, file)
                    corresponding_json_file = os.path.join(file_path, file.replace(".png", ".json"))
                    txt_file = file.replace(".png", ".txt")
                    txt_path = os.path.join(save_small_path, txt_file)

                    if os.path.exists(corresponding_json_file):
                        with open(corresponding_json_file, 'r', encoding='utf-8') as f:
                            data_dict = json.load(f)
                        image_height = data_dict["imageHeight"]
                        image_width = data_dict["imageWidth"]
                        with open(txt_path, "w") as f:
                            for data_message in data_dict['shapes']:
                                label = data_message['label']
                                points = data_message['points']
                                pts = np.array(points)
                                rect = np.array([np.min(pts[:, 0]), np.min(pts[:, 1]), np.max(pts[:, 0]), np.max(pts[:, 1])])
                                rect1 = deepcopy(rect)
                                annotation = xywh2yolo(rect1, pts, image_height, image_width)

                                str_label = str(label_file.index(label)) + " "
                                str_label += ' '.join(map(str, annotation.ravel())) + "\n"

                                f.write(str_label)

                        print("Converted:", corresponding_json_file)
                    else:
                        open(txt_path, 'a').close()  # 创建空的.txt文件

                        print("No corresponding json file for:", image_file)
