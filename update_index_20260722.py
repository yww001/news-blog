#!/usr/bin/env python3
import json
import re

# Load news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260722.json', 'r', encoding='utf-8') as f:
    news_data = json.load(f)

# Read the current index.html
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Update date in title and subtitle
html_content = re.sub(
    r'<title>2026年\d+月\d+日 环球新闻</title>',
    '<title>2026年07月22日 环球新闻</title>',
    html_content
)
html_content = re.sub(
    r'2026年\d+月\d+日',
    '2026年07月22日',
    html_content
)

# Generate new news cards HTML
new_cards = []
for news in news_data:
    num = news['number']
    title = news['title']
    summary = news['summary']
    tag = news['tag']
    img_path = f'images/news_20260722_{num}.png'
    
    card_html = f'''<article class="news-card" data-tag="{tag}">
    <img class="news-image" src="{img_path}" alt="{title}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{num}</span>
        <h3 class="news-title">{title}</h3>
        <p class="news-summary">{summary}</p>
        <div><span class="tag">{tag}</span></div>
    </div>
</article>'''
    new_cards.append(card_html)

new_cards_html = '\n'.join(new_cards)

# Find the news grid section and replace
# The pattern finds the news-grid div and replaces all article cards inside it
pattern = r'(<div class="news-grid">\s*).*?(</div>\s*</div>\s*<script)'
replacement = r'\1' + new_cards_html + r'\n\n\n\2'

html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# Write the updated HTML
with open('/home/swg/.openclaw/workspace/news-blog/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("index.html updated successfully!")
print(f"Updated with {len(news_data)} news cards")