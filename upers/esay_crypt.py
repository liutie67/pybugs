from key_manager import generate_and_save_key, get_cipher_suite
import json
import sys


def encrypt_json_file(input_file, output_file):
    """加密JSON文件"""
    try:
        # 获取加密套件
        cipher_suite = get_cipher_suite()

        # 读取原始JSON文件
        with open(input_file, 'rb') as f:
            json_data = f.read()

        # 加密数据
        encrypted_data = cipher_suite.encrypt(json_data)

        # 保存加密后的文件
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)

        print(f"文件 {input_file} 已加密并保存为 {output_file}")
        return True

    except Exception as e:
        print(f"加密过程中出错: {str(e)}")
        return False


if __name__ == "__main__":
    encrypt_json_file('json/query_mdg.json', 'enc/query_mdg.enc')
    encrypt_json_file('json/query_lyjgs.json', 'enc/query_lyjgs.enc')