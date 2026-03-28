#!/usr/bin/env python3
"""
生成24日历史页面
使用24日的真实搜索结果
"""

# 24日的新闻数据（基于真实搜索结果）
news_data = [
    {
        "title": "特朗普称与伊朗进行\"富有成效\"的对话 伊朗外交部否认",
        "summary": "美国总统特朗普23日表示，美国和伊朗在过去两天进行了\"非常良好且富有成效\"的对话，已形成协议要点。基于这些会谈，将对伊朗发电厂及能源基础设施的打击行动推迟5天。伊朗外交部则否认与美国进行了任何谈判。",
        "tags": ["国际", "军事"],
        "image": "news_1.png"
    },
    {
        "title": "习近平在河北雄安新区考察 强调牢牢把握雄安新区功能定位",
        "summary": "3月23日，中共中央总书记、国家主席、中央军委主席习近平在河北雄安新区考察，并主持召开深入推进雄安新区高质量建设和发展座谈会。他强调，要牢牢把握雄安新区作为北京非首都功能疏解集中承载地的首要功能定位，努力建设新时代创新高地。",
        "tags": ["国内", "政治"],
        "image": "news_2.png"
    },
    {
        "title": "特朗普暂停打击伊朗能源设施 推迟5天以等待谈判结果",
        "summary": "美国总统特朗普在社交媒体发文表示，已指示国防部将对伊朗发电厂及能源基础设施的军事打击行动推迟5天，前提是正在进行中的会议取得成功。这一表态暂时遏制了冲突进一步升级的风险，国际油价随之下跌超过10%。",
        "tags": ["国际", "经济"],
        "image": "news_3.png"
    },
    {
        "title": "以军在德黑兰发动\"大规模袭击\" 伊朗向以色列发射7轮导弹",
        "summary": "以色列国防总参谋长表示将加强在黎巴嫩的地面行动，以将真主党驱逐至远离边界的地区。24日，以色列国防军监测到伊朗向以色列发射7轮导弹攻击，其中一枚导弹直接击中特拉维夫市中心，造成建筑受损和人员受伤。",
        "tags": ["国际", "军事"],
        "image": "news_4.png"
    },
    {
        "title": "国务院批复《雄安新区发展规划纲要》 推进高质量建设",
        "summary": "国家发展改革委、河北省联合印发关于深入推进雄安新区高质量建设和发展意见，要求统筹推进启动区、起步区等建设。华能集团等央企总部入驻雄安新区，为加快建设新型能源体系作出新贡献。北京四中雄安校区已投入使用，现有学生380多人。",
        "tags": ["国内", "经济"],
        "image": "news_5.png"
    },
    {
        "title": "国际能源署警告中东能源危机将对全球经济构成\"重大威胁\"",
        "summary": "国际能源总干事法提赫・比罗尔警告称，中东战争引发的能源危机正对全球经济构成\"重大威胁\"，并补充\"没有哪个国家能够幸免\"。根据分析数据，自战争开始以来通过霍尔木兹海峡的货物运输量骤降了95%，全球每天损失1100万桶原油。",
        "tags": ["国际", "能源"],
        "image": "news_6.png"
    },
    {
        "title": "习近平第四次来到雄安新区 亲自决策领航\"未来之城\"建设",
        "summary": "从谋划选址到规划建设再到深入推进高质量建设和发展，习近平总书记亲自决策、亲自部署、亲自推动，为雄安新区发展领航指路。这是2017年以来，习近平第四次来到雄安新区，倾注大量心血，推动高质量发展。",
        "tags": ["国内", "政治"],
        "image": "news_7.png"
    },
    {
        "title": "美伊双方否认会谈 俄方强调必须立即停止敌对行动",
        "summary": "伊朗外交部表示与美国开展\"不存在对话\"，否认特朗普会谈的说法。俄罗斯外长拉夫罗夫与伊朗外长阿拉格齐进行电话交流，强调\"必须立即停止敌对行动并寻求政治解决\"。分析认为，美伊双方都有降级谈判的意向。",
        "tags": ["国际", "外交"],
        "image": "news_8.png"
    },
    {
        "title": "中东战争导致多国能源设施受损 全球能源供应受严重影响",
        "summary": "自美以攻势开始以来，已有9个国家的至少40处能源基础设施遭受\"严重或极严重破坏\"。为应对能源危机，中国已宣布限制国内燃油价格上涨、希腊实施燃料补贴、印尼计划削减支出以抵御战争带来的经济后果。",
        "tags": ["国际", "经济"],
        "image": "news_9.png"
    },
    {
        "title": "雄安新区建设取得重大阶段性成果 努力创造\"雄安质量\"",
        "summary": "经过各方共同努力，雄安新区建设和发展取得重大阶段性成果。实践充分证明，党中央关于建设雄安新区的决策是完全正确的。新区将系统谋划一体抓好高质量建设和高效能治理，大力发展新质生产力，培育现代化产业体系。",
        "tags": ["国内", "发展"],
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

# 写入新文件
with open("/home/swg/.openclaw/workspace/news-blog/repo/history/20260324.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ 已生成24日HTML页面")
print("使用24日真实新闻数据")
print("主要新闻：特朗普伊朗谈判、雄安新区、中东能源危机")
