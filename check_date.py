#!/usr/bin/env python3
"""手动生成环球新闻首页 - 2026年08月22日"""
import json
import os
from datetime import datetime

# 日期
today = datetime.now()
date_str = today.strftime("%Y年%m月%d日")
date_num = today.strftime("%Y%m%d")

print(f"日期: {date_str}")
print(f"日期数字: {date_num}")

# 检查是否有今天的新闻数据
news_data_file = f"news_data_{date_num}.json"
if os.path.exists(news_data_file):
    with open(news_data_file, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
    print(f"找到现有数据: {len(news_data.get('news', []))} 条")
else:
    print("无现有数据，需要生成")
    news_data = None

# 检查 index.html 日期
if os.path.exists("index.html"):
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
    if date_str in content:
        print(f"index.html 已是 {date_str}")
    else:
        print("index.html 需要更新")
