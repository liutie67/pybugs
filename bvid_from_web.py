import platform
from datetime import datetime
from itertools import islice
import requests

from url2mp3mp4 import getmp3mp4
from upers.query_manager import get_query_dic, save_query_dic2enc


def get1up(uper, lice=None, video_path='./video', exist_nm=5):
    link = 'https://api.bilibili.com/x/space/wbi/arc/search'
    query_dic = get_query_dic(uper)
    total_times_try = 0
    e_nm = 0
    downloaded = 0
    upload_dates = []
    folders = []
    titles = []
    bvids = []
    # 查询参数
    for query in islice(query_dic['pages'], lice):
        try:
            # 发送请求：获取bvid数据
            link_json = requests.get(url=link, params=query_dic['pages'][query], headers=query_dic['headers']).json()
            # 提取视频信息所在列表
            v_list = link_json["data"]["list"]["vlist"]
            # for循环遍历，提取列表里面元素bvid值
            for v in v_list:
                bvid = v["bvid"]
                # bvids.append(bvid)
                url = f'https://www.bilibili.com/video/{bvid}/?spm_id_from=333.1387.upload.video_card.click'
                print('1', total_times_try, end='\t')
                e, upload_date, title, folder = getmp3mp4(bvid=bvid, video_path=video_path, headers=query_dic['headers'], url=url, query_dic=query_dic['pages'][query],
                          combined=True, uper=uper)
                if e == 'existed':
                    e_nm += 1
                else:
                    e_nm = 0
                    upload_dates.append(upload_date)
                    folders.append(folder)
                    titles.append(title)
                    bvids.append(bvid)
                    downloaded = downloaded + 1
                if e_nm >= exist_nm and lice is not None:
                    break
        except requests.exceptions.RequestException as err:
            total_times_try += 1
            print(f"请求失败：{err}")
            print()
            print('????????????????????????????????????????????????????????????????????????????????????????')
            print('????????????????????????????????????????????????????????????????????????????????????????')
            print('?????????????????????????????????????', query, '重新尝试 ???????????????????????????????????????')
            print('????????????????????????????????????????????????????????????????????????????????????????')
            print('????????????????????????????????????????????????????????????????????????????????????????')
            print()
            # 发送请求：获取bvid数据
            link_json = requests.get(url=link, params=query_dic['pages'][query], headers=query_dic['headers']).json()
            # 提取视频信息所在列表
            v_list = link_json["data"]["list"]["vlist"]
            # for循环遍历，提取列表里面元素bvid值
            for v in v_list:
                bvid = v["bvid"]
                # bvids.append(bvid)
                url = f'https://www.bilibili.com/video/{bvid}/?spm_id_from=333.1387.upload.video_card.click'
                print('2', total_times_try, end='\t')
                e, upload_date, title, folder = getmp3mp4(bvid=bvid, video_path=video_path, headers=query_dic['headers'], url=url, query_dic=query_dic['pages'][query],
                          combined=True, uper=uper)
                if e == 'existed':
                    e_nm += 1
                else:
                    e_nm = 0
                    upload_dates.append(upload_date)
                    folders.append(folder)
                    titles.append(title)
                    bvids.append(bvid)
                    downloaded = downloaded + 1
                if e_nm >= exist_nm and lice is not None:
                    break

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query_dic['dones']['last_done'] = timestamp
        query_dic['dones']['done_'+query] = timestamp
        save_query_dic2enc(uper, query_dic)

        print()
        print('----------------------------------------------------------------------------------------')
        print('----------------------------------------------------------------------------------------')
        print('-------------------------------------', query, '下载完成 ---------------------------------------')
        print('----------------------------------------------------------------------------------------')
        print('----------------------------------------------------------------------------------------')
        print()

    return downloaded, uper, upload_dates, titles, folders, bvids


if __name__ == '__main__':
    # 使用示例
    system = platform.system()
    print('--------------', system, '--------------')
    if system == 'Linux':
        media_path = 'path/to/video'
        get1up(uper='uper', lice=1, video_path=media_path)
    elif system == 'Darwin':
        media_path = 'path/to/video'
        get1up(uper='uper', lice=None, video_path=media_path)
