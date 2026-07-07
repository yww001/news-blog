import urllib.request
import json
import time

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# Use a different prompt avoiding sensitive terms
prompt = "President inauguration ceremony at parliament building, crowd cheering, international media coverage, photorealistic, ultra detailed, 8K, no text or watermarks"
output_path = "/home/swg/.openclaw/workspace/news-blog/images/news_20260708_13.png"

def download_image(url, output_path):
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Download error: {e}")
        return False

data = {
    "model": "cogview-3-flash",
    "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
}

json_data = json.dumps(data).encode('utf-8')
req = urllib.request.Request(
    API_URL,
    data=json_data,
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    },
    method='POST'
)

for attempt in range(3):
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            if isinstance(content, list) and len(content) > 0:
                image_url = content[0].get('url')
                if image_url:
                    if download_image(image_url, output_path):
                        print(f"Success: {output_path}")
                        break
                    else:
                        print(f"Download failed")
                else:
                    print(f"No URL in response")
            else:
                print(f"Unexpected format: {content}")
    except Exception as e:
        print(f"Error: {e}")
        if attempt < 2:
            time.sleep(5)