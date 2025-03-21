import os

# 设置需要处理的文件夹路径
folder_path = 'C:/Users/28645/Desktop/数据结构/'


# 检查路径是否存在
if not os.path.exists(folder_path):
    print("文件夹路径不存在，请检查路径设置")
else:
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            print(f"处理文件: {filename}")  # 打印文件名
            if '【蓝研知己】数据结构应用题训练营做题本' in filename:
                new_filename = filename.replace('【蓝研知己】数据结构应用题训练营做题本', '数据结构')
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_filename)

                # 检查新的文件路径是否已经存在
                if os.path.exists(new_file_path):
                    print(f"文件已存在: {new_file_path}")
                else:
                    os.rename(old_file_path, new_file_path)
                    print(f"重命名: {filename} -> {new_filename}")  # 打印重命名信息