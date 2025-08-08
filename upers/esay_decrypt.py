from key_manager import get_cipher_suite
import sys


def decrypt_json_file(input_file, output_file):
    """解密JSON文件"""
    try:
        # 获取加密套件
        cipher_suite = get_cipher_suite()

        # 读取加密文件
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()

        # 解密数据
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        # 保存解密后的文件
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)

        print(f"文件 {input_file} 已解密并保存为 {output_file}")
        return True

    except Exception as e:
        print(f"解密过程中出错: {str(e)}")
        return False


if __name__ == "__main__":
    decrypt_json_file('enc/query_mdg.enc', 'query_mdg.json')
    decrypt_json_file('enc/query_lyjgs.enc', 'query_lyjgs.json')