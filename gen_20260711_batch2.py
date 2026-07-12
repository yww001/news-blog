#!/usr/bin/env python3
import urllib.request, json, base64, time
API_KEY = '88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB'
API_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
DATE_STR = '20260711'

prompts = {
    '11': 'Southern European city street in extreme heat, thermometer showing very high temperature, dry cracked earth, people shielding from sun, heat haze, photorealistic, ultra detailed, 8K',
    '12': 'Typhoon striking coastal Chinese city with huge waves crashing on seawall, palm trees bending in strong wind, heavy rain, emergency rescue boats, photorealistic, ultra detailed, 8K',
    '13': 'World Cup football stadium with excited fans waving national flags, night game with floodlights, aerial view of modern sports arena, photorealistic, ultra detailed, 8K',
    '14': 'Archaeologists carefully excavating ancient bronze artifacts at archaeological site, golden bronze masks and ceremonial objects, photorealistic, ultra detailed, 8K',
    '15': 'Bitcoin cryptocurrency symbol glowing on digital screen, crypto trading chart showing downward trend, dark trading room with multiple monitors, photorealistic, ultra detailed, 8K',
    '16': 'Sleek modern foldable smartphone displaying colorful interface, thin bezel screen, premium electronic device, dark elegant background, photorealistic, ultra detailed, 8K',
    '17': 'Peace negotiation table with Russian and Ukrainian flags facing each other, international diplomats in discussion, grand conference room, photorealistic, ultra detailed, 8K',
    '18': 'Elderly Chinese citizens exercising in morning park, tai chi practice, modern city skyline background, photorealistic, ultra detailed, 8K',
    '19': 'SpaceX rocket launching into space at night, fiery exhaust trail, stars in dark sky, Cape Canaveral launch pad, photorealistic, ultra detailed, 8K',
    '20': 'Oil refinery complex at sunset with large storage tanks and industrial pipes, orange sky reflecting on facility, photorealistic, ultra detailed, 8K',
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

print('Batch 2/2 done')