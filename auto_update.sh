#!/bin/bash
# 自动更新新闻脚本（增强版 - 含质量检查）
# 用于 cron 定时任务

cd /home/swg/.openclaw/workspace/news-blog || exit 1

# 记录日志
LOG_FILE="/home/swg/.openclaw/workspace/news-blog/logs/cron_$(date '+%Y-%m-%d').log"
echo "========================================" >> "$LOG_FILE"
echo "自动更新任务启动（增强版） - $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

SUCCESS=0

# 更新今天的新闻（增强版 - 含质量检查）
echo "📰 步骤1: 更新新闻（含质量检查）..." >> "$LOG_FILE"
python3 auto_update.py --news-count 20 >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "❌ 更新失败" >> "$LOG_FILE"
    SUCCESS=1
fi

echo "========================================" >> "$LOG_FILE"
echo "完成时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 通知用户
if [ $SUCCESS -eq 0 ]; then
    echo "✅ 自动更新完成"
    ../notify.sh "格式早上7点更新新闻任务完成。"
else
    echo "⚠️ 自动更新有错误完成"
    ../notify.sh "⚠️ 格式早上7点更新新闻任务完成（有错误）。"
fi
