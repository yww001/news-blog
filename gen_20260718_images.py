#!/usr/bin/env python3
"""Generate news images for 2026年07月18日 using CogView-3-Flash API"""

import base64
import json
import os
import time
import urllib.request
import urllib.error

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
IMAGE_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
DATE_STR = "20260718"

news_data = [
    {
        "id": "01",
        "title": "2026世界人工智能大会在上海闭幕 发布《上海AI宣言》",
        "prompt": "Scientists and government officials attending the World AI Conference in Shanghai, grand exhibition hall with robotic displays, confetti and celebration, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "02",
        "title": "中国上半年外贸进出口总值超28万亿元 创历史同期新高",
        "prompt": "Busy container port with colorful shipping containers, massive cargo ships, cranes loading and unloading, aerial view of modern logistics hub, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "03",
        "title": "中美重启经贸磋商 双方在北京举行高层会谈",
        "prompt": "Formal diplomatic meeting room with Chinese and American flags facing each other, distinguished delegates shaking hands, elegant interior design, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "04",
        "title": "华为发布Mate 70系列 搭载鸿蒙5.0操作系统",
        "prompt": "Sleek modern smartphone on a reflective surface, holographic display effects, elegant product photography studio lighting, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "05",
        "title": "A股三大指数集体上涨 沪指重回3400点",
        "prompt": "Stock market trading floor with large digital displays showing rising charts, people analyzing data, modern financial district background, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "06",
        "title": "欧盟通过对华电动车加征关税决定 中国商务部回应",
        "prompt": "Electric vehicles charging at a modern station, Chinese and European flags in background, sustainable energy concept, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "07",
        "title": "2026年世界杯第三名争夺战打响 摩洛哥对阵克罗地亚",
        "prompt": "Exciting football stadium filled with passionate fans, players in action on the pitch, colorful national flags and banners, dramatic lighting, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "08",
        "title": "中国成功发射全球首颗6G试验卫星",
        "prompt": "Rocket launching into clear blue sky, satellite deployed in orbit above Earth, modern space launch facility, dramatic smoke trail, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "09",
        "title": "第47届世界遗产大会开幕 中国新增3处世界遗产",
        "prompt": "Magnificent UNESCO World Heritage site, ancient Chinese architecture with mountains and clouds, tourists admiring the view, golden hour lighting, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "10",
        "title": "美联储宣布维持利率不变 鲍威尔称9月可能降息",
        "prompt": "Federal Reserve building in Washington DC, authoritative exterior, American flag waving, financial district skyline, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "11",
        "title": "俄罗斯与乌克兰举行第三轮和平谈判",
        "prompt": "Diplomatic conference room with peace negotiations, Russian and Ukrainian delegations at separate tables, mediators present, neutral location, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "12",
        "title": "苹果发布iOS 20系统 引入AI全面升级Siri",
        "prompt": "Modern Apple Store interior with glowing logo, person using iPhone with colorful interface, minimalist elegant design, soft ambient lighting, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "13",
        "title": "南方多省高温持续 最高气温突破40度",
        "prompt": "Scorching summer heat wave, thermometer showing 40 degrees, wilting flowers and dry ground, sun glare, urban street scene in extreme heat, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "14",
        "title": "比特币价格突破10万美元 再创历史新高",
        "prompt": "Golden Bitcoin coin on reflective surface, digital artwork of cryptocurrency symbols, dramatic lighting with gold and green tones, futuristic concept, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "15",
        "title": "日本首相访华 双方签署多项合作协议",
        "prompt": "Japanese and Chinese flags side by side, diplomatic ceremony with officials signing agreements, formal setting with national emblems, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "16",
        "title": "谷歌发布Gemini 2.0 称其为最强大模型",
        "prompt": "Futuristic AI technology concept, glowing neural network visualization, powerful computer hardware in server room, blue and purple lighting, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "17",
        "title": "中国队获得2026年IMO国际数学奥林匹克团体第一",
        "prompt": "Young students celebrating winning gold medals at international mathematics Olympiad, proud faces holding trophies, academic ceremony, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "18",
        "title": "故宫博物院北院区正式对外开放",
        "prompt": "Magnificent Forbidden City palace complex, stunning traditional Chinese architecture with intricate golden details, visitors walking through grand gates, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "19",
        "title": "土耳其正式成为金砖国家成员",
        "prompt": "BRICS summit meeting with diverse world leaders, international diplomatic conference, flags of member nations displayed, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "id": "20",
        "title": "台风格美来袭 东南沿海启动应急响应",
        "prompt": "Powerful typhoon approaching coastline, dramatic storm clouds and heavy rain over the sea, coastal city with emergency response vehicles, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    }
]

def generate_image(news_id, prompt, retry=2):
    filename = f"{IMAGE_DIR}/news_{DATE_STR}_{news_id}.png"
    if os.path.exists(filename):
        print(f"  [SKIP] {news_id} already exists")
        return True
    
    for attempt in range(retry + 1):
        try:
            payload = {
                "model": "cogview-3-flash",
                "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                API_URL,
                data=data,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            
            content = result["choices"][0]["message"]["content"]
            if content.startswith("data:image/png;base64,"):
                b64_data = content.split(",", 1)[1]
                img_data = base64.b64decode(b64_data)
                with open(filename, "wb") as f:
                    f.write(img_data)
                print(f"  [OK] {news_id}: {filename}")
                return True
            else:
                print(f"  [ERR] {news_id}: unexpected response format")
                print(f"       {content[:100]}")
        except Exception as e:
            print(f"  [ERR] {news_id} attempt {attempt+1}: {e}")
            if attempt < retry:
                time.sleep(3)
    
    return False

if __name__ == "__main__":
    os.makedirs(IMAGE_DIR, exist_ok=True)
    success = 0
    for item in news_data:
        print(f"Generating image {item['id']}...")
        if generate_image(item["id"], item["prompt"]):
            success += 1
        time.sleep(1)
    
    print(f"\n=== Done: {success}/{len(news_data)} images generated ===")