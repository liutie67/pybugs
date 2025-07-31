import subprocess


# def combine_video_audio(video_path, audio_path, output_path):
#     cmd = [
#         "ffmpeg",
#         "-i", video_path,  # 输入视频
#         "-i", audio_path,  # 输入音频
#         "-c:v", "copy",  # 视频流直接复制（不重新编码）
#         "-c:a", "copy",  # 音频转为AAC（兼容性最好，若原音频已是AAC可改为"copy"）
#         "-map", "0:v:0",  # 选择视频流
#         "-map", "1:a:0",  # 选择音频流
#         "-shortest",  # 以视频和音频中较短的时长为准
#         output_path
#     ]
#     subprocess.run(cmd, check=True)


from datetime import datetime

def combine_video_audio(video_path, audio_path, output_path, log_file=None):
    # Create a timestamp for the log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_path
    ]

    # Open log file in append mode if specified
    if log_file:
        with open(log_file, 'a') as f:
            # Write timestamp
            f.write(f"\n[{timestamp}] Executing command: {' '.join(cmd)}\n")
            f.flush()

            # Run command, redirecting both stdout and stderr to the log file
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.STDOUT,  # Combine stderr with stdout
                text=True,
                check=True
            )

            # Write completion message
            f.write(f"[{timestamp}] Command completed successfully\n")
    else:
        # If no log file specified, run normally (output will go to console)
        subprocess.run(cmd, check=True)

def replace_illegal_char(title):
    title = title.replace('\\', '_0_')
    title = title.replace('|', '_1_')
    title = title.replace(':', '_2_')
    title = title.replace('"', '_3_')
    title = title.replace('?', '_4_')
    return title