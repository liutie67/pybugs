# 导入数据请求模块：需要安装 pip install requests
import requests
# 导入正则表达式模块
import re
# 导入json模块
import json
# 导入subprocess
import subprocess
import os
# 导入合并mp4和mp3相关模块
from moviepy.editor import VideoFileClip, AudioFileClip


"""发送请求：模拟浏览器对url地址发送请求"""
# 模拟浏览器
headers = {
    "cookie":"buvid3=44A481E6-5998-3EED-9381-3AE7248A944396020infoc; b_nut=1752550396; _uuid=32EB238E-3714-8105F-7797-4B14F1B1B10CB96631infoc; header_theme_version=OPEN; enable_web_push=DISABLE; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; buvid4=44C5173C-615F-7ECB-4AE6-48561F46CBBA96869-025071511-1A%2Fbp2hxpBrpqjbv3apscw%3D%3D; buvid_fp=be0d24e57c8322965c4a554f4422fdc9; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTI4MDk2MTIsImlhdCI6MTc1MjU1MDM1MiwicGx0IjotMX0.QarBpGruaf6r1Fa5rXN4zaKB614v2xOzIDvExJpcWiI; bili_ticket_expires=1752809552; rpdid=|(um)~ukuYl|0J'u~lkll|RY~; home_feed_column=4; browser_resolution=1390-883; b_lsid=10CDE6894_1980D059FD1; CURRENT_FNVAL=4048; SESSDATA=2c227872%2C1768119354%2Cdec3d%2A71; bili_jct=c7ac4227b0728f8411c00f5b7fcf7c4c; DedeUserID=35537088; DedeUserID__ckMd5=4b3b14ac5b0c8900; sid=6nj1pgj6; CURRENT_QUALITY=112",
    "referer":"https://search.bilibili.com/all?vt=59962979&keyword=%E9%9B%B7%E5%AE%87%E8%AE%B2%E6%95%85%E4%BA%8B&from_source=webtop_search&spm_id_from=333.1007&search_source=3",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}
# 请求网址：视频播放页面
url = 'https://www.bilibili.com/video/BV1E937z8EcC/?spm_id_from=333.337.search-card.all.click&vd_source=0a9fa60dc05e0583c5edde1708d6eba1'
# 发送请求
response = requests.get(url, headers=headers, stream=True)
total_length = int(response.headers.get('content-length', 0))

"""获取数据：获取服务器返回相应数据"""
# 获取相应的文本数据
html = response.text
# print(html)
"""解析数据：提取我们需要的数据内容"""
# 提取标题
title = re.findall(',"title":"(.*?)","pubdate":', html)[0]
print(title)
# 提取视频信息
info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
print(info)
print(type(info))
json_info = json.loads(info)
print(json_info)
print(type(json_info))
# 字符串是什么样的 -> str = "字'符'串" 里面"外面'，反之亦然
# 提取视频链接
url_video = json_info['data']['dash']['video'][0]['baseUrl']
print(url_video)
# 提取音频链接
url_audio = json_info['data']['dash']['audio'][0]['baseUrl']
print(url_audio)

os.makedirs("video", exist_ok=True)
"""数据保存"""
# 获取视频内容
video_content = requests.get(url_video, headers=headers).content
# 获取音频内容
audio_content = requests.get(url_audio, headers=headers).content

# 视频数据保存
with open("video/" + title + ".mp4", "wb") as video:
    # 写入数据
    video.write(video_content)

# 音频数据保存
with open("video/" + title + ".mp3", "wb") as audio:
    # 写入数据
    audio.write(audio_content)

# 确保输出目录存在
os.makedirs("data", exist_ok=True)

video_path = f"video/{title}.mp4"
audio_path = f"video/{title}.mp3"
output_path = f"data/{title}_output.mp4"

video = VideoFileClip(video_path)
audio = AudioFileClip(audio_path)

if audio.duration != video.duration:
    audio = audio.set_duration(video.duration)

final_clip = video.set_audio(audio)
final_clip.write_videofile(
    output_path,
    codec="libx264",
    audio_codec="aac",
    threads=4,
    verbose=False
)

# cmd = [
#     "ffmpeg",
#     "-hide_banner",
#     "-i", video_path,
#     "-i", audio_path,
#     "-c:v", "copy",      # 视频流直接复制
#     "-c:a", "aac",       # 音频转AAC
#     "-strict", "experimental",
#     output_path
# ]
#
# try:
#     subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
#     print(f"合并成功: {output_path}")
# except FileNotFoundError:
#     print("错误：请确保ffmpeg已安装并添加到PATH")
# except subprocess.CalledProcessError as e:
#     print(f"合并失败:\n{e.stderr.decode()}")