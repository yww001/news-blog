#!/usr/bin/env python3
"""Generate images for 20260820 and 20260821 archive pages"""
import os
import re
import json
import time
from PIL import Image
import io

BLOG_PATH = "/home/swg/.openclaw/workspace/news-blog"
IMAGES_DIR = os.path.join(BLOG_PATH, "images")

def extract_news_from_html(html_path):
    """Extract news titles and summaries from HTML"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract news items
    pattern = r'<article class="news-card"[^>]*>.*?<span class="news-number">(\d+)</span>.*?<h3 class="news-title">(.*?)</h3>.*?<p class="news-summary">(.*?)</p>.*?<span class="tag">(.*?)</span>'
    matches = re.findall(pattern, content, re.DOTALL)
    
    news_items = []
    for m in matches:
        num, title, summary, tag = m
        news_items.append({
            'news-number': num.zfill(2),
            'news-title': title.strip(),
            'news-summary': summary.strip(),
            'tag': tag.strip()
        })
    return news_items

def generate_image_prompt(title, summary, tag, date):
    """Generate image generation prompt from news item"""
    # Extract key visual elements from title and summary
    prompt = f"{title}, {summary[:100]}..., photorealistic, ultra detailed, 8K, high resolution, professional news photography"
    return prompt

def generate_cover_prompt(date):
    """Generate cover image prompt"""
    return f"Global news headline montage for {date}, world map with digital data streams, photorealistic, ultra detailed, 8K, high resolution, cinematic lighting"

def main():
    # Process both dates
    dates = ['20260820', '20260821']
    
    for date in dates:
        html_path = os.path.join(BLOG_PATH, "history", "2026", "08", f"{date}.html")
        if not os.path.exists(html_path):
            print(f"HTML not found: {html_path}")
            continue
        
        print(f"\nProcessing {date}...")
        news_items = extract_news_from_html(html_path)
        print(f"Found {len(news_items)} news items")
        
        # Generate news images
        for i, item in enumerate(news_items, 1):
            num = item['news-number']
            filename = f"news_{date}_{num}.png"
            filepath = os.path.join(IMAGES_DIR, filename)
            
            if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
                print(f"  ✓ {filename} exists")
                continue
            
            prompt = generate_image_prompt(item['news-title'], item['news-summary'], item['tag'], date)
            print(f"  → Generating {filename}: {item['news-title'][:40]}...")
            
            # Call image_generate tool (will be done via hermes_tools)
            # For now, just log what would be generated
            # This script is for planning; actual generation uses image_generate tool
        
        # Generate cover image
        cover_filename = f"cover_{date}.png"
        cover_path = os.path.join(IMAGES_DIR, cover_filename)
        if not os.path.exists(cover_path):
            cover_prompt = generate_cover_prompt(date)
            print(f"  → Generating cover: {cover_filename}")
    
    print("\nDone planning. Now generating images via image_generate tool...")

if __name__ == "__main__":
    main()
