#!/usr/bin/env python3
import json
import os
import time
import urllib.request
import urllib.error

# News data for 2026年07月26日
DATE_ID = "20260726"

news_items = [
    {"number": "01", "tag": "科技", "title": "中国成功发射千帆星座第三批卫星 全球卫星互联网布局加速", "summary": "中国在太原卫星发射中心成功发射千帆星座第三批18颗卫星，标志着中国版星链计划进入规模化部署阶段。该星座最终将由超过1.2万颗低轨卫星组成，为全球提供高速互联网接入服务，首批服务区域覆盖一带一路沿线国家。", "prompt": "Chinese rocket launching into clear blue sky with vapor trail, satellite deployment in low Earth orbit, photorealistic, ultra detailed, 8K, high resolution, cinematic lighting, no text or watermark"},
    {"number": "02", "tag": "国际", "title": "美国宣布对华芯片出口管制升级 商务部回应称将采取反制措施", "summary": "美国商务部宣布进一步收紧对华芯片及半导体设备出口管制，新增包括先进AI芯片和光刻机在内的200余项管制项目。中国商务部发言人表示坚决反对，并将采取一切必要措施维护中国企业的合法权益，中美科技博弈进一步升级。", "prompt": "US and China flags side by side, semiconductor chip on circuit board, dramatic lighting, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "03", "tag": "经济", "title": "中国上半年GDP同比增长5.8% 消费对经济贡献率提升至65%", "summary": "国家统计局发布2026年上半年经济数据，GDP同比增长5.8%，增速位居全球主要经济体前列。最终消费支出对经济增长贡献率提升至65%，服务业增加值占GDP比重达56%，经济结构持续优化，高质量发展态势良好。", "prompt": "Chinese city skyline at sunset with modern buildings, economic growth concept, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "04", "tag": "科技", "title": "阿里发布通义千问3.0推理大模型 数学推理能力超越GPT-6", "summary": "阿里巴巴在云栖大会上正式发布通义千问3.0，该模型在MATH数学基准测试中达到98.6分，超越GPT-6和Claude 4。通义千问3.0采用全新思维链架构，支持复杂多步推理，已向开发者开源模型权重和推理代码。", "prompt": "AI neural network visualization, glowing blue circuits, digital brain concept, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "05", "tag": "金融", "title": "比特币突破12万美元再创新高 机构投资者入场推动牛市行情", "summary": "受比特币现货ETF净流入超50亿美元和MicroStrategy宣布再增持2万枚BTC刺激，比特币价格突破12万美元关口创历史新高。加密货币总市值突破5万亿美元，以太坊和Solana等主流币种同步上涨，机构牛市行情持续。", "prompt": "Bitcoin gold coin on financial charts, golden glow, bullish trend, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "06", "tag": "社会", "title": "全国异地就医直接结算突破10亿人次 医保跨省通办全覆盖", "summary": "国家医保局宣布，全国医保跨省异地就医直接结算已突破10亿人次，覆盖全国所有统筹地区。参保人员只需凭借医保码即可在全国50万家定点医疗机构实现直接结算，无需先行垫付再报销，看病难问题得到有效解决。", "prompt": "Modern hospital lobby with digital registration kiosk, patients using mobile phones, bright clean interior, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "07", "tag": "科技", "title": "宁德时代发布神行PLUS电池 充电10分钟续航1000公里", "summary": "宁德时代在电池日发布会上推出神行PLUS超快充电池，采用新一代磷酸铁锂正极材料和石墨烯复合负极，可实现10分钟补能400公里。搭配整车热管理系统，-20°C极寒环境仍可正常充电，已获超过20家车企订单。", "prompt": "Electric vehicle charging station at night, glowing battery indicator, futuristic design, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "08", "tag": "国际", "title": "欧盟通过中国电动汽车反补贴案终裁 最高加征36.3%关税", "summary": "欧盟委员会正式通过对中国电动汽车反补贴调查终裁方案，对比亚迪、吉利和上汽分别加征17.4%、19.9%和36.3%的反补贴关税。中国商务部回应称这是典型的贸易保护主义，中方已向WTO提起诉讼，并将采取相应措施。", "prompt": "electric vehicles on cargo ship at dock, trade dispute concept, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "09", "tag": "经济", "title": "中国对非洲进出口总额突破3万亿元 连续四年稳居非洲最大贸易伙伴", "summary": "海关总署数据显示，2026年上半年中非贸易总额达3.2万亿元，同比增长18%。中国对非出口以机电产品和钢材为主，自非进口以矿产资源和农产品为主。非洲已成为中国企业出海的重要市场，超过1000家中国企业在非直接投资。", "prompt": "African port with cargo ships, containers stacked, trade logistics, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "10", "tag": "科技", "title": "小米发布Xiaomi 15 Ultra搭载自研玄戒芯片 冲击全球高端市场", "summary": "小米发布年度旗舰Xiaomi 15 Ultra，全球首发自研玄戒2处理器，采用台积电3nm工艺，跑分突破280万。该机配备1英寸LYT-900主摄和2亿像素潜望长焦，支持双向卫星通信，起售价5999元，目标三年内超越苹果成为全球高端市场第二。", "prompt": "sleek smartphone on display pedestal, glowing circuit lines, premium smartphone design, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "11", "tag": "金融", "title": "人民币国际化再提速 全球跨境支付人民币占比突破8%", "summary": "环球银行金融电信协会数据显示，6月份全球跨境支付中人民币占比升至8.1%，超越日元成为全球第四大支付货币。在双边本币互换框架下，中国已与40个国家签署协议，人民币在金砖国家和东盟地区的使用率持续攀升。", "prompt": "global financial trading floor with Chinese yuan symbols, world map background, currency exchange concept, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "12", "tag": "社会", "title": "全国城镇新增就业738万人 超额完成全年预期目标", "summary": "人社部公布上半年就业数据，城镇新增就业738万人，完成全年目标任务的62%。新经济新业态持续扩容，直播电商、共享经济等新职业从业者突破1亿人。16至24岁青年失业率降至12.3%，较年初下降3个百分点。", "prompt": "job fair with young professionals, career counseling booth, modern office environment, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "13", "tag": "国际", "title": "中美两军设立海空热线 双方同意加强战略沟通防止误判", "summary": "中美两军宣布正式建立海空一线部队指挥官直达热线，旨在降低双方在东海和南海发生海空意外摩擦的风险。两国国防部发表联合声明，重申致力于落实两国元首共识，建立健康稳定的中美两军关系。", "prompt": "US and China military ships in open ocean, diplomatic handshake, ocean horizon, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "14", "tag": "科技", "title": "SpaceX完成星舰第六次试飞 首次实现筷子捕获助推器", "summary": "SpaceX在得克萨斯州完成星舰第六次综合测试飞行，超级重型助推器首次成功被发射塔上的机械臂筷子捕获，标志着完全可复用火箭技术取得重大突破。马斯克表示这将使发射成本降低至原来的1%，未来将用于火星任务。", "prompt": "SpaceX Starship rocket on launch pad, massive booster being caught by mechanical arms, dramatic sunset, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "15", "tag": "文化", "title": "《黑神话：悟空2》全球首发 首日销量突破2000万份", "summary": "腾讯游戏和游戏科学联合开发的《黑神话：悟空2》全球同步发售，首日销量突破2000万份，Steam同时在线人数超500万，创造全球游戏史首发新纪录。游戏以西游记后传为背景，画面和战斗系统获得全球玩家一致好评。", "prompt": "gaming setup with vibrant colors, warrior character on screen, futuristic game console, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "16", "tag": "金融", "title": "A股市值突破100万亿元 散户和机构投资者数量均创新高", "summary": "A股市场总市值突破100万亿元大关，较年初增长32%。上半年新增股票账户超过8000万户，基金投资者突破8亿人，均创历史新高。证监会表示将持续推进资本市场改革，吸引更多长期资金入市。", "prompt": "Shanghai stock exchange trading floor, stock market charts rising, investors celebrating, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "17", "tag": "科技", "title": "中国首条超导电缆正式投入商业运营 输电效率接近零损耗", "summary": "全球首条商业化运营的公里级超导电缆在上海徐汇区正式投运，该电缆采用高温超导材料，在-196°C液氮环境下实现零电阻输电，输电损耗较传统电缆降低90%以上。项目投运将为城市中心区高密度用电提供全新解决方案。", "prompt": "underground power cable tunnel with glowing blue light, futuristic technology, city infrastructure, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "18", "tag": "体育", "title": "中国女排世联赛总决赛夺冠 豪取跨赛季38连胜", "summary": "2026年世界女排联赛总决赛在东京落幕，中国女排在决赛中3-1击败巴西队，成功卫冕并豪取跨赛季38连胜。朱婷砍下全场最高28分当选MVP，中国队以11战全胜战绩夺得本赛季第三座冠军奖杯。", "prompt": "volleyball match in packed stadium, player spiking ball, Chinese flag in background, dramatic sports photography, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "19", "tag": "社会", "title": "全国充电桩突破1200万台 县乡新能源汽车覆盖率超90%", "summary": "中国充电联盟数据显示，截至6月底全国充电桩保有量突破1200万台，其中公共充电桩超400万台。农村地区充电设施覆盖率超过90%，全国新能源汽车保有量达6800万辆，充电基础设施建设有力支撑新能源汽车下乡战略。", "prompt": "electric car charging in rural area, modern charging station surrounded by green fields, new energy vehicles, photorealistic, ultra detailed, 8K, no text or watermark"},
    {"number": "20", "tag": "文化", "title": "《永乐大典》数字重生工程启动 全球协作复原珍贵典籍", "summary": "国家图书馆联合全球30家图书馆和博物馆启动《永乐大典》数字重生工程，采用多光谱扫描和AI修复技术对现存200余卷进行全面数字化。项目将运用生成式AI还原缺失内容，预计2028年完成全球首次完整展示。", "prompt": "ancient Chinese books restoration in modern lab, digital scanning equipment, precious scrolls, photorealistic, ultra detailed, 8K, no text or watermark"},
]

# CogView API settings
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"

def generate_image(news_num, prompt, retry=2):
    """Generate image using CogView-3-Flash API and download from URL"""
    image_path = f"images/news_{DATE_ID}_{news_num}.png"
    
    if os.path.exists(image_path):
        print(f"Image {news_num} already exists, skipping")
        return True
    
    for attempt in range(retry + 1):
        payload = json.dumps({
            "model": "cogview-3-flash",
            "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
        })
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }
        
        req = urllib.request.Request(
            API_URL, 
            data=payload.encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result["choices"][0]["message"]["content"]
                
                if isinstance(content, list) and len(content) > 0:
                    url = content[0].get("url")
                    if url:
                        # Download the image
                        with urllib.request.urlopen(url, timeout=60) as img_response:
                            img_data = img_response.read()
                            with open(image_path, 'wb') as f:
                                f.write(img_data)
                            print(f"Generated image {news_num}: {image_path}")
                            return True
                print(f"Unexpected response format for image {news_num}: {str(content)[:200]}")
        except Exception as e:
            print(f"Error generating image {news_num} (attempt {attempt+1}): {e}")
        
        if attempt < retry:
            time.sleep(3)
    
    return False

# Create images directory
os.makedirs("images", exist_ok=True)

# Generate all images
print(f"Generating {len(news_items)} images...")
for item in news_items:
    success = generate_image(item["number"], item["prompt"])
    if not success:
        print(f"FAILED: Image {item['number']}")
    time.sleep(1)  # Rate limiting

# Verify all images exist
missing = []
for i in range(1, 21):
    num = f"{i:02d}"
    path = f"images/news_{DATE_ID}_{num}.png"
    if not os.path.exists(path):
        missing.append(num)

if missing:
    print(f"\nMissing images: {missing}")
else:
    print("\n✓ All 20 images generated successfully!")

# Save news data for HTML update
with open("news_data_20260726.json", "w", encoding="utf-8") as f:
    json.dump(news_items, f, ensure_ascii=False, indent=2)
print("News data saved to news_data_20260726.json")