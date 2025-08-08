import json
import os

from upers.key_manager import get_cipher_suite
from upers.esay_crypt import encrypt_json_file


def get_query_dic(uper):
    # 获取加密套件
    cipher_suite = get_cipher_suite()

    # 读取加密文件
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'enc', f'query_{uper}.enc')
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()

    # 解密数据
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    decrypted_data = decrypted_data.decode('utf-8')

    query_dic = json.loads(decrypted_data)

    return query_dic

def save_query_dic2enc(uper, query_dic):
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(abs_dir_path, 'json'), exist_ok=True)
    save_file = os.path.join(abs_dir_path, 'json', f'query_{uper}.json')
    with open(save_file, 'w', encoding='utf-8') as f:
        json.dump(query_dic, f, ensure_ascii=False, indent=4)

    output_file = os.path.join(abs_dir_path, 'enc', f'query_{uper}.enc')
    encrypt_json_file(save_file, output_file)

    return 0


if __name__ == '__main__':
    dic = get_query_dic('mdg')
    print(dic)