# 导入合并mp4和mp3相关模块
# from moviepy.editor import *


# # 确保输出目录存在
# os.makedirs("data", exist_ok=True)
#
# video_path = f"video/{title}.mp4"
# audio_path = f"video/{title}.mp3"
# output_path = f"data/{title}_output.mp4"
#
# video = VideoFileClip(video_path)
# audio = AudioFileClip(audio_path)
#
# if audio.duration != video.duration:
#     audio = audio.set_duration(video.duration)
#
# final_clip = video.set_audio(audio)
# final_clip.write_videofile(
#     output_path,
#     codec="libx264",
#     audio_codec="aac",
#     threads=4,
#     verbose=False
# )