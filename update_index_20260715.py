#!/usr/bin/env python3
"""Update index.html for 2026年07月15日"""

DATE_STR = "20260715"
DATE_DISPLAY = "2026年07月15日"

NEWS = [
    {
        "number": "01",
        "tag": "国际",
        "title": "二十国集团峰会印度开幕 聚焦全球经济治理改革",
        "summary": "二十国集团（G20）领导人峰会在印度新德里开幕，会议重点讨论全球经济治理体系改革、债务减免和气候融资等议题。中国国家主席习近平发表重要讲话，呼吁完善全球经济治理，构建开放型世界经济。峰会期间将签署多项基础设施合作协议，总金额超过500亿美元。",
        "image": f"images/news_{DATE_STR}_01.png"
    },
    {
        "number": "02",
        "tag": "科技",
        "title": "中国宣布新一代量子计算机原型 运算能力破世界纪录",
        "summary": "中国科学技术大学宣布成功研制105量子比特超导量子计算机原型，在特定任务上实现亿亿次运算能力，创下量子计算领域新的世界纪录。该成果将在密码分析、药物研发和人工智能等领域产生深远影响。科研团队表示将进一步提升量子比特数量和纠缠质量。",
        "image": f"images/news_{DATE_STR}_02.png"
    },
    {
        "number": "03",
        "tag": "金融",
        "title": "美联储宣布维持利率不变 暗示下半年降息可能",
        "summary": "美国联邦储备委员会宣布维持联邦基金利率在5.25%至5.5%不变，符合市场预期。美联储主席鲍威尔表示通胀率正在接近目标水平，若经济数据持续改善，下半年可能开始降息。市场分析师预计首次降息将在9月会议落地，美股三大指数应声上涨。",
        "image": f"images/news_{DATE_STR}_03.png"
    },
    {
        "number": "04",
        "tag": "经济",
        "title": "欧盟就中国电动汽车加征关税达成共识",
        "summary": "欧盟成员国就对中国电动汽车加征反补贴关税达成共识，计划从今年10月起对进口中国新能源汽车征收最高35%的额外关税。欧盟委员会表示此举旨在保护本土汽车产业，中方对此表示强烈不满，称将采取相应措施维护企业合法权益。",
        "image": f"images/news_{DATE_STR}_04.png"
    },
    {
        "number": "05",
        "tag": "国际",
        "title": "日本福岛核废水排海一年 渔业形象受损仍在持续",
        "summary": "日本福岛第一核电站核废水排海进入第二年，尽管东京电力公司强调处理水符合安全标准，但日本渔业形象受损仍在持续。中国、韩国等邻国继续限制日本水产品进口，日本渔业相关产业损失超过2000亿日元。",
        "image": f"images/news_{DATE_STR}_05.png"
    },
    {
        "number": "06",
        "tag": "科技",
        "title": "苹果发布iPhone 17系列 搭载自研AI芯片",
        "summary": "苹果公司发布iPhone 17系列旗舰手机，首次搭载自研Neural Engine AI芯片，AI处理能力提升3倍。新机型采用钛合金边框和固态电池技术，续航能力突破48小时。苹果同时推出升级版AirPods和Apple Watch，库克表示这是最强大的iPhone产品线。",
        "image": f"images/news_{DATE_STR}_06.png"
    },
    {
        "number": "07",
        "tag": "科技",
        "title": "全球最大双燃料动力货轮完成首航",
        "summary": "全球最大双燃料动力集装箱货轮在青岛港完成首航，该船采用液化天然气和甲醇双燃料系统，最大载货量达24000标箱。船舶设计融合多项节能减排技术，整体碳排放较传统货轮降低30%以上，为航运业绿色转型提供新方案。",
        "image": f"images/news_{DATE_STR}_07.png"
    },
    {
        "number": "08",
        "tag": "体育",
        "title": "巴黎奥运会倒计时一周年 场馆建设进入冲刺",
        "summary": "2026年巴黎夏季奥运会倒计时一周年，组委会公布奖牌设计和火炬传递路线。赛事组委会表示47个比赛场馆建设进入最后冲刺阶段，奥运村已交付使用。本届奥运会将首次实现全部场馆100%使用可再生能源供电。",
        "image": f"images/news_{DATE_STR}_08.png"
    },
    {
        "number": "09",
        "tag": "国际",
        "title": "乌克兰加入欧盟谈判正式启动",
        "summary": "乌克兰加入欧盟的正式谈判在卢森堡启动，首轮谈判涉及司法改革、反腐败措施和市场经济接轨等30个章节。欧盟委员会表示这是历史性时刻，但乌方仍需在法治和媒体自由等领域进行深度改革。俄罗斯对此表示强烈反对。",
        "image": f"images/news_{DATE_STR}_09.png"
    },
    {
        "number": "10",
        "tag": "科技",
        "title": "SpaceX星舰完成首次载人轨道飞行任务",
        "summary": "SpaceX星舰完成首次载人轨道飞行任务，4名私人宇航员在轨停留3天后安全返回地球。这次任务标志着商业载人航天进入新阶段，马斯克表示将在明年开始常规化商业运营，往返地球轨道的票价有望降至数百万美元。",
        "image": f"images/news_{DATE_STR}_10.png"
    },
    {
        "number": "11",
        "tag": "国际",
        "title": "德国总理朔尔茨访华 签署多项合作协议",
        "summary": "德国总理朔尔茨率团访问中国，与中国国务院总理李强举行会谈，双方签署涵盖新能源汽车、绿色化工和数字经济领域的12项合作协议。朔尔茨表示脱钩不是选项，德中经贸合作对双方都至关重要。",
        "image": f"images/news_{DATE_STR}_11.png"
    },
    {
        "number": "12",
        "tag": "金融",
        "title": "比特币价格突破10万美元 创历史新高",
        "summary": "比特币价格突破10万美元大关，创下历史新高，主要受美国比特币现货ETF获批和机构投资者加仓推动。加密货币总市值突破3.5万亿美元，以太坊等其他主流加密货币同步上涨。各国央行正加速研究央行数字货币应对挑战。",
        "image": f"images/news_{DATE_STR}_12.png"
    },
    {
        "number": "13",
        "tag": "科技",
        "title": "全球人工智能监管框架在联合国达成一致",
        "summary": "联合国大会通过首个全球人工智能治理框架，涵盖AI安全标准、数据隐私保护、算法透明度和武器化风险防范等核心议题。中美欧等主要经济体均表示支持，框架建立国际AI监管合作机制，但具体实施细节仍需进一步磋商。",
        "image": f"images/news_{DATE_STR}_13.png"
    },
    {
        "number": "14",
        "tag": "经济",
        "title": "中国上半年GDP增长5.5% 经济运行稳中有进",
        "summary": "国家统计局公布上半年经济数据，GDP同比增长5.5%，其中二季度增长5.3%。消费回升和出口改善带动经济持续恢复，高技术制造业和现代服务业增势良好。国务院表示将加大宏观政策调节力度，巩固经济回升向好态势。",
        "image": f"images/news_{DATE_STR}_14.png"
    },
    {
        "number": "15",
        "tag": "文化",
        "title": "埃及金字塔区新考古发现 出土保存完好的古王国时期墓葬",
        "summary": "埃及旅游和文物部宣布，在吉萨金字塔区附近发现一座保存完好的古王国时期高级官员墓葬，出土包括金箔面具、彩绘木棺和象形文字纸卷在内的200余件珍贵文物。这一发现将为研究古埃及社会结构提供重要考古依据。",
        "image": f"images/news_{DATE_STR}_15.png"
    },
    {
        "number": "16",
        "tag": "社会",
        "title": "亚马逊森林砍伐面积创15年新低",
        "summary": "巴西环境部公布数据，今年上半年亚马逊森林砍伐面积较去年同期下降42%，创下15年来最低水平。巴西总统卢拉表示雨林保护取得历史性进展，得益于卫星监测强化和环保执法力度加大。但环保组织提醒仍需持续努力。",
        "image": f"images/news_{DATE_STR}_16.png"
    },
    {
        "number": "17",
        "tag": "科技",
        "title": "美国火星采样返回任务进入关键测试阶段",
        "summary": "NASA宣布火星采样返回任务进入关键测试阶段，毅力号火星车已完成22管岩芯样本封装，准备交接给后续着陆器。任务计划于2033年将样本送回地球，科学家希望借此揭示火星是否存在古老生命痕迹。",
        "image": f"images/news_{DATE_STR}_17.png"
    },
    {
        "number": "18",
        "tag": "社会",
        "title": "联合国教科文组织将中医纳入全球医学纲要",
        "summary": "世界卫生组织下属联合国教科文组织宣布将中医正式纳入全球医学纲要，与现代医学并列。这意味着中医将在全球医疗体系中获得正式认可，各国将在中医标准制定、教育培训和药物监管方面加强国际合作。",
        "image": f"images/news_{DATE_STR}_18.png"
    },
    {
        "number": "19",
        "tag": "国际",
        "title": "印度成为全球人口第一大国 劳动力红利待释放",
        "summary": "印度人口规模正式超越中国成为全球第一，联合国预测到2050年印度人口将突破16亿。印度政府表示人口红利为经济发展提供重要机遇，但需加快教育改革、技能培训和就业岗位创造，以充分释放劳动力潜力。",
        "image": f"images/news_{DATE_STR}_19.png"
    },
    {
        "number": "20",
        "tag": "社会",
        "title": "全球珊瑚白化事件频发 大堡礁面临生存危机",
        "summary": "澳大利亚海洋学研究所发出警告，全球海域正经历有记录以来最严重的珊瑚白化事件，大堡礁健康区域已不足30%。海水温度上升导致珊瑚排斥共生藻类而白化死亡，科学家呼吁紧急减排并建立更多海洋保护区。",
        "image": f"images/news_{DATE_STR}_20.png"
    },
]


def gen_news_card(news: dict) -> str:
    return f'''<article class="news-card" data-tag="{news["tag"]}">
    <img class="news-image" src="{news["image"]}" alt="{news["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{news["number"]}</span>
        <h3 class="news-title">{news["title"]}</h3>
        <p class="news-summary">{news["summary"]}</p>
        <div><span class="tag">{news["tag"]}</span></div>
    </div>
</article>'''


def main():
    # Read the original index.html
    with open("/home/swg/.openclaw/workspace/news-blog/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace date in title
    content = content.replace(
        "<title>2026年07月14日 环球新闻</title>",
        f"<title>{DATE_DISPLAY} 环球新闻</title>"
    )
    
    # Replace meta description
    content = content.replace(
        '<meta name="description" content="2026年07月14日全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">',
        f'<meta name="description" content="{DATE_DISPLAY}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">'
    )
    
    # Replace cover subtitle
    content = content.replace(
        "<p class=\"cover-subtitle\">全球20条热点新闻 · 2026年07月14日</p>",
        f"<p class=\"cover-subtitle\">全球20条热点新闻 · {DATE_DISPLAY}</p>"
    )
    
    # Generate new news cards HTML
    new_news_cards = "\n".join(gen_news_card(news) for news in NEWS)
    
    # Find and replace the news grid section
    # The news grid starts after "</div>" of warning and ends before "</div>" of news-grid
    import re
    
    # Replace the entire news-grid div content
    pattern = r'<div class="news-grid">.*?</div>\s*<div class="comments-section">'
    replacement = f'<div class="news-grid">\n{new_news_cards}\n</div>\n            <div class="comments-section">'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write updated index.html
    with open("/home/swg/.openclaw/workspace/news-blog/index.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("index.html updated successfully!")


if __name__ == "__main__":
    main()