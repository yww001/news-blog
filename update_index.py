#!/usr/bin/env python3
"""Update index.html for 2026年07月24日."""
import json

# Read news data
with open("news_data_20260724.json", "r", encoding="utf-8") as f:
    news_items = json.load(f)

# Build new news cards HTML
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

# Read current index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace date references (07月23日 -> 07月24日)
html = html.replace("2026年07月23日", "2026年07月24日")

# Find and replace news grid section
# The grid starts after the warning div and ends before the closing </div> of content
start_marker = '<div class="warning">'
end_marker = '</div>\n        </div>\n    <script src="https://giscus.app/client.js"'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

new_section = start_marker + '''
                                                <div class="news-grid">
''' + cards_html + '''
</div>
        </div>
    <script src="https://giscus.app/client.js"
'''

new_html = html[:start_idx] + new_section + html[end_idx + len(end_marker):]

# Write updated index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("index.html updated successfully!")
print(f"Total news cards: {len(news_items)}")