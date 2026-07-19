#!/usr/bin/env python3
"""Generate news and images for 2026年07月20日"""
import base64
import json
import os
import re
import time
import requests

DATE = "2026年07月20日"
DATE_STR = "20260720"

WORK_DIR = "/home/swg/.openclaw/workspace/news-blog"
IMAGES_DIR = os.path.join(WORK_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

NEWS = [
    {"number": "01", "title": "西班牙加时2-1力克阿根廷 队史首夺世界杯冠军", "summary": "2026年美加墨世界杯决赛在纽约新泽西大都会人寿体育场落幕，西班牙通过加时赛2-1战胜阿根廷，队史首次捧起大力神杯。开场第8分钟莫拉塔首开纪录，下半场梅西点球扳平，加时赛第108分钟奥亚萨瓦尔头球绝杀。西班牙以7战全胜战绩夺冠，成为世界杯历史上首支全胜夺冠的球队。全球超过10亿观众收看了这场巅峰对决。", "tag": "体育", "image_prompt": "A dramatic football stadium scene at night, New York MetLife Stadium filled with 80000 spectators, Spanish flag celebration, golden trophy on pitch, dramatic floodlights, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "02", "title": "2026世界人工智能大会在上海闭幕 达成多项合作协议", "summary": "为期4天的2026世界人工智能大会暨人工智能全球治理高级别会议在上海闭幕。本届大会以共促开放、共享发展为主题，吸引了来自全球60多个国家和地区的超过8000家企业参展。大会期间签署合作协议超过200项，总金额突破500亿元人民币。国家主席习近平出席闭幕式并发表重要讲话。", "tag": "科技", "image_prompt": "Modern AI conference exhibition hall in Shanghai, large LED screens displaying AI technology, humanoid robots on display, international visitors, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "03", "title": "特斯拉Optimus Gen-3机器人量产版正式交付 售价2万美元", "summary": "特斯拉在上海超级工厂举行Optimus Gen-3机器人量产版交付仪式，首批交付1000台。马斯克通过视频连线表示，这是人类历史上首次大规模量产人形机器人。该机器人身高1.73米，体重56公斤，可连续工作8小时，能完成家庭服务、工业制造等多种任务。订单已超过50万台，交付周期预计排至2028年。", "tag": "科技", "image_prompt": "Humanoid robot in modern factory setting, sleek white design, Tesla logo visible, robotic arms working on assembly line, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "04", "title": "人民币汇率升破7.0关口 创三年新高", "summary": "在岸人民币对美元汇率盘中升破7.0重要心理关口，创下2023年以来的最高水平。外汇交易中心数据显示，人民币对美元中间价较前一日上调428个基点。分析认为，美联储降息预期升温、美元指数持续走弱以及外资加速流入人民币资产是主要推动因素。央行表示人民币汇率具有稳定基础，将继续双向波动。", "tag": "金融", "image_prompt": "Chinese yuan and US dollar banknotes, financial charts showing upward trend, modern banking district background, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "05", "title": "欧盟委员会主席冯德莱恩访华 中欧达成多项共识", "summary": "欧盟委员会主席冯德莱恩对中国进行正式访问，国家主席习近平在北京钓鱼台国宾馆会见她。双方就中欧经贸合作、人工智能治理、气候变化等议题深入交换意见，达成包括启动数字贸易协定谈判、深化绿色能源合作在内的一系列共识。这是冯德莱恩任内第三次访华，被视为中欧关系回暖的重要信号。", "tag": "国际", "image_prompt": "European Union and China flags side by side, formal diplomatic meeting in Beijing garden setting, businessmen shaking hands, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "06", "title": "中国上半年GDP同比增长5.2% 经济运行稳中有进", "summary": "国家统计局发布2026年上半年经济数据，上半年国内生产总值同比增长5.2%，其中二季度增长5.0%。高技术制造业投资增长15.8%，新能源汽车、锂电池和光伏产品出口增长强劲。统计局表示，下半年将加大宏观政策调节力度，推动经济持续回升向好，实现全年5%左右的发展目标。", "tag": "经济", "image_prompt": "Modern Chinese city skyline with cranes, construction activity, economic growth charts overlay, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "07", "title": "全球首个人形机器人格斗联赛总决赛在深圳落幕", "summary": "众擎URKL全球人形机器人自由格斗联赛总决赛在深圳市体育馆落幕，中国战队赤霄击败日本战队钢拳夺得冠军。决赛中两台人形机器人在3分钟内完成拳击、闪避和综合格斗动作对决，吸引全球超过5000万观众在线观看。赛事主办方宣布，明年将在全球10个城市举办巡回赛。", "tag": "科技", "image_prompt": "Humanoid robot fighting in arena, dramatic lighting, cheering crowd in background, Shenzhen arena, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "08", "title": "比特币重返10万美元上方 加密市场全面回暖", "summary": "比特币价格重返10万美元关口，24小时涨幅超过8%，加密货币总市值回升至3.5万亿美元。分析师认为机构投资者逢低买入、比特币现货ETF持续净流入是主要推动力。以太坊、Solana等主流加密货币同步上涨，市场恐慌指数降至45，显示投资者情绪明显改善。", "tag": "金融", "image_prompt": "Bitcoin coin on glowing background, cryptocurrency charts showing recovery, digital gold concept, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "09", "title": "三星堆遗址新出土文物超过8000件 青铜神树完整拼接", "summary": "四川省文物考古研究院公布三星堆遗址最新考古进展，2025年至今新出土文物总数超过8000件，其中国宝级文物47件。考古队成功完成青铜神树的拼接修复工作，这棵高达3.95米的神树是目前已知最大的商代青铜器。国家文物局表示，新发现为研究古蜀文明提供了突破性证据。", "tag": "文化", "image_prompt": "Ancient bronze tree artifact in museum, golden lighting, Sanxingdui archaeological site workers, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "10", "title": "日本福岛核污水排放满三周年 渔业抗议持续", "summary": "日本福岛第一核电站核污水排放进入第三年，累计排放量已超过8万吨。中国、韩国等周边国家抗议声浪持续，韩国渔民在首尔举行大规模示威。日本政府表示排放水已通过国际原子能机构认证，但中韩等国仍维持停止进口日本水产品的措施。日本渔业经济损失估计超过2000亿日元。", "tag": "国际", "image_prompt": "Fukushima nuclear power plant coastline, fishing boats protest at sea, anti-nuclear demonstration signs, dramatic sky, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "11", "title": "华为发布鸿蒙PC操作系统 打破Windows垄断格局", "summary": "华为在深圳发布鸿蒙PC版操作系统，正式进军桌面计算领域。余承东表示，鸿蒙PC系统支持x86和ARM双架构，可运行Windows和安卓应用。首批搭载该系统的电脑将于8月上市，起售价3999元。分析师认为，这可能打破国内PC市场Windows近乎垄断的局面，对微软形成直接挑战。", "tag": "科技", "image_prompt": "Huawei laptop computer with HarmonyOS interface, modern office environment, Chinese tech company branding, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "12", "title": "华北黄淮强降雨持续 北京发布防汛二级响应", "summary": "受副热带高压影响，华北黄淮地区强降雨天气持续，北京、天津、河北等地降雨量已超过300毫米，达到特大暴雨级别。北京市防汛指挥部启动二级应急响应，城市副中心、新机场等重点项目工地已停工。气象部门预报本轮降雨将持续至22日，呼吁市民减少不必要出行，避开低洼地带。", "tag": "社会", "image_prompt": "Heavy rainfall flooding city streets, Beijing cityscape, emergency rescue vehicles, people with umbrellas, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "13", "title": "英国正式申请加入金砖国家机制 引发国际关注", "summary": "英国外交大臣在喀山举行的金砖国家外长会议上正式递交加入申请，成为首个申请加入金砖机制的七国集团成员。英国首相约翰逊表示，脱欧后英国需要重新定位全球伙伴关系，金砖国家代表新兴市场和发展中国家的崛起。英国加入问题将在今年10月金砖峰会上正式讨论。", "tag": "国际", "image_prompt": "London Big Ben and BRICS countries flags together, diplomatic meeting room, global politics concept, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "14", "title": "全国碳市场成交额突破2万亿元 绿电交易成新热点", "summary": "生态环境部公布数据，全国碳排放权交易市场累计成交额突破2万亿元人民币，成为全球覆盖温室气体排放量最大的碳市场。目前已有超过4500家企业纳入碳配额管理。同期，绿电交易规模同比增长180%，新能源企业通过绿电交易实现额外收益超过300亿元。", "tag": "经济", "image_prompt": "Wind turbines and solar panels in green field, carbon trading data visualization, stock market overlay, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "15", "title": "国产大飞机C939完成首飞 航程覆盖全球主要城市", "summary": "中国商飞自主研发的C939大型客机在陕西阎良成功首飞，该机型采用最新一代复合材料和LEAP发动机，航程达15000公里，可覆盖全球主要城市。首飞持续58分钟，各项参数正常。中国商飞表示，C939计划2028年取得适航证，2029年交付航空公司使用。", "tag": "科技", "image_prompt": "Chinese homemade passenger aircraft C939 taking off, blue sky with clouds, aviation technology, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "16", "title": "俄乌和平谈判取得实质进展 停火协议框架达成", "summary": "俄罗斯与乌克兰代表在维也纳举行的第四轮和平谈判取得重大突破，双方就停火协议框架达成原则性共识。土耳其总统埃尔多安与联合国秘书长特使联合主持会议，双方同意设立人道主义走廊并重启粮食出口通道。欧盟对此表示欢迎，称这是冲突爆发以来最重要的外交突破。", "tag": "国际", "image_prompt": "Peace negotiation table, Russian and Ukrainian flags, diplomats in suits, Vienna palace setting, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "17", "title": "沪深交易所发布减持新规 堵住融券绕道漏洞", "summary": "上海和深圳证券交易所联合发布《上市公司股东减持股份实施细则》修订版，明确禁止大股东通过融券绕道减持，堵住政策漏洞。新规要求扣除战略投资者承诺锁定部分后方可计算可减持数量。证监会表示，新规旨在维护中小投资者利益，促进市场健康发展，即日起施行。", "tag": "金融", "image_prompt": "Shanghai Stock Exchange trading floor, stock charts and graphs, securities regulatory building, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "18", "title": "中国科学家成功培育耐盐碱水稻新品系 亩产突破900公斤", "summary": "青岛海水稻研发中心宣布，中国科学家在新疆塔克拉玛干沙漠边缘的盐碱地上试种的耐盐碱水稻新品系海稻96获得重大突破，亩产达到912公斤，刷新盐碱地水稻种植世界纪录。海稻96可在pH 10以下的盐碱地生长，灌溉用水减少50%。按目前推广速度，2030年前可为中国新增2亿亩良田。", "tag": "社会", "image_prompt": "Rice paddies in desert oasis, Chinese scientists in white lab coats examining rice plants, Xinjiang landscape, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "19", "title": "印度月船4号传回首批月背数据 发现水冰资源", "summary": "印度空间研究组织公布，月船4号探测器已在月球背面成功开展科学探测，首批传回数据显示在南极永久阴影区发现了大量水冰资源。印度总理莫迪表示，这是印度探月工程的重大里程碑。科学家估计，这些水冰资源可供未来月球基地使用超过100年。中国嫦娥系列任务为印度月背软着陆提供了重要技术参考。", "tag": "科技", "image_prompt": "Moon surface with lunar rover, Indian flag planted, Earth visible in background, water ice discovery concept, photorealistic, ultra detailed, 8K, high resolution"},
    {"number": "20", "title": "《黑神话：悟空》DLC大闹天宫上线 首日销量破千万", "summary": "国产3A游戏《黑神话：悟空》首个DLC大闹天宫全球同步上线，上线首日销量突破1000万份，创下游戏史DLC首发销量新纪录。游戏科学CEO冯骥表示，DLC历时2年开发，包含完整的天宫地图、全新Boss战和延续剧情。Steam平台同时在线玩家峰值突破200万，多个海外媒体给出满分评价。", "tag": "文化", "image_prompt": "Chinese mythology game scene, Sun Wukong fighting heavenly soldiers, beautiful Chinese palace background, photorealistic, ultra detailed, 8K, high resolution"}
]

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
MODEL = "cogview-3-flash"

def generate_image(news_number, prompt, retry=0):
    if retry > 2:
        print(f"  [FAIL] Image {news_number} failed after 3 retries")
        return False
    try:
        print(f"  Generating image {news_number}...")
        payload = {"model": MODEL, "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]}
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        
        # CogView returns a URL in content array
        content = data["choices"][0]["message"]["content"]
        if isinstance(content, list) and len(content) > 0:
            image_url = content[0].get("url") or content[0]
        elif isinstance(content, str):
            image_url = content
        else:
            print(f"  [FAIL] Unexpected content format: {type(content)}")
            return False
        
        # Download image from URL
        img_resp = requests.get(image_url, timeout=60)
        img_resp.raise_for_status()
        
        output_path = os.path.join(IMAGES_DIR, f"news_{DATE_STR}_{news_number}.png")
        with open(output_path, "wb") as f:
            f.write(img_resp.content)
        print(f"  [OK] Saved {os.path.basename(output_path)} ({len(img_resp.content)} bytes)")
        return True
    except Exception as e:
        print(f"  [RETRY] Image {news_number}: {e}")
        time.sleep(3)
        return generate_image(news_number, prompt, retry + 1)

print(f"Generating news for {DATE}")
print("=" * 60)

# Generate all images
success_count = 0
for news in NEWS:
    if generate_image(news["number"], news["image_prompt"]):
        success_count += 1

print(f"\nImages generated: {success_count}/20")

if success_count == 0:
    print("ERROR: No images generated!")
    exit(1)

print("Now updating index.html...")

# Update index.html
index_path = os.path.join(WORK_DIR, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Update title and date
html = re.sub(r"<title>.*?环球新闻</title>", f"<title>{DATE} 环球新闻</title>", html)
html = re.sub(r'content="[^"]*全球\d+条热点新闻[^"]*"', f'content="{DATE}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态"', html)
html = re.sub(r"全球20条热点新闻 · \d{4}年\d{2}月\d{2}日", f"全球20条热点新闻 · {DATE}", html)

# Build news cards HTML
news_cards = ""
for news in NEWS:
    img_path = f"images/news_{DATE_STR}_{news['number']}.png"
    card = f'''<article class="news-card" data-tag="{news["tag"]}">
    <img class="news-image" src="{img_path}" alt="{news["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{news["number"]}</span>
        <h3 class="news-title">{news["title"]}</h3>
        <p class="news-summary">{news["summary"]}</p>
        <div><span class="tag">{news["tag"]}</span></div>
    </div>
</article>'''
    news_cards += card + "\n"

# Replace news grid
pattern = r'<div class="news-grid">.*?</div>\s*</div>\s*</div>'
replacement = f'<div class="news-grid">\n\n{news_cards}\n\n                </div>\n        </div>\n        </div>'
html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)
print("index.html updated!")

# Save news data
news_data_path = os.path.join(WORK_DIR, f"news_data_{DATE_STR}.json")
with open(news_data_path, "w", encoding="utf-8") as f:
    json.dump(NEWS, f, ensure_ascii=False, indent=2)
print(f"News data saved to {news_data_path}")

print("\n" + "=" * 60)
print("Done!")