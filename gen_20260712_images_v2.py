import json
import base64
import os
import requests
from pathlib import Path
import time

date_slug = "20260712"
images_dir = Path("/home/swg/.openclaw/workspace/news-blog/images")
images_dir.mkdir(exist_ok=True)

news_items = [
    {"number": "01", "prompt": "United Nations aid convoy trucks entering humanitarian corridor, desert road, Gaza strip background, medical tents, relief workers, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "02", "prompt": "Chinese rocket launch at dusk, Wenchang space launch center, Long March rocket ascending, smoke trail, modern space technology, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "03", "prompt": "Bitcoin cryptocurrency concept, golden Bitcoin coin with glowing symbol, digital trading charts background, financial technology, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "04", "prompt": "French National Assembly building, Paris skyline, French tricolor flags, political rally, democratic election atmosphere, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "05", "prompt": "SpaceX Starship landing on drone ship at sunset, rocket booster being caught by robotic arms, ocean waves, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "06", "prompt": "Modern cargo port with container ships, Chinese flag, cranes loading containers, busy trade scene, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "07", "prompt": "Typhoon hitting coastal Chinese city, heavy rain and wind, flooded streets, emergency responders, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "08", "prompt": "NATO summit meeting in Ankara, world leaders at conference table, military flags, diplomatic atmosphere, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "09", "prompt": "NVIDIA GPU chip close-up with blue LED lighting, futuristic technology, data center servers, AI computing concept, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "10", "prompt": "Naval ships from multiple countries in formation, South China Sea backdrop, military vessels, international navy exercise, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "11", "prompt": "Oil barrel and energy industry concept, gasoline station with rising price display, global energy crisis, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "12", "prompt": "Artificial intelligence brain visualization, glowing neural network, university research laboratory, scientific researchers, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "13", "prompt": "Iranian president taking oath of office, parliament building in Tehran, Iranian flag, diplomatic ceremony, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "14", "prompt": "Chinese yuan currency with red background, financial district buildings, money exchange rate concept, banking technology, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "15", "prompt": "Japanese city with traditional buildings, emergency vehicles, earthquake aftermath, people evacuating calmly, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "16", "prompt": "BRICS summit meeting, Beijing venue, world leaders from multiple countries, Chinese and international flags, international cooperation, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "17", "prompt": "Apple iPhone with glowing screen, iOS interface, futuristic smartphone technology, AI assistant concept, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "18", "prompt": "World Cup football match in Mexico stadium, goalkeeper making dramatic save, night game atmosphere, fans cheering, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "19", "prompt": "Coral reef bleaching underwater scene, colorful corals turning white, tropical fish, ocean warming concept, environmental crisis, photorealistic, ultra detailed, 8K, no text or watermarks"},
    {"number": "20", "prompt": "Tesla electric cars on assembly line in modern factory, Shanghai industrial setting, robotic arms building vehicles, electric vehicle manufacturing, photorealistic, ultra detailed, 8K, no text or watermarks"}
]

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

for item in news_items:
    num = item["number"]
    prompt = item["prompt"]
    filename = f"news_{date_slug}_{num}.png"
    filepath = images_dir / filename
    
    if filepath.exists():
        print(f"[{num}] Already exists, skipping")
        continue
    
    print(f"[{num}] Generating...")
    
    data = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    for attempt in range(2):
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=30)
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                if isinstance(content, list) and len(content) > 0:
                    img_url = content[0].get("url", "")
                    if img_url:
                        img_response = requests.get(img_url, timeout=30)
                        if img_response.status_code == 200:
                            with open(filepath, "wb") as f:
                                f.write(img_response.content)
                            print(f"[{num}] SUCCESS: {filename} ({len(img_response.content)} bytes)")
                            break
                        else:
                            print(f"[{num}] Download failed: {img_response.status_code}, retrying...")
                else:
                    print(f"[{num}] Unexpected format, retrying...")
            else:
                print(f"[{num}] API error: {str(result)[:100]}, retrying...")
        except Exception as e:
            print(f"[{num}] Error: {e}, retrying...")
        
        time.sleep(2)
    else:
        print(f"[{num}] FAILED after 2 attempts")
    
    time.sleep(1)

print("\n=== Checking generated images ===")
for i in range(1, 21):
    num = str(i).zfill(2)
    filepath = images_dir / f"news_{date_slug}_{num}.png"
    if filepath.exists():
        size = filepath.stat().st_size
        print(f"  {num}: ✓ ({size} bytes)")
    else:
        print(f"  {num}: ✗ missing")