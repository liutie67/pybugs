import platform
import time
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
            time.sleep(10)

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
                try:
                    e, upload_date, title, folder = getmp3mp4(bvid=bvid, video_path=video_path, headers=query_dic['headers'], url=url, query_dic=query_dic['pages'][query],
                              combined=True, uper=uper)
                except Exception as err:
                    print("尝试二·失败 ", err)
                    return None, None, None, None, None, None

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
        # print('----------------------------------------------------------------------------------------')
        # print('----------------------------------------------------------------------------------------')
        print('-------------------------------------', query, '下载完成 ---------------------------------------')
        # print('----------------------------------------------------------------------------------------')
        # print('----------------------------------------------------------------------------------------')
        print()

    return downloaded, uper, upload_dates, titles, folders, bvids


def get_fav_folder(fav_id, lice=None, video_path='./video', exist_nm=5):
    """
    抓取公开收藏夹数据
    :param fav_id: 收藏夹的唯一标识
    """
    # 收藏夹的专用接口
    link = 'https://api.bilibili.com/x/v3/fav/resource/list'
    # 加载加密字典（需要包含 headers 和 pages 参数）
    query_dic = get_query_dic(fav_id)

    total_times_try = 0
    e_nm = 0
    downloaded = 0
    upload_dates = []
    folders = []
    titles = []
    bvids = []

    # 查询参数：按 query_dic 中预设的页码进行遍历
    for query in islice(query_dic['pages'], lice):
        try:
            # 发送请求：获取当前页的收藏列表数据
            link_json = requests.get(url=link, params=query_dic['pages'][query], headers=query_dic['headers']).json()

            # 校验接口返回状态并提取收藏列表（收藏夹的数据结构与 UP 主不同）
            if link_json.get("code") != 0 or not link_json.get("data") or not link_json["data"].get("medias"):
                print(f"获取数据异常或该页无数据，跳过 {query}")
                continue

            v_list = link_json["data"]["medias"]

            # for循环遍历，提取列表里面元素 bvid 值
            for v in v_list:
                # 过滤掉收藏夹中已失效（被 UP 主删除）的视频
                if v.get('title') == '已失效视频':
                    continue

                bvid = v["bvid"]
                url = f'https://www.bilibili.com/video/{bvid}/?spm_id_from=333.1387.upload.video_card.click'
                print('1', total_times_try, end='\t')

                # 传入 fav_id 作为 getmp3mp4 创建文件夹的依据
                e, upload_date, title, folder = getmp3mp4(bvid=bvid,
                                                          video_path=video_path,
                                                          headers=query_dic['headers'],
                                                          url=url,
                                                          query_dic=query_dic['pages'][query],
                                                          combined=True,
                                                          uper=fav_id,
                                                          mode='fav')

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
            time.sleep(10)

            total_times_try += 1
            print(f"请求失败：{err}")
            print()
            print('????????????????????????????????????????????????????????????????????????????????????????')
            print('????????????????????????????????????????????????????????????????????????????????????????')
            print('?????????????????????????????????????', query, '重新尝试 ???????????????????????????????????????')
            print('????????????????????????????????????????????????????????????????????????????????????????')
            print('????????????????????????????????????????????????????????????????????????????????????????')
            print()

            # 尝试二：重新发送请求
            link_json = requests.get(url=link, params=query_dic['pages'][query], headers=query_dic['headers']).json()

            if link_json.get("code") != 0 or not link_json.get("data") or not link_json["data"].get("medias"):
                continue

            v_list = link_json["data"]["medias"]

            for v in v_list:
                if v.get('title') == '已失效视频':
                    continue

                bvid = v["bvid"]
                url = f'https://www.bilibili.com/video/{bvid}/?spm_id_from=333.1387.upload.video_card.click'
                print('2', total_times_try, end='\t')
                try:
                    e, upload_date, title, folder = getmp3mp4(bvid=bvid,
                                                              video_path=video_path,
                                                              headers=query_dic['headers'],
                                                              url=url,
                                                              query_dic=query_dic['pages'][query],
                                                              combined=True,
                                                              uper=fav_id,
                                                              mode='fav')
                except Exception as err:
                    print("尝试二·失败 ", err)
                    return None, None, None, None, None, None

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

        # 保存记录状态，加密写回
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query_dic['dones']['last_done'] = timestamp
        query_dic['dones']['done_' + query] = timestamp
        save_query_dic2enc(fav_id, query_dic)

        print()
        # print('----------------------------------------------------------------------------------------')
        # print('----------------------------------------------------------------------------------------')
        print('-------------------------------------', query, '下载完成 ---------------------------------------')
        # print('----------------------------------------------------------------------------------------')
        # print('----------------------------------------------------------------------------------------')
        print()

    return downloaded, fav_id, upload_dates, titles, folders, bvids


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
