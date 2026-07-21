#!/usr/bin/env python3
import json
import os
import base64
import urllib.request
import urllib.error

# CogView API settings
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

# Load news data
with open('/home/swg/.openclaw/workspace/news-blog/news_data_20260722.json', 'r', encoding='utf-8') as f:
    news_data = json.load(f)

def generate_image(prompt, output_path):
    """Generate image using CogView API"""
    content = f"Image prompt: {prompt}"
    
    payload = json.dumps({
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": content}]
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    req = urllib.request.Request(
        API_URL,
        data=payload.encode('utf-8'),
        headers=headers
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            msg_content = result['choices'][0]['message']['content']
            
            # Handle list format: [{"url": "..."}]
            if isinstance(msg_content, list) and len(msg_content) > 0:
                image_url = msg_content[0].get('url')
                if image_url:
                    # Download image from URL
                    img_req = urllib.request.Request(image_url)
                    with urllib.request.urlopen(img_req, timeout=60) as img_response:
                        image_data = img_response.read()
                        with open(output_path, 'wb') as f:
                            f.write(image_data)
                    return True
            elif isinstance(msg_content, str) and msg_content.startswith('data:image'):
                # Handle base64 format
                base64_data = msg_content.split('data:image/png;base64,')[1]
                image_data = base64.b64decode(base64_data)
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                return True
            else:
                print(f"Unknown format: {type(msg_content)}")
                return False
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode()[:200]}")
        return False
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        return False

# Generate images for all 20 news items
success_count = 0
fail_count = 0
failed_items = []

for news in news_data:
    num = news['number']
    prompt = news['image_prompt']
    output_path = f'/home/swg/.openclaw/workspace/news-blog/images/news_20260722_{num}.png'
    
    print(f"Generating image {num}: {news['title'][:30]}...")
    
    # Retry once on failure
    for attempt in range(2):
        if generate_image(prompt, output_path):
            print(f"  Success: {output_path}")
            success_count += 1
            break
        else:
            if attempt == 0:
                print(f"  Retry...")
            else:
                print(f"  Failed!")
                fail_count += 1
                failed_items.append(num)

print(f"\n=== Summary ===")
print(f"Success: {success_count}")
print(f"Failed: {fail_count}")
if failed_items:
    print(f"Failed items: {failed_items}")