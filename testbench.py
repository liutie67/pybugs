# from datetime import datetime
# timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print(timestamp)


"""
将keys.txt里文件名的特殊字符替换
"""
# from title_txt_file import read_file_contents, save_title_to_file
# file_path = "/Users/liutie/Public/Drop Box/马督工/default-默认"
# titles = read_file_contents(file_path)
# for title in titles:
#     # if ('\\' in title) or ('|' in title) or (':' in title):
#     title = title.replace('\\', '_0_').replace('|', '_1_').replace(':', '_2_').replace('"', '_3_')
#     # print(title)
#     save_title_to_file(title, file_name='keys-1.txt', file_path=file_path)

"""
替换指定文件夹里所有文件文件名里的特殊字符
"""
# import os
# def rename_files_in_directory(directory, modification_func):
#     """
#     读取指定目录所有文件，对文件名做指定修改后保存
#     :param directory: 要处理的目录路径
#     :param modification_func: 文件名修改函数，接受原文件名，返回修改后的文件名
#     """
#     # 确保目录存在
#     if not os.path.isdir(directory):
#         print(f"错误：目录 '{directory}' 不存在")
#         return
#     # 遍历目录中的所有文件
#     for filename in os.listdir(directory):
#         # 获取文件的完整路径
#         old_path = os.path.join(directory, filename)
#
#         # 跳过目录，只处理文件
#         if os.path.isfile(old_path):
#             # 获取新文件名
#             new_filename = modification_func(filename)
#             new_path = os.path.join(directory, new_filename)
#
#             # 如果新文件名与旧文件名不同，则重命名
#             if new_filename != filename:
#                 try:
#                     os.rename(old_path, new_path)
#                     print(f"重命名: '{filename}' -> '{new_filename}'")
#                 except Exception as e:
#                     print(f"重命名 '{filename}' 失败: {e}")
# # 示例使用方式
# if __name__ == "__main__":
#     # 示例1: 在所有文件名前添加前缀
#     def add_prefix(filename):
#         return "prefix_" + filename
#     # 示例2: 替换文件名中的特定字符串
#     def replace_string(filename):
#         return filename.replace("\\", "_0_").replace("|", "_1_").replace(":", "_2_").replace('"', "_3_")
#     # 示例3: 去除文件名中的空格
#     def remove_prefix(filename):
#         if filename[:1] == "_":
#             return filename[1:]
#         else:
#             return filename
#     # 指定要处理的目录
#     target_directory = "./video/马督工/default-默认"  # 替换为你的目录路径
#     # 执行重命名
#     rename_files_in_directory(target_directory, modification_func=replace_string)