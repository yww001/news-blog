#!/usr/bin/env python3
"""Generate images for 2026年07月17日 news using CogView-3-Flash API"""

import os
import json
import base64
import subprocess
import time
from pathlib import Path

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
NEWS_FILE = "news_data_20260717.json"
OUTPUT_DIR = "images"

def load_news():
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_image(news_item, retry=True):
    """Generate image using CogView-3-Flash API"""
    import urllib.request
    
    news_num = news_item["number"]
    prompt = news_item["image_prompt"]
    output_path = f"{OUTPUT_DIR}/news_20260717_{news_num}.png"
    
    # Check if already exists
    if os.path.exists(output_path):
        print(f"Image {news_num} already exists, skipping")
        return True
    
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            
            # Extract base64 image
            if "data:image/png;base64," in content:
                b64_data = content.split("data:image/png;base64,")[1]
            elif "data:image/jpeg;base64," in content:
                b64_data = content.split("data:image/jpeg;base64,")[1]
            else:
                b64_data = content
            
            # Remove any markdown formatting
            b64_data = b64_data.strip().strip("`").strip()
            
            image_data = base64.b64decode(b64_data)
            
            with open(output_path, "wb") as f:
                f.write(image_data)
            
            print(f"Generated image {news_num}: {output_path}")
            return True
    except Exception as e:
        print(f"Error generating image {news_num}: {e}")
        if retry:
            print(f"Retrying image {news_num}...")
            time.sleep(3)
            return generate_image(news_item, retry=False)
        return False

def main():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    news_items = load_news()
    print(f"Loaded {len(news_items)} news items")
    
    success_count = 0
    for news in news_items:
        if generate_image(news):
            success_count += 1
        time.sleep(1)  # Rate limiting
    
    print(f"\nGenerated {success_count}/{len(news_items)} images successfully")

if __name__ == "__main__":
    main()