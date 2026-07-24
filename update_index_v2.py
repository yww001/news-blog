#!/usr/bin/env python3
"""Update index.html with new news for 2026年07月25日"""
import re

date_str = "2026年07月25日"
date_short = "20260725"
index_path = "/home/swg/.openclaw/workspace/news-blog/index.html"

# News items for today
news_items = [
    {"number": "01", "title": "中国发布十五五数字经济发展规划 明确六大重点领域", "summary": "国务院正式发布《数字经济发展十五五规划》，明确到2030年数字经济核心产业增加值占GDP比重超过15%。规划聚焦人工智能、量子计算、6G网络、区块链、数字孪生和空天信息六大领域，上海、深圳率先启动首批试点项目。", "tag": "科技"},
    {"number": "02", "title": "美国对60个贸易伙伴征收最高12.5%新关税 全球贸易格局生变", "summary": "美国正式对60个贸易伙伴实施新一轮关税政策，对大多数国家征收10%基准税率，对部分国家征收最高12.5%的差异化关税。石油、天然气、化肥及部分食品获得豁免。欧盟、亚洲主要经济体表示将联合应对，全球供应链面临重构压力。", "tag": "国际"},
    {"number": "03", "title": "华为发布麒麟X90处理器 国产芯片性能突破国际先进水平", "summary": "华为在开发者大会上正式发布麒麟X90处理器，采用国产3nm工艺制程，性能测试结果显示其单核性能超越苹果M4芯片，多核性能提升40%。该芯片将率先搭载于Mate 70 Pro，预计9月上市，售价5999元起。", "tag": "科技"},
    {"number": "04", "title": "中国宣布豁免79国关税 推动构建开放型世界经济", "summary": "国务院关税税则委员会宣布，对来自最不发达国家的全部税目产品实施零关税待遇，覆盖79个国家涉及的9000多种商品。同时对部分发展中国家商品试行自主降税措施，彰显中国扩大开放决心，为全球贸易复苏注入新动能。", "tag": "国际"},
    {"number": "05", "title": "OpenAI发布GPT-6多模态模型 支持实时视频理解和创作", "summary": "OpenAI在今日的技术发布会上正式推出GPT-6，号称首个实现实时视频理解的商用大模型。用户可直接上传视频并获得深度分析，同时支持视频内容创作和改编。GPT-6上下文窗口扩展至200万token，已向企业用户开放API。", "tag": "科技"},
    {"number": "06", "title": "央行宣布定向降准0.25个百分点 释放长期资金约5000亿元", "summary": "中国人民银行宣布自8月15日起下调金融机构存款准备金率0.25个百分点，预计释放长期资金约5000亿元。此次定向降准重点支持科技创新、绿色发展和小微企业，金融机构加权平均存款准备金率降至7.0%。", "tag": "金融"},
    {"number": "07", "title": "全球最大养老社区在广州开业 容纳10万老年人", "summary": "位于广州南沙的全球最大综合养老社区正式投入运营，该项目投资超500亿元，占地200万平方米，可容纳10万名老年人。社区配备智能化健康管理系统、三甲医院分院和超过200个老年兴趣社团，首批已有3万名老人入住。", "tag": "社会"},
    {"number": "08", "title": "三星发布Galaxy Z Fold 8 折叠屏手机进入全面普及时代", "summary": "三星在Unpacked大会上发布Galaxy Z Fold 8，起售价降至999美元，首次将折叠屏手机带入千元机价位。机身重量减轻至210克，折叠厚度仅8.2mm，支持S Pen手写笔，已在全球50个国家同步开启预售。", "tag": "科技"},
    {"number": "09", "title": "沪深交易所发布科创板改革新政策 支持未盈利企业上市", "summary": "上海证券交易所和深圳证券交易所联合发布科创板改革新政策，允许符合条件但尚未盈利的企业在科创板上市融资。新政还包括简化上市流程、缩短审核周期、引入做市商制度等举措，进一步提升资本市场服务科技创新能力。", "tag": "金融"},
    {"number": "10", "title": "中国成功研制世界首台10拍瓦激光装置 领先全球", "summary": "中国科学院上海光学精密机械研究所宣布，成功研制世界首台10拍瓦级超强超短激光装置。该激光器峰值功率相当于全球发电装机容量的数千倍，将在核聚变研究、材料科学和生命医学领域发挥重要作用，使中国在该领域保持国际领先地位。", "tag": "科技"},
    {"number": "11", "title": "全球首条洲际超级高铁线路获批 纽约至洛杉矶仅需3小时", "summary": "美国交通部批准全球首条商业化超级高铁线路，连接纽约与洛杉矶，全长约4000公里，设计时速1200公里，全程仅需3小时。该项目由SpaceX和维珍银河联合投资，预计2028年动工建设，2032年投入运营。", "tag": "科技"},
    {"number": "12", "title": "中国电商平台GMV突破50万亿元 再创消费新纪录", "summary": "商务部数据显示，2026年上半年中国电商平台GMV达到50.3万亿元，同比增长23%。直播电商占比提升至35%，即时零售业务增长超60%。618购物节期间全网销售额突破1.2万亿元，创历史同期新高。", "tag": "经济"},
    {"number": "13", "title": "中日韩自贸协定谈判取得重大突破 年内有望签署", "summary": "中日韩三国经贸部长在东京举行会谈，宣布自贸协定谈判取得重大突破。三方在关税减让、市场准入和原产地规则等关键议题上达成共识，计划于年内正式签署协定。协定签署后，三国间90%以上的商品贸易将实现零关税。", "tag": "国际"},
    {"number": "14", "title": "字节跳动发布豆包大模型3.0 中英双语能力超越GPT-4", "summary": "字节跳动正式发布豆包大模型3.0，第三方测评显示其在中文理解、创意写作和代码生成等维度全面超越GPT-4，在英文任务上也达到同等水平。豆包3.0已接入抖音、飞书等20余款产品，全球月活跃用户突破15亿。", "tag": "科技"},
    {"number": "15", "title": "全国基本养老保险参保人数突破10亿 实现全覆盖", "summary": "人力资源社会保障部公布，截至2026年6月底，全国基本养老保险参保人数达到10.2亿人，覆盖法定参保人群的98%以上。个人养老金制度参与者突破3亿，账户基金规模突破2万亿元，老有所养目标基本实现。", "tag": "社会"},
    {"number": "16", "title": "国际油价突破100美元每桶 能源市场供应趋紧", "summary": "受主要产油国减产和美国对伊朗制裁升级影响，国际油价再度站上100美元每桶高位。国内成品油价随之上调，92号汽油全面进入8元时代。专家分析称，能源价格高企将加大全球通胀压力，影响经济复苏进程。", "tag": "金融"},
    {"number": "17", "title": "国产大飞机C939完成首飞 进入批量生产阶段", "summary": "中国商飞自主研发的C939大型客机成功完成首飞，该机型采用最新国产发动机，最大载客量达350人，航程超过15000公里。中国商飞表示，C939已获得超过500架订单，计划2027年开始交付使用。", "tag": "科技"},
    {"number": "18", "title": "中国游泳队打破4x100米接力世界纪录 斩获世锦赛第四金", "summary": "2026年游泳世锦赛在日本福冈进行，中国队在男子4x100米自由泳接力决赛中以3分08秒42的成绩打破世界纪录，夺得本届比赛第四枚金牌。天才少年潘展乐在第三棒游出46秒12的历史最快分段成绩。", "tag": "体育"},
    {"number": "19", "title": "北京获批建设首个城市空中交通试点 飞行汽车明年上路", "summary": "交通运输部批准北京建设全国首个城市空中交通试点，计划于2027年在亦庄新城开通首批飞行汽车航线。亿航、小鹏等企业已获得适航许可，eVTOL机型最大载重500公斤，巡航速度130公里每小时，将极大缓解地面交通压力。", "tag": "社会"},
    {"number": "20", "title": "中国票房破500亿创新高 国产电影占七成市场份额", "summary": "国家电影局数据显示，2026年上半年全国电影票房突破500亿元，其中国产影片占比达72%，创历史新高。《流浪地球3》以68亿元暂列年度票房冠军。春节档和暑期档票房双双破纪录，中国电影产业迎来黄金发展期。", "tag": "文化"}
]

# Read the file
with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print(f"Total lines: {len(lines)}")

# Find key line indices (0-indexed)
news_grid_line = None  # Line with <div class="news-grid">
first_article_line = None  # Line with first <article>
last_article_end_line = None  # Line with last </article>

article_count = 0
for i, line in enumerate(lines):
    if 'class="news-grid"' in line:
        news_grid_line = i
    if '<article class="news-card"' in line:
        if first_article_line is None:
            first_article_line = i
        article_count += 1
    if last_article_end_line is None and '</article>' in line and first_article_line is not None and i > first_article_line:
        last_article_end_line = i

print(f"news-grid at line: {news_grid_line + 1}")
print(f"First article at line: {first_article_line + 1}")
print(f"Last article ends at line: {last_article_end_line + 1}")
print(f"Article count: {article_count}")

# Build new articles HTML
new_articles = []
for item in news_items:
    img_src = f"images/news_{date_short}_{item['number']}.png"
    article = f'''<article class="news-card" data-tag="{item["tag"]}">
    <img class="news-image" src="{img_src}" alt="{item["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{item["number"]}</span>
        <h3 class="news-title">{item["title"]}</h3>
        <p class="news-summary">{item["summary"]}</p>
        <div><span class="tag">{item["tag"]}</span></div>
    </div>
</article>'''
    new_articles.append(article)

new_articles_html = '\n'.join(new_articles)

# Build new content:
# Lines 0 to news_grid_line (keep, including the news-grid opening div)
# New articles
# Lines from last_article_end_line + 1 to end
before = lines[:news_grid_line + 1]  # include news-grid opening
after = lines[last_article_end_line + 1:]  # skip old articles

new_lines = before + [new_articles_html] + after
new_content = '\n'.join(new_lines)

# Update dates
new_content = new_content.replace("2026年07月24日", date_str)

# Write
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("index.html updated successfully")

# Verify
with open(index_path, 'r', encoding='utf-8') as f:
    verify = f.read()
count = verify.count('class="news-card"')
print(f"Article count after update: {count}")