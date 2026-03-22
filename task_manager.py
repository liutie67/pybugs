import json
import time
import requests
from pathlib import Path
from loguru import logger

# 引入你的爬虫和上面的 AI 模块
from bvid_from_web import get1up, get_fav_folder
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

        if 'fav_' in uper_id:
            down_count, _, upload_dates, titles, folders, bvids = get_fav_folder(
                fav_id=uper_id, lice=1, video_path=config['media_path'], exist_nm=3,
            )
        else:
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
                ai_result = generate_video_summary(str(video_file), bvids[i], config)

                # 统一规格化为列表，方便统一逻辑处理
                llm_config = config['llm_model']
                if isinstance(llm_config, list):
                    model_list = llm_config
                    summary_list = ai_result
                else:
                    model_list = [llm_config]
                    summary_list = [ai_result]

                # 3. 推送前截断 (250-300字)
                # 确保飞书通知简洁，不刷屏
                summary_sections = []
                limit = 280  # 单个模型的字数限制

                for model_name, content in zip(model_list, summary_list):
                    # 防止内容为空的处理
                    content = str(content) if content else "无内容"
                    # 截断
                    short_s = content[:limit] + "..." if len(content) > limit else content
                    # 格式: 🤖 [模型名] \n 内容
                    summary_sections.append(f"🤖 [{model_name}]\n{short_s}")

                # 将所有模型的总结用换行隔开
                final_summary_text = "\n".join(summary_sections)

                # 4. 拼装单条详情
                detail = (
                    f"➡️ {uper_name}\n"
                    f"🎬 {titles[i]}\n"
                    f"🔗 https://www.bilibili.com/video/{bvids[i]}\n"
                    f"👂 听写:({config['whisper_model']})\n"
                    f"📝 主要内容:\n"
                    f"{final_summary_text}"
                )

                update_details.append(detail)
                update_details.append("-" * 15)

        # 发送汇总消息
    if total_new > 0:
        final_msg = f"✅ 更新报告 ({total_new}个视频)\n" + "\n".join(update_details)
        push_to_feishu(config['feishu_webhook'], final_msg)
        logger.success("扫描任务完成且已推送")