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

# 替换日期
old_date = re.search(r'<title>\d{4}年\d{2}月\d{2}日 环球新闻</title>', html).group(0)
new_date = f'<title>{data["date"]} 环球新闻</title>'
html = html.replace(old_date, new_date)

# 替换 meta description
old_meta = re.search(r'<meta name="description" content="\d{4}年\d{2}月\d{2}日[^"]*"', html).group(0)
new_meta = f'<meta name="description" content="{data["date"]}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">'
html = html.replace(old_meta, new_meta)

# 替换 cover-subtitle 日期
old_subtitle = re.search(r'<p class="cover-subtitle">全球20条热点新闻 · \d{4}年\d{2}月\d{2}日</p>', html).group(0)
new_subtitle = f'<p class="cover-subtitle">全球20条热点新闻 · {data["date"]}</p>'
html = html.replace(old_subtitle, new_subtitle)

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
