# # -*- coding: utf-8 -*-
#
# import json
# import os
#
#
# def convert_coco_to_yolov5(annotations_file, output_dir):
#     with open(annotations_file, 'r') as f:
#         data = json.load(f)
#
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#
#     images = {}
#     for image in data['images']:
#         images[image['id']] = {'file_name': image['file_name'], 'width': image['width'], 'height': image['height']}
#
#     for annotation in data['annotations']:
#         category_id = annotation['category_id']
#         image_id = annotation['image_id']
#         image = images[image_id]
#
#         # os.path.splitext(image['file_name'])将图像文件名（例如："image001.jpg"）分为两部分：文件名（不包括扩展名）和扩展名。
#         # 这个函数返回一个包含两个元素的元组，第一个元素是文件名（不包括扩展名），第二个元素是扩展名。
#         file_name = os.path.splitext(image['file_name'])[0] + '.txt'
#         output_path = os.path.join(output_dir, file_name)
#
#         # 首先，检查所有轮廓线信息是否属于相同的物体类别
#         category_id = annotation.get('category_id')
#         if category_id is None:
#             raise ValueError('category_id is missing in the annotation')
#
#         # 然后，遍历所有轮廓线信息并进行归一化处理
#         for segmentation in annotation['segmentation']:
#             normalized_coordinates = [coord / image['width'] if index % 2 == 0 else coord / image['height']
#                                       for index, coord in enumerate(segmentation)]
#
#             # 最后，将归一化后的信息写入文件中
#             with open(output_path, 'a') as f:
#                 f.write(f"{category_id} " + " ".join(map(str, normalized_coordinates)) + "\n")
#
#
# if __name__ == '__main__':
#     # annotations_file = r'D:\segment-anything\example_dataset\annotations.json'
#     # output_dir = r'D:\segment-anything\example_dataset'
#     annotations_file = r"./coco/annotations/instances_train2017.json"
#     output_dir = r"./coco"
#     convert_coco_to_yolov5(annotations_file, output_dir)


"""
author: Wu
https://github.com/Weifeng-Chen/DL_tools/issues/3
2021/1/24
COCO 格式的数据集转化为 YOLO 格式的数据集，源代码采取遍历方式，太慢，
这里改进了一下时间复杂度，从O(nm)改为O(n+m)，但是牺牲了一些内存占用
--json_path 输入的json文件路径
--save_path 保存的文件夹名字，默认为当前目录下的labels。
"""

import os
import json
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--json_path', default='./coco/annotations/instances_train2017.json', type=str, help="input: coco format(json)")
parser.add_argument('--save_path', default='./coco/labels', type=str, help="specify where to save the output dir of labels")
arg = parser.parse_args()


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = box[0] + box[2] / 2.0
    y = box[1] + box[3] / 2.0
    w = box[2]
    h = box[3]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


if __name__ == '__main__':
    json_file = arg.json_path  # COCO Object Instance 类型的标注
    ana_txt_save_path = arg.save_path  # 保存的路径

    data = json.load(open(json_file, 'r'))
    if not os.path.exists(ana_txt_save_path):
        os.makedirs(ana_txt_save_path)

    id_map = {}  # coco数据集的id不连续！重新映射一下再输出！
    for i, category in enumerate(data['categories']):
        id_map[category['id']] = i

    # 通过事先建表来降低时间复杂度
    max_id = 0
    for img in data['images']:
        max_id = max(max_id, img['id'])
    # 注意这里不能写作 [[]]*(max_id+1)，否则列表内的空列表共享地址
    img_ann_dict = [[] for i in range(max_id + 1)]
    for i, ann in enumerate(data['annotations']):
        img_ann_dict[ann['image_id']].append(i)

    for img in tqdm(data['images']):
        filename = img["file_name"]
        img_width = img["width"]
        img_height = img["height"]
        img_id = img["id"]
        head, tail = os.path.splitext(filename)
        ana_txt_name = head + ".txt"  # 对应的txt名字，与jpg一致
        f_txt = open(os.path.join(ana_txt_save_path, ana_txt_name), 'w')
        '''for ann in data['annotations']:
            if ann['image_id'] == img_id:
                box = convert((img_width, img_height), ann["bbox"])
                f_txt.write("%s %s %s %s %s\n" % (id_map[ann["category_id"]], box[0], box[1], box[2], box[3]))'''
        # 这里可以直接查表而无需重复遍历
        for ann_id in img_ann_dict[img_id]:
            ann = data['annotations'][ann_id]
            box = convert((img_width, img_height), ann["bbox"])
            f_txt.write("%s %s %s %s %s\n" % (id_map[ann["category_id"]], box[0], box[1], box[2], box[3]))
        f_txt.close()
