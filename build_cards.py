#!/usr/bin/env python3
import json

with open("news_data_20260724.json", "r", encoding="utf-8") as f:
    news_items = json.load(f)

# Build news cards HTML
cards_html = ""
for item in news_items:
    num = item["number"]
    title = item["title"]
    summary = item["summary"]
    tag = item["tag"]
    image = item["image"]
    cards_html += f'''<article class="news-card" data-tag="{tag}">
    <img class="news-image" src="{image}" alt="{title}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{num}</span>
        <h3 class="news-title">{title}</h3>
        <p class="news-summary">{summary}</p>
        <div><span class="tag">{tag}</span></div>
    </div>
</article>
'''

with open("/tmp/cards_20260724.html", "w") as f:
    f.write(cards_html)
print("Cards saved to /tmp/cards_20260724.html")