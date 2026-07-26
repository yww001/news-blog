#!/usr/bin/env python3
import json
import re

DATE_DISPLAY = "2026年07月26日"
DATE_ID = "20260726"

# Read news data
with open("news_data_20260726.json", "r", encoding="utf-8") as f:
    news_items = json.load(f)

# Read current index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update title
html = re.sub(r'<title>.*?环球新闻</title>', f'<title>{DATE_DISPLAY} 环球新闻</title>', html)

# Update meta description
html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{DATE_DISPLAY}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">', html)

# Update cover subtitle
html = re.sub(r'<p class="cover-subtitle">.*?</p>', f'<p class="cover-subtitle">全球20条热点新闻 · {DATE_DISPLAY}</p>', html)

# Build new news cards HTML
new_cards = []
for item in news_items:
    num = item["number"]
    tag = item["tag"]
    title = item["title"]
    summary = item["summary"]
    img_path = f"images/news_{DATE_ID}_{num}.png"
    
    card = f'''<article class="news-card" data-tag="{tag}">
    <img class="news-image" src="{img_path}" alt="{title}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{num}</span>
        <h3 class="news-title">{title}</h3>
        <p class="news-summary">{summary}</p>
        <div><span class="tag">{tag}</span></div>
    </div>
</article>'''
    new_cards.append(card)

new_cards_html = "\n".join(new_cards)

# Find the news-grid div and replace all article elements inside it
# The pattern matches from <div class="news-grid"> to the next </div>
pattern = r'<div class="news-grid">.*?</div>\s*</div>'
replacement = f'<div class="news-grid">\n{new_cards_html}\n\n</div>'

html = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Write updated index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"✓ index.html updated with {len(news_items)} news cards for {DATE_DISPLAY}")

# Verify key elements are preserved
if 'video id="coverVideo"' in html and 'src="videos/cover.mp4"' in html:
    print("✓ Video element preserved")
else:
    print("✗ WARNING: Video element may have been modified!")

if 'images/website-background-8k.png' in html:
    print("✓ Background image preserved")
else:
    print("✗ WARNING: Background image may have been modified!")