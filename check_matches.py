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
    notyour_files = []
    for file in missing_files:
        if "充电专属" in file:
            notyour_files.append(file)
    notyour_files = set(notyour_files)
    missing_files =  missing_files - notyour_files
    if missing_files:
        print("---以下文件缺失:")
        i = 1
        for file in sorted(missing_files):
            print(f"{i}\t - {file}")
            i += 1
    else:
        print("=-=目录包含所有预期的文件。")

    # 找出多余的文件（在目录中但不在titles中）
    extra_files = existing_files - expected_files
    for file in ['keys.txt', 'ffmpeg.log', '.DS_Store']:
        if file in extra_files:
            extra_files.remove(file)
    if extra_files:
        print("+++以下多余的文件存在于目录中:")
        i = 1
        for file in sorted(extra_files):
            print(f"{i}\t + {file}")
            i += 1
        print()
    else:
        print("=+=目录中没有多余的文件。")
        print()


# 示例用法
if __name__ == "__main__":
    # directory_path = "/Users/liutie/Public/Drop Box/马督工"  # 替换为你要检查的目录路径
    directory_path = "/media/liutie/备用盘/video/mdg"

    upers = os.listdir(directory_path)
    for uper in upers:
        if uper[0] != '.':
            print(uper, ': ')
            ck = os.path.join(directory_path, uper)
            check_files_in_directory(ck, extension='.mp4')