import json
import time
from typing import Union, List

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


def generate_video_summary(video_path: str, bvid: str, config: dict) -> Union[str, List[str]]:
    """
    对视频进行语音识别并生成总结，同时保存完整快照
    """
    path_obj = Path(video_path)
    if not path_obj.exists():
        logger.error(f"文件不存在: {video_path}")
        return "错误：视频文件缺失。"

    try:
        # --- 1. 语音转写 (多语言自适应) ---
        logger.info(f"[{bvid}] 开始转写 (自动语种识别)...")
        result = mlx_whisper.transcribe(
            str(path_obj),
            path_or_hf_repo=config['whisper_model'],
            initial_prompt="Hello, welcome to my video. Let's get started!",  # 这是一个通用技巧，用带标点的英文引导模型输出标点
            # language 参数留空或不写，默认自动检测
        )
        transcript = result.get('text', '').strip()

        if not transcript:
            return "未能识别到有效语音。"

        # --- 2. LLM 总结 (强约束提示词) ---
        llm_config = config['llm_model']
        # 判断是单个模型字符串还是模型列表
        is_multi_model = isinstance(llm_config, list)
        models = llm_config if is_multi_model else [llm_config]

        logger.info(f"[{bvid}] 开始生成总结，使用模型: {models}...")

        # """
        # Write the summary in the SAME LANGUAGE as the transcript (e.g., if the transcript is English, summarize in English; if Chinese, summarize in Chinese).
        # # 注意：如果你希望所有外语视频都强制总结为中文，请将上面这行改为：Write the summary strictly in Simplified Chinese.
        # """

        # 采用全英文指令设定强边界，但要求模型根据输入内容智能决定输出语言
        prompt = f"""You are a highly efficient content summarizer. Analyze the <transcript> and provide a direct, concise summary.

        <transcript>
        {transcript}
        </transcript>

        [STRICT CONSTRAINTS]
        1. Output Language: Write the summary strictly in Simplified Chinese.
        2. Format: Output exactly ONE single continuous paragraph. NO bullet points, NO lists, NO newlines.
        3. Zero Filler: Output the summary DIRECTLY. Do NOT use introductory phrases like "The video discusses", "Summary:", or "Here is the summary".
        """

        summaries_list = []
        for model_name in models:
            try:
                # 遍历模型列表进行推理
                # 可以适当增加 temperature 参数控制稳定性，建议 0.3 左右
                response = ollama.chat(model=model_name, messages=[
                    {'role': 'user', 'content': prompt}
                ], options={'temperature': 0.3})

                summaries_list.append(response['message']['content'].strip())
                logger.info(f"[{bvid}] 模型 {model_name} 总结完成。")

            except Exception as e:
                err_msg = f"模型 {model_name} 生成出错: {str(e)}"
                logger.error(err_msg)
                summaries_list.append(err_msg)

        # 如果配置是列表则返回列表，是字符串则返回字符串
        final_summary = summaries_list if is_multi_model else summaries_list[0]

        # --- 3. 存储详尽日志 (快照) ---
        # 即使飞书只推送300字，本地也要存下完整的 transcript 和 summary
        snapshot_data = {
            "bvid": bvid,
            "video_title": path_obj.name,
            "process_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            # 这里自动适配：如果是多模型，summary_full 为 list；单模型则为 str
            "transcript": transcript,  # 存下完整字幕，方便以后搜索
            "summary_full": final_summary,  # 存下完整总结
            "models_used": models  # 额外记录使用了哪些模型
        }
        _save_snapshot(config.get('snapshot_dir'), bvid, snapshot_data)

        return final_summary

    except Exception as e:
        logger.exception(f"AI 环节崩溃: {e}")
        return f"AI 处理异常: {str(e)}"