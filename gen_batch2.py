import urllib.parse, requests, io
from PIL import Image
from pathlib import Path
import time

news_items = [
    (11, 'AI language model Chinese artificial intelligence large language model futuristic technology interface digital brain neural network'),
    (12, 'Middle East peace treaty Riyadh summit Gulf countries cooperation Iran Saudi peace agreement signing ceremony desert diplomacy'),
    (13, 'digital yuan RMB digital currency internationalization cross-border payment Chinese currency globalization fintech revolution mobile payment'),
    (14, 'SpaceX Starship moon mission commercial space flight moon landing rocket in space lunar base concept science fiction'),
    (15, 'German manufacturing industry factory automation industrial production European economy precision engineering automotive factory'),
    (16, 'Southeast Asia digital economy Singapore city e-commerce delivery mobile payment young entrepreneurs tech hub Asia'),
    (17, 'nuclear fusion reactor tokamak fusion device plasma physics experiment China scientific achievement infinite clean energy futuristic laboratory'),
    (18, 'London City financial district Canary Wharf London Bridge British economy financial services historic architecture UK'),
    (19, 'renewable energy wind turbines solar panels green energy investment clean power plant sustainable future environmental protection'),
    (20, 'Chinese internet giants tech company headquarters stock market performance digital economy growth modern office building'),
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
print('Batch 2 done')