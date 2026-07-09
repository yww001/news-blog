#!/usr/bin/env python3
import base64
import json
import os
import time
import urllib.request
import urllib.error

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
DATE_STR = "20260710"
IMAGES_DIR = "/home/swg/.openclaw/workspace/news-blog/images"

failed = [
    ("03", "Chinese yuan digital coins, gold currency symbol, financial market trading, photorealistic, ultra detailed, 8K, no text or watermarks"),
    ("16", "Diplomatic meeting at White House, US and Japan flags, formal handshake, two leaders conversation, photorealistic, ultra detailed, 8K, no text or watermarks"),
]

for num, prompt in failed:
    filename = f"news_{DATE_STR}_{num}.png"
    filepath = f"{IMAGES_DIR}/{filename}"
    
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
                content = data['choices'][0]['message']['content']
                if isinstance(content, list):
                    url = content[0]['url']
                else:
                    url = content
                
                img_req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                    img_data = img_resp.read()
                    with open(filepath, 'wb') as f:
                        f.write(img_data)
                print(f"[{num}] Success!")
                break
        except Exception as e:
            print(f"[{num}] Error (attempt {attempt+1}): {e}")
            time.sleep(3)
    time.sleep(1)

print("Done!")