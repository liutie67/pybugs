import subprocess
# 导入合并mp4和mp3相关模块
from moviepy.editor import *

from title_txt_file import read_file_contents


def combine_video_audio(video_path, audio_path, output_path):
    cmd = [
        "ffmpeg",
        "-i", video_path,  # 输入视频
        "-i", audio_path,  # 输入音频
        "-c:v", "copy",  # 视频流直接复制（不重新编码）
        "-c:a", "copy",  # 音频转为AAC（兼容性最好，若原音频已是AAC可改为"copy"）
        "-map", "0:v:0",  # 选择视频流
        "-map", "1:a:0",  # 选择音频流
        "-shortest",  # 以视频和音频中较短的时长为准
        output_path
    ]
    subprocess.run(cmd, check=True)

read_from = '/Volumes/tish/1113902-房产那些事儿'
save_to = '/Volumes/tish/房产那些事儿'
# 确保输出目录存在
os.makedirs(save_to, exist_ok=True)
titles = read_file_contents(read_from)

for title in titles:
    video_path = read_from + f"/{title}.mp4"
    audio_path = read_from + f"/{title}.mp3"
    output_path = save_to + f"/{title}.mp4"

    # 检查输出文件是否已存在
    if os.path.exists(output_path):
        print(f"文件已存在，跳过处理: {output_path}")
        continue

    # 检查输入文件是否存在
    if not os.path.exists(video_path) or not os.path.exists(audio_path):
        print(f"输入文件缺失，跳过处理: {title}")
        continue

    try:
        # video = VideoFileClip(video_path)
        # audio = AudioFileClip(audio_path)
        #
        # if audio.duration != video.duration:
        #     audio = audio.set_duration(video.duration)
        #
        # final_clip = video.set_audio(audio)
        # final_clip.write_videofile(
        #     output_path,
        #     codec="h264_videotoolbox",
        #     audio_codec="aac",
        #     verbose=False
        # )
        #
        # # 关闭剪辑以释放资源
        # video.close()
        # audio.close()
        # final_clip.close()

        # 调用示例
        combine_video_audio(video_path, audio_path, output_path)
        print(f"处理完成: {title}")
    except Exception as e:
        print(f"处理 {title} 时出错: {str(e)}")

# from concurrent.futures import ThreadPoolExecutor
# import threading
#
# # 确保输出目录存在
# os.makedirs("/Volumes/tish/composed", exist_ok=True)
# titles = read_file_contents("/Volumes/tish/1113902-房产那些事儿")
#
# # 创建一个线程锁，用于确保文件删除操作的线程安全
# file_lock = threading.Lock()
#
# def process_video(title):
#     try:
#         video_path = f"/Volumes/tish/1113902-房产那些事儿/{title}.mp4"
#         audio_path = f"/Volumes/tish/1113902-房产那些事儿/{title}.mp3"
#         output_path = f"/Volumes/tish/composed/{title}.mp4"
#
#         video = VideoFileClip(video_path)
#         audio = AudioFileClip(audio_path)
#
#         if audio.duration != video.duration:
#             audio = audio.set_duration(video.duration)
#
#         final_clip = video.set_audio(audio)
#         final_clip.write_videofile(
#             output_path,
#             codec="h264_videotoolbox",
#             audio_codec="aac",
#             verbose=False,
#         )
#
#         # 关闭剪辑以释放资源
#         video.close()
#         audio.close()
#         final_clip.close()
#
#         # 使用锁来确保安全删除文件
#         with file_lock:
#             if os.path.exists(video_path):
#                 os.remove(video_path)
#             if os.path.exists(audio_path):
#                 os.remove(audio_path)
#
#         print(f"处理完成并清理: {title}")
#     except Exception as e:
#         print(f"处理 {title} 时出错: {str(e)}")
#
#
# # 使用ThreadPoolExecutor进行多线程处理
# # 设置max_workers为CPU核心数的2-4倍，根据你的硬件调整
# with ThreadPoolExecutor(max_workers=os.cpu_count()//2) as executor:
#     executor.map(process_video, titles)
#
# print("所有任务处理完成！")