from cryptography.fernet import Fernet
import os


KEY_FILE = 'upers.key'


def generate_and_save_key():
    """生成并保存加密密钥到文件"""
    if os.path.exists(KEY_FILE):
        raise FileExistsError("密钥文件已存在，请勿重复生成。")

    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    print(f"新密钥已生成并保存到 {KEY_FILE}。")
    return key


def load_key():
    """从文件加载加密密钥"""
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("未找到密钥文件，请先生成密钥")

    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()


def get_cipher_suite():
    """获取加密套件"""
    key = load_key()
    return Fernet(key)


if __name__ == '__main__':
    generate_and_save_key()
