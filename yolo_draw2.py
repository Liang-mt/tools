import os
from PIL import Image, ImageDraw


def read_yolo_data(txt_path):
    yolo_data = []
    with open(txt_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            class_id = int(values[0])
            x_center, y_center, bbox_width, bbox_height = map(float, values[1:])
            yolo_data.append((class_id, x_center, y_center, bbox_width, bbox_height))
    return yolo_data


def draw_bbox(image_path, yolo_data):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    for data in yolo_data:
        class_id, x_center, y_center, bbox_width, bbox_height = data
        x_min = int((x_center - bbox_width / 2) * width)
        y_min = int((y_center - bbox_height / 2) * height)
        x_max = int((x_center + bbox_width / 2) * width)
        y_max = int((y_center + bbox_height / 2) * height)
        if class_id ==1 :
            draw.rectangle([x_min, y_min, x_max, y_max], outline="green")

        #print((y_min, x_min), (y_max, x_max))

    del draw

    return img


def main():
    img_folder = r"C:/Users/28645/Desktop/VOCdevkit/VOC2007/images/"
    txt_folder = r"C:/Users/28645/Desktop/VOCdevkit/VOC2007/labels2/"

    for file in os.listdir(txt_folder):
        if file.endswith('.txt'):
            txt_path = os.path.join(txt_folder, file)
            yolo_data = read_yolo_data(txt_path)

            image_path = os.path.join(img_folder, file[:-4] + '.jpg')
            #image_path = os.path.join(img_folder, file[:-4] + '.png')
            img_with_bbox = draw_bbox(image_path, yolo_data)

            # If you want to save the image with bbox
            output_path = os.path.join(img_folder, 'output', file[:-4] + '_with_bbox.jpg')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img_with_bbox.save(output_path)
            print("finish:" + output_path)


if __name__ == '__main__':
    main()