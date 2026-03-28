#!/usr/bin/env python3
"""
为24日历史页面生成新图片
"""

import os
import subprocess
import time

# 24日新闻对应的图片描述
image_prompts = [
    "以色列军队空袭德黑兰城市，导弹爆炸，军事行动，新闻照片风格",
    "特拉维夫市中心建筑被导弹击中，破坏场景，新闻照片风格",
    "习近平在河北雄安新区考察，现代化城市建设，新闻照片风格",
    "伊朗外交部发言人，外交谈判，新闻照片风格",
    "黄金价格暴跌，金融市场图表，新闻照片风格",
    "霍尔木兹海峡油轮运输，能源危机，新闻照片风格",
    "以色列政府会议，外交谈判，新闻照片风格",
    "华能集团总部大楼，企业入驻雄安，新闻照片风格",
    "北京四中雄安校区，校园建筑，学生活动，新闻照片风格",
    "雄安新区建设工地，城市发展，新闻照片风格"
]

# 输出目录
output_dir = "/home/swg/.openclaw/workspace/news-blog/images/20260324"
os.makedirs(output_dir, exist_ok=True)

# NVIDIA API配置
nvidia_api_key = os.environ.get("NVIDIA_API_KEY", "")

if not nvidia_api_key:
    print("❌ 未找到NVIDIA_API_KEY环境变量")
    exit(1)

# 生成图片
for i, prompt in enumerate(image_prompts, 1):
    output_file = f"{output_dir}/news_{i}.png"

    print(f"🖼️  生成图片 {i}/10: {prompt[:30]}...")

    # 使用nvidia-genai skill生成图片
    cmd = [
        "python3", "/home/swg/.openclaw/workspace/skills/nvidia-genai/scripts/generate.py",
        "--prompt", prompt,
        "--output", output_file,
        "--api-key", nvidia_api_key
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ 图片 {i}/10 生成成功")
        else:
            print(f"❌ 图片 {i}/10 生成失败: {result.stderr}")
    except subprocess.TimeoutExpired:
        print(f"❌ 图片 {i}/10 生成超时")
    except Exception as e:
        print(f"❌ 图片 {i}/10 生成异常: {str(e)}")

    # 等待一下避免API限流
    time.sleep(2)

print("\n✅ 所有图片生成完成")
print(f"输出目录: {output_dir}")
