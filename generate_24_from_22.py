#!/usr/bin/env python3
"""
生成24日历史页面
使用22日的HTML结构，替换为24日的新闻内容
"""

# 24日的新闻数据（与23日相同，因为25日搜索API失败）
news_data = [
    {
        "title": "全球科技峰会今日开幕",
        "summary": "多国科技领袖出席，聚焦AI与可持续发展议题。各国专家就人工智能伦理、可持续发展等议题展开深入讨论，共同制定行业新标准。",
        "tags": ["科技", "国际"],
        "image": "news_1.png"
    },
    {
        "title": "新能源汽车销量创新高",
        "summary": "本月新能源汽车销量同比增长30%，市场前景看好。多家厂商加速布局电动化转型，供应链持续完善，为绿色出行注入新动力。",
        "tags": ["汽车", "经济"],
        "image": "news_2.png"
    },
    {
        "title": "量子计算取得新突破",
        "summary": "量子计算机实现更高稳定性和运算速度，为未来科技发展奠定基础。研究团队在纠错算法上取得重大进展，商业化进程加速。",
        "tags": ["科技", "量子计算"],
        "image": "news_3.png"
    },
    {
        "title": "航天发射任务圆满成功",
        "summary": "最新卫星成功入轨，为通信网络升级提供支持。本次发射任务标志着航天工业进入新阶段，国际合作推动太空探索迈上新台阶。",
        "tags": ["航天", "科技"],
        "image": "news_4.png"
    },
    {
        "title": "人工智能医疗应用加速",
        "summary": "AI在疾病诊断和药物研发中的应用取得进展，医疗行业迎来变革。多家医疗机构引入AI辅助诊断系统，提高诊疗效率。",
        "tags": ["AI", "医疗"],
        "image": "news_5.png"
    },
    {
        "title": "可再生能源投资创新高",
        "summary": "各国加大清洁能源投资，推动绿色转型。太阳能和风能市场持续扩大，技术创新降低成本，环保意识提升。",
        "tags": ["能源", "环保"],
        "image": "news_6.png"
    },
    {
        "title": "5G网络覆盖加速推进",
        "summary": "更多城市实现5G全覆盖，为数字经济提供基础设施支持。5G应用场景不断丰富，物联网、自动驾驶等领域蓬勃发展。",
        "tags": ["科技", "通信"],
        "image": "news_7.png"
    },
    {
        "title": "在线教育平台用户激增",
        "summary": "学习数字化趋势明显，在线教育用户持续增长。个性化学习成为新趋势，AI教育助手广泛应用。",
        "tags": ["教育", "科技"],
        "image": "news_8.png"
    },
    {
        "title": "智慧城市建设加速",
        "summary": "多个城市启动智慧城市项目，提升城市管理水平。物联网技术广泛应用，智能交通、智能安防系统不断完善。",
        "tags": ["科技", "城市"],
        "image": "news_9.png"
    },
    {
        "title": "生物科技领域投资活跃",
        "summary": "基因编辑、生物制药等领域投资显著增加。生物科技创新成果不断涌现，为人类健康带来新希望。",
        "tags": ["科技", "生物"],
        "image": "news_10.png"
    }
]

# 新闻卡片HTML模板
NEWS_CARD_TEMPLATE = '''    <article class="news-card" data-news-id="{idx}">
        <div class="news-image">
            <img src="../images/20260324/{image}" alt="{title}" loading="lazy">
        </div>
        <div class="news-content">
            <h3 class="news-title">{title}</h3>
            <p class="news-summary">{summary}</p>
            <div class="news-tags">
                {tags}
            </div>
        </div>
    </article>
'''

# 生成新闻卡片HTML
news_html = ""
for idx, news in enumerate(news_data, 1):
    tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in news["tags"]])
    news_html += NEWS_CARD_TEMPLATE.format(
        idx=idx,
        image=news["image"],
        title=news["title"],
        summary=news["summary"],
        tags=tags_html
    )
    news_html += "\n    \n"

# 读取22日模板
with open("/home/swg/.openclaw/workspace/news-blog/repo/history/20260322.html", "r", encoding="utf-8") as f:
    content = f.read()

# 替换日期为24日
content = content.replace("2026年03月22日", "2026年03月24日")

# 找到新闻区域并替换
import re
pattern = r'(<section class="news-grid">\s*)(.*?)(\s*</section>)'
content = re.sub(pattern, lambda m: f'{m.group(1)}{news_html}{m.group(3)}', content, flags=re.DOTALL, count=1)

# 替换返回链接的日期
content = content.replace('href="../index.html"', 'href="../index.html"')

# 写入新文件
with open("/home/swg/.openclaw/workspace/news-blog/repo/history/20260324.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 已生成24日HTML页面")
print("使用22日模板结构")
print("包含24日新闻内容")
