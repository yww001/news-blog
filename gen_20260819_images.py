#!/usr/bin/env python3
"""Generate 20 news images via Pollinations (flux model), 1024x768, save as PNG.
For each image: download from Pollinations, convert to PNG, verify size > 10KB,
retry with seed variation if too small.
"""
import os, sys, json, time, urllib.parse, urllib.request, io
from pathlib import Path
from PIL import Image

BLOG = Path("/home/swg/.openclaw/workspace/news-blog")
IMG_DIR = BLOG / "images"
IMG_DIR.mkdir(exist_ok=True)

with open(BLOG / "news_data_20260819.json") as f:
    data = json.load(f)

news_list = data["news"]
DATE = "20260819"

# Per-news prompts (concise English scenes; matches each card's visual subject)
PROMPTS = {
    "01": "China Ecuador summit meeting, leaders shaking hands in Great Hall of the People Beijing, flags of both nations, photorealistic, ultra detailed",
    "02": "OpenAI GPT-6 logo on smartphone screen showing chat interface in Chinese, modern WeChat environment, photorealistic, ultra detailed",
    "03": "Electric flying taxi eVTOL aircraft flying over Shenzhen Bay skyscrapers, urban skyline, photorealistic, ultra detailed",
    "04": "Aerial view of Strait of Hormuz with oil tankers, US Navy destroyer escort, dramatic sunset over Persian Gulf, photorealistic, ultra detailed",
    "05": "Bullish stock exchange floor with screens showing green numbers, Chinese investors celebrating, modern trading hall, photorealistic, ultra detailed",
    "06": "WeChat smartphone showing AI video editing interface, person creating short video content on phone, photorealistic, ultra detailed",
    "07": "BYD electric cars lineup on Tokyo dealership showroom, Japanese city street outside, modern showroom, photorealistic, ultra detailed",
    "08": "Global grain silos with wheat corn rice harvest, falling price charts, world map background, photorealistic, ultra detailed",
    "09": "Huawei HarmonyOS desktop PC computer on office desk, modern workspace, user working with Chinese interface, photorealistic, ultra detailed",
    "10": "Rescue workers in Flores Indonesia earthquake aftermath, collapsed buildings, helicopters delivering aid, photorealistic, ultra detailed",
    "11": "Chinese State Council meeting room, officials discussing economic policy, large screens showing data, photorealistic, ultra detailed",
    "12": "Starlink satellite network orbiting earth at night, multiple satellites with glowing communication beams, photorealistic, ultra detailed",
    "13": "Northeast China reconstruction site, workers rebuilding dikes and infrastructure, post-flood recovery, photorealistic, ultra detailed",
    "14": "Unitree H2 humanoid robot running on track, dynamic motion, futuristic design, photorealistic, ultra detailed",
    "15": "Olympic anti-doping laboratory, scientists analyzing samples with microscopes, Paris 2024 logo on wall, photorealistic, ultra detailed",
    "16": "China-Kyrgyzstan-Uzbekistan railway construction, workers laying tracks through mountain valley, dramatic landscape, photorealistic, ultra detailed",
    "17": "Cancer patient receiving CAR-T cell therapy, hospital infusion room, hopeful atmosphere, doctor beside, photorealistic, ultra detailed",
    "18": "Black Myth Zhong Kui game character in mystical Chinese underworld, dramatic lighting, video game art style cinematic, photorealistic, ultra detailed",
    "19": "South Korea Japan leaders shaking hands in Tokyo diplomatic meeting, flags of both nations, formal setting, photorealistic, ultra detailed",
    "20": "Nvidia H300 GPU chip close-up, glowing circuit board, futuristic tech showcase, photorealistic, ultra detailed",
}

def gen_one(num, prompt, max_retries=3):
    out = IMG_DIR / f"news_{DATE}_{num}.png"
    base_prompt = f"{prompt}, 8K, high resolution, cinematic lighting, no text, no watermark"
    for attempt in range(max_retries):
        seed = 20260819 + int(num) * 7 + attempt * 1000
        encoded = urllib.parse.quote(base_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=768&model=flux&nologo=true&seed={seed}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                content = resp.read()
            if len(content) < 5000:
                print(f"  [{num}] attempt {attempt+1}: too small ({len(content)}B), retrying...")
                time.sleep(2)
                continue
            img = Image.open(io.BytesIO(content)).convert("RGB")
            img.save(out, "PNG", optimize=True)
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

print(f"\nDone. Failed: {failed}")
