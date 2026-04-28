#!/bin/bash
# Git 自动提交推送脚本
# Usage: ./upload.sh "commit message"

cd /home/swg/.openclaw/workspace/news-blog || exit 1

COMMIT_MSG="${1:-自动更新 $(date '+%Y-%m-%d %H:%M')}"

# 检查是否有更改
if git diff --quiet && git diff --cached --quiet; then
    echo "ℹ️  没有检测到更改，跳过提交"
    exit 0
fi

# 添加所有更改
git add -A

# 提交
git commit -m "$COMMIT_MSG" || { echo "❌ 提交失败"; exit 1; }

# 推送
git push origin main || { echo "❌ 推送失败"; exit 1; }

echo "✅ Git 提交推送成功: $COMMIT_MSG"
exit 0
