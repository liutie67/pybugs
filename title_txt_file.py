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
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []


# 示例使用
if __name__ == "__main__":
    # 要保存的字符串，包含空格和汉字
    title = "这是一个示例标题 包含空格和汉字"
    # 目标文件路径
    file_path = "./video/example.txt"

    # 保存到文件
    save_title_to_file(title, file_path)

    # 读取并验证
    read_contents = read_file_contents(file_path)
    print("文件内容:", read_contents)
    print("最后一行是否匹配:", read_contents[-1] == title)