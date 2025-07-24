import os.path


def save_title_to_file(title, file_path, logging=False):
    """
    将字符串title保存到指定txt文件中，支持追加模式，确保包含空格、汉字等能正确保存和读取

    :param title: 要保存的字符串，可能包含空格、汉字等
    :param file_path: 目标txt文件路径
    """
    try:
        # 使用utf-8编码以支持汉字等非ASCII字符
        # 模式'a+'表示追加读写，文件不存在则创建
        with open(os.path.join(file_path, 'keys.txt'), 'a+', encoding='utf-8') as file:
            file.write(title + '\n')  # 添加换行符以便区分多次写入的内容
        if logging: print(f"成功将内容写入文件: {file_path}")
    except Exception as e:
        print(f"写入文件时出错: {e}")


def read_file_contents(file_path, logging=False):
    """
    读取txt文件内容并返回

    :param file_path: 要读取的txt文件路径
    :return: 文件内容的列表，每行作为一个元素
    """
    try:
        with open(os.path.join(file_path, 'keys.txt'), 'r', encoding='utf-8') as file:
            contents = file.readlines()
        # 去除每行末尾的换行符
        return [line.strip() for line in contents]
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
        existing_titles = read_file_contents(file_path, logging)

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
    save_title_to_file(title, file_path)
    save_title_to_file(title2, file_path)
    save_title_to_file(title3, file_path)

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