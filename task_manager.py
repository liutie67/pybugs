import json
import time
import requests
from pathlib import Path
from loguru import logger

# 引入你的爬虫和上面的 AI 模块
from bvid_from_web import get1up
from ai_summarize_video.localai_video_summarize import generate_video_summary


def push_to_feishu(webhook_url: str, content: str):
    """发送飞书通知"""
    if not webhook_url:
        logger.warning("未配置飞书 Webhook，跳过推送")
        return

    payload = {
        "msg_type": "text",
        "content": {"text": content}
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        result = response.json()
        if result.get("code") == 0:
            logger.info("飞书消息推送成功")
        else:
            logger.error(f"飞书推送失败: {result.get('msg')}")
    except Exception as e:
        logger.error(f"飞书推送请求发生异常: {e}")


def run_bilibili_task(config: dict):
    """
    核心任务流程
    :param config: 包含路径、key、up主信息的配置字典
    """
    logger.info(">>> 启动 Bili 增量扫描 <<<")

    update_details = []
    total_new = 0

    for uper_id in config['upers']:
        uper_name = config['uper_names'].get(uper_id, uper_id)

        print(f'{uper_name}({uper_id}): ')
        # 爬虫下载
        down_count, _, upload_dates, titles, folders, bvids = get1up(
            uper=uper_id, lice=1, video_path=config['media_path'], exist_nm=3,
        )

        if down_count > 0:
            total_new += down_count
            for i in range(down_count):
                # 1. 寻找视频文件
                video_file = Path(config['media_path']) / uper_id / folders[
                    i] / f"{upload_dates[i]}{bvids[i]}{titles[i]}.mp4"

                # 2. 调用 AI 模块
                full_summary = generate_video_summary(str(video_file), bvids[i], config)

                # 3. 推送前截断 (250-300字)
                # 确保飞书通知简洁，不刷屏
                limit = 280
                short_summary = full_summary[:limit] + "..." if len(full_summary) > limit else full_summary

                # 4. 拼装单条详情
                detail = (
                    f"➡️ {uper_name}"
                    f"🎬 {titles[i]}\n"
                    f"🔗 https://www.bilibili.com/video/{bvids[i]}\n"
                    f"🤖 ({config['whisper_model']})"
                    f"🤖 ({config['llm_model']})"
                    f"📝 主要内容: "
                    f"{short_summary}"
                )
                update_details.append(detail)
                update_details.append("-" * 15)

        # 发送汇总消息
    if total_new > 0:
        final_msg = f"✅ 更新报告 ({total_new}个视频)\n\n" + "\n".join(update_details)
        push_to_feishu(config['feishu_webhook'], final_msg)
        logger.success("扫描任务完成且已推送")