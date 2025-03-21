import cv2
import os
import numpy as np
from PIL import Image


def yolo_to_yolo_keypoints(img, x):
    img_w, img_h = img.size
    label, x, y, w, h = x
    x_t = x * img_w
    y_t = y * img_h
    w_t = w * img_w
    h_t = h * img_h

    x1 = (x_t - w_t / 2) / img_w
    y1 = (y_t - h_t / 2) / img_h

    x2 = (x_t + w_t / 2) / img_w
    y2 = (y_t - h_t / 2) / img_h

    x3 = (x_t + w_t / 2) / img_w
    y3 = (y_t + h_t / 2) / img_h

    x4 = (x_t - w_t / 2) / img_w
    y4 = (y_t + h_t / 2) / img_h

    return (label, x, y, w, h, x1, y1, x2, y2, x3, y3, x4, y4)


# 获取图片和标签文件的路径列表
image_dir = "./testhel/train/images/"
label_dir = "./testhel/train/labels/"
image_files = os.listdir(image_dir)
label_files = os.listdir(label_dir)

# 创建一个新的文件夹来存放转换后的标签文件
new_label_dir = "./testhel/train/labels2/"
if not os.path.exists(new_label_dir):
    os.makedirs(new_label_dir)

# 遍历每个文件，调用函数，写入新的标签文件
for image_file, label_file in zip(image_files, label_files):
    image_path = os.path.join(image_dir, image_file)
    label_path = os.path.join(label_dir, label_file)
    new_label_path = os.path.join(new_label_dir, label_file)

    # 读取图片和标签文件
    img = Image.open(image_path)
    with open(label_path, 'r') as f:
        lb = np.array([x.split() for x in f.read().strip().splitlines()], dtype=np.float32)  # labels

    # 对每个标签，调用函数，得到转换后的坐标
    new_lb = []
    for x in lb:
        test = yolo_to_yolo_keypoints(img, x)
        new_lb.append(test)

    # 写入新的标签文件，每行一个标签，用空格分隔
    with open(new_label_path, 'w') as f:
        for test in new_lb:
            test_str = ' '.join(map(str, test))  # 把元组转换成字符串
            f.write(test_str + '\n')  # 写入一行
