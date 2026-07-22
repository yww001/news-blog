#!/usr/bin/env python3
from urllib.parse import quote
import subprocess
import time

prompts = {
    "09": "Scientist in laboratory with glowing superconducting material, levitating magnet, cryogenic equipment, photorealistic, ultra detailed, 8K",
    "10": "Palace Museum entrance with digital holographic artifacts floating, traditional Chinese architecture meets futuristic technology, photorealistic, ultra detailed, 8K",
    "11": "Three world leaders shaking hands at international summit meeting, flags of three countries in background, photorealistic, ultra detailed, 8K",
    "12": "High-performance GPU chip with colorful lighting effects, data center background with cooling systems, photorealistic, ultra detailed, 8K",
    "13": "Huge cruise ship sailing in calm ocean waters, hydrogen fuel cells visible, eco-friendly green energy concept, photorealistic, ultra detailed, 8K",
    "14": "Bitcoin coin with glowing golden symbols, cryptocurrency trading chart rising, digital future concept, photorealistic, ultra detailed, 8K",
    "15": "Modern electric vehicle assembly line with robots, Chinese EV brands, clean factory environment, photorealistic, ultra detailed, 8K",
    "16": "Latest iPhone model on display in Apple Store, sleek design with glowing screen, photorealistic, ultra detailed, 8K, high resolution",
    "17": "Tennis player serving at China Open, packed stadium with Chinese flags, photorealistic, ultra detailed, 8K, high resolution",
    "18": "Bustling Shanghai shopping district at night with neon lights, luxury stores, crowds of shoppers, photorealistic, ultra detailed, 8K",
    "19": "Epic Chinese historical film set with elaborate costumes and sets, dramatic scene with actors in ancient costumes, photorealistic, ultra detailed, 8K",
    "20": "Offshore wind farm in ocean with dozens of wind turbines, dramatic sunset, green energy concept, photorealistic, ultra detailed, 8K"
}

for num, prompt in prompts.items():
    url = f"https://image.pollinations.ai/prompt/{quote(prompt, safe='')}?width=1024&height=1024&nologo=true"
    output = f"/home/swg/.openclaw/workspace/news-blog/images/news_20260723_{num}.png"
    print(f"Generating {num}...", end=" ", flush=True)
    result = subprocess.run(f'curl -s -L "{url}" -o "{output}"', shell=True, timeout=120)
    time.sleep(3)
    print("Done!")

print("\nAll images regenerated!")