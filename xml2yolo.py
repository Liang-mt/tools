import xml.etree.ElementTree as ET
import os


def convert_annotation(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取图像尺寸
    size = root.find('size')
    img_width = int(size.find('width').text)
    img_height = int(size.find('height').text)

    txt_lines = []

    for obj in root.findall('object'):
        class_name = obj.find('name').text
        class_idx = None

        # 汽车类别处理逻辑
        if class_name == 'car':
            #difficulty = int(obj.find('difficulty').text)
            class_idx = 0  #car →  0

        # 装甲板类别处理逻辑
        elif class_name == 'armor':
            color = obj.find('armor_color').text.strip().lower()
            if color == 'red':
                class_idx = 1  # 红色装甲板 → 1
            elif color == 'blue':
                class_idx = 2  # 蓝色装甲板 → 2

        if class_idx is None:
            continue  # 跳过未定义类别

        # 坐标转换
        bbox = obj.find('bndbox')
        xmin = float(bbox.find('xmin').text)
        ymin = float(bbox.find('ymin').text)
        xmax = float(bbox.find('xmax').text)
        ymax = float(bbox.find('ymax').text)

        # 归一化计算（保留6位小数）
        x_center = round((xmin + xmax) / (2 * img_width), 6)
        y_center = round((ymin + ymax) / (2 * img_height), 6)
        w = round((xmax - xmin) / img_width, 6)
        h = round((ymax - ymin) / img_height, 6)

        # 边界检查（防止超出[0,1]范围）
        x_center = max(0.0, min(1.0, x_center))
        y_center = max(0.0, min(1.0, y_center))
        w = max(0.0, min(1.0, w))
        h = max(0.0, min(1.0, h))

        txt_lines.append(f"{class_idx} {x_center} {y_center} {w} {h}")

    # 生成输出文件
    txt_filename = os.path.splitext(os.path.basename(xml_file))[0] + '.txt'
    txt_path = os.path.join(output_dir, txt_filename)
    with open(txt_path, 'w') as f:
        f.write('\n'.join(txt_lines))


# 批量处理配置
xml_dir = 'C:/Users/28645/Desktop/VOCdevkit/VOC2007/Annotations'
output_dir = 'C:/Users/28645/Desktop/VOCdevkit/VOC2007/labels2'
os.makedirs(output_dir, exist_ok=True)

# 遍历XML文件
for filename in os.listdir(xml_dir):
    if filename.lower().endswith('.xml'):
        xml_path = os.path.join(xml_dir, filename)
        convert_annotation(xml_path, output_dir)