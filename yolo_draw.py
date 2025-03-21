import os
import cv2

def read_yolo_data(model,txt_path):
    yolo_data = []
    if model == "1":
        with open(txt_path, 'r') as file:
            for line in file:
                values = line.strip().split()
                class_id = int(values[0])
                x1,y1,x2,y2,x3,y3,x4,y4= map(float, values[1:10])
                yolo_data.append((class_id, x1,y1,x2,y2,x3,y3,x4,y4))
    if model == "2":
        with open(txt_path, 'r') as file:
            for line in file:
                values = line.strip().split()
                class_id = int(values[0])
                x_center, y_center, bbox_width, bbox_height, x1, y1, x2, y2, x3, y3, x4, y4= map(float,values[1:14])
                yolo_data.append( (class_id, x_center, y_center, bbox_width, bbox_height, x1, y1, x2, y2, x3, y3, x4, y4))
    if model == "3":
        with open(txt_path, 'r') as file:
            for line in file:
                values = line.strip().split()
                class_id = int(values[0])
                x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = map(float, values[1:12])
                yolo_data.append((class_id, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5))
    if model == "4":
        with open(txt_path, 'r') as file:
            for line in file:
                values = line.strip().split()
                class_id = int(values[0])
                x_center, y_center, bbox_width, bbox_height, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = map(float,values[1:16])
                yolo_data.append((class_id, x_center, y_center, bbox_width, bbox_height, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5))
    if model == "5":
        with open(txt_path, 'r') as file:
            for line in file:
                values = line.strip().split()
                class_id = int(values[0])
                x_center, y_center, bbox_width, bbox_height= map(float,values[1:6])
                yolo_data.append((class_id, x_center, y_center, bbox_width, bbox_height))
    return yolo_data



def draw_bbox(model,image_path, yolo_data):
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    #初始化各个值，无实际意义
    class_id, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    if model == "1" or model == "2":
        for data in yolo_data:
            if model == "1":
                class_id, x1, y1, x2, y2, x3, y3, x4, y4 = data
            if model == "2":
                class_id, x_center, y_center, bbox_width, bbox_height, x1, y1, x2, y2, x3, y3, x4, y4= data

            x1 = int(x1 * width)
            x2 = int(x2 * width)
            x3 = int(x3 * width)
            x4 = int(x4 * width)

            y1 = int(y1 * height)
            y2 = int(y2 * height)
            y3 = int(y3 * height)
            y4 = int(y4 * height)

            cv2.line(img, (x1, y1), (x2, y2), (250, 250, 12), 2)
            cv2.line(img, (x2, y2), (x3, y3), (250, 250, 12), 2)
            cv2.line(img, (x3, y3), (x4, y4), (250, 250, 12), 2)
            cv2.line(img, (x4, y4), (x1, y1), (250, 250, 12), 2)

    if model == "3" or model == "4":
        for data in yolo_data:
            if model == "3":
                class_id,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5 = data
            if model == "4":
                class_id, x_center, y_center, bbox_width, bbox_height,x1,y1,x2,y2,x3,y3,x4,y4,x5,y5 = data

            x1 = int(x1 * width)
            x2 = int(x2 * width)
            x3 = int(x3 * width)
            x4 = int(x4 * width)
            x5 = int(x5 * width)


            y1 = int(y1 * height)
            y2 = int(y2 * height)
            y3 = int(y3 * height)
            y4 = int(y4 * height)
            y5 = int(y5 * height)

            cv2.line(img, (x1,y1), (x2,y2), (250, 250, 12), 2)
            cv2.line(img, (x2,y2), (x3,y3), (250, 250, 12), 2)
            cv2.line(img, (x3,y3), (x4,y4), (250, 250, 12), 2)
            cv2.line(img, (x4,y4), (x5,y5), (250, 250, 12), 2)
            cv2.line(img, (x5,y5), (x1,y1), (250, 250, 12), 2)

            cv2.circle(img, (x1,y1), 10, (250, 250, 12), 2)
            cv2.circle(img, (x3,y3), 10, (250, 250, 12), 2)
            cv2.putText(img, str(class_id), (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)

    return img


if __name__ == '__main__':

    model = input("1装甲板四点模型/2装甲板四点模型yoloface格式/3能量机关五点模型/4能量机关五点模型yoloface格式: ") #类别 + 关键点的数据集格式
    img_folder = 'C:/Users/28645/Desktop/buff_total/liang2_/'
    txt_folder = 'C:/Users/28645/Desktop/buff_total/keypointlabel/'

    for file in os.listdir(txt_folder):
        if file.endswith('.txt'):
            txt_path = os.path.join(txt_folder, file)
            yolo_data = read_yolo_data(model,txt_path)

            image_path = os.path.join(img_folder, file[:-4] + '.jpg')
            img_with_bbox = draw_bbox(model,image_path, yolo_data)

            # If you want to display the image with bbox
            # cv2.imshow(f'Image with BBox: {file[:-4]}.jpg', img_with_bbox)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # If you want to save the image with bbox
            output_path = os.path.join(img_folder, 'output', file[:-4] + '_with_bbox.jpg')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, img_with_bbox)
            print("finish:" + output_path)


