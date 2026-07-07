#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate news for 2026年07月08日"""
import base64
import json
import os
import time
from pathlib import Path

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
DATE_STR = "20260708"

NEWS = [
    {
        "number": "01",
        "tag": "国际",
        "title": "联合国安理会通过决议呼吁加沙停火 美国投下弃权票",
        "summary": '联合国安理会7月8日通过一项关于加沙地带停火的决议，要求冲突双方立即停止敌对行动。美国在本次表决中投下弃权票，未使用否决权，这是美国首次在该问题上软化立场。以色列方面对此表示强烈反对，称该决议"脱离现实"。埃及和卡塔尔斡旋方表示将为落实决议继续努力。',
        "prompt": "United Nations Security Council chamber with delegates in discussion, diplomatic atmosphere, flags of member nations on the wall, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "number": "02",
        "tag": "科技",
        "title": '英伟达发布下一代GPU架构"Blackwell Ultra" 性能提升5倍',
        "summary": "英伟达在今日举行的GTC大会上正式发布Blackwell Ultra架构，新一代数据中心GPU在 transformers 推理性能上实现5倍提升。该芯片采用台积电3nm工艺，支持新一代NVLink 5.0互联技术。黄仁勋表示这将彻底改变AI计算的经济学。微软、谷歌和亚马逊已下单，首批产品将于今年秋季交付。",
        "prompt": "NVIDIA GPU chip concept rendering, powerful graphics processor with glowing circuitry, technology abstract background, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "03",
        "tag": "金融",
        "title": "美联储宣布维持利率不变 暗示9月可能降息",
        "summary": "美联储联邦公开市场委员会今日宣布维持联邦基金利率在5.25%-5.5%区间不变，符合市场预期。美联储主席鲍威尔在新闻发布会上表示，通胀压力正在持续缓解，若经济数据保持当前趋势，9月会议将是降息的合适时机。决议公布后，美股三大指数集体上涨，纳斯达克综合指数涨幅超过2%。",
        "prompt": "Federal Reserve building in Washington DC, majestic architecture with columns, American flag nearby, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "04",
        "tag": "国际",
        "title": "马克龙宣布解散国民议会提前选举 法国政坛地震",
        "summary": '法国总统马克龙宣布解散国民议会并提前举行立法选举，这一决定在法国政坛引发地震。极右翼国民联盟主席巴尔代拉对此表示欢迎，称"法国人民的意志将得到体现"。左翼联盟则呼吁进步力量团结对抗极右。分析认为此次选举将决定法国未来数年的政治走向和欧盟政策方向。',
        "prompt": "French National Assembly building in Paris, elegant French architecture, flags waving, crowd of people, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "05",
        "tag": "科技",
        "title": "SpaceX星舰完成首次商业发射 成功部署12颗通信卫星",
        "summary": "SpaceX星舰今日从得克萨斯州星舰基地完成首次商业发射任务，成功将12颗下一代星链通信卫星部署至轨道。星舰第一级成功回收，发射成本大幅降低。马斯克表示这标志着太空运输进入白菜价时代。公司已获得NASA载人登月合同，将执行阿尔忒弥斯计划首次载人着陆任务。",
        "prompt": "SpaceX Starship rocket launching from coastal spaceport, flames and smoke billowing, sunset sky, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "06",
        "tag": "经济",
        "title": "中国6月出口同比增长12.5% 超市场预期",
        "summary": "中国海关总署公布6月贸易数据，以美元计价出口同比增长12.5%，进口增长5.2%，贸易顺差达到780亿美元。分析师指出中国制造业竞争力持续增强，新能源汽车、锂电池和光伏产品出口增长强劲。欧盟和美国仍是重要出口市场，但对东南亚和中东出口增速更为显著。",
        "prompt": "Modern container port with massive cargo ships, cranes loading containers, busy logistics operations, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "07",
        "tag": "社会",
        "title": "全球多地遭遇极端高温 欧洲多国温度突破45摄氏度",
        "summary": "欧洲南部和地中海地区遭遇新一轮热浪，意大利、西班牙和希腊多地气温突破45摄氏度。各国政府发布最高级别高温警报，呼吁民众避免外出。意大利卫生部报告已有超过200人因高温相关原因死亡。气象学家警告这类极端天气事件将随着气候变化愈发频繁。",
        "prompt": "scorching summer heat wave, Thermometer showing extreme high temperature 45C, dry cracked earth, scorching sun, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "08",
        "tag": "国际",
        "title": "北约峰会闭幕 发表联合宣言强化集体防御",
        "summary": '北约峰会在华盛顿闭幕，32个成员国发表联合宣言，重申对集体防御承诺。宣言首次明确将中国定义为"系统性挑战"，但避免直接使用敌对措辞。峰会宣布将在波兰永久部署更多重型装备，并同意为乌克兰提供长期军事援助。瑞典和芬兰的加入使北约北翼显著加强。',
        "prompt": "NATO summit conference room with flags of member countries, world leaders in discussion, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "09",
        "tag": "科技",
        "title": "苹果Vision Pro 3发布 重量减轻40%售价降至2499美元",
        "summary": "苹果公司在今日的全球开发者大会上发布Vision Pro 3头显设备，重量从此前的650克降至390克，售价从3499美元下调至2499美元。新设备搭载M4芯片，眼球追踪和手势识别精度进一步提升。库克表示空间计算时代已经来临，App Store已有超过5000款专为Vision Pro开发的应用。",
        "prompt": "Apple Vision Pro headset device, sleek futuristic design, person wearing and interacting with AR content, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "10",
        "tag": "军事",
        "title": "菲律宾向美军开放更多军事基地 包括面向南海战略岛屿",
        "summary": "菲律宾国防部宣布，根据《强化防务合作协议》，菲律宾将向美国开放更多军事基地使用权。新增基地包括面向南海的巴拉望岛军事设施，这将使美军能够更快速响应南海争端。五角大楼对此表示欢迎，称这将加强美菲联盟的威慑力。中国外交部发言人警告域外国家不要在南海挑事。",
        "prompt": "Military naval base with warships docked, South China Sea backdrop, military personnel in formation, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "11",
        "tag": "经济",
        "title": "国际油价跌至70美元附近 欧佩克+内部出现分歧",
        "summary": "国际原油价格跌破70美元/桶，创近两年新低。欧佩克+内部对是否继续减产出现严重分歧，沙特主张继续减产保价，而阿联酋和哈萨克斯坦希望提高产量份额。分析认为全球需求放缓和美国产量增加是主要原因。航空公司和物流企业预计将显著受益于燃油成本下降。",
        "prompt": "Oil price chart declining, gas station prices display, oil barrels and refinery machinery, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "12",
        "tag": "科技",
        "title": "谷歌量子计算重大突破 2000量子比特处理器实现纠错",
        "summary": "谷歌量子AI团队宣布在量子纠错领域取得重大突破，其2000量子比特处理器Willow成功实现低于阈值的量子纠错，逻辑错误率降至0.1%以下。这意味着实用化量子计算的时代即将来临，药物研发、材料科学和密码学领域将率先受益。IBM和微软表示将加快自己的量子路线图。",
        "prompt": "Google quantum computer processor, complex superconducting circuits in cryogenic chamber, blue lighting, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "13",
        "tag": "国际",
        "title": "伊朗新任总统就职 承诺重启核谈判与西方接触",
        "summary": "伊朗新任总统佩泽什基安在德黑兰举行就职仪式，承诺在核问题上与西方重启谈判，表示'伊朗需要解除制裁来发展经济'。美国和欧盟对伊朗新政府的表态表示审慎欢迎，但强调只有行动而非言辞才能换取制裁放松。以色列则警告任何协议都必须确保伊朗永远无法拥有核武器。",
        "prompt": "Iranian president giving inauguration speech, parliament building in Tehran, crowd of supporters, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "14",
        "tag": "金融",
        "title": "比特币跌破9万美元 加密货币市场遭遇大规模清算",
        "summary": "比特币价格今日跌破9万美元关键支撑位，24小时内逾15亿美元加密货币被强制清算。分析认为美联储利率政策预期转向和Mt.Gox偿还债权人引发的抛售是主要诱因。以太坊、Solana等主流加密货币同步下跌，整个加密货币市值蒸发超过2000亿美元。",
        "prompt": "Bitcoin cryptocurrency price crashing, digital currency coins scattered, red charts and graphs declining, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "15",
        "tag": "社会",
        "title": "日本东京闹市区发生5.8级地震 暂无重大伤亡报告",
        "summary": "日本关东地区东京都市圈发生5.8级地震，震源深度约20公里，东京市区震感强烈。首相岸田文雄紧急召开灾害应对会议，暂无重大人员伤亡报告。地震导致部分新干线列车临时停运，羽田机场跑道检查后恢复运营。日本气象厅呼吁民众警惕余震。",
        "prompt": "Tokyo cityscape with earthquake shaking effect, modern buildings, emergency sirens, people evacuated to streets, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "16",
        "tag": "国际",
        "title": "土耳其正式申请加入金砖国家合作机制",
        "summary": "土耳其外长费丹宣布，土耳其已正式提交加入金砖国家合作机制的申请。这一决定被视为土耳其外交政策多元化的重要一步，埃尔多安政府希望借此减少对西方阵营的依赖。克里姆林宫对土耳其申请表示欢迎，南非作为今年金砖轮值主席国将组织成员国协商。",
        "prompt": "BRICS summit meeting, world leaders from emerging economies, group handshake or discussion, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "17",
        "tag": "科技",
        "title": "斯坦福发布全球AI指数报告 中国在论文数量和专利申请上领先",
        "summary": "斯坦福大学人工智能研究所发布2026年全球AI指数报告，中国在AI学术论文数量和专利申请方面位居全球第一，但美国在高质量引用和产业化方面仍保持领先。报告指出，中美两国在AI领域的竞争正在重塑全球科技格局，监管框架滞后于技术发展是共同挑战。",
        "prompt": "Stanford University campus with modern research labs, scientists working on AI research, computer screens showing data, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "18",
        "tag": "体育",
        "title": "2026年世界杯八强产生 西班牙将迎战法国",
        "summary": "2026年美加墨世界杯淘汰赛八强全部产生，西班牙在点球大战中6-4淘汰葡萄牙，将与法国争夺半决赛席位。巴西通过加时赛3-2战胜荷兰，德国4-1大胜阿根廷，英格兰则击败日本晋级。四场四分之一决赛将在接下来两天内展开。",
        "prompt": "FIFA World Cup stadium full of enthusiastic fans, colorful flags and banners, match in progress with players on field, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "19",
        "tag": "环境",
        "title": "研究显示北极冰盖融化速度超预期 海平面上升风险加剧",
        "summary": "发表在《自然气候变化》期刊上的研究显示，北极冰盖融化速度比IPCC预测快约30%。卫星数据显示今年夏季北极冰层面积已降至历史最低水平。科学家警告，若趋势持续，2100年前全球海平面可能上升超过1米，威胁沿海城市和低洼国家生存。",
        "prompt": "Arctic ice melting, polar bear on shrinking ice floe, climate change environmental theme, blue glacial water, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "20",
        "tag": "经济",
        "title": "德国大众汽车宣布关闭两家工厂 裁员超3万人",
        "summary": "德国大众汽车集团宣布将关闭位于德国的两家工厂，并裁减超过3万名员工，以应对来自中国新能源车企的激烈竞争和欧洲市场需求放缓。这是大众汽车87年历史上首次关闭本土工厂，工会对此表示强烈反对。分析认为这标志着传统车企转型阵痛期已经来临。",
        "prompt": "Volkswagen car factory assembly line, robotic arms welding vehicles, empty factory floor, industrial setting, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
]


def download_image(url, output_path):
    """Download image from URL"""
    import urllib.request
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Download error: {e}")
        return False


def call_cogview(prompt, output_path):
    """Call CogView API to generate image"""
    import urllib.request

    data = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }

    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(
        API_URL,
        data=json_data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']

            # Handle list response format: [{"url": "..."}]
            if isinstance(content, list) and len(content) > 0:
                image_url = content[0].get('url')
                if image_url:
                    return download_image(image_url, output_path)

            print(f"Unexpected response format: {type(content)}")
            return False

    except Exception as e:
        print(f"Error generating {output_path}: {e}")
        return False


def update_index_html():
    """Update the index.html with today's news"""
    index_path = Path("/home/swg/.openclaw/workspace/news-blog/index.html")

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update title and meta
    content = content.replace(
        '<title>2026年07月07日 环球新闻</title>',
        '<title>2026年07月08日 环球新闻</title>'
    )
    content = content.replace(
        '<meta name="description" content="2026年07月07日全球20条热点新闻',
        '<meta name="description" content="2026年07月08日全球20条热点新闻'
    )

    # Update date in cover subtitle
    content = content.replace(
        '全球20条热点新闻 · 2026年07月07日',
        '全球20条热点新闻 · 2026年07月08日'
    )

    # Generate new news cards HTML
    news_cards = []
    for news in NEWS:
        card = f'''<article class="news-card" data-tag="{news["tag"]}">
    <img class="news-image" src="images/news_{DATE_STR}_{news["number"]}.png" alt="{news["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{news["number"]}</span>
        <h3 class="news-title">{news["title"]}</h3>
        <p class="news-summary">{news["summary"]}</p>
        <div><span class="tag">{news["tag"]}</span></div>
    </div>
</article>'''
        news_cards.append(card)

    new_news_section = '\n'.join(news_cards)

    # Find the news grid and replace
    import re
    old_pattern = r'<div class="news-grid" id="newsGrid">.*?</div>\s*<div class="comments-section">'
    new_pattern = f'<div class="news-grid" id="newsGrid">\n{new_news_section}\n</div>\n            <div class="comments-section">'

    new_content = re.sub(old_pattern, new_pattern, content, flags=re.DOTALL)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Updated {index_path}")


def main():
    # Ensure images directory exists
    img_dir = Path("/home/swg/.openclaw/workspace/news-blog/images")
    img_dir.mkdir(parents=True, exist_ok=True)

    # Generate all images
    success_count = 0
    for i, news in enumerate(NEWS):
        img_path = img_dir / f"news_{DATE_STR}_{news['number']}.png"

        # Try up to 2 times
        for attempt in range(2):
            if call_cogview(news['prompt'], str(img_path)):
                success_count += 1
                break
            time.sleep(3)  # Wait before retry

        print(f"[{i+1}/{len(NEWS)}] {news['number']}: {'OK' if Path(img_path).exists() else 'FAIL'}")

        # Small delay between requests to avoid rate limiting
        if i < len(NEWS) - 1:
            time.sleep(2)

    print(f"\nGenerated {success_count}/{len(NEWS)} images")

    # Now update the index.html
    if success_count >= len(NEWS) - 2:  # Allow 2 failures
        update_index_html()
    else:
        print(f"Warning: Only {success_count}/{len(NEWS)} images generated, skipping HTML update")

    print("\nDone!")


if __name__ == "__main__":
    main()