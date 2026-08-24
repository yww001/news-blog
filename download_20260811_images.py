#!/usr/bin/env python3
"""Download all 20 images from URLs collected via image_generate tool."""
import json
import urllib.request
import os
from pathlib import Path

BLOG = Path("/home/swg/.openclaw/workspace/news-blog")
IMG_DIR = BLOG / "images"
DATE = "20260811"

# URLs collected from image_generate tool calls
URLS = {
    "01": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811020700aa1b5b3fbb4342d0_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=IkssBIAXT0YLfeEFznJNFfr2Nxc%3D&Expires=1786990028",
    "02": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811020709e473d765ff2f402e_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=e%2BLGhLUGqwPEt6HiwxsHcBrn7ec%3D&Expires=1786990040",
    "03": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811020721ec9c8b98d5b14b6e_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=1%2Bdqp9ZAiok%2FOdhVbEP3nnflxUA%3D&Expires=1786990053",
    "04": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811020735c4a7734d52e4429c_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=WRl8bXtyOiwIxZzOhRbMElRb3JQ%3D&Expires=1786990063",
    "05": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811020757062a85c4fa484c48_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=NG4r%2BmOd7TW0Bv3YVSHEr49g2Y8%3D&Expires=1786990088",
    "06": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811020809b435164f975e49ab_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=TZgD6mm9r4syfaZMiagGLhFQ24w%3D&Expires=1786990097",
    "07": "/home/swg/.hermes/cache/images/pollinations_20260811_020829_25f6e9b2.png",
    "08": "/home/swg/.hermes/cache/images/pollinations_20260811_020914_b7b0ee1f.png",
    "09": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811020928ef8018f30b254f34_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=GrDU8stCcEj%2FRaJU1WJNlYfwfG4%3D&Expires=1786990180",
    "10": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811020941b12853e0087d4775_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=qOOBfgEoXGhIsQRZwngH9OMr0Ps%3D&Expires=1786990189",
    "11": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811021007b28104be3d744773_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=CqSLaD9alIrZaXa24B3fAGdhNVs%3D&Expires=1786990217",
    "12": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/202608110210183508a68da0aa4db3_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=QfRFogzaCeJ6HY%2FhJ5xz%2FVHZGJI%3D&Expires=1786990226",
    "13": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811021031d67748beb84c4567_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=63VL9jG1U7gwa8vCODqcaH2UCVI%3D&Expires=1786990239",
    "14": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/2026081102104097826422541a464a_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=jFoitLlEb9XC6MC8I49sldmvQ%2Fg%3D&Expires=1786990251",
    "15": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/2026081102105391a0df75bdb842e0_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=75E32PYwvSxG4GVu5FOWCzdn9rQ%3D&Expires=1786990261",
    "16": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811021102966f5f9079974f44_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=2SAhtu807HMjqfsKpi4Vc9vQWig%3D&Expires=1786990272",
    "17": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/20260811021117cab45f4cfdb944d3_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=qZS2ts3IgS0y07nRXbOlauccxbQ%3D&Expires=1786990285",
    "18": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/202608110211265dd2ef60a3e44720_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=G78Nkgu8M4nJrNNxaOUb6HlbjtM%3D&Expires=1786990294",
    "19": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/202608110211356df6afa76a394fc5_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=OpnNCSP2TF%2BcPFK7je8GtrhIpOw%3D&Expires=1786990304",
    "20": "https://maas-watermark-prod-new.cn-wlcb.ufileos.com/2026081102114521d685b0edcd46d7_watermark.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=VZ4oYq6dT3rWe1igBqvwx8AVrp8%3D&Expires=1786990313",
}

results = {}
for num, src in URLS.items():
    dst = IMG_DIR / f"news_{DATE}_{num}.png"
    try:
        if src.startswith("http"):
            req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            with open(dst, 'wb') as f:
                f.write(data)
        else:
            # Local file path (pollinations fallback)
            import shutil
            shutil.copy(src, dst)
        size = dst.stat().st_size
        results[num] = size
        status = "OK" if size > 10000 else "TOO SMALL"
        print(f"  [{num}] {size:>8} bytes - {status}")
    except Exception as e:
        results[num] = 0
        print(f"  [{num}] FAILED: {e}")

# Summary
total = sum(1 for s in results.values() if s > 10000)
print(f"\nDownloaded: {total}/20 images (>10KB)")
if total < 20:
    print("FAILED:", [n for n, s in results.items() if s <= 10000])
