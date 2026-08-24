#!/usr/bin/env python3
"""Generate 20 news images via Pollinations (flux model), 768x768, save as JPEG.
For each image: download from Pollinations, convert to JPEG, verify size > 10KB,
retry with seed variation if too small.
"""
import os, sys, json, time, urllib.parse, urllib.request, io
from pathlib import Path
from PIL import Image

BLOG = Path("/home/swg/.openclaw/workspace/news-blog")
IMG_DIR = BLOG / "images"
IMG_DIR.mkdir(exist_ok=True)

with open(BLOG / "news_data_20260818.json") as f:
    data = json.load(f)

news_list = data["news"]
DATE = "20260818"

# Per-news prompts (concise English scenes; matches each card's visual subject)
PROMPTS = {
    "01": "Chile foreign minister arriving in Beijing, handshake with Chinese official at capital airport, flags of Chile and China, photorealistic, ultra detailed",
    "02": "Abstract AI server racks with glowing circuit boards, data center, peak pricing graph, photorealistic, ultra detailed",
    "03": "Long March 2C rocket launching from Taiyuan Satellite Launch Center, dramatic fire and smoke, blue sky, photorealistic, ultra detailed",
    "04": "Aerial view of Strait of Hormuz oil tankers at sunset, Persian Gulf, photorealistic, ultra detailed",
    "05": "Unitree humanoid robot on stock exchange trading floor with Chinese investors, LED screens showing IPO numbers, photorealistic, ultra detailed",
    "06": "Alibaba company logo, corporate boardroom, sale handshake, business people, photorealistic, ultra detailed",
    "07": "US Capitol building with AI safety protest, futuristic AI agents on screens, photorealistic, ultra detailed",
    "08": "OpenAI logo projected on office wall, modern tech startup vibe, glowing AI brain, photorealistic, ultra detailed",
    "09": "Industrial Fulconn Foxconn AI server factory, rows of Nvidia GPU racks, photorealistic, ultra detailed",
    "10": "Devastating flood in Chiba Japan, helicopter rescue over submerged houses, rainy atmosphere, photorealistic, ultra detailed",
    "11": "Nvidia CEO Jensen Huang on stage with Wall Street logos behind, AI Compute Alliance, photorealistic, ultra detailed",
    "12": "Aftermath of 7.7 earthquake in Flores Indonesia, damaged village, rescue workers, photorealistic, ultra detailed",
    "13": "SpaceX Starship rocket landing on launch tower, chopsticks catching booster, dramatic lighting, photorealistic, ultra detailed",
    "14": "Northeast China flood aftermath, heavy machinery rebuilding dikes, farmers in rice fields, photorealistic, ultra detailed",
    "15": "China-Kyrgyzstan-Uzbekistan railway construction in mountain valley, workers laying tracks, photorealistic, ultra detailed",
    "16": "Olympic anti-doping lab scientists analyzing samples, Paris 2024 logo, photorealistic, ultra detailed",
    "17": "Black Myth Zhong Kui game character, mystical Chinese underworld, dramatic lighting, photorealistic, ultra detailed",
    "18": "Cancer patient receiving CAR-T cell therapy in hospital, hopeful atmosphere, photorealistic, ultra detailed",
    "19": "South Korea and Japan leaders shaking hands in Tokyo, flags, diplomatic setting, photorealistic, ultra detailed",
    "20": "Global wheat corn rice grain silos with rising price charts, world map background, photorealistic, ultra detailed",
}

def gen_one(num, prompt, max_retries=3):
    out = IMG_DIR / f"news_{DATE}_{num}.png"
    base_prompt = f"{prompt}, 8K, high resolution, cinematic lighting, no text, no watermark"
    for attempt in range(max_retries):
        seed = 20260818 + int(num) * 7 + attempt * 1000
        encoded = urllib.parse.quote(base_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=768&model=flux&nologo=true&seed={seed}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                content = resp.read()
            if len(content) < 5000:
                print(f"  [{num}] attempt {attempt+1}: too small ({len(content)}B), retrying...")
                time.sleep(2)
                continue
            img = Image.open(io.BytesIO(content)).convert("RGB")
            img.save(out, "JPEG", quality=85)
            size = out.stat().st_size
            if size < 10000:
                print(f"  [{num}] attempt {attempt+1}: post-save too small ({size}B), retrying...")
                time.sleep(2)
                continue
            print(f"  [{num}] ✅ {size//1024} KB")
            return True
        except Exception as e:
            print(f"  [{num}] attempt {attempt+1}: {e}")
            time.sleep(3)
    return False

failed = []
for n in news_list:
    num = n["news-number"]
    prompt = PROMPTS.get(num, n["news-title"])
    print(f"Generating image {num}: {n['news-title'][:40]}")
    if not gen_one(num, prompt):
        failed.append(num)

print(f"\n=== Done. Failed: {failed if failed else 'none'} ===")
sys.exit(1 if failed else 0)
