#!/usr/bin/env python3
"""Update index.html with 2026年07月17日 news"""

import json

with open("news_data_20260717.json", "r", encoding="utf-8") as f:
    news_items = json.load(f)

# Read existing index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update date in title and cover
html = html.replace("2026年07月16日", "2026年07月17日")
html = html.replace("2026年07月 - 历史存档", "2026年07月17日 环球新闻")
html = html.replace("2026年 - 历史新闻", "2026年07月17日 环球新闻")

# Build new news cards HTML
new_cards = []
for news in news_items:
    card = f'''<article class="news-card" data-tag="{news["tag"]}">
    <img class="news-image" src="images/news_20260717_{news["number"]}.png" alt="{news["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{news["number"]}</span>
        <h3 class="news-title">{news["title"]}</h3>
        <p class="news-summary">{news["summary"]}</p>
        <div><span class="tag">{news["tag"]}</span></div>
    </div>
</article>'''
    new_cards.append(card)

new_cards_html = "\n".join(new_cards)

# Find and replace news grid section
import re

# Match the news grid content between <div class="news-grid"> and </div>
pattern = r'<div class="news-grid">.*?</div>\s*</div>'
replacement = f'<div class="news-grid">\n{new_cards_html}\n</div>\n            </div>'

# Use DOTALL to match across lines
html_new = re.sub(pattern, replacement, html, flags=re.DOTALL)

# Write updated index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_new)

print("index.html updated successfully!")
print(f"Updated with {len(news_items)} news items")