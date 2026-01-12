import json
import time

import mlx_whisper
import ollama
from loguru import logger
from pathlib import Path


def _save_snapshot(snapshot_dir, bvid, data):
    """私有函数：保存 AI 处理的原始快照"""
    if not snapshot_dir:
        return

    try:
        folder = Path(snapshot_dir) / time.strftime("%Y-%m-%d")
        folder.mkdir(parents=True, exist_ok=True)

        file_path = folder / f"{bvid}_ai_data.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"AI 原始快照已存至: {file_path}")
    except Exception as e:
        logger.error(f"保存快照失败: {e}")


def generate_video_summary(video_path: str, bvid: str, config: dict) -> str:
    """
    对视频进行语音识别并生成总结，同时保存完整快照
    """
    path_obj = Path(video_path)
    if not path_obj.exists():
        logger.error(f"文件不存在: {video_path}")
        return "错误：视频文件缺失。"

    try:
        # --- 1. 语音转写 ---
        logger.info(f"[{bvid}] 开始转写...")
        result = mlx_whisper.transcribe(
            str(path_obj),
            path_or_hf_repo=config['whisper_model'],
            language='zh',
            initial_prompt="这是一段中文视频，请使用简体中文转录，并正确添加标点符号。"
        )
        transcript = result.get('text', '')

        if not transcript:
            return "未能识别到有效语音。"

        # --- 2. LLM 总结 ---
        logger.info(f"[{bvid}] 开始生成总结...")
        prompt = (
            "你是一个专业的中文内容编辑。请阅读以下【视频转录文本】，并生成一份精简的摘要。\n\n"
            f"<视频转录文本>\n{transcript}\n</视频转录文本>\n\n"
            "【输出要求】\n1. 禁止分点 2. 唯一纯文本段落 3. 200字以内 4. 直接输出内容。"
        )

        response = ollama.chat(model=config['llm_model'], messages=[
            {'role': 'user', 'content': prompt}
        ])
        summary = response['message']['content'].strip()

        # --- 3. 存储详尽日志 (快照) ---
        # 即使飞书只推送300字，本地也要存下完整的 transcript 和 summary
        snapshot_data = {
            "bvid": bvid,
            "video_title": path_obj.name,
            "process_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "transcript": transcript,  # 存下完整字幕，方便以后搜索
            "summary_full": summary  # 存下完整总结
        }
        _save_snapshot(config.get('snapshot_dir'), bvid, snapshot_data)

        return summary

    except Exception as e:
        logger.exception(f"AI 环节崩溃: {e}")
        return f"AI 处理异常: {str(e)}"