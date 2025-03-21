# import os
# import shutil
#
# # 设置图片文件夹和文本文件夹的路径
# image_folder = 'C:/Users/28645/Desktop/dataset/glasses/images/'
# txt_folder = 'C:/Users/28645/Desktop/dataset/glasses/labels/'
#
# # 获取图片文件夹下的所有文件
# image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
#
# # 检查每个图片文件是否有对应的同名文本文件
# for image_file in image_files:
#     image_file_name = os.path.splitext(image_file)[0]
#     txt_file_name = image_file_name + '.txt'
#     txt_file_path = os.path.join(txt_folder, txt_file_name)
#
#     # 如果同名文本文件不存在，则创建一个空的文本文件
#     if not os.path.isfile(txt_file_path):
#         with open(txt_file_path, 'w') as txt_file:
#             pass
#
# print('任务完成')

#统计指定文件夹（./hair/labels/）下所有以 .txt 结尾的文件中以 1 开头的行的数量
# import os
#
# def count_lines_start_with_one(file_path):
#     count = 0
#     with open(file_path, 'r') as file:
#         for line in file:
#             if line.strip().startswith('3'):
#                 count += 1
#     return count
#
# def count_lines_start_with_one_in_folder(folder_path):
#     total_count = 0
#     for file in os.listdir(folder_path):
#         if file.endswith('.txt'):
#             file_path = os.path.join(folder_path, file)
#             count = count_lines_start_with_one(file_path)
#             total_count += count
#             print(f'{file}: {count}')
#
#     print(f'Total count: {total_count}')
#
# folder_path = 'C:/Users/28645/Desktop/dataset/white/labels/'
# count_lines_start_with_one_in_folder(folder_path)


#修改label标签，把首字符为“1”的改成“3”
# import os
#
#
# def modify_files():
#     folder = r'C:/Users/28645/Desktop/血型/O/'  # 替换为实际的文件夹路径
#
#     for filename in os.listdir(folder):
#         if not filename.endswith('.txt'):
#             continue
#
#         filepath = os.path.join(folder, filename)
#         lines = []
#
#         with open(filepath, 'r') as f:
#             for line in f:
#                 if line.startswith('2'):
#                     line = '3' + line[1:]
#                 lines.append(line)
#
#         with open(filepath, 'w') as f:
#             f.writelines(lines)
#
#         print(f"已修改文件 {filename}")
#
# modify_files()

#将yoloface格式数据集转换位关键点数据集格式
# import os
# import fileinput
#
# folder_path = 'C:/Users/28645/Desktop/test/label/'
#
# # 获取文件夹下所有txt文件
# txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
#
# # 循环处理每个txt文件
# for file in txt_files:
#     file_path = os.path.join(folder_path, file)
#     with fileinput.FileInput(file_path, inplace=True, backup='.bak') as f:
#         for line in f:
#             items = line.split(' ')
#             result = items[0] + ' ' + ' '.join(items[5:15])
#             print(result, end='')
#
# # 删除备份文件
# for file in txt_files:
#     backup_file_path = os.path.join(folder_path, file + '.bak')
#     if os.path.exists(backup_file_path):
#         os.remove(backup_file_path)


import os
import shutil

def move_json_files(source_folder, destination_folder):
    # 获取源文件夹中所有文件和文件夹的列表
    items = os.listdir(source_folder)

    for item in items:
        # 构建文件/文件夹的完整路径
        item_path = os.path.join(source_folder, item)

        if item.endswith(".jpg"):
            # 如果是以.json结尾的文件，则移动到目标文件夹
            shutil.move(item_path, destination_folder)

        elif os.path.isdir(item_path):
            # 如果是文件夹，则递归调用函数，处理文件夹内的文件
            move_json_files(item_path, destination_folder)

# 设定源文件夹和目标文件夹的路径
source_folder = "C:/Users/28645/Desktop/血型/labels/"
destination_folder = "C:/Users/28645/Desktop/血型/images/"

# 调用函数来移动.json文件
move_json_files(source_folder, destination_folder)



# import os
#
# def rename_files_with_matching_names(folder1, folder2):
#     jpg_files = [f for f in os.listdir(folder1) if f.endswith('.jpg')]
#     txt_files = [f for f in os.listdir(folder2) if f.endswith('.txt')]
#
#     for i in range(min(len(jpg_files), len(txt_files))):
#         jpg_file = os.path.join(folder1, jpg_files[i])
#         txt_file = os.path.join(folder2, txt_files[i])
#
#         new_jpg_name = f'{i+37:00d}.jpg'
#         new_txt_name = f'{i+37:00d}.txt'
#
#         os.rename(jpg_file, os.path.join(folder1, new_jpg_name))
#         os.rename(txt_file, os.path.join(folder2, new_txt_name))
#         print(f'Renamed {jpg_files[i]} to {new_jpg_name}')
#         print(f'Renamed {txt_files[i]} to {new_txt_name}')
#
# # 请将'folder1'和'folder2'替换为你实际的文件夹路径
# rename_files_with_matching_names('C:/Users/28645/Desktop/血型/O/', 'C:/Users/28645/Desktop/血型/O/')
