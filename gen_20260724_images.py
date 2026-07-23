#!/usr/bin/env python3
"""Generate news images for 2026年07月24日 using CogView-3-Flash API."""

import requests
import json
import os
import time

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

IMG_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
DATE_STR = "20260724"

NEWS = [
    {
        "num": "01",
        "title": "全球人工智能合作组织在上海正式成立",
        "summary": "世界人工智能合作组织成立仪式在上海举行，这是全球首个人工智能政府间国际组织。国务院副总理出席开幕式并致辞，来自50多个国家的代表参会。该组织旨在推动全球AI治理标准制定、技术共享和人才培养。",
        "tag": "科技",
        "prompt": "UN delegates gathering at an international AI conference in Shanghai, holographic world map display, solemn ceremony with flags of many nations, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "02",
        "title": "特朗普宣布对数十个国家加征新关税 引发全球贸易震荡",
        "summary": "美国总统特朗普宣布对欧盟、东南亚等数十个国家加征新一轮关税，税率最高达40%。此举引发全球金融市场震荡，道指期货下跌超过500点。欧盟表示将采取对等报复措施，全球贸易战阴云再起。",
        "tag": "国际",
        "prompt": "US White House press conference, president at podium announcing trade tariffs, international trade concept, stock market screens showing decline, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "03",
        "title": "中国成功发射神舟二十一号载人飞船",
        "summary": "中国在酒泉卫星发射中心成功发射神舟二十一号载人飞船，3名航天员将前往中国空间站执行任务。神舟二十一号将对接空间站核心舱，航天员将在轨驻留6个月，开展多项科学实验和技术测试。",
        "tag": "科技",
        "prompt": "Chinese rocket launching at night from desert launch pad, smoke trails illuminating sky, space mission control room with engineers celebrating, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "04",
        "title": "普华永道中国在上海成立人工智能研究院",
        "summary": "普华永道宣布在上海成立人工智能研究院，将全球AI领域的深厚积淀与中国本土业务优势深度融合。研究院将聚焦AI在金融、医疗、制造业等领域的应用创新，助力中国企业数字化转型。",
        "tag": "科技",
        "prompt": "Modern Shanghai skyline with Pudong skyscrapers, tech company headquarters interior with AI research laboratory, holographic data displays, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "05",
        "title": "中日韩领导人会议在首尔举行 达成多项合作协议",
        "summary": "第12次中日韩领导人会议在首尔举行，三国领导人就经贸、科技、环保等领域合作达成广泛共识。三国同意加快建设东亚区域全面经济伙伴关系，推动构建更加紧密的亚太命运共同体。",
        "tag": "国际",
        "prompt": "World leaders in suits shaking hands at formal summit meeting in Seoul, three-country flags in background, diplomatic conference hall, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "06",
        "title": "比特币价格突破12万美元 加密货币市场持续繁荣",
        "summary": "比特币价格突破12万美元大关，创历史新高。分析师认为，美国比特币ETF持续获批和机构投资者大量入场是主要推动力。加密货币总市值突破4.5万亿美元，以太坊等主流币种同步上涨。",
        "tag": "金融",
        "prompt": "Bitcoin cryptocurrency concept art, golden Bitcoin coin on digital background, cryptocurrency trading charts rising, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "07",
        "title": "上海成为全球首个万亿级消费城市",
        "summary": "上海市商务委宣布，2026年上半年上海社会消费品零售总额突破1万亿元，成为全球首个万亿级消费城市。首店经济、首发经济和夜经济发展迅猛，国际消费中心城市建设成效显著。",
        "tag": "社会",
        "prompt": "Aerial view of bustling Shanghai at night, neon lights, crowded shopping district Nanjing Road, luxury stores and restaurants, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "08",
        "title": "中国深度参与IAEA全球核能发展计划",
        "summary": "国际原子能机构宣布中国将深度参与其全球核能发展计划，中核集团与IAEA签署合作协议，中国将提供自主研发的第三代核电技术，支持发展中国家建设核电站。",
        "tag": "国际",
        "prompt": "Nuclear power plant with cooling towers at sunset, peaceful countryside background, clean energy concept, blue sky with white clouds, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "09",
        "title": "中国新能源汽车产量突破1200万辆",
        "summary": "中国汽车工业协会数据显示，2026年上半年新能源汽车产量达到1220万辆，同比增长42%。新能源汽车渗透率已达55%。比亚迪、理想汽车和蔚来位列销量前三，中国新能源车出口量继续保持全球第一。",
        "tag": "经济",
        "prompt": "Modern electric car factory assembly line in China, humanoid robots working alongside humans, electric vehicles being assembled, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "10",
        "title": "张艺谋执导《满江红2》票房突破60亿元",
        "summary": "导演张艺谋执导的古装大片《满江红2》票房正式突破60亿元，超越前作成，为中国影史第二卖座影片。影片由沈腾、易烊千玺主演，已在全球60多个国家上映。",
        "tag": "文化",
        "prompt": "Ancient Chinese palace courtyard with actors in Song dynasty costume, dramatic lighting with red lanterns, cinematic movie poster style, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "11",
        "title": "欧洲央行宣布降息25个基点 宽松周期启动",
        "summary": "欧洲央行宣布将主要利率下调25个基点，正式启动宽松周期。央行行长拉加德表示，通胀率已回落至2.1%的目标水平，经济增长需要更多支持。欧央行预计2026年欧元区经济增长1.4%。",
        "tag": "金融",
        "prompt": "European Central Bank headquarters in Frankfurt, euro currency coins and banknotes, financial district with euro flags, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "12",
        "title": "中国科学家实现量子计算重大突破",
        "summary": "中国科学技术大学宣布，在超导量子计算领域取得重大突破，成功实现100量子比特的稳定操控。量子计算速度比经典计算机快1亿倍，为密码破译和新药研发带来革命性变化。",
        "tag": "科技",
        "prompt": "Scientists in Chinese laboratory working with quantum computer, complex quantum circuit with glowing blue light, cryogenic cooling system, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "13",
        "title": "中国电动汽车在欧盟市场份额突破30%",
        "summary": "欧洲汽车协会数据显示，中国品牌电动汽车在欧盟市场份额已达31%，超越欧美传统车企。比亚迪、蔚来等品牌在欧洲多个国家销量位居前列，中国电动车性价比优势明显。",
        "tag": "经济",
        "prompt": "Electric vehicles charging at modern charging station in Europe, Chinese brand EVs lined up, green energy concept, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "14",
        "title": "特斯拉发布Optimus Gen4机器人 具备完整家务能力",
        "summary": "特斯拉在AI日活动中发布Optimus Gen4人形机器人，这是首款具备完整家庭服务能力的商用机器人。机器人身高170厘米，可完成打扫、烹饪、照顾老人等日常家务，售价约2.5万美元。",
        "tag": "科技",
        "prompt": "Humanoid robot serving food in modern kitchen, home environment, warm lighting, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "15",
        "title": "苹果发布iPhone 19系列 搭载自研AI神经引擎",
        "summary": "苹果发布iPhone 19 Pro系列，首次搭载自研A20 AI神经引擎芯片，专门为端侧AI优化，支持实时语音翻译和智能摄影。iPhone 19 Pro起售价1299美元，中国市场同步首发。",
        "tag": "科技",
        "prompt": "Apple Store grand opening with crowd, iPhone smartphones on display, sleek glass design, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "16",
        "title": "英伟达Blackwell Ultra GPU开始量产 AI算力提升200%",
        "summary": "英伟达宣布Blackwell Ultra GPU开始量产，相比前代产品AI算力提升200%。该芯片采用台积电3nm工艺，支持更高的内存带宽。谷歌、Meta和亚马逊已下单，芯片供不应求。",
        "tag": "科技",
        "prompt": "High-tech GPU chip close-up, blue electronic circuits, data center server room with glowing lights, AI computing concept, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "17",
        "title": "全球最大氢能游轮完成欧洲首航",
        "summary": "全球最大的氢燃料电池游轮在挪威完成欧洲首航，可搭载2000名乘客的游轮完全使用绿色氢能源，航行过程零排放。游轮设计航速22节，续航力达6000海里，氢能航运时代正式开启。",
        "tag": "社会",
        "prompt": "Huge cruise ship sailing in Norwegian fjords surrounded by mountains, clean blue water, zero emission, futuristic design, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "18",
        "title": "中国女排世界杯四连胜 晋级决赛",
        "summary": "2026年女排世界杯预选赛继续进行，中国女排在半决赛中以3-1战胜美国队，取得四连胜。队长朱婷砍下全场最高的30分，龚翔宇贡献18分。中国队以全胜战绩晋级决赛。",
        "tag": "体育",
        "prompt": "Chinese women's volleyball team celebrating victory on court, players jumping with joy holding trophy, championship atmosphere, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "19",
        "title": "全球极端高温天气持续 多国发布高温预警",
        "summary": "入夏以来，全球多国遭遇极端高温天气，北半球多个城市气温突破45°C。欧盟气象机构警告称，2026年可能成为有记录以来最热的年份之一，呼吁各国加强应对气候变化措施。",
        "tag": "社会",
        "prompt": "Extreme summer heatwave in city, temperature gauge showing high reading, dry cracked earth, people seeking shade, heat shimmer effect, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
    {
        "num": "20",
        "title": "全球最大规模海上风电场在福建全面投产",
        "summary": "位于福建海域的全球最大规模海上风电场全面建成投产，总装机容量达600万千瓦。该风电场采用最新抗台风技术，每年可发绿电240亿千瓦时，相当于减少碳排放1900万吨。",
        "tag": "科技",
        "prompt": "Massive offshore wind farm in the ocean with dozens of wind turbines spinning, coastal scenery, clear blue sea, clean energy, photorealistic, ultra detailed, 8K, high resolution, no text"
    },
]

def generate_image(item, retry=2):
    """Generate image using CogView-3-Flash API."""
    num = item["num"]
    prompt = item["prompt"]
    filename = f"{IMG_DIR}/news_{DATE_STR}_{num}.png"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    for attempt in range(retry):
        try:
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
            data = resp.json()
            
            if "choices" not in data:
                print(f"  No choices: {str(data)[:200]}")
                time.sleep(5)
                continue
            
            content = data["choices"][0]["message"]["content"]
            # content is a list like [{"url": "..."}]
            url_list = content if isinstance(content, list) else json.loads(content)
            url = url_list[0]["url"]
            
            # Download image
            img_resp = requests.get(url, timeout=60)
            with open(filename, "wb") as f:
                f.write(img_resp.content)
            
            print(f"  ✓ {num}: saved ({len(img_resp.content)} bytes)")
            return True
            
        except Exception as e:
            print(f"  ✗ {num} attempt {attempt+1} error: {e}")
            time.sleep(5)
    
    print(f"  ✗ FAILED: {num}")
    return False

def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    
    # Remove test file
    test_file = f"{IMG_DIR}/test.png"
    if os.path.exists(test_file):
        os.remove(test_file)
    
    results = {}
    for i, item in enumerate(NEWS):
        num = item["num"]
        title = item["title"]
        print(f"\n[{i+1}/20] Generating {num}: {title}")
        ok = generate_image(item)
        results[num] = ok
        time.sleep(2)  # Be nice to the API
    
    print("\n\n=== Summary ===")
    success = sum(1 for v in results.values() if v)
    for num, ok in results.items():
        print(f"  {num}: {'✓' if ok else '✗'}")
    print(f"\nTotal: {success}/20 succeeded")
    
    # Save news data
    news_data = []
    for item in NEWS:
        news_data.append({
            "number": item["num"],
            "title": item["title"],
            "summary": item["summary"],
            "tag": item["tag"],
            "image": f"images/news_{DATE_STR}_{item['num']}.png"
        })
    
    json_path = f"/home/swg/.openclaw/workspace/news-blog/news_data_{DATE_STR}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    print(f"News data saved: {json_path}")

if __name__ == "__main__":
    main()