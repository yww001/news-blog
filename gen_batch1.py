import urllib.parse, requests, io
from PIL import Image
from pathlib import Path
import time

news_items = [
    (1, 'futuristic quantum computer chip microscopic view glowing blue circuits quantum bits visualization scientific laboratory high-tech hardware dark background'),
    (2, 'China US cooperation AI artificial intelligence bilateral summit meeting Geneva conference world leaders technology governance international diplomacy'),
    (3, 'stock market trading China A-share market stock price rising Shanghai stock exchange financial charts bullish trend modern city skyline'),
    (4, 'Mars mission spacecraft launching Chinese rocket space exploration red planet Mars background rocket flames dramatic sky'),
    (5, 'peace negotiation Russia Ukraine conflict resolution diplomatic talks UN security council diplomats world peace international relations'),
    (6, 'Japanese and Chinese flags waving Beijing cityscape diplomatic ceremony bilateral meeting cultural exchange Asian diplomacy'),
    (7, 'semiconductor chip manufacturing global supply chain high-tech factory silicon wafer production clean room environment technology industry'),
    (8, 'Chinese electric vehicles EV cars charging modern charging station BYD cars new energy transportation green technology electric future'),
    (9, 'European Central Bank ECB Frankfurt monetary policy meeting Euro currency bank building financial district European finance'),
    (10, 'South Korea AI safety initiative artificial intelligence security global cooperation Seoul cityscape technology governance international agreement'),
]

img_dir = Path('images')
img_dir.mkdir(exist_ok=True)

for num, prompt in news_items:
    output_path = img_dir / f'news_20260704_{num:02d}.png'
    print(f'[{num:02d}] Generating...', flush=True)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f'https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&model=flux'
    try:
        resp = requests.get(url, timeout=90, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code == 200 and len(resp.content) > 1000:
            img = Image.open(io.BytesIO(resp.content))
            if img.mode != 'RGB': img = img.convert('RGB')
            img.save(output_path, 'PNG')
            print(f'  -> OK', flush=True)
        else:
            print(f'  -> FAILED {resp.status_code}', flush=True)
    except Exception as e:
        print(f'  -> ERROR: {e}', flush=True)
    time.sleep(2)
print('Batch 1 done')