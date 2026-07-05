#!/usr/bin/env python3
"""Retry generating failed images for news 02, 03, 13, 14"""

import base64
import json
import os
import time
import urllib.request

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
IMAGES_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
DATE = "20260706"

FAILED_ITEMS = [
    {
        "number": "02",
        "title": "中俄海上联合演习在青岛正式启动",
        "image_prompt": "A naval port with Chinese and Russian warships docked side by side, naval personnel in uniform standing at attention during a military ceremony, flags of both countries waving, harbor cranes in background, photorealistic, ultra detailed, 8K, high resolution, naval military ceremony"
    },
    {
        "number": "03",
        "title": "特朗普与普京通话提议调解俄乌战争",
        "image_prompt": "Two world leaders in formal suits meeting at a diplomatic summit, American and Russian flags displayed prominently, journalists and cameras in background, serious diplomatic atmosphere, photorealistic, ultra detailed, 8K, high resolution, international diplomacy meeting"
    },
    {
        "number": "13",
        "title": "美联储维持利率不变暗示降息",
        "image_prompt": "Federal Reserve building facade in Washington DC, American flag waving, Federal Reserve chairman speaking at press conference with microphones, stock market screens in background showing financial data, photorealistic, ultra detailed, 8K, high resolution, central bank monetary policy"
    },
    {
        "number": "14",
        "title": "中国经济上半年GDP增长消费贡献率首超投资",
        "image_prompt": "Modern Beijing city skyline with tall skyscrapers and Chinese flag, busy commercial district with pedestrians and traffic, economic growth concept with rising charts, photorealistic, ultra detailed, 8K, high resolution, economic development cityscape"
    }
]

def generate_image(news_num, prompt, retries=3):
    """Generate image using CogView-3-Flash API"""
    filename = f"{IMAGES_DIR}/news_{DATE}_{news_num}.png"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = json.dumps({
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }, ensure_ascii=False).encode("utf-8")
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                API_URL,
                data=data,
                headers=headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
            
            image_url = None
            if isinstance(content, list):
                image_url = content[0].get("url")
            elif isinstance(content, str):
                if "data:image" in content:
                    b64_data = content.split("data:image/png;base64,")[1]
                    image_data = base64.b64decode(b64_data)
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    print(f"[{news_num}] Generated base64 image: {filename}")
                    return True
                elif "http" in content:
                    image_url = content
            
            if image_url:
                print(f"[{news_num}] Downloading from: {image_url[:60]}...")
                with urllib.request.urlopen(image_url, timeout=60) as img_resp:
                    image_data = img_resp.read()
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    print(f"[{news_num}] Generated image: {filename}")
                    return True
            else:
                print(f"[{news_num}] Unexpected format: {type(content)}")
                
        except Exception as e:
            print(f"[{news_num}] Error (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(3)
    
    print(f"[{news_num}] Failed after {retries} attempts")
    return False


def main():
    print("Retrying failed images...")
    print("=" * 60)
    
    success_count = 0
    for item in FAILED_ITEMS:
        print(f"\nRetrying news {item['number']}: {item['title']}")
        if generate_image(item['number'], item['image_prompt']):
            success_count += 1
        time.sleep(2)
    
    print(f"\n{'=' * 60}")
    print(f"Retry complete: {success_count}/{len(FAILED_ITEMS)} succeeded")
    
    # Verify all images exist
    print("\nVerifying all 20 images exist...")
    all_exist = True
    for i in range(1, 21):
        num = f"{i:02d}"
        path = f"{IMAGES_DIR}/news_{DATE}_{num}.png"
        exists = os.path.exists(path)
        status = "✓" if exists else "✗ MISSING"
        print(f"  {num}: {status}")
        if not exists:
            all_exist = False
    
    if all_exist:
        print("\n✓ All 20 images generated successfully!")
    else:
        print("\n✗ Some images still missing")


if __name__ == "__main__":
    main()