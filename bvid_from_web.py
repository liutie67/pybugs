# 请求网址：视频ID数据包
from datetime import datetime
from itertools import islice

import requests
import json

from url2mp3mp4 import getmp3mp4


headers = {
    "cookie": "buvid3=91276CE0-CFE0-A545-BA8A-B36A0E0279CE65976infoc; b_nut=1752732365; _uuid=A17BA8FC-B6C1-28C2-E7F10-79C77A4A510F1066615infoc; enable_web_push=DISABLE; home_feed_column=5; browser_resolution=1795-968; buvid4=38A6AADE-2460-DCFE-4342-1B18C9CEFF1E66769-025071714-1A%2Fbp2hxpBrpqjbv3apscw%3D%3D; buvid_fp=427828aa957ae69edab1f904065678ce; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTMzMjgzNTYsImlhdCI6MTc1MzA2OTA5NiwicGx0IjotMX0.dcWfh8GFM_SGGesiFQh3cwKWkNBNDKfcWP41Y05VDcE; bili_ticket_expires=1753328296; CURRENT_FNVAL=2000; rpdid=|(um)~ukuYl|0J'u~lJ|Y|R)k; sid=8l9dzykr; b_lsid=D7DF6610D_198353B2EEC; bsource=search_bing"
    , "referer": "https://space.bilibili.com/316568752/upload/video"
    , "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
}
link = 'https://api.bilibili.com/x/space/wbi/arc/search'
uper = 'mdg'
lice = 1

with open('query_' + uper + '.json', encoding='utf-8') as f:
    query_dic = json.load(f)
totol_times_try = 0
# 查询参数
for query in islice(query_dic['pages'], lice):
    # if 'DONE' in query_dic[query]:
    #     print()
    #     print('****************************************************************************************')
    #     print('****************************************************************************************')
    #     print('*************************************', query, '完成跳过 ***************************************')
    #     print('****************************************************************************************')
    #     print('****************************************************************************************')
    #     print()
    #     continue
    try:
        # 发送请求：获取bvid数据
        link_json = requests.get(url=link, params=query_dic['pages'][query], headers=headers).json()
        # 提取视频信息所在列表
        v_list = link_json["data"]["list"]["vlist"]
        # for循环遍历，提取列表里面元素bvid值
        for v in v_list:
            bvid = v["bvid"]
            # bvids.append(bvid)
            url = f'https://www.bilibili.com/video/{bvid}/?spm_id_from=333.1387.upload.video_card.click'
            print('1', totol_times_try, end='\t')
            getmp3mp4(bvid=bvid, video_path='./video', headers=headers, url=url, query_dic=query_dic['pages'][query],
                      combined=True, uper=uper)
    except requests.exceptions.RequestException as e:
        totol_times_try += 1
        print(f"请求失败：{e}")
        print()
        print('????????????????????????????????????????????????????????????????????????????????????????')
        print('????????????????????????????????????????????????????????????????????????????????????????')
        print('?????????????????????????????????????', query, '重新尝试 ???????????????????????????????????????')
        print('????????????????????????????????????????????????????????????????????????????????????????')
        print('????????????????????????????????????????????????????????????????????????????????????????')
        print()
        # 发送请求：获取bvid数据
        link_json = requests.get(url=link, params=query_dic['pages'][query], headers=headers).json()
        # 提取视频信息所在列表
        v_list = link_json["data"]["list"]["vlist"]
        # for循环遍历，提取列表里面元素bvid值
        for v in v_list:
            bvid = v["bvid"]
            # bvids.append(bvid)
            url = f'https://www.bilibili.com/video/{bvid}/?spm_id_from=333.1387.upload.video_card.click'
            print('2', totol_times_try, end='\t')
            getmp3mp4(bvid=bvid, video_path='./video', headers=headers, url=url, query_dic=query_dic['pages'][query],
                      combined=True, uper=uper)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query_dic['dones']['last_done'] = timestamp
    query_dic['dones']['done_'+query] = timestamp
    with open('query_' + uper + '.json', 'w', encoding='utf-8') as f:
        json.dump(query_dic, f, ensure_ascii=False, indent=4)

    print()
    print('----------------------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------------------')
    print('-------------------------------------', query, '下载完成 ---------------------------------------')
    print('----------------------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------------------')
    print()
