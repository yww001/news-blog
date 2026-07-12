#!/usr/bin/env python3
"""Update index.html with new news for 2026年07月11日"""
from pathlib import Path

DATE_STR = "20260711"
DATE_DISPLAY = "2026年07月11日"

# Build news cards string
news_cards = '''            <div class="news-grid">
<article class="news-card" data-tag="军事">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_01.png" alt="中国罕见试射潜射洲际导弹 展示二次核打击能力" loading="lazy">
    <div class="news-content">
        <span class="news-number">01</span>
        <h3 class="news-title">中国罕见试射潜射洲际导弹 展示二次核打击能力</h3>
        <p class="news-summary">中国海军091型核潜艇在南海海域向太平洋发射了一枚巨浪-3型洲际弹道导弹，射程覆盖美国全境。五角大楼随即发表声明称正在评估此次试射。中国国防部回应称这是例行训练，不针对任何国家和目标。军事专家分析认为此举意在向域外势力展示可靠的海基核威慑能力。</p>
        <div><span class="tag">军事</span></div>
    </div>
</article>
<article class="news-card" data-tag="军事">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_02.png" alt="环太平洋军演美日联合反潜演习 针对中国潜艇威胁" loading="lazy">
    <div class="news-content">
        <span class="news-number">02</span>
        <h3 class="news-title">环太平洋军演美日联合反潜演习 针对中国潜艇威胁</h3>
        <p class="news-summary">2026年环太平洋军事演习在夏威夷海域拉开帷幕，美日两国首次进行联合反潜战演习，模拟追踪柴电潜艇。演习背景是近年来中国潜艇在第一岛链活动频繁。美国海军表示此次演习旨在提升联盟联合作战能力，维护海上航行自由。</p>
        <div><span class="tag">军事</span></div>
    </div>
</article>
<article class="news-card" data-tag="经济">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_03.png" alt="中国汽车出口单月首破百万辆 创历史新纪录" loading="lazy">
    <div class="news-content">
        <span class="news-number">03</span>
        <h3 class="news-title">中国汽车出口单月首破百万辆 创历史新纪录</h3>
        <p class="news-summary">中国汽车工业协会发布数据显示，6月中国汽车出口达103.7万辆，环比增长11.6%，同比增长75.1%，首次实现单月突破百万辆大关。新能源汽车占出口总量近四成，成为出口增长新引擎。比亚迪、奇瑞等车企在欧洲和东南亚市场份额持续攀升。</p>
        <div><span class="tag">经济</span></div>
    </div>
</article>
<article class="news-card" data-tag="国际">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_04.png" alt="纳米比亚总统访华 中非合作论坛再添新成果" loading="lazy">
    <div class="news-content">
        <span class="news-number">04</span>
        <h3 class="news-title">纳米比亚总统访华 中非合作论坛再添新成果</h3>
        <p class="news-summary">纳米比亚总统内通博·南迪-恩代特瓦于7月5日至11日对华进行国事访问，国家主席习近平在人民大会堂举行欢迎仪式。两国签署能源、基础设施、数字经济等领域合作协议，涉及金额超过50亿美元。此访正值中非合作论坛成立26周年，双边关系迈上新台阶。</p>
        <div><span class="tag">国际</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_05.png" alt="豆包千问宣布关停智能体 美团开源万亿参数大模型" loading="lazy">
    <div class="news-content">
        <span class="news-number">05</span>
        <h3 class="news-title">豆包千问宣布关停智能体 美团开源万亿参数大模型</h3>
        <p class="news-summary">字节跳动旗下豆包千问团队突然宣布将于7月15日关停所有智能体产品，业界哗然。同日，美团宣布开源其万亿参数大模型Sonic，内测性能在MMLU榜单上超越GPT-4o。分析师指出国内AI厂商正在经历新一轮洗牌，大模型竞争进入差异化阶段。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="国际">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_06.png" alt="荷兰外贸大臣访华 试图解决安世半导体出口管制争端" loading="lazy">
    <div class="news-content">
        <span class="news-number">06</span>
        <h3 class="news-title">荷兰外贸大臣访华 试图解决安世半导体出口管制争端</h3>
        <p class="news-summary">荷兰外贸与发展合作大臣舍尔茨玛率商业代表团访问北京和上海，17家荷兰企业随行。此访旨在游说中国放松对荷兰企业的报复性限制，并希望美国政府放宽芯片设备出口管制限制。荷兰ASML公司表示希望维护中国客户利益，但受制于美国实体清单管制。</p>
        <div><span class="tag">国际</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_07.png" alt="DeepMind经典研究获ICML 2026大奖 AlphaFold再获突破" loading="lazy">
    <div class="news-content">
        <span class="news-number">07</span>
        <h3 class="news-title">DeepMind经典研究获ICML 2026大奖 AlphaFold再获突破</h3>
        <p class="news-summary">谷歌DeepMind团队在国际机器学习大会上斩获最佳论文奖，其最新版本的AlphaFold 3能够预测蛋白质与其他生物分子复合物的三维结构。中国学者在此次大会获奖数量创下新高，北京大学团队提出的新架构引业界关注。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="金融">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_08.png" alt="美联储降息预期升温 全球股市迎来反弹行情" loading="lazy">
    <div class="news-content">
        <span class="news-number">08</span>
        <h3 class="news-title">美联储降息预期升温 全球股市迎来反弹行情</h3>
        <p class="news-summary">美国6月CPI数据低于预期，美联储主席暗示可能在9月启动降息。全球风险资产应声上涨，纳斯达克指数单周上涨4.2%，比特币重返10万美元上方。欧洲央行率先降息25个基点，日本央行维持负利率政策不变。</p>
        <div><span class="tag">金融</span></div>
    </div>
</article>
<article class="news-card" data-tag="国际">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_09.png" alt="英国新财相公布经济刺激计划 减税200亿英镑提振增长" loading="lazy">
    <div class="news-content">
        <span class="news-number">09</span>
        <h3 class="news-title">英国新财相公布经济刺激计划 减税200亿英镑提振增长</h3>
        <p class="news-summary">英国新任财政大臣在议会发表首个预算演讲，宣布减税200亿英镑并增加NHS医疗支出300亿英镑。预算案包括降低个人所得税起征点、提高资本利得税豁免门槛等措施。保守党议员对减税力度仍不满意，工党则批评预算案加剧财政赤字。</p>
        <div><span class="tag">国际</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_10.png" alt="欧盟AI法案正式生效 违规企业最高罚款35亿欧元" loading="lazy">
    <div class="news-content">
        <span class="news-number">10</span>
        <h3 class="news-title">欧盟AI法案正式生效 违规企业最高罚款35亿欧元</h3>
        <p class="news-summary">欧盟人工智能法案正式在全体成员国生效，成为全球首个全面监管AI的立法。法案对高风险AI系统实施严格准入制度，聊天机器人须明确披露身份，违者最高罚款全球营业额的7%。谷歌、微软等科技巨头已成立合规团队应对审查。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="环境">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_11.png" alt="欧洲热浪破纪录 西班牙多地气温超45摄氏度" loading="lazy">
    <div class="news-content">
        <span class="news-number">11</span>
        <h3 class="news-title">欧洲热浪破纪录 西班牙多地气温超45摄氏度</h3>
        <p class="news-summary">欧洲南部遭遇罕见高温热浪，西班牙安达卢西亚地区最高气温达47.2度，创下7月历史极值。意大利、希腊、葡萄牙多地气温超过43度，造成至少200人死亡。欧洲多家医院启动紧急预案，多国发出最高级别红色预警。科学家呼吁加速能源转型应对极端气候常态化。</p>
        <div><span class="tag">环境</span></div>
    </div>
</article>
<article class="news-card" data-tag="社会">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_12.png" alt="台风美莎克袭击华南 广西水库决堤万人转移" loading="lazy">
    <div class="news-content">
        <span class="news-number">12</span>
        <h3 class="news-title">台风美莎克袭击华南 广西水库决堤万人转移</h3>
        <p class="news-summary">今年第四号台风美莎克在广东沿海登陆，最大风力达14级。广西横州两座小型水库在暴雨中决堤，下游村庄紧急转移民众超过一万人。广东、福建启动防台风一级应急响应，南部战区出动官兵两万人待命。国家防总要求确保人民群众生命安全。</p>
        <div><span class="tag">社会</span></div>
    </div>
</article>
<article class="news-card" data-tag="体育">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_13.png" alt="2026年世界杯参赛名单全部确定 48强激战亚北美" loading="lazy">
    <div class="news-content">
        <span class="news-number">13</span>
        <h3 class="news-title">2026年世界杯参赛名单全部确定 48强激战亚北美</h3>
        <p class="news-summary">世界杯预选赛附加赛尘埃落定，2026年世界杯48支参赛球队全部产生。这是赛事首次由三国联合举办，美国、加拿大、墨西哥将承办全部104场比赛。中国男足在亚洲区预选赛中表现不佳，再次无缘世界杯决赛圈。揭幕战将于明年6月11日在纽约巨人体育场打响。</p>
        <div><span class="tag">体育</span></div>
    </div>
</article>
<article class="news-card" data-tag="文化">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_14.png" alt="三星堆遗址考古新发现 祭祀场所改写古蜀历史" loading="lazy">
    <div class="news-content">
        <span class="news-number">14</span>
        <h3 class="news-title">三星堆遗址考古新发现 祭祀场所改写古蜀历史</h3>
        <p class="news-summary">四川省文物考古研究院宣布，在三星堆遗址北部新发掘区发现距今约3200年的大型祭祀场所，出土青铜器、玉器和象牙器物超过三千件。新发现证明古蜀文明与中原夏商文明存在密切交流，青铜神树最新修复工作也取得重要进展。</p>
        <div><span class="tag">文化</span></div>
    </div>
</article>
<article class="news-card" data-tag="金融">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_15.png" alt="比特币跌破10万美元心理关口 加密市场全线回调" loading="lazy">
    <div class="news-content">
        <span class="news-number">15</span>
        <h3 class="news-title">比特币跌破10万美元心理关口 加密市场全线回调</h3>
        <p class="news-summary">比特币价格日内跌破10万美元整数关口，为近三个月来首次。加密货币市场总市值蒸发超过2000亿美元，以太坊、狗狗币等主流币种普遍跌幅超过15%。分析师认为这是牛市中的正常回调，机构投资者逢低买入推动价格企稳。</p>
        <div><span class="tag">金融</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_16.png" alt="三星发布Galaxy Z Fold6 折叠屏手机市场激战升级" loading="lazy">
    <div class="news-content">
        <span class="news-number">16</span>
        <h3 class="news-title">三星发布Galaxy Z Fold6 折叠屏手机市场激战升级</h3>
        <p class="news-summary">三星在法国巴黎发布Galaxy Z Fold6折叠屏旗舰，售价12999元起，搭载自研Exynos 2500芯片和全新Galaxy AI助手。苹果折叠屏iPhone据传将在秋季发布，折叠屏手机市场竞争进入白热化阶段。三星还同步推出智能眼镜Galaxy Ring，进军可穿戴AI设备市场。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="国际">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_17.png" alt="俄乌和平谈判重启 土耳其担任调解人" loading="lazy">
    <div class="news-content">
        <span class="news-number">17</span>
        <h3 class="news-title">俄乌和平谈判重启 土耳其担任调解人</h3>
        <p class="news-summary">在土耳其总统埃尔多安斡旋下，俄罗斯与乌克兰代表在伊斯坦布尔举行新一轮和平谈判。双方就停火框架达成初步共识，但领土边界等核心议题仍存在分歧。联合国秘书长呼吁双方保持克制，美国和欧盟对谈判表示谨慎欢迎。</p>
        <div><span class="tag">国际</span></div>
    </div>
</article>
<article class="news-card" data-tag="社会">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_18.png" alt="中国人口负增长持续 15省养老金统筹上调" loading="lazy">
    <div class="news-content">
        <span class="news-number">18</span>
        <h3 class="news-title">中国人口负增长持续 15省养老金统筹上调</h3>
        <p class="news-summary">国家统计局数据显示，2026年上半年出生人口同比下降8%，人口负增长趋势延续。人社部宣布调整全国养老金统筹方案，15个省份养老金上调3%，惠及超过1.3亿退休人员。专家呼吁加快建立多层次养老保障体系应对老龄化挑战。</p>
        <div><span class="tag">社会</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_19.png" alt="SpaceX星舰完成第100次发射 商业航天成本大幅下降" loading="lazy">
    <div class="news-content">
        <span class="news-number">19</span>
        <h3 class="news-title">SpaceX星舰完成第100次发射 商业航天成本大幅下降</h3>
        <p class="news-summary">SpaceX星舰完成第100次轨道级发射任务，将32颗星链卫星送入轨道。马斯克宣布星舰发射成本已降至每次1500万美元，较最初计划降低60%。SpaceX已占据全球商业航天发射市场85%以上份额，多国政府和企业寻求与其合作。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="经济">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_20.png" alt="OPEC+意外宣布深化减产 国际油价单周暴涨12%" loading="lazy">
    <div class="news-content">
        <span class="news-number">20</span>
        <h3 class="news-title">OPEC+意外宣布深化减产 国际油价单周暴涨12%</h3>
        <p class="news-summary">石油输出国组织OPEC+在维也纳召开紧急会议，宣布将每日原油产量再削减100万桶，持续至2027年底。沙特能源大臣表示此举旨在稳定全球石油市场供需平衡。美国对此表示反对，称将进一步施压OPEC+放松管制。受此影响，布伦特原油价格单周暴涨12%至每桶98美元。</p>
        <div><span class="tag">经济</span></div>
    </div>
</article>
            </div>'''

# Read current index.html
index_path = Path('/home/swg/.openclaw/workspace/news-blog/index.html')
content = index_path.read_text(encoding='utf-8')

# Replace date in title
content = content.replace(
    '<title>2026年07月10日 环球新闻</title>',
    '<title>2026年07月11日 环球新闻</title>'
)

# Replace date in meta description
content = content.replace(
    '2026年07月10日全球20条热点新闻',
    '2026年07月11日全球20条热点新闻'
)

# Replace date in cover subtitle
content = content.replace(
    '全球20条热点新闻 · 2026年07月10日',
    '全球20条热点新闻 · 2026年07月11日'
)

# Find and replace news grid section
old_grid_start = '<div class="news-grid">'
old_grid_end = '</div>\n            <div class="comments-section">'

start_idx = content.find(old_grid_start)
end_idx = content.find(old_grid_end)

if start_idx != -1 and end_idx != -1:
    # Replace content from <div class="news-grid"> to end of </div> before comments
    content = content[:start_idx] + news_cards + '\n            <div class="comments-section">' + content[end_idx + len(old_grid_end):]

# Write updated content
index_path.write_text(content, encoding='utf-8')
card_count = content.count('<article class="news-card"')
print('index.html updated successfully for', DATE_DISPLAY)
print('Updated', card_count, 'news cards')