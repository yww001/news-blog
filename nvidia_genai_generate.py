#!/usr/bin/env python3
"""
NVIDIA SD3 图片生成脚本
Usage: python3 nvidia_genai_generate.py "prompt" --output /path/to/output.png [--model ...]
"""

import os
import sys
import argparse
import requests
import base64
import json
from pathlib import Path


def generate_image(prompt, output_path, model="stabilityai/stable-diffusion-3-medium",
                   ratio="16:9", steps=50, cfg=7.5, seed=None, api_key=None):
    """通过 NVIDIA API 生成图片"""
    
    api_key = api_key or os.environ.get("NVIDIA_API_KEY", "")
    if not api_key:
        print("❌ NVIDIA_API_KEY 未设置")
        return False
    
    # 解析比例 (16:9 -> width, height)
    w, h = map(int, ratio.split(":"))
    # 根据比例计算尺寸，保持合理大小
    base = 1024
    width = base
    height = int(base * h / w)
    if width > height:
        width, height = 1344, 768  # 16:9 标准分辨率
    
    # API 端点
    url = f"https://integrate.api.nvidia.com/v1/chat/completions"
    
    # 构建请求
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"""Generate an image with the following prompt. Return the image as base64 PNG.

Prompt: {prompt}

Requirements:
- Style: Photorealistic news photography, National Geographic / Reuters style
- Quality: 8K resolution, professional journalism
- Aspect ratio: {ratio}
- The image must be a real photograph, no cartoons, no illustrations
- Vibrant colors, natural lighting, cinematic composition
- Return ONLY the base64-encoded PNG image, no text, no markdown"""
            }
        ],
        "max_tokens": 1024,
        "stream": False
    }
    
    if seed:
        payload["seed"] = seed
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"🎨 Generating image...")
    print(f"   Model: {model}")
    print(f"   Size: {width}x{height}")
    print(f"   Steps: {steps}, CFG: {cfg}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=300)
        
        if response.status_code != 200:
            print(f"❌ API 错误: {response.status_code} - {response.text[:200]}")
            return False
        
        result = response.json()
        
        # 从 response 中提取 base64 图片
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # 清理 markdown 格式
        if "```" in content:
            for line in content.split("\n"):
                if line.startswith("data:image") or (line.strip().startswith("iVBOR") and len(line) > 100):
                    content = line.strip()
                    break
            else:
                # 提取 base64 部分
                import re
                match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)', content)
                if match:
                    content = match.group(1)
                else:
                    match = re.search(r'([A-Za-z0-9+/]{100,})', content.replace("\n", ""))
                    if match:
                        content = match.group(1)
        
        if not content or len(content) < 1000:
            print(f"❌ 未找到有效的图片数据")
            print(f"   Response: {content[:200] if content else 'empty'}")
            return False
        
        # 解码并保存
        image_data = base64.b64decode(content)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(image_data)
        
        size_kb = len(image_data) / 1024
        print(f"✅ 图片已保存: {output_path} ({size_kb:.0f} KB)")
        return True
        
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时")
        return False
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="NVIDIA SD3 图片生成")
    parser.add_argument("prompt", help="图片描述提示词")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    parser.add_argument("--model", default="stabilityai/stable-diffusion-3-medium", help="模型名称")
    parser.add_argument("--ratio", default="16:9", help="宽高比")
    parser.add_argument("--steps", type=int, default=50, help="推理步数")
    parser.add_argument("--cfg", type=float, default=7.5, help="CFG 引导强度")
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument("--api-key", help="NVIDIA API Key (覆盖环境变量)")
    
    args = parser.parse_args()
    
    success = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        model=args.model,
        ratio=args.ratio,
        steps=args.steps,
        cfg=args.cfg,
        seed=args.seed,
        api_key=args.api_key
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
