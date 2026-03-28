#!/bin/bash
# 晚上存档脚本 - 将今日新闻存档到历史
# 时间：UTC 0:00 (北京时间 08:00)
# 用途：将首页新闻存档到历史页面

set -e

REPO_DIR="/home/swg/.openclaw/workspace/news-blog/repo"
SOURCE_DATE="20260322"  # 使用03月22日作为模板

# 获取今天的日期（动态）
TODAY_STR=$(date '+%Y年%m月%d日')
TODAY_FILE=$(date '+%Y%m%d')
CURRENT_DATE=$(date '+%Y-%m-%d')

echo "========================================"
echo "晚上存档任务启动 - $CURRENT_DATE"
echo "========================================"
echo "📅 存档日期：$TODAY_STR"
echo "📁 文件名：$TODAY_FILE.html"
echo "📋 模板：$SOURCE_DATE.html"
echo ""

cd $REPO_DIR

# 步骤1：拷贝模板文件
echo "📝 步骤1：拷贝模板文件..."
if [ ! -f "history/$SOURCE_DATE.html" ]; then
    echo "❌ 错误：找不到模板文件 history/$SOURCE_DATE.html"
    exit 1
fi
cp "history/$SOURCE_DATE.html" "history/$TODAY_FILE.html"
echo "✅ 已拷贝：history/$SOURCE_DATE.html → history/$TODAY_FILE.html"
echo ""

# 步骤2：替换日期
echo "📝 步骤2：替换日期..."
SOURCE_DATE_STR="2026年03月22日"
sed -i "s/$SOURCE_DATE_STR/$TODAY_STR/g" "history/$TODAY_FILE.html"
sed -i "s/images\/$SOURCE_DATE\//images\/$TODAY_FILE\//g" "history/$TODAY_FILE.html"
echo "✅ 已将所有 $SOURCE_DATE_STR 替换为 $TODAY_STR"
echo "✅ 已将图片路径从 images/$SOURCE_DATE/ 改为 images/$TODAY_FILE/"
echo ""

# 步骤3：从首页提取新闻并替换
echo "📝 步骤3：从首页提取新闻内容并替换..."

python3 << PYTHON_EOF
import re

# 从bash获取变量
today_file = "$TODAY_FILE"

# 读取首页
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
except:
    print("❌ 错误：无法读取首页 index.html")
    exit(1)

# 读取目标历史文件
try:
    with open(f"history/{today_file}.html", 'r', encoding='utf-8') as f:
        history_content = f.read()
except:
    print(f"❌ 错误：无法读取历史文件 history/{today_file}.html")
    exit(1)

# 从首页提取新闻网格内容
start = index_content.find('<div class="news-grid" id="newsGrid">')
if start != -1:
    depth = 1
    pos = start + len('<div class="news-grid" id="newsGrid">')
    while depth > 0 and pos < len(index_content):
        next_open = index_content.find('<div', pos)
        next_close = index_content.find('</div>', pos)
        
        if next_close == -1:
            break
        
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                end = next_close + 6
                news_grid = index_content[start:end]
                break
            pos = next_close + 6

# 提取每个news-card
card_pattern = r'<div class="news-card">(.*?)</div>\s*</div>'
cards = re.findall(card_pattern, news_grid, re.DOTALL)

# 提取每个article
article_pattern = r'<article class="news-card"[^>]*>(.*?)</article>'
articles = re.findall(article_pattern, history_content, re.DOTALL)

# 逐个替换article
new_content = history_content
for i, card in enumerate(cards):
    if i >= len(articles):
        break
    
    # 提取图片路径
    img_match = re.search(r'<img src="([^"]+)"', card)
    if img_match:
        img_path = img_match.group(1)
        img_path = img_path.replace('images/', f'../images/{today_file}/')
    
    # 提取标题
    title_match = re.search(r'<h3 class="news-title">(.*?)</h3>', card)
    title = title_match.group(1) if title_match else "无标题"
    
    # 提取摘要
    summary_match = re.search(r'<p class="news-summary">(.*?)</p>', card)
    summary = summary_match.group(1) if summary_match else "无内容"
    
    # 提取标签
    tags = re.findall(r'<span class="tag">(.*?)</span>', card)
    
    # 构建新的article
    old_article = f'<article class="news-card"[^>]*>{articles[i]}</article>'
    new_article = f'''<article class="news-card" data-news-id="{i+1}">
        <div class="news-image">
            <img src="{img_path}" alt="{title}" loading="lazy">
        </div>
        <div class="news-content">
            <h3 class="news-title">{title}</h3>
            <p class="news-summary">{summary}</p>
            <div class="news-tags">'''
    
    for tag in tags:
        new_article += f'\n                <span class="tag">{tag}</span>'
    
    new_article += '''
            </div>
        </div>
    </article>'''
    
    new_content = re.sub(old_article, new_article, new_content, count=1, flags=re.DOTALL)

# 写回文件
with open(f"history/{today_file}.html", 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ 已将首页新闻内容替换到 history/{today_file}.html")

PYTHON_EOF

echo ""

# 步骤4：复制首页图片
echo "📝 步骤4：复制首页图片..."
mkdir -p "images/$TODAY_FILE"

python3 << PYTHON_EOF
import re
import shutil
import os

today_file = "$TODAY_FILE"  # 从bash获取

# 读取首页
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# 提取所有图片路径
img_pattern = r'<img src="images/(news_\d+\.png)"'
matches = re.findall(img_pattern, index_content)

if matches:
    print(f"✅ 从首页找到 {len(matches)} 张图片")
    
    # 拷贝并重命名图片
    for i, img_name in enumerate(matches, 1):
        src_path = f"images/{img_name}"
        dst_path = f"images/{today_file}/news_{i}.png"
        
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
            print(f"  ✅ {img_name} → news_{i}.png")
        else:
            print(f"  ⚠️  警告：找不到 {src_path}")
else:
    print("❌ 错误：无法从首页提取图片路径")

PYTHON_EOF

echo "✅ 已复制首页图片到 images/$TODAY_FILE/"
echo ""

# 步骤5：重命名图片为 news_102.png, news_103.png... 格式
echo "📝 步骤5：重命名图片..."
cd "images/$TODAY_FILE"
for i in {1..10}; do
    if [ -f "news_${i}.png" ]; then
        new_num=$((i + 101))
        mv "news_${i}.png" "news_${new_num}.png"
        echo "  ✅ news_${i}.png → news_${new_num}.png"
    fi
done
cd "$REPO_DIR"
echo "✅ 已重命名所有图片"
echo ""

# 步骤6：更新历史索引页面
echo "📝 步骤6：更新历史索引页面..."

python3 << PYTHON_EOF
import re

# 从bash获取变量
today_file = "$TODAY_FILE"
today_date_str = "$TODAY_STR"

# 读取历史索引文件
with open('history.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取今日新闻标题（用于索引描述）
try:
    with open(f'index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # 提取前3条新闻标题
    titles = []
    for match in re.finditer(r'<h3 class="news-title">(.*?)</h3>', index_html):
        title = match.group(1).strip()
        titles.append(title.split('·')[0])  # 取"·"前面的部分
        if len(titles) >= 3:
            break
    
    # 生成描述（取前3个标题的前几个字）
    description = '、'.join([t[:10] for t in titles[:3]])
    if len(description) > 30:
        description = description[:30] + '...'
    
except:
    # 如果无法提取，使用默认描述
    description = "每日新闻更新，涵盖科技、财经、国际等领域"

# 检查是否已包含今日的链接
if today_file not in content:
    # 生成新的历史项
    new_item = f'''
        <a href="history/{today_file}.html" class="history-item">
            <h3>{today_date_str}</h3>
            <p>{description}</p>
        </a>'''

    # 找到最后一个 </a> 标签
    last_a_pos = content.rfind('</a>')
    if last_a_pos != -1:
        # 在最后一个 </a> 后面插入新项
        new_content = content[:last_a_pos + len('</a>')] + new_item + content[last_a_pos + len('</a>'):]
        
        # 写回
        with open('history.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 历史索引已更新：添加 {today_date_str} 链接")
else:
    print(f"⏭️  历史索引已包含 {today_date_str}，跳过更新")

PYTHON_EOF

echo ""

# 步骤7：Git提交推送
echo "📝 步骤7：提交到Git..."
git add history/$TODAY_FILE.html images/$TODAY_FILE/ history.html
git commit -m "晚上存档：添加$TODAY_STR历史页面

- 拷贝历史模板并替换日期
- 从首页提取新闻内容
- 复制并更新图片
- 重命名图片为 news_102.png 格式
- 更新历史索引页面"

if git push; then
    echo "✅ 步骤7完成：Git推送成功"
    PUSH_SUCCESS=1
else
    echo "❌ 步骤7失败：Git推送失败"
    PUSH_SUCCESS=0
fi
echo ""

# 步骤8：发送飞书通知
echo "📝 步骤8：发送飞书通知..."
if [ $PUSH_SUCCESS -eq 1 ]; then
    /home/swg/.openclaw/workspace/news-blog/notify.sh "格式晚上7点存档任务完成。"
    echo "✅ 步骤8完成：飞书通知已发送"
else
    /home/swg/.openclaw/workspace/news-blog/notify.sh "⚠️ 格式晚上7点存档任务完成（Git推送失败）。"
    echo "⚠️ 步骤8完成：发送失败通知"
fi
echo ""

echo "========================================"
echo "✅ 晚上存档任务完成！"
echo "========================================"
echo "📅 存档日期：$TODAY_STR"
echo "📁 历史文件：history/$TODAY_FILE.html"
echo "📂 图片目录：images/$TODAY_FILE/"
echo "📤 Git推送：$([ $PUSH_SUCCESS -eq 1 ] && echo '成功 ✅' || echo '失败 ❌')"
echo "🕐 完成时间：$(date '+%Y-%m-%d %H:%M:%S UTC')"
echo "========================================"
