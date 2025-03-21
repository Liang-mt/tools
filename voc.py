import os

if __name__ == "__main__":
    from pybaseutils.maker import convert_voc2yolo

    # 定义类别数
    class_name = ["fire"]
    # VOC数据目录
    data_root = "C:/Users/28645/Desktop/fire/"
    # 保存输出yolo格式数据目录
    out_text_dir = os.path.join(data_root, "labels")
    # 开始转换,vis=True进行可视化
    convert_voc2yolo.convert_voc2yolo(data_root, out_text_dir, class_name=class_name, vis=False)