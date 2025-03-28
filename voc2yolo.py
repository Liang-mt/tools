# 将VOC格式标注文件（xml文件）转换成Yolo格式标注文件（txt文件）

import xml.etree.ElementTree as ET
import os

voc_folder = r"C:/Users/28645/Desktop/血型/Annotations/"  # 储存voc格式的标注文件的文件夹，相对路径
yolo_folder = r"C:/Users/28645/Desktop/血型/yolo_label/"  # 转换后的yolo格式标注文件的储存文件夹，相对路径

class_id = ["A", "B", "AB", "O"]  # 储存数据集中目标种类名称的列表，接下来的转换函数中会将该列表中种类名称对应的列表索引号作为写入yolo标注文件中该类目标的种类序号


# voc标注的目标框坐标值转换到yolo标注的目标框坐标值的函数
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


# 对单个voc标注文件进行转换成其对应的yolo文件的函数
def convert_annotation(xml_file):

    file_name = xml_file.strip(".xml")  # 这一步将所有voc格式标注文件取出后缀名“.xml”，方便接下来作为yolo格式标注文件的名称
    in_file = open(os.path.join(voc_folder, xml_file))  # 打开当前转换的voc标注文件
    out_file = open(os.path.join(yolo_folder, file_name + ".txt", ), 'w')  # 创建并打开要转换成的yolo格式标注文件
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        cls = obj.find('name').text
        cls_id = class_id.index(cls)
        b = (float(0),
             float(w),
             float(0),
             float(h))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


xml_fileList = os.listdir(voc_folder)  # 将所有voc格式的标注文件的名称取出存放到列表xml_fileList中
for xml_file in xml_fileList:  # 这里的for循环开始依次对所有voc格式标注文件生成其对应的yolo格式的标注文件
    convert_annotation(xml_file)

print("success！")


