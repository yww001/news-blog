import urllib.request
import json
import time

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

prompt = "Global news headline 2026, world leaders meeting at UN building, photorealistic, ultra detailed, 8K"

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

try:
    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        content = result['choices'][0]['message']['content']
        print(f"Success! Content type: {type(content)}")
        if isinstance(content, list):
            print(f"URL: {content[0].get('url', 'No URL')[:80]}...")
except Exception as e:
    print(f"Error: {e}")