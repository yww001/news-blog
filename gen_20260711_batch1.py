#!/usr/bin/env python3
import urllib.request, json, base64, time
API_KEY = '88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB'
API_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
DATE_STR = '20260711'

prompts = {
    '01': 'Chinese navy submarine launching missile in ocean, dramatic waves, military vessel, smoke rising, photorealistic, ultra detailed, 8K',
    '02': 'US Navy destroyer and Japanese anti-submarine aircraft conducting joint naval exercise in Pacific Ocean, photorealistic, ultra detailed, 8K',
    '03': 'Modern automobile factory assembly line with hundreds of new cars, robotic arms, Chinese manufacturing plant, photorealistic, ultra detailed, 8K',
    '04': 'Chinese and African leaders shaking hands at official ceremony in front of flags, grand government building, photorealistic, ultra detailed, 8K',
    '05': 'Futuristic AI data center with glowing blue server racks, artificial intelligence visualization, photorealistic, ultra detailed, 8K',
    '06': 'Dutch trade minister meeting Chinese officials in modern conference room, diplomatic meeting, photorealistic, ultra detailed, 8K',
    '07': 'Scientists in modern research laboratory studying protein structures on holographic display, DNA helix, photorealistic, ultra detailed, 8K',
    '08': 'Stock market trading floor with glowing digital displays showing rising stock charts, traders, photorealistic, ultra detailed, 8K',
    '09': 'British Parliament building in London, Big Ben, red double-decker buses, Westminster Bridge, photorealistic, ultra detailed, 8K',
    '10': 'European Parliament building in Brussels with EU flags, AI brain hologram overlay, photorealistic, ultra detailed, 8K',
}

for num, prompt in prompts.items():
    payload = json.dumps({'model': 'cogview-3-flash', 'messages': [{'role': 'user', 'content': f'Image prompt: {prompt}'}]}).encode('utf-8')
    req = urllib.request.Request(API_URL, data=payload, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            result = json.loads(resp.read().decode())
            content = result['choices'][0]['message']['content']
            url = content[0]['url']
            with urllib.request.urlopen(url, timeout=30) as img_resp:
                img_data = img_resp.read()
                path = f'images/news_{DATE_STR}_{num}.png'
                open(path, 'wb').write(img_data)
                print(f'OK {num} ({len(img_data)} bytes)')
    except Exception as e:
        print(f'FAIL {num}: {e}')
    time.sleep(1.5)

print('Batch 1/2 done')