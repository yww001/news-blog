#!/usr/bin/env python3
"""手动生成环球新闻首页 - 2026年08月22日"""
import json
import os
import subprocess
from datetime import datetime

# 日期
today = datetime.now()
date_str = today.strftime("%Y年%m月%d日")
date_num = today.strftime("%Y%m%d")

print(f"=== 手动生成环球新闻首页 ===")
print(f"日期: {date_str}")
print(f"日期数字: {date_num}")

# 检查是否有今天的新闻数据
news_data_file = f"news_data_{date_num}.json"
if os.path.exists(news_data_file):
    with open(news_data_file, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    print(f"✓ 找到现有数据: {len(news_data.get('news', []))} 条")
else:
    print(f"✗ 无现有数据，检查最近的数据...")
    # 检查最近的数据
    recent_files = sorted([f for f in os.listdir('.') if f.startswith('news_data_') and f.endswith('.json')], reverse=True)
    if recent_files:
        print(f"  最近的数据: {recent_files[0]}")
        with open(recent_files[0], 'r', encoding='utf-8') as f:
            last_data = json.load(f)
        print(f"  包含 {len(last_data.get('news', []))} 条新闻")
    else:
        print("  无可用数据")
        last_data = None

# 检查 index.html 日期
if os.path.exists("index.html"):
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    if date_str in content:
        print(f"✓ index.html 已是 {date_str}")
    else:
        print(f"✗ index.html 需要更新")
        # 检查最新提交的日期
        result = subprocess.run(['git', 'log', '--oneline', '-1', 'index.html'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  最新提交: {result.stdout.strip()}")

print("\n=== 需要手动运行首页生成任务 ===")
print("原因: cron 任务连续三天失败 (HTTP 404)")
print("已修复: 切换模型从 minimaxai/minimax-m3 到 anthropic/claude-sonnet-4")
print("下次自动运行: 2026-08-23 02:00")
