import json
import os
import requests
import re

from title_txt_file import save_title_to_file

def getmp3mp4(bvid, video_path, headers, url):
    if len(bvid) < 2:
        print('bvid is too short')
        return

    # 发送请求
    response = requests.get(url, headers=headers, stream=True)
    # total_length = int(response.headers.get('content-length', 0))

    """获取数据：获取服务器返回相应数据"""
    # 获取相应的文本数据
    html = response.text
    # print(html)

    """解析数据：提取我们需要的数据内容"""
    # 提取标题
    title = re.findall(',"title":"(.*?)","pubdate":', html)
    title = title[0]
    # print(title)
    # 提取视频信息
    info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
    uploadDate = re.findall('itemprop="uploadDate" content="(.*?)">', html)[0]
    uploadDate = uploadDate.replace(' ', '-').replace(':', '-')
    try:
        ugc_season = re.findall(r'"ugc_season":\s*{\s*"id":\s*(\d+),\s*"title":\s*"([^"]+)"', html)[0]
    except IndexError:
        print('No Season Video: ', end='')
        ugc_season = ('default', '默认')
    # print(type(info))
    json_info = json.loads(info)
    # print(json_info)
    # print(type(json_info))
    # 字符串是什么样的 -> str = "字'符'串" 里面"外面'，反之亦然
    # 提取视频链接
    url_video = json_info['data']['dash']['video'][0]['baseUrl']
    # print(url_video)
    # 提取音频链接
    url_audio = json_info['data']['dash']['audio'][0]['baseUrl']
    # print(url_audio)

    """数据保存"""
    # 获取视频内容
    video_content = requests.get(url_video, headers=headers).content
    # 获取音频内容
    audio_content = requests.get(url_audio, headers=headers).content

    video_folder = os.path.join(video_path, ugc_season[0] + '-' + ugc_season[1])
    # 确保输出目录存在
    os.makedirs(video_folder, exist_ok=True)
    # 视频数据保存
    with open(os.path.join(video_folder, uploadDate + bvid + title + ".mp4"), "wb") as video:
        # 写入数据
        video.write(video_content)

    # 音频数据保存
    with open(os.path.join(video_folder, uploadDate + bvid + title + ".mp3"), "wb") as audio:
        # 写入数据
        audio.write(audio_content)

    save_title_to_file(uploadDate + bvid + title, video_folder)

    print("title:", title, "bvid:", bvid, "下载成功。")