import shutil
import tempfile
from pathlib import Path
from google import genai
from google.genai import types
import time
from datetime import datetime


def gemini_summarize_video(video_path, api_key, log_dir=None):
    """
    使用 Google Gemini API 上传并总结本地视频内容。

    该函数会自动处理中文路径问题（通过创建临时副本），上传视频到 Gemini，
    轮询处理状态，并在生成总结后清理本地及云端的临时文件。

    Parameters
    ----------
    video_path : str
        本地视频文件的绝对路径或相对路径。
    api_key : str
        Google AI Studio 的 API Key。
    log_dir : str, optional
        是否将处理日志和最终结果保存为本地 .txt 文件，默认为 None。

    Returns
    -------
    str
        API 生成的视频总结文本。如果发生严重错误，返回错误描述字符串。

    Raises
    ------
    FileNotFoundError
        如果提供的 video_path 不存在。
    ValueError
        如果视频在云端处理失败 (State: FAILED)。

    Notes
    -----
    - 使用了 `tempfile` 创建临时副本以避免非 ASCII 路径上传错误。
    - 生成结束后会自动调用 `client.files.delete` 清理云端占用。
    """

    # 1. 初始化客户端
    client = genai.Client(api_key=api_key)

    # 用于内存中存储日志
    logs = []

    def log(message):
        """记录带时间戳的日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        logs.append(entry)
        if log_dir is not None:
            print(entry)  # 如果需要保存日志，通常也希望在控制台看到进度

    # 标准化路径
    vp = Path(video_path)

    # 获取系统临时目录 (自动适配 Mac/Win/Linux)
    temp_dir = Path(tempfile.gettempdir())

    # 使用固定前缀+原始后缀，确保是纯英文路径
    temp_vp = temp_dir / f'video_to_summarize{vp.suffix}'

    try:
        log(f"任务开始。目标文件: {vp.name}")

        # 2. 本地文件检查与临时拷贝
        if not vp.exists():
            raise FileNotFoundError(f"找不到文件: {vp.name}")

        # 复制文件到临时目录
        shutil.copy(vp, temp_vp)
        log(f"已创建临时副本: {temp_vp}")
        log("正在上传视频到 Gemini File API (这可能需要一点时间)...")
        video_file = client.files.upload(file=temp_vp)
        log(f"上传成功。File URI: {video_file.uri}")

        # 3. 等待视频处理 (Gemini 需要时间解析视频)
        log("正在等待视频处理状态变为 ACTIVE...")
        while video_file.state.name == "PROCESSING":
            time.sleep(2)
            # 刷新文件状态
            video_file = client.files.get(name=video_file.name)

        if video_file.state.name == "FAILED":
            raise ValueError(f"视频处理失败 (State: {video_file.state.name})")

        log("视频就绪，开始生成内容。")

        # 4. 设置模型和提示词
        prompt = (
            f"文件名：{vp.name}\n"
            "请观看这个视频，并生成一份中文总结。\n"
            "要求：\n"
            "1. 内容紧凑，严格控制在 200 字左右。\n"
            "2. 重点概括核心观点、关键事件或重要细节。\n"
            "3. 直接输出总结段落，绝不包含任何客套话或标题。"
        )

        log("发送生成请求...")
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[video_file, prompt],
            config=types.GenerateContentConfig(
                temperature=0.7
            )
        )

        # 获取结果并去除首尾空白
        summary_result = response.text.strip()
        log("总结生成完毕。")

        # 5. 根据参数决定是否保存日志文件
        if log_dir is not None:
            log_dir = Path(log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)
            timestamp_str = datetime.now().strftime("%Y%m%d(%H%M%S)")
            # 清理文件名中的非法字符，防止日志文件名报错
            safe_name = "".join([c for c in vp.stem if c.isalnum() or c in (' ', '-', '_')]).strip()
            log_filename = log_dir / f"gemini_log_{safe_name}_{timestamp_str}.txt"

            with open(log_filename, "w", encoding="utf-8") as f:
                # 写入处理日志
                f.write("\n".join(logs))
                f.write("\n\n" + "=" * 30 + " 视频总结结果 " + "=" * 30 + "\n\n")
                # 写入最终结果
                f.write(summary_result)

            print(f"\n[System] 日志和结果已保存至文件: {log_filename}")

        return summary_result

    except Exception as e:
        error_msg = f"发生错误: {str(e)}"
        log(error_msg)
        if log_dir is not None:
            # 即使出错也尝试保存已有日志
            log_dir = Path(log_dir)
            log_filename = log_dir / f"gemini_error_log.txt"
            with open(log_filename, "a", encoding="utf-8") as f:
                f.write("\n".join(logs))
        return error_msg

    finally:
        # 6. 清理本地临时文件
        if temp_vp.exists():
            try:
                temp_vp.unlink()
            except Exception as e:
                print(f"[Warning] 本地临时文件清理失败: {e}")

        # 7. 清理云端文件 (强烈建议开启)
        # if video_file:
        #     try:
        #         client.files.delete(name=video_file.name)
        #         # 使用 print 避免污染 log 列表（因为任务已经结束）
        #         print(f"[{datetime.now().strftime('%H:%M:%S')}] 已清理云端临时文件: {video_file.name}")
        #     except Exception as e:
        #         print(f"[Warning] 云端文件清理失败: {e}")


# --- 使用示例 ---
if __name__ == "__main__":
    # 替换为你的 Key
    MY_API_KEY = "Your_API_Key"
    VIDEO_PATH = "test_video.mp4"  # 确保目录下有这个视频

    # 模式 2: 纯净模式，只拿结果
    summary = gemini_summarize_video(VIDEO_PATH, MY_API_KEY)
    print(summary)
