import json
import os
import requests
import re

from title_txt_file import save_title_to_file, is_title_exist
from utils import combine_video_audio, replace_illegal_char

def getmp3mp4(bvid, video_path, headers, url, query_dic=None, combined=False, uper=''):
    if len(bvid) < 2:
        print('bvid is too short')
        return

    # 初始化调用次数（如果不存在）
    if not hasattr(getmp3mp4, "call_count"):
        getmp3mp4.call_count = 0
    # 增加计数并打印
    getmp3mp4.call_count += 1
    if query_dic is None:
        print(getmp3mp4.call_count, end='\t')
    else:
        pn = query_dic["pn"]
        ps = int(query_dic["ps"])
        print(getmp3mp4.call_count, '\t', pn + ' -', getmp3mp4.call_count % ps, end='\t')

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
    title = title[:60]
    title = replace_illegal_char(title)
    # print(title)
    # 提取视频信息
    info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
    uploadDate = re.findall('itemprop="uploadDate" content="(.*?)">', html)[0]
    uploadDate = uploadDate.replace(' ', '-').replace(':', '-')
    try:
        ugc_season = re.findall(r'"ugc_season":\s*{\s*"id":\s*(\d+),\s*"title":\s*"([^"]+)"', html)[0]
        print(ugc_season[0] + '-' + ugc_season[1]+': ', end='\t')
    except IndexError:
        print('No Season Video: ', end='\t')
        ugc_season = ('default', '默认')
    # print(type(info))
    json_info = json.loads(info)
    # print(json_info)
    # print(type(json_info))
    # 字符串是什么样的 -> str = "字'符'串" 里面"外面'，反之亦然

    video_folder = replace_illegal_char(os.path.join(video_path, uper, ugc_season[0] + '-' + ugc_season[1]))
    # video_file = os.path.join(uper, video_folder)

    # 确保输出目录存在
    os.makedirs(video_folder, exist_ok=True)

    if is_title_exist(uploadDate + bvid + title, video_folder):
        print(uploadDate + bvid + title, "已下载，跳过。")
        return 'existed'
    elif is_title_exist(uploadDate + bvid + title + " 跳过:充电专属", video_folder):
        print(uploadDate + bvid + title + " 跳过:充电专属", "已存在，跳过。")
        return 'existed'

    try:
        # 提取视频链接
        url_video = json_info['data']['dash']['video'][0]['baseUrl']
        # print(url_video)
        # 提取音频链接
        url_audio = json_info['data']['dash']['audio'][0]['baseUrl']
        # print(url_audio)
    except KeyError:
        save_title_to_file(uploadDate + bvid + title + " 跳过:充电专属", video_folder)
        return print("跳过充电专属视频!")

    """数据保存"""
    # 获取视频内容
    video_content = requests.get(url_video, headers=headers).content
    # 获取音频内容
    audio_content = requests.get(url_audio, headers=headers).content

    # 视频数据保存
    with open(os.path.join(video_folder, uploadDate + bvid + title + "-s.mp4"), "wb") as video:
        # 写入数据
        video.write(video_content)

    # 音频数据保存
    with open(os.path.join(video_folder, uploadDate + bvid + title + "-s.mp3"), "wb") as audio:
        # 写入数据
        audio.write(audio_content)

    if combined:
        combine_video_audio(video_path=os.path.join(video_folder, uploadDate + bvid + title + "-s.mp4"),
                            audio_path=os.path.join(video_folder, uploadDate + bvid + title + "-s.mp3"),
                            output_path=os.path.join(video_folder, uploadDate + bvid + title + ".mp4"),
                            log_file=os.path.join(video_folder, "ffmpeg.log"))
        os.remove(os.path.join(video_folder, uploadDate + bvid + title + "-s.mp4"))
        os.remove(os.path.join(video_folder, uploadDate + bvid + title + "-s.mp3"))

    save_title_to_file(uploadDate + bvid + title, video_folder)
    print("title:", title, "bvid:", bvid, "下载成功。")

    return 0, uploadDate, title, video_folder