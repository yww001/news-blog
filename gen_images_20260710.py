#!/usr/bin/env python3
import base64
import json
import os
import time
import urllib.request
import urllib.error
from pathlib import Path

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
DATE_STR = "20260710"
IMAGES_DIR = Path("/home/swg/.openclaw/workspace/news-blog/images")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS = [
    "Futuristic AI brain concept, glowing neural network, blue digital light, humanoid robot silhouette, photorealistic, ultra detailed, 8K, no text or watermarks",
    "World leaders at G20 summit conference hall, international flags, diplomatic meeting atmosphere, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Chinese yuan digital currency concept, golden coins with yuan symbol, global financial network, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Apple store with folding iPhone display, customers examining new device, modern retail lighting, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Chinese lunar spacecraft launching from tropical coast, rocket exhaust flames, blue sky, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Chinese central bank building, financial district, people walking past, modern architecture, photorealistic, ultra detailed, 8K, no text or watermarks",
    "British Parliament building, London sky, political demonstration, crowds, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Tesla autonomous taxi concept, sleek futuristic vehicle, no driver, city street background, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Chinese aircraft carrier at sea, jet fighters on deck, naval fleet formation, blue ocean waves, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Container port with cargo ships, cranes loading containers, international trade, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Huawei laptop computer on modern desk, Chinese technology, office environment, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Power transmission towers at sunset, heat wave, high voltage electricity, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Underwater pipeline investigation, deep sea evidence gathering, European flags background, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Warren Buffett portrait concept, Berkshire Hathaway headquarters, stock market charts, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Archaeological site excavation, ancient bronze artifacts, Chinese excavation site, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Japanese Prime Minister meeting US President in White House, bilateral talks, flags of both nations, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Chinese women's volleyball team celebrating victory, trophy, players jumping with joy, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Brain computer interface concept, neural signals visualization, medical technology, photorealistic, ultra detailed, 8K, no text or watermarks",
    "Coral reef bleaching underwater, colorful coral turning white, marine life, ocean blue, photorealistic, ultra detailed, 8K, no text or watermarks",
    "SpaceX Starship launching at night, rocket exhaust flames illuminating sky, ocean launch pad, photorealistic, ultra detailed, 8K, no text or watermarks"
]

def generate_image(prompt, num):
    filename = f"news_{DATE_STR}_{num:02d}.png"
    filepath = IMAGES_DIR / filename
    
    if filepath.exists():
        print(f"[{num:02d}] Already exists, skipping")
        return True
    
    payload = json.dumps({
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    })
    
    req = urllib.request.Request(
        API_URL,
        data=payload.encode('utf-8'),
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                # Extract URL from response
                content = data['choices'][0]['message']['content']
                if isinstance(content, list):
                    url = content[0]['url']
                else:
                    url = content
                
                # Download image
                img_req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                    img_data = img_resp.read()
                    with open(filepath, 'wb') as f:
                        f.write(img_data)
                print(f"[{num:02d}] Success: {filename}")
                return True
        except Exception as e:
            print(f"[{num:02d}] Error (attempt {attempt+1}): {e}")
            time.sleep(3)
    
    return False

# Generate all images
success_count = 0
for i, prompt in enumerate(PROMPTS, 1):
    if generate_image(prompt, i):
        success_count += 1
    time.sleep(1.5)

print(f"\nGenerated {success_count}/{len(PROMPTS)} images")