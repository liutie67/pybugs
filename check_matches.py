import os

from title_txt_file import read_file_contents


def check_files_in_directory(directory, extension=''):
    """
    检查指定目录是否包含文件名列表中的所有文件，并打印缺失和多余的文件

    :param extension: '.mp4', '.mp3'
    :param directory: 要检查的目录路径
    # :param titles: 预期的文件名列表
    """
    # 获取目录中实际存在的文件列表
    existing_files = set(os.listdir(directory))
    expected_files = set(read_file_contents(directory, extension=extension))

    # 找出缺失的文件（在titles中但不在目录中）
    missing_files = expected_files - existing_files
    if missing_files:
        print("以下文件缺失:")
        i = 1
        for file in sorted(missing_files):
            print(f"{i}\t - {file}")
            i += 1
    else:
        print("目录包含所有预期的文件。")

    # 找出多余的文件（在目录中但不在titles中）
    extra_files = existing_files - expected_files
    if extra_files:
        print("\n以下多余的文件存在于目录中:")
        i = 1
        for file in sorted(extra_files):
            print(f"{i}\t + {file}")
            i += 1
    else:
        print("\n目录中没有多余的文件。")


# 示例用法
if __name__ == "__main__":
    directory_path = "./video/马督工/default-默认"  # 替换为你要检查的目录路径

    check_files_in_directory(directory_path, extension='.mp4')