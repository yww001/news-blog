#!/usr/bin/env python3
import urllib.request, json, base64, time, sys

API_KEY = '88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB'
API_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
DATE_STR = '20260711'

retry_items = {
    '04': 'Chinese president and African president shaking hands at grand ceremony with red carpet and national flags, Palace of the People Beijing, photorealistic, ultra detailed, 8K',
    '06': 'Dutch trade minister meeting Chinese delegation in elegant conference room, international business diplomacy, flags of both nations, photorealistic, ultra detailed, 8K',
    '11': 'Southern European city street in extreme heat wave, thermometer showing very high temperature above 45 degrees, dry cracked earth, people trying to cool down, photorealistic, ultra detailed, 8K',
    '12': 'Typhoon hitting coastal Chinese city, massive waves crashing against seawall, heavy rain, emergency vehicles, palm trees swaying violently, photorealistic, ultra detailed, 8K',
    '13': 'World Cup football stadium full of cheering fans waving flags at night, colorful floodlights illuminating the pitch, aerial panoramic view, photorealistic, ultra detailed, 8K',
    '14': 'Archaeologists carefully uncovering ancient golden bronze masks and sacred artifacts at Chinese archaeological dig site, photorealistic, ultra detailed, 8K',
    '15': 'Bitcoin logo on digital display with downward trending chart, cryptocurrency trading interface, dark trading room with multiple screens, photorealistic, ultra detailed, 8K',
    '16': 'Premium foldable smartphone with brilliant display showing colorful interface, sleek modern design, studio lighting, photorealistic, ultra detailed, 8K',
    '17': 'Peace talks diplomatic meeting, Russian and Ukrainian flags facing each other across conference table, international diplomats in discussion, photorealistic, ultra detailed, 8K',
    '18': 'Elderly Chinese people practicing tai chi in morning park, modern cityscape skyline background, healthy active seniors, photorealistic, ultra detailed, 8K',
    '19': 'SpaceX rocket launching at night from Cape Canaveral, brilliant fire trail against starry sky, smoke billowing, photorealistic, ultra detailed, 8K',
    '20': 'Oil refinery complex at sunset, huge storage tanks, industrial pipes, orange and gold sky, photorealistic, ultra detailed, 8K',
}

for num, prompt in retry_items.items():
    payload = json.dumps({'model': 'cogview-3-flash', 'messages': [{'role': 'user', 'content': f'Image prompt: {prompt}'}]}).encode('utf-8')
    req = urllib.request.Request(API_URL, data=payload, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=50) as resp:
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
    time.sleep(2)

print('Retry done')