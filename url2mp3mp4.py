import json
import os
import requests
import re

from bs4 import BeautifulSoup

from title_txt_file import save_title_to_file, is_title_exist
from utils import combine_video_audio, replace_illegal_char


def getmp3mp4(bvid, video_path, headers, url, query_dic=None, combined=False, uper='', mode='up'):
    if len(bvid) < 2:
        print('bvid is too short')
        return None, None, None, None

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
        print(getmp3mp4.call_count, '\t', str(pn) + ' -', getmp3mp4.call_count % ps, end='\t')

    # 发送请求
    response = requests.get(url, headers=headers, stream=True)
    # total_length = int(response.headers.get('content-length', 0))

    """获取数据：获取服务器返回相应数据"""
    # 获取相应的文本数据
    html = response.text
    # print(html)

    soup = BeautifulSoup(html, 'html.parser')

    # 定位 class 为 video-title 的 h1 标签
    h1_tag = soup.find('h1', class_='video-title')

    new_title = 'DefaulT'
    if h1_tag:
        # .get('title') 获取 title 属性，比 .text 更保险，防止标签内有其他隐藏元素
        new_title = h1_tag.get('title')
        # 输出: 【年度总结】一口气了解过去一年的全球经济｜关税战新格局
    else:
        # 备选方案：如果找不到 h1，找 title 标签并去除后缀
        title_tag = soup.find('title')
        if title_tag:
            full_title = title_tag.text
            new_title = full_title.split('_哔哩哔哩')[0]

    """解析数据：提取我们需要的数据内容"""

    # === 根据 mode 提取 UP 主的 UID ===
    uid_folder = ""
    if mode == 'fav':
        try:
            # B站视频页面的 window.__INITIAL_STATE__ 中包含了 owner 结构
            uid_match = re.search(r'"owner":\s*\{\s*"mid":\s*(\d+)', html)
            if uid_match:
                uid_folder = uid_match.group(1)
            else:
                # 备选正则：如果没找到 owner 结构，尝试匹配空间主页链接
                uid_match_alt = re.search(r'space\.bilibili\.com/(\d+)', html)
                uid_folder = uid_match_alt.group(1) if uid_match_alt else "unknown_uid"
        except Exception as e:
            print(f"UID提取异常: {e}")
            uid_folder = "unknown_uid"

    # 提取标题
    title = re.findall(',"title":"(.*?)","pubdate":', html)
    if title:
        title = title[0]
    else:
        title = new_title

    if 'v2' in uper:
        title = new_title
    title = title[:60]
    title = replace_illegal_char(title).replace('/', '_5_')

    # 提取视频信息
    info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
    uploadDate = re.findall('itemprop="uploadDate" content="(.*?)">', html)[0]
    uploadDate = uploadDate.replace(' ', '-').replace(':', '-')

    try:
        ugc_season = re.findall(r'"ugc_season":\s*{\s*"id":\s*(\d+),\s*"title":\s*"([^"]+)"', html)[0]
        print(ugc_season[0] + '-' + ugc_season[1] + ': ', end='\t')
    except IndexError:
        print('No Season Video: ', end='\t')
        ugc_season = ('default', '默认')

    json_info = json.loads(info)

    # === 修改：根据 mode 动态组合文件夹路径 ===
    if mode == 'fav':
        # 收藏夹模式：video_path / uper(即收藏夹名) / UID / 剧集名
        video_folder = replace_illegal_char(
            os.path.join(video_path, uper, uid_folder, ugc_season[0] + '-' + ugc_season[1]))
    else:
        # UP主模式：video_path / uper / 剧集名
        video_folder = replace_illegal_char(os.path.join(video_path, uper, ugc_season[0] + '-' + ugc_season[1]))
    # =======================================

    # 确保输出目录存在
    os.makedirs(video_folder, exist_ok=True)

    if is_title_exist(uploadDate + bvid + title, video_folder):
        print(uploadDate + bvid + title, "已下载，跳过。")
        return 'existed', None, None, None
    elif is_title_exist(uploadDate + bvid + title + " 跳过:充电专属", video_folder):
        print(uploadDate + bvid + title + " 跳过:充电专属", "已存在，跳过。")
        return 'existed', None, None, None

    try:
        # 提取视频链接
        url_video = json_info['data']['dash']['video'][0]['baseUrl']
        # 提取音频链接
        url_audio = json_info['data']['dash']['audio'][0]['baseUrl']
    except KeyError:
        save_title_to_file(uploadDate + bvid + title + " 跳过:充电专属", video_folder)
        print("跳过充电专属视频!")
        return None, None, None, None

    """数据保存"""
    # 获取视频内容
    video_content = requests.get(url_video, headers=headers).content
    # 获取音频内容
    audio_content = requests.get(url_audio, headers=headers).content

    # 视频数据保存
    with open(os.path.join(video_folder, uploadDate + bvid + title + "-s.mp4"), "wb") as video:
        video.write(video_content)

    # 音频数据保存
    with open(os.path.join(video_folder, uploadDate + bvid + title + "-s.mp3"), "wb") as audio:
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