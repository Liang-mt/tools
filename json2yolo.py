import json
import os
import numpy as np
from copy import deepcopy
import cv2

def xywh2yolo_armor(model,rect,landmarks_sort,imageheight,imagewidth):
    h = imageheight
    w = imagewidth
    if model == "1":

        annotation = np.zeros((1, 8))

        annotation[0, 0] = landmarks_sort[0][0] / w  # l0_x
        annotation[0, 1] = landmarks_sort[0][1] / h  # l0_y
        annotation[0, 2] = landmarks_sort[1][0] / w  # l1_x
        annotation[0, 3] = landmarks_sort[1][1] / h  # l1_y
        annotation[0, 4] = landmarks_sort[2][0] / w  # l2_x
        annotation[0, 5] = landmarks_sort[2][1] / h  # l2_y
        annotation[0, 6] = landmarks_sort[3][0] / w  # l3_x
        annotation[0, 7] = landmarks_sort[3][1] / h  # l3_y


    if model == "2":
        rect[0] = max(0, rect[0])
        rect[1] = max(0, rect[1])
        rect[2] = min(w - 1, rect[2]-rect[0])
        rect[3] = min(h - 1, rect[3]-rect[1])
        annotation = np.zeros((1, 12))
        annotation[0, 0] = (rect[0] + rect[2] / 2) / w  # cx
        annotation[0, 1] = (rect[1] + rect[3] / 2) / h  # cy
        annotation[0, 2] = rect[2] / w  # w
        annotation[0, 3] = rect[3] / h  # h

        annotation[0, 4] = landmarks_sort[0][0] / w  # l0_x
        annotation[0, 5] = landmarks_sort[0][1] / h  # l0_y
        annotation[0, 6] = landmarks_sort[1][0] / w  # l1_x
        annotation[0, 7] = landmarks_sort[1][1] / h  # l1_y
        annotation[0, 8] = landmarks_sort[2][0] / w  # l2_x
        annotation[0, 9] = landmarks_sort[2][1] / h # l2_y
        annotation[0, 10] = landmarks_sort[3][0] / w  # l3_x
        annotation[0, 11] = landmarks_sort[3][1] / h  # l3_y



    return annotation

def xywh2yolo_buff(model,rect,landmarks_sort,imageheight,imagewidth):
    h = imageheight
    w = imagewidth
    if model == "1":

        annotation = np.zeros((1, 10))

        annotation[0, 0] = landmarks_sort[0][0] / w  # l0_x
        annotation[0, 1] = landmarks_sort[0][1] / h  # l0_y
        annotation[0, 2] = landmarks_sort[1][0] / w  # l1_x
        annotation[0, 3] = landmarks_sort[1][1] / h  # l1_y
        annotation[0, 4] = landmarks_sort[2][0] / w  # l2_x
        annotation[0, 5] = landmarks_sort[2][1] / h  # l2_y
        annotation[0, 6] = landmarks_sort[3][0] / w  # l3_x
        annotation[0, 7] = landmarks_sort[3][1] / h  # l3_y
        annotation[0, 8] = landmarks_sort[4][0] / w  # l4_x
        annotation[0, 9] = landmarks_sort[4][1] / h  # l4_y

    if model == "2":
        rect[0] = max(0, rect[0])
        rect[1] = max(0, rect[1])
        rect[2] = min(w - 1, rect[2]-rect[0])
        rect[3] = min(h - 1, rect[3]-rect[1])
        annotation = np.zeros((1, 14))
        annotation[0, 0] = (rect[0] + rect[2] / 2) / w  # cx
        annotation[0, 1] = (rect[1] + rect[3] / 2) / h  # cy
        annotation[0, 2] = rect[2] / w  # w
        annotation[0, 3] = rect[3] / h  # h

        annotation[0, 4] = landmarks_sort[0][0] / w  # l0_x
        annotation[0, 5] = landmarks_sort[0][1] / h  # l0_y
        annotation[0, 6] = landmarks_sort[1][0] / w  # l1_x
        annotation[0, 7] = landmarks_sort[1][1] / h  # l1_y
        annotation[0, 8] = landmarks_sort[2][0] / w  # l2_x
        annotation[0, 9] = landmarks_sort[2][1] / h # l2_y
        annotation[0, 10] = landmarks_sort[3][0] / w  # l3_x
        annotation[0, 11] = landmarks_sort[3][1] / h  # l3_y
        annotation[0, 12] = landmarks_sort[4][0] / w  # l4_x
        annotation[0, 13] = landmarks_sort[4][1] / h  # l4_y


    return annotation

def order_points(pts):
    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


if __name__ == "__main__":
    model = input("1纯关键点格式/2yoloface格式: ")
    pic_file = r"C:/Users/28645/Desktop/buff_total/liang2_"
    file_path = r"C:/Users/28645/Desktop/buff_total/labels"
    save_small_path = r"C:/Users/28645/Desktop/buff_total/keypointlabel"
    #label_file = ['no_red', 'no_blue']
    label_file = ['0', '1','2', '3']
    for root, dirs, files in os.walk(pic_file):
            for file in files:
                if file.endswith(".jpg"):
                    image_file = os.path.join(root, file)
                    corresponding_json_file = os.path.join(file_path, file.replace(".jpg", ".json"))
                    txt_file = file.replace(".jpg", ".txt")
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
                                annotation = xywh2yolo_buff(model, rect1, pts, image_height, image_width)

                                str_label = str(label_file.index(label)) + " "
                                str_label += ' '.join(map(str, annotation.ravel())) + "\n"

                                f.write(str_label)

                        print("Converted:", corresponding_json_file)
                    else:
                        open(txt_path, 'a').close()  # 创建空的.txt文件

                        print("No corresponding json file for:", image_file)
