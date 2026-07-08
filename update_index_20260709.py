#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update index.html for 2026年07月09日"""
import re
from pathlib import Path

WORKDIR = Path("/home/swg/.openclaw/workspace/news-blog")
DATE_STR = "20260709"
DATE_CN = "2026年07月09日"

NEWS = [
    {
        "number": "01", "tag": "国际",
        "title": "联合国停火决议进入第二天 加沙人道主义援助开始恢复",
        "summary": "联合国停火决议通过后的第二天，加沙地带人道主义援助通道正式重新开放。世界粮食计划署车队从埃及边境进入加沙，为当地平民运送食品、医疗物资和饮用水。联合国秘书长古特雷斯表示，'这是恢复和平的第一步'，但强调实现永久停火仍需各方共同努力。以色列军方表示将'配合人道主义停火'，但保留对恐怖袭击的自卫权。",
        "prompt": "United Nations aid convoy trucks, photorealistic, 8K"
    },
    {
        "number": "02", "tag": "科技",
        "title": "英伟达Blackwell Ultra全面量产 台积电产能紧张",
        "summary": "英伟达宣布Blackwell Ultra GPU已进入全面量产阶段，但台积电3nm工艺产能紧张导致供不应求。分析师预计新芯片缺货情况将持续至明年第一季度。黄仁勋在财报电话会上表示，AI算力需求'远远超出预期'，公司正在与代工厂密切合作扩产。英伟达股价在盘后交易中上涨超过5%。",
        "prompt": "NVIDIA AI datacenter, photorealistic, 8K"
    },
    {
        "number": "03", "tag": "金融",
        "title": "比特币重返10万美元上方 加密市场情绪回暖",
        "summary": "比特币价格今日重返10万美元关键心理位，加密货币市场整体情绪明显回暖。分析师认为美联储9月降息预期升温是本轮上涨的主要驱动力。机构资金持续流入比特币ETF，灰度等主要产品的净流入量创一个月新高。以太坊同步上涨突破3500美元。",
        "prompt": "Bitcoin cryptocurrency, photorealistic, 8K"
    },
    {
        "number": "04", "tag": "国际",
        "title": "法国国民议会选举首轮投票结束 极右翼领先",
        "summary": "法国国民议会选举首轮投票结束，极右翼国民联盟以34%的得票率领先所有政党。马克龙所在的复兴党仅获得21%选票，排名第三。执政联盟面临严重挫折，巴黎多地爆发抗议示威。左翼联盟人民阵线获得29%选票，位居第二。选举最终结果将于7月12日揭晓。",
        "prompt": "French voting booth, photorealistic, 8K"
    },
    {
        "number": "05", "tag": "科技",
        "title": "SpaceX星舰回收无人机船升级 可同时回收两枚助推器",
        "summary": "SpaceX宣布其最新型无人机船已升级完成，可以同时回收星舰的两枚助推器。这项技术突破将显著降低发射成本，预期可将星舰每次发射成本降至500万美元以下。马斯克表示这将是太空探索'完全可重复使用'的最后一环。SpaceX同时宣布获得日本JAXA的月球补给合同。",
        "prompt": "SpaceX drone ship, photorealistic, 8K"
    },
    {
        "number": "06", "tag": "经济",
        "title": "中国上半年GDP同比增长5.8% 高质量发展成效显现",
        "summary": "国家统计局公布上半年经济数据，GDP同比增长5.8%，增速比一季度加快0.2个百分点。高技术制造业投资增长12.5%，新能源汽车、锂电池和光伏产品出口增长强劲。消费对经济增长的贡献率超过60%。经济学家预计全年有望实现5.5%左右的增长目标。",
        "prompt": "Modern Chinese city skyline, photorealistic, 8K"
    },
    {
        "number": "07", "tag": "社会",
        "title": "欧洲热浪持续 意大利消防员扑灭多起山林大火",
        "summary": "欧洲南部热浪进入第三周，意大利南部多地发生山林大火，消防部门出动超过2000名消防员参与灭火。希腊、土耳其和西班牙同样面临火灾风险，多国请求欧盟民防机制支援。欧洲多家医院报告因高温相关疾病就诊人数增加三倍。气象预报显示热浪可能持续至下周。",
        "prompt": "Wildfire in Mediterranean landscape, photorealistic, 8K"
    },
    {
        "number": "08", "tag": "国际",
        "title": "北约宣布向波兰增派万人部队 俄罗斯表示强烈反对",
        "summary": "北约在布鲁塞尔宣布将向波兰永久增派一万名士兵，强化北约东翼防御。美国将派遣4000人，德国2000人，英国和加拿大各1500人。这是冷战以来北约最大规模的军事部署调整。俄罗斯外交部发言人扎哈罗娃表示，北约'正在将欧洲推向战争边缘'，俄方将采取'对等回应措施'。",
        "prompt": "NATO military base, photorealistic, 8K"
    },
    {
        "number": "09", "tag": "科技",
        "title": "苹果Vision Pro 3首销日排队抢购 库克称供应充足",
        "summary": "苹果Vision Pro 3今日在全球Apple Store开启首销，多地出现排队抢购人潮。售价2499美元的新款头显供货充足，店内可直接购买无需预约。苹果CEO库克在东京表参道店接受采访时表示，'空间计算正在改变人们的工作和生活方式'。App Store下载量突破百万的应用已超过200款。",
        "prompt": "Apple Store Vision Pro, photorealistic, 8K"
    },
    {
        "number": "10", "tag": "军事",
        "title": "美菲在南海举行联合军演 中国舰队全程跟踪监视",
        "summary": "美国和菲律宾在南海海域启动代号'肩并肩'的年度联合军事演习，参演兵力超过1.5万人，创历史新高。演习内容包括反舰导弹实弹射击和两栖登陆演练。中国南部战区派舰艇全程跟踪监视，并在演习区域进行例行战备巡逻。中国外交部敦促域外国家不要在南海'挑事生非'。",
        "prompt": "US Philippines military exercise, photorealistic, 8K"
    },
    {
        "number": "11", "tag": "经济",
        "title": "欧佩克+达成新减产协议 沙特额外自愿减产100万桶",
        "summary": "欧佩克+视频会议达成新减产协议，沙特承诺额外自愿减产100万桶/日，以提振低迷的国际油价。协议有效期至2027年6月。俄罗斯同意限制石油出口，但保留根据市场情况调整的权利。国际油价应声上涨3%，布伦特原油重回75美元上方。航空股和能源股普遍上涨。",
        "prompt": "Global energy industry meeting, photorealistic, 8K"
    },
    {
        "number": "12", "tag": "科技",
        "title": "谷歌Willow量子处理器开始云服务 开放商业试用",
        "summary": "谷歌宣布其2000量子比特Willow处理器正式开放云服务试用，首批合作客户包括辉瑞、IBM和多家金融机构。企业可以通过谷歌云平台远程调用量子算力，用于药物分子模拟、金融风险计算和密码学研究。谷歌同时宣布将在加州建造世界最大的量子计算数据中心。",
        "prompt": "Google quantum computer, photorealistic, 8K"
    },
    {
        "number": "13", "tag": "国际",
        "title": "伊朗核谈判重启 维也纳举行首轮会谈",
        "summary": "伊朗与伊核问题六国在维也纳举行恢复履约谈判以来的首次面对面会谈。伊朗代表团表示愿意讨论'所有悬而未决的问题'，但坚持要求解除所有制裁。美国谈判代表表示对话'具有建设性'，但拒绝对结果做出预测。欧盟外交与安全政策高级代表主持本轮会谈。",
        "prompt": "Vienna conference hall diplomats, photorealistic, 8K"
    },
    {
        "number": "14", "tag": "金融",
        "title": "美联储褐皮书发布 美国经济温和增长但通胀担忧犹存",
        "summary": "美联储最新褐皮书显示，美国经济整体保持温和增长态势，12个地区中有9个报告经济活动小幅扩张。消费支出保持韧性，劳动力市场供需趋于平衡。但企业报告工资和价格粘性依然较强，通胀压力未见明显缓解。分析师预计9月降息25个基点的概率超过70%。",
        "prompt": "Federal Reserve building, photorealistic, 8K"
    },
    {
        "number": "15", "tag": "社会",
        "title": "日本石川县发生5.3级余震 核电站设施正常运转",
        "summary": "日本石川县能登地区发生5.3级余震，震源深度约10公里，震感遍及北陆地区多条新干线一度降速运行。气象厅表示这是7月5日7.1级强震的正常余震序列，呼吁民众警惕山体滑坡风险。东京电力公司确认区域内核电站辐射监测数值无异常。",
        "prompt": "Japan earthquake aftermath, photorealistic, 8K"
    },
    {
        "number": "16", "tag": "国际",
        "title": "金砖国家扩员谈判完成 沙特伊朗埃塞加入程序启动",
        "summary": "金砖国家合作机制扩员谈判在南非约翰内斯堡完成，沙特阿拉伯、伊朗和埃塞俄比亚的加入程序正式启动。克里姆林宫表示欢迎更多发展中国家参与合作。美国和欧盟对金砖机制扩员表示密切关注。中国外交部赞赏南南合作的新台阶。",
        "prompt": "BRICS summit meeting, photorealistic, 8K"
    },
    {
        "number": "17", "tag": "科技",
        "title": "斯坦福AI报告引争议 中国AI论文数量超美国引质疑",
        "summary": "斯坦福AI指数报告因将中国列为AI论文数量和专利申请第一大国而引发学术界争议。多位美国学者指出，中国统计口径过于宽泛，且论文质量仍落后于美国。报告显示，中国在图像识别和自动驾驶专利方面领先，美国在基础大模型和芯片设计领域保持优势。中美AI竞争格局日益复杂。",
        "prompt": "University research laboratory AI, photorealistic, 8K"
    },
    {
        "number": "18", "tag": "体育",
        "title": "世界杯1/4决赛开打 西班牙4比2淘汰法国晋级四强",
        "summary": "2026年世界杯四分之一决赛在洛杉矶展开争夺，西班牙以4比2战胜法国，晋级半决赛。法国队上半场2比1领先，但西班牙下半场连入三球完成逆转。19岁小将加维上演帽子戏法，当选全场最佳。另一场四分之一决赛中，德国通过点球大战6比5淘汰英格兰。半决赛西班牙将战德国。",
        "prompt": "World Cup football match, photorealistic, 8K"
    },
    {
        "number": "19", "tag": "环境",
        "title": "研究警告北极冰盖或在2035年夏季完全消融",
        "summary": "发表在科学杂志上的最新研究发出严厉警告，北极冰盖可能在2035年夏季出现首次完全消融，比此前预测提前15年。研究基于过去十年卫星数据和海洋温度变化趋势，警告海平面上升风险将显著加速。格陵兰岛冰盖流失速度已是上世纪末的三倍，多国政府被呼吁紧急制定应对方案。",
        "prompt": "Arctic ice sheet melting, photorealistic, 8K"
    },
    {
        "number": "20", "tag": "经济",
        "title": "大众德国工厂关闭进入第二天 工会威胁无限期罢工",
        "summary": "大众汽车关闭两家德国工厂和裁员3万人的计划进入第二天，工会IG Metall威胁发动无限期罢工。工会在沃尔夫斯堡总部组织大规模示威，超过5万名工人参与。大众管理层表示转型不可避免，承诺为每位被裁员工提供再就业培训。目前双方谈判陷入僵局。",
        "prompt": "Volkswagen factory protest, photorealistic, 8K"
    },
]

def build_news_card(news):
    return f'''<article class="news-card" data-tag="{news["tag"]}">
    <img class="news-image" src="images/news_{DATE_STR}_{news["number"]}.png" alt="{news["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{news["number"]}</span>
        <h3 class="news-title">{news["title"]}</h3>
        <p class="news-summary">{news["summary"]}</p>
        <div><span class="tag">{news["tag"]}</span></div>
    </div>
</article>'''

# Read current index.html
index_file = WORKDIR / "index.html"
with open(index_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace title and meta description
content = re.sub(r'<title>.*?</title>', f'<title>{DATE_CN} 环球新闻</title>', content)
content = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{DATE_CN}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态"', content)

# Replace cover subtitle date
content = re.sub(r'全球20条热点新闻 · \d{4}年\d{1,2}月\d{1,2}日', f'全球20条热点新闻 · {DATE_CN}', content)

# Build all news cards
all_cards = "\n".join(build_news_card(n) for n in NEWS)

# Replace news grid section - find and replace everything between <div class="news-grid"> and </div>
news_grid_pattern = r'<div class="news-grid" id="newsGrid">.*?</div>\s*<div class="comments-section">'
replacement = f'<div class="news-grid" id="newsGrid">\n{all_cards}\n</div>\n            <div class="comments-section">'
content = re.sub(news_grid_pattern, replacement, content, flags=re.DOTALL)

# Write updated index.html
with open(index_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ index.html updated for {DATE_CN}")
print(f"✅ Updated {len(NEWS)} news cards")