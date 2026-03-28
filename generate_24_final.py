#!/usr/bin/env python3
"""
生成24日历史页面（重新设计）
使用与25日首页完全不同的24日新闻
"""

# 24日的新闻数据（确保与25日首页完全不同）
news_data = [
    {
        "title": "以军空袭德黑兰造成122人被送医 黎巴嫩真主党加强火力",
        "summary": "以色列国防军对德黑兰发动大规模空袭，攻击了50多个目标。在过去24小时内，共有122人被送往医院。以色列总参谋长表示将加强在黎巴嫩的有针对性地面行动。",
        "tags": ["国际", "军事"],
        "image": "news_1.png"
    },
    {
        "title": "以色列三栋建筑被导弹击中 经济影响持续扩大",
        "summary": "一枚导弹直接击中特拉维夫市中心，造成三栋建筑受损。在海法、贝尔谢巴等多地都有被导弹击中的报告。国际能源署警告中东能源危机将对全球经济构成重大威胁。",
        "tags": ["国际", "经济"],
        "image": "news_2.png"
    },
    {
        "title": "习近平考察雄安新区 李强蔡奇丁薛祥 高规格团队展现重视",
        "summary": "3月23日，习近平抵达雄安新区考察，华能集团总部已迁入。北京四中雄安校区投入使用，现有学生380多人。习近平强调要牢牢把握雄安新区功能定位，坚持质量优先。",
        "tags": ["国内", "政治"],
        "image": "news_3.png"
    },
    {
        "title": "伊朗否认与美方谈判 称特朗普表态为心理战",
        "summary": "伊朗外交部否认与美国进行任何谈判。伊朗迈赫尔通讯社称不存在任何直接或间接接触，特朗普的表态旨在降低能源价格并为军事计划争取时间。俄方强调必须立即停止敌对行动。",
        "tags": ["国际", "外交"],
        "image": "news_4.png"
    },
    {
        "title": "黄金价格暴跌近7% 国际油价大幅回落",
        "summary": "3月23日现货黄金价格接连失守5个整数关口，最低跌至4100美元下方。特朗普表示推迟对伊朗发电厂打击5天后，原油价格暴跌超过10%，欧洲股市全线回升。",
        "tags": ["国际", "财经"],
        "image": "news_5.png"
    },
    {
        "title": "霍尔木兹海峡运输量骤降95% 全球能源供应面临严重挑战",
        "summary": "根据分析数据，自战争开始以来，通过霍尔木兹海峡的货物运输量骤降了95%，全球每天损失1100万桶原油。埃及等地计划暂停销售液化石油气，多国推出补贴应对能源危机。",
        "tags": ["国际", "能源"],
        "image": "news_6.png"
    },
    {
        "title": "以色列舆论担心特朗普为宣布胜利而在谈判中妥协",
        "summary": "以色列国内媒体分析认为，特朗普表态对以方有些意外。虽然不完全拒绝美伊谈判，但以方坚持以红线为前提，即必须将浓缩铀运出伊朗并摧毁其导弹能力。以方担心特朗普可能在谈判中做出过多妥协。",
        "tags": ["国际", "政治"],
        "image": "news_7.png"
    },
    {
        "title": "华能集团入驻雄安新区 千名员工迁驻激发创新活力",
        "summary": "中国华能集团有限公司总部迁驻雄安新区。习近平走进企业运营监控中心，听取创新情况汇报。华能集团将利用迁入机遇，激发干部职工创新创业，为建设能源强国作出新贡献。",
        "tags": ["国内", "经济"],
        "image": "news_8.png"
    },
    {
        "title": "北京四中雄安校区投入使用 师生总数超380人",
        "summary": "北京市援建的北京四中雄安校区于2023年8月投入使用。习近平走进教室与师生交流，希望把北京四中的好经验带过来。在学校食堂，习近平叮嘱要确保学生饮食安全，勉励孩子们惜福奋进与雄安一起成长。",
        "tags": ["国内", "教育"],
        "image": "news_9.png"
    },
    {
        "title": "雄安新区建设取得重大阶段性成果 李强丁薛祥出席座谈会",
        "summary": "李强表示要深入推进雄安新区高质量建设，在承接北京非首都功能疏解上力求新进展。丁薛祥指出要高水平建设雄安中关村科技园，促进产学研融通创新。新区将积极探索智慧城市管理，建设美丽雄安。",
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

print("✅ 已重新生成24日HTML页面")
print("新闻内容与25日首页完全不同")
print("主要事件：以军空袭德黑兰、黄金价格暴跌、雄安新区、能源危机等")
