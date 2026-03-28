#!/bin/bash
# 飞书通知脚本

# 用户ID
USER_ID="ou_9249627924cb237809a9e6c6c0aa7801"

# 消息内容
MESSAGE="$1"

# 调用飞书通知（使用环境变量设置的通知服务）
if [ -n "$OPENCLAW_NOTIFY_ENDPOINT" ]; then
    curl -s -X POST "$OPENCLAW_NOTIFY_ENDPOINT" \
        -H "Content-Type: application/json" \
        -d "{\"user_id\":\"$USER_ID\",\"message\":\"$MESSAGE\"}" \
        > /dev/null 2>&1
fi

# 同时写入状态文件
STATUS_DIR="/home/swg/.openclaw/workspace/news-blog/status"
mkdir -p "$STATUS_DIR"
echo "$(date '+%Y-%m-%d %H:%M:%S') - $MESSAGE" >> "$STATUS_DIR/notifications.log"

# 使用飞书API发送通知
python3 << PYTHON_EOF
import json
import requests
import os

# 飞书配置
OPENCLAW_CONFIG = "/home/swg/.openclaw/openclaw.json"
USER_ID = "$USER_ID"
MESSAGE = "$MESSAGE"

def load_feishu_config():
    """从 openclaw.json 加载飞书配置"""
    with open(OPENCLAW_CONFIG, 'r') as f:
        config = json.load(f)
    return config['channels']['feishu']

def get_tenant_access_token(app_id, app_secret):
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, json=data)
    result = response.json()
    if result.get('code') != 0:
        raise Exception(f"获取 token 失败: {result.get('msg')}")
    return result['tenant_access_token']

def send_message(user_id, message, app_id, app_secret):
    """发送文本消息到飞书用户"""
    # 获取 token
    token = get_tenant_access_token(app_id, app_secret)

    # 发送消息
    send_url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    content = json.dumps({"text": message})

    data = {
        "receive_id": user_id,
        "msg_type": "text",
        "content": content
    }

    # receive_id_type 需要作为查询参数传递
    params = {
        "receive_id_type": "open_id"
    }

    send_response = requests.post(send_url, headers=headers, params=params, json=data)
    send_result = send_response.json()

    if send_result.get('code') != 0:
        raise Exception(f"发送消息失败: {send_result.get('msg')}")

    print(f"✅ 消息已成功发送给用户 {user_id}")

try:
    config = load_feishu_config()
    app_id = config.get('appId')
    app_secret = config.get('appSecret')

    if app_id and app_secret:
        send_message(USER_ID, MESSAGE, app_id, app_secret)
    else:
        print("⚠️ 飞书未配置，跳过通知")
except Exception as e:
    print(f"❌ 发送飞书通知失败: {e}")

PYTHON_EOF
