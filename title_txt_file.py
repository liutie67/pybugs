import os


def save_title_to_file(title, file_path, file_name='keys.txt', logging=False):
    """
    将字符串title保存到指定txt文件中，支持追加模式，确保包含空格、汉字等能正确保存和读取。
    如果文件中已存在完全相同的行，则跳过写入。

    :param title: 要保存的字符串，可能包含空格、汉字等
    :param file_path: 目标txt文件路径
    :param file_name: 文件名，默认为'keys.txt'
    :param logging: 是否打印日志信息，默认为False
    """
    try:
        full_path = os.path.join(file_path, file_name)

        # 检查文件是否存在，如果不存在则直接写入
        if not os.path.exists(full_path):
            with open(full_path, 'a+', encoding='utf-8') as file:
                file.write(title + '\n')
            if logging:
                print(f"文件不存在，已创建并成功将内容写入文件: {full_path}")
            return

        # 检查是否已存在相同的行
        with open(full_path, 'r', encoding='utf-8') as file:
            existing_lines = file.readlines()

        # 去除每行的换行符进行比较
        if any(line.strip() == title.strip() for line in existing_lines):
            if logging:
                print(f"内容已存在，跳过写入: {title}")
            return

        # 追加写入新内容
        with open(full_path, 'a', encoding='utf-8') as file:
            file.write(title + '\n')

        if logging:
            print(f"成功将内容写入文件: {full_path}")

    except Exception as e:
        print(f"写入文件时出错: {e}")


def read_file_contents(file_path, extension='', file_name='keys.txt', logging=False):
    """
    读取txt文件内容并返回

    :param logging:
    :param file_name:
    :param extension: 读取文件名后额外添加后缀extension, 例如".mp4"
    :param file_path: 要读取的txt文件路径
    :return: 文件内容的列表，每行作为一个元素
    """
    try:
        with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as file:
            contents = file.readlines()
        # 去除每行末尾的换行符
        return [line.strip() + extension for line in contents]
    except FileNotFoundError as e:
        print(f"key.txt未创建: {e}", end='')
        return []

def is_title_exist(title, file_path, logging=False):
    """
    检查给定的title是否已经存在于文件中（可能是任意一行）

    :param title: 要检查的字符串
    :param file_path: 目标txt文件路径
    :return: 如果存在返回True，否则返回False
    """
    try:
        # 读取文件内容
        existing_titles = read_file_contents(file_path, logging=logging)

        # 检查title是否在现有内容中
        return title in existing_titles
    except Exception as e:
        print(f"检查title存在性时出错: {e}")
        return False


# 示例使用
if __name__ == "__main__":
    # 要保存的字符串，包含空格和汉字
    title = "这是一个示例标题 包含空格和汉字"
    title2 = "title2 123 /*-"
    title3 = "title3 951 09*ssa"

    # 目标文件路径
    file_path = "./video"
    # 保存到文件
    save_title_to_file(title, file_path, file_name='exemple.txt')
    save_title_to_file(title2, file_path, file_name='exemple.txt')
    save_title_to_file(title3, file_path, file_name='exemple.txt')

    # 检查title是否存在
    exists3 = is_title_exist(title3, file_path)
    print(f"Title '{title3}' 是否存在: {exists3}")
    exists2 = is_title_exist(title2, file_path)
    print(f"Title '{title2}' 是否存在: {exists2}")

    os.remove(os.path.join(file_path, 'keys.txt'))
    exists = is_title_exist(title, file_path)
    print(f"Title '{title}' 是否存在: {exists}")

    # 读取并验证
    # read_contents = read_file_contents(file_path)
    # print("文件内容:", read_contents)
    # print("最后一行是否匹配:", read_contents[-1] == title)

