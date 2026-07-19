#!/usr/bin/env python3
"""Retry failed images for 2026年07月20日"""
import os
import time
import requests

DATE_STR = "20260720"
IMAGES_DIR = "/home/swg/.openclaw/workspace/news-blog/images"

FAILED = [
    ("04", "Chinese yuan and US dollar banknotes, financial charts showing upward trend, modern banking district background, photorealistic, ultra detailed, 8K, high resolution"),
    ("05", "European Union and China flags side by side, formal diplomatic meeting in Beijing garden setting, businessmen shaking hands, photorealistic, ultra detailed, 8K, high resolution"),
    ("12", "Heavy rainfall flooding city streets, Beijing cityscape, emergency rescue vehicles, people with umbrellas, photorealistic, ultra detailed, 8K, high resolution"),
]

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
MODEL = "cogview-3-flash"

def generate_image(news_number, prompt, retry=0):
    if retry > 3:
        print(f"  [FAIL] Image {news_number} failed after 3 retries")
        return False
    try:
        print(f"  Generating image {news_number}...")
        payload = {"model": MODEL, "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]}
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        if isinstance(content, list) and len(content) > 0:
            image_url = content[0].get("url") or content[0]
        elif isinstance(content, str):
            image_url = content
        else:
            print(f"  [FAIL] Unexpected content format: {type(content)}")
            return False
        img_resp = requests.get(image_url, timeout=60)
        img_resp.raise_for_status()
        output_path = os.path.join(IMAGES_DIR, f"news_{DATE_STR}_{news_number}.png")
        with open(output_path, "wb") as f:
            f.write(img_resp.content)
        print(f"  [OK] Saved {os.path.basename(output_path)} ({len(img_resp.content)} bytes)")
        return True
    except Exception as e:
        print(f"  [RETRY] Image {news_number}: {e}")
        time.sleep(5)
        return generate_image(news_number, prompt, retry + 1)

print("Retrying failed images...")
for number, prompt in FAILED:
    generate_image(number, prompt)

print("\nDone!")