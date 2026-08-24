#!/usr/bin/env python3
"""从 news_data_YYYYMMDD.json 生成 index.html，仅替换日期、卡片、图片路径。
保留原有 cover-section（视频标签）、导航栏、CSS 变量、布局、背景图。
"""
import json, re, sys, os
from pathlib import Path

BLOG = Path("/home/swg/.openclaw/workspace/news-blog")
date_compact = sys.argv[1]  # e.g. 20260808

with open(BLOG / f"news_data_{date_compact}.json") as f:
    data = json.load(f)

with open(BLOG / "index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 替换日期 - 支持多种 title 格式
date_compact_short = data["date"].replace("年", "").replace("月", "").replace("日", "")
# format 1: "全球20条热点新闻 - 2026年08月16日 | 环球新闻"
title_pattern = re.compile(r'<title>全球20条热点新闻 - \d{4}年\d{2}月\d{2}日 \| 环球新闻</title>')
title_match = title_pattern.search(html)
if title_match:
    html = html.replace(title_match.group(0), f'<title>全球20条热点新闻 - {data["date"]} | 环球新闻</title>')
else:
    # format 2: "2026年08月16日 环球新闻"
    title_pattern2 = re.compile(r'<title>\d{4}年\d{2}月\d{2}日 环球新闻</title>')
    title_match2 = title_pattern2.search(html)
    if title_match2:
        html = html.replace(title_match2.group(0), f'<title>{data["date"]} 环球新闻</title>')

# 替换 meta description
desc_pattern = re.compile(r'<meta name="description" content="\d{4}年\d{2}月\d{2}日[^"]*"[^>]*>')
desc_match = desc_pattern.search(html)
if desc_match:
    html = html.replace(desc_match.group(0), f'<meta name="description" content="{data["date"]}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">')

# 替换 cover-subtitle 日期
subtitle_pattern = re.compile(r'<p class="cover-subtitle">全球20条热点新闻 · \d{4}年\d{2}月\d{2}日</p>')
subtitle_match = subtitle_pattern.search(html)
if subtitle_match:
    html = html.replace(subtitle_match.group(0), f'<p class="cover-subtitle">全球20条热点新闻 · {data["date"]}</p>')

# 替换 footer 日期
footer_pattern = re.compile(r'所有新闻内容仅供参考，请以官方发布为准 · \d{4}年\d{2}月\d{2}日')
footer_match = footer_pattern.search(html)
if footer_match:
    html = html.replace(footer_match.group(0), f'所有新闻内容仅供参考，请以官方发布为准 · {data["date"]}')

# 替换所有 news-card 块：抓 <article ...>...</article>
card_pattern = re.compile(r'<article class="news-card" data-tag="[^"]*">.*?</article>', re.DOTALL)
existing_cards = card_pattern.findall(html)
print(f"Existing cards: {len(existing_cards)}")

# 按数据生成新卡片
new_cards = []
for n in data["news"]:
    num = n["news-number"]
    title = n["news-title"]
    summary = n["news-summary"]
    tag = n["tag"]
    img = f"images/news_{date_compact}_{num}.png"
    card = f'''<article class="news-card" data-tag="{tag}">
    <img class="news-image" src="{img}" alt="{title}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{num}</span>
        <h3 class="news-title">{title}</h3>
        <p class="news-summary">{summary}</p>
        <div><span class="tag">{tag}</span></div>
    </div>
</article>'''
    new_cards.append(card)

# 在第一个 <article 之前到末尾 </article> 后保留：实际上我们要做的是
# 把旧卡片序列整段替换为新卡片序列（位置：第一个 <article 起到最后一个 </article> 止）
first_idx = html.find('<article')
last_idx = html.rfind('</article>') + len('</article>')
new_block = '\n'.join(new_cards)
html = html[:first_idx] + new_block + html[last_idx:]

with open(BLOG / "index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Written index.html with {len(new_cards)} cards for {data['date']}")
