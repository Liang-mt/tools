# import os
#
# folder = 'C:/Users/28645/Desktop/armor/armor_finnal/labels/'  # 替换为你的文件夹路径
# import os
#
# def process_files_in_folder(folder_path):
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(folder_path, filename)
#             process_file(file_path)
#
# def process_file(file_path):
#     with open(file_path, 'r') as f:
#         lines = f.readlines()
#
#     filtered_lines = [line for line in lines if int(line.split()[0]) <= 17]
#
#     with open(file_path, 'w') as f:
#         f.writelines(filtered_lines)
#
# folder_path = 'C:/Users/28645/Desktop/armor/armor_finnal/labels/'  # 将 'your_folder_path' 替换为实际的文件夹路径
# process_files_in_folder(folder_path)


# import os
#
# def count_lines_starting_with_1(file_path):
#     count = 0
#
#     with open(file_path, 'r') as f:
#         for line in f:
#             if line.startswith('3 '):
#                 count += 1
#
#     return count
#
# def count_lines_in_folder(folder_path):
#     total_count = 0
#
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(folder_path, filename)
#             count = count_lines_starting_with_1(file_path)
#             total_count += count
#
#     return total_count
#
# folder_path = 'C:/Users/28645/Desktop/buff_total/yololabel/'  # 将 'your_folder_path' 替换为实际的文件夹路径
# total_count = count_lines_in_folder(folder_path)
# print('总行数:', total_count)


import numpy as np
import matplotlib.pyplot as plt

def speed_target_function(t, a, omega, b):
    return a * np.sin(omega * t) + b

# 参数范围
a_min = 0.780
a_max = 1.045
omega_min = 1.884
omega_max = 2.000

# 参数取值
a_values = np.linspace(a_min, a_max, 100)
omega_values = np.linspace(omega_min, omega_max, 100)
b = 2.090 - a_values[0]  # 根据条件 b = 2.090 - a

# 绘制图像
plt.figure(figsize=(10, 6))

for a in a_values:
    spd = speed_target_function(30, a, omega_values, b)
    plt.plot(omega_values, spd, label=f'a={a}')

plt.title('Speed Target Function')
plt.xlabel('ω (rad/s)')
plt.ylabel('spd (rad/s)')
plt.legend()
plt.grid(True)
plt.show()