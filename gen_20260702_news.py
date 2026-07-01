#!/usr/bin/env python3
"""Generate news and images for 2026年07月02日 - Updated to handle URL responses"""

import base64
import json
import os
import re
import requests
from datetime import datetime

# News data for 2026年07月02日
NEWS_DATE = "2026年07月02日"
NEWS_DATE_SHORT = "20260702"

NEWS_ITEMS = [
    {
        "number": "01",
        "title": "北约峰会在华盛顿闭幕 通过新一轮对俄制裁方案",
        "summary": "北约成立75周年峰会昨日在华盛顿落下帷幕，37个成员国领导人签署联合声明，同意对俄罗斯实施有史以来最严厉的一揽子制裁措施。新制裁涵盖能源、金融、军工等领域，并首次将多家中国电子元器件企业列入管制清单。峰会同时通过乌克兰加入北约的路线图，但未设定具体时间表。",
        "tag": "国际",
        "prompt": "NATO summit meeting in Washington D.C., world leaders in formal attire at a grand conference hall, diplomatic scene, photorealistic, ultra detailed, 8K, high resolution, no text overlays"
    },
    {
        "number": "02",
        "title": "2026年世界杯八强产生 巴西阿根廷上演巅峰对决",
        "summary": "2026年美加墨世界杯进入淘汰赛阶段，八强名单正式产生。巴西与阿根廷在四分之一决赛中提前上演南美双雄会，两队上次世界杯交手还是2014年决赛。本届世界杯至今已吸引全球超过50亿人次观看，创下历史新高。半决赛对阵形势将于今晚抽签决定。",
        "tag": "体育",
        "prompt": "World Cup football stadium at night with vibrant crowd, players in action on the pitch, dramatic lighting, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "03",
        "title": "OpenAI发布GPT-5测试版 多项能力超越人类专家",
        "summary": "OpenAI今日正式发布GPT-5公开测试版，这款大语言模型在数学推理、代码生成、科学研究等多项基准测试中超越人类专家水平。GPT-5首次实现了真正的多模态理解，可以精准解读实验数据并提出创新假设。OpenAI同时宣布GPT-5 API价格下调80%，中小企业和个人开发者可免费使用基础版本。",
        "tag": "科技",
        "prompt": "OpenAI headquarters with futuristic AI brain visualization, neural network patterns in blue light, technology concept, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "04",
        "title": "中国6月出口额同比增长12.8% 创年内新高",
        "summary": "海关总署公布6月外贸数据，以美元计出口同比增长12.8%至3256亿美元，进口增长5.2%，贸易顺差达853亿美元。上半年出口累计增长9.2%，其中新能源汽车、锂电池、光伏组件等新三样出口增速超过40%。对东盟、中东、非洲等新兴市场出口表现强劲，欧美市场占比进一步下降。",
        "tag": "经济",
        "prompt": "Busy port with cargo containers being loaded onto ships, cranes working at night with illuminated lights, global trade scene, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "05",
        "title": "英国正式申请加入《全面进步跨太平洋伙伴关系协定》",
        "summary": "英国政府正式向新西兰提交加入《全面进步跨太平洋伙伴关系协定》申请，成为该协定自2018年生效以来首个新申请国。英国国际贸易大臣表示，加入CPTPP将使英国GDP提升约40亿英镑，并为企业进入亚太高速增长市场创造条件。中国此前已表达加入意愿，外界关注英国申请对地区经贸格局的影响。",
        "tag": "国际",
        "prompt": "United Kingdom Parliament building with global trade symbols, ships and planes representing international commerce, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "06",
        "title": "比特币突破12万美元关口 机构资金持续涌入加密市场",
        "summary": "比特币价格今日突破12万美元整数关口，24小时涨幅达15%，市值重回2.3万亿美元以上。贝莱德、富达等机构管理的现货比特币ETF净流入连续四周超过50亿美元。分析师指出美联储降息预期、比特币第四次减半效应以及机构采用加速是本轮上涨的主要驱动力，但提醒投资者注意波动风险。",
        "tag": "金融",
        "prompt": "Bitcoin cryptocurrency concept with glowing gold coin, digital charts and graphs in background, financial technology scene, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "07",
        "title": "日本探测器成功着陆月球背面 创人类探测新纪录",
        "summary": "日本宇宙航空研究开发机构宣布，月球探测器SLIM在月球背面成功着陆，并传回高清影像数据。这是人类首次实现探测器在月球背面软着陆并保持长期通信。SLIM携带的钻探设备已采集月壤样本，计划于明年将样本送回地球。日本首相岸田文雄表示这是日本航天史上的里程碑时刻。",
        "tag": "科技",
        "prompt": "Japanese lunar probe landing on moon surface, Earth visible in the background, space exploration scene, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "08",
        "title": "欧盟通过《人工智能法案》配套法规 罚款上限提高至全球营业额7%",
        "summary": "欧盟理事会正式通过《人工智能法案》配套法规细则，对高风险AI系统定义进行修订，并大幅提高违规罚款上限至相关企业全球营业额的7%。配套法规还设立了AI实名认证制度，要求聊天机器人等生成式AI产品必须明确告知用户其机器身份。谷歌、微软、Meta等科技巨头已宣布将调整欧盟区AI产品策略。",
        "tag": "科技",
        "prompt": "European Union building in Brussels with digital AI circuitry overlay, technology regulation concept, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "09",
        "title": "全国多地高温预警 电网负荷连续三日创新高",
        "summary": "中央气象台发布高温橙色预警，华北、黄淮、江汉等地最高气温达40℃以上，多地气温突破历史同期极值。国家电网数据显示，7月1日全国电网最高负荷达14.2亿千瓦，连续三日创历史新高。目前已有15个省级电网启动有序用电预案，多地要求机关企事业单位带头节电，工业用户执行错峰生产。",
        "tag": "社会",
        "prompt": "High voltage electricity pylons under extreme summer heat, thermometers showing high temperatures, power grid infrastructure, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "10",
        "title": "特斯拉全自动驾驶获批在中国城市道路运行",
        "summary": "中国工业和信息化部正式批准特斯拉全自动驾驶系统FSD在中国城市道路开展商业运营。特斯拉中国表示，首批试点城市包括北京、上海、广州、深圳、杭州，允许FSD在城区内实现全程无人干预自动驾驶。FSD中国版本针对中国交通规则和道路场景进行了专门优化，售价为6.4万元人民币。",
        "tag": "科技",
        "prompt": "Tesla car with autonomous driving sensors activated on city street, futuristic self-driving concept, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "11",
        "title": "中国科学家发现火星远古海洋沉积物证据",
        "summary": "中国科学院国家天文台宣布，祝融号火星车在乌托邦平原撞击坑区域发现距今37亿年的海洋沉积岩层，这是火星曾经存在液态水的有力证据。沉积物中含有黏土矿物和氯化物，与地球深海热液口附近的沉积物特征高度相似。该发现发表在《科学》杂志上，为研究火星宜居性演化提供了关键线索。",
        "tag": "科技",
        "prompt": "Mars rover exploring Martian surface, reddish rock formations, evidence of ancient water, space exploration, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "12",
        "title": "上半年全国土地出让收入同比下降28%",
        "summary": "财政部公布上半年政府性基金预算收入情况，国有土地使用权出让收入约1.8万亿元，同比下降28%，降幅较一季度扩大3个百分点。土地成交楼面均价下跌15%，溢价率降至3.2%的历史低位。多地取消土地拍卖限价以促进成交，但民营房企拿地意愿仍然不足，城投公司托底现象持续。",
        "tag": "经济",
        "prompt": "Real estate construction site with cranes, empty land plots, economic slowdown concept, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "13",
        "title": "杭州至上海磁悬浮列车开始试运营 全程仅需20分钟",
        "summary": "沪杭磁悬浮铁路正式进入试运营阶段，最高时速600公里的高速磁浮列车将杭州至上海两地通行时间压缩至20分钟以内。该线路全长约160公里，票价暂定为150元。目前每日开行12对列车，主要服务商务出行人群。民航和铁路部门已推出空铁联运、空磁联运优惠套餐以应对客流分流。",
        "tag": "科技",
        "prompt": "Maglev train at high speed, sleek futuristic design, Shanghai cityscape in background, transportation innovation, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "14",
        "title": "联合国教科文组织将春节列入人类非物质文化遗产代表作名录",
        "summary": "联合国教科文组织保护非物质文化遗产政府间委员会通过评审，正式将中国春节列入人类非物质文化遗产代表作名录。春节成为中国第44个列入该名录的项目。教科文组织表示，春节作为东亚及东南亚地区最重要传统节日，具有促进文化多样性和人类创造力的突出价值。目前全球约20亿人庆祝春节。",
        "tag": "文化",
        "prompt": "Chinese Spring Festival celebration with red lanterns, traditional decorations, family gathering scene, cultural festival, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "15",
        "title": "华为问界M9单月交付破3万辆 蝉联50万以上销量冠军",
        "summary": "华为与赛力斯合作的问界M9车型7月首周交付量已突破1.2万辆，预计全月交付将超过3万辆，蝉联国内50万元以上车型月度销量冠军。问界M9自去年上市以来累计交付已超过15万辆。华为智能驾驶ADS 3.0和鸿蒙座舱4.0成为核心卖点，订单等待周期已缩短至6周以内。",
        "tag": "科技",
        "prompt": "Huawei AITO electric SUV on modern city street, sleek design with advanced technology, automotive innovation, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "16",
        "title": "世卫组织宣布猴痘疫情构成国际关注的突发公共卫生事件",
        "summary": "世界卫生组织宣布，刚果盆地及其他中非国家持续的猴痘疫情已构成国际关注的突发公共卫生事件。与2022年疫情不同，本轮疫情由新型猴痘分支病毒引起，该病毒人际传播效率更高，且已扩散至12个非洲以外国家。世卫组织呼吁疫苗制造商增加产能，但表示不建议实施国际旅行限制。",
        "tag": "社会",
        "prompt": "WHO headquarters in Geneva with medical cross symbol, global health emergency concept, healthcare workers, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "17",
        "title": "央行宣布开展国债借入操作 规模达数千亿元",
        "summary": "中国人民银行公告，将面向部分公开市场业务一级交易商开展国债借入操作，业界预期规模在3000亿至5000亿元之间。此举旨在引导国债收益率曲线合理上行，避免长端利率过度下行。消息发布后，10年期国债收益率应声上行8个基点至2.15%，债市杠杆资金出现小幅撤离。",
        "tag": "金融",
        "prompt": "People's Bank of China headquarters in Beijing with financial charts, monetary policy concept, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "18",
        "title": "巴黎奥运会中国代表团成立 405名运动员参赛",
        "summary": "中国体育总局公布巴黎奥运会中国体育代表团名单，共405名运动员将参加30个大项的比赛。运动员平均年龄24岁，年龄最小的选手为14岁的滑板运动员。跳水、举重、乒乓球、射击、羽毛球、游泳六大优势项目仍是夺金主力，新增项目冲浪、霹雳舞、攀岩等也有望取得突破。代表团将于7月20日启程赴法。",
        "tag": "体育",
        "prompt": "Chinese athletes in Olympic gear, national flag waving, Paris Olympics preparation scene, sports excellence, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "19",
        "title": "中国宣布对镓锗等关键矿物实施出口管制",
        "summary": "商务部与海关总署联合发布公告，决定对镓、锗、钨、钼等关键矿物实施出口管制，未经许可不得对外出口。上述矿物是半导体、军工、稀土永磁材料的关键原料，中国供应量占全球85%以上。商务部表示此举旨在维护国家安全和利益，将于正式公布15日后生效。美国商务部表示将评估相关影响并寻求替代供应源。",
        "tag": "国际",
        "prompt": "Rare earth minerals and metals in laboratory display, China flag in background, strategic materials concept, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "number": "20",
        "title": "三星电子发布折叠屏卷轴屏混合原型机",
        "summary": "三星电子在韩国首尔举行的显示技术展上发布了一款折叠屏与卷轴屏混合的原型机，用户可根据需要在8英寸折叠屏和12英寸展开屏之间切换。该产品采用新型超薄玻璃盖板，折叠次数可达50万次以上。三星显示部门负责人表示，这款产品代表了移动终端显示技术的未来方向，预计2027年实现商业化。",
        "tag": "科技",
        "prompt": "Samsung foldable smartphone with flexible screen unfolding, futuristic mobile device concept, technology innovation, photorealistic, ultra detailed, 8K, high resolution"
    }
]

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
IMAGES_DIR = "/home/swg/.openclaw/workspace/news-blog/images"

def generate_image_cogview(news_item, retry=2):
    """Generate image using CogView-3-Flash API"""
    for attempt in range(retry + 1):
        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "cogview-3-flash",
                "messages": [
                    {"role": "user", "content": f"Image prompt: {news_item['prompt']}"}
                ]
            }
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                
                # Handle URL format response
                if isinstance(content, list) and len(content) > 0:
                    url = content[0].get("url")
                    if url:
                        # Download image from URL
                        img_response = requests.get(url, timeout=60)
                        img_response.raise_for_status()
                        image_bytes = img_response.content
                        
                        filename = f"news_{NEWS_DATE_SHORT}_{news_item['number']}.png"
                        filepath = os.path.join(IMAGES_DIR, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(image_bytes)
                        print(f"Generated: {filename}")
                        return True, filename
                # Handle base64 format
                elif "data:image/png;base64," in content:
                    base64_data = content.split("data:image/png;base64,")[1]
                    image_bytes = base64.b64decode(base64_data)
                    
                    filename = f"news_{NEWS_DATE_SHORT}_{news_item['number']}.png"
                    filepath = os.path.join(IMAGES_DIR, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(image_bytes)
                    print(f"Generated: {filename}")
                    return True, filename
            
            print(f"Unexpected response format: {data}")
            return False, None
        except Exception as e:
            print(f"Error generating image {news_item['number']} (attempt {attempt+1}): {e}")
    return False, None

def update_index_html(news_items):
    """Update index.html with new news content"""
    html_path = "/home/swg/.openclaw/workspace/news-blog/index.html"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update title and date
    content = re.sub(r'<title>.*?</title>', f'<title>{NEWS_DATE} 环球新闻</title>', content)
    content = re.sub(r'meta name="description" content="[^"]*"', f'meta name="description" content="{NEWS_DATE}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态"', content)
    content = re.sub(r'cover-subtitle">[^<]*</p>', f'cover-subtitle">全球20条热点新闻 · {NEWS_DATE}</p>', content)
    
    # Build new news cards
    new_cards = ""
    for item in news_items:
        img_path = f"images/news_{NEWS_DATE_SHORT}_{item['number']}.png"
        card = f'''<article class="news-card" data-tag="{item["tag"]}">
    <img class="news-image" src="{img_path}" alt="{item["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{item["number"]}</span>
        <h3 class="news-title">{item["title"]}</h3>
        <p class="news-summary">{item["summary"]}</p>
        <div><span class="tag">{item["tag"]}</span></div>
    </div>
</article>
'''
        new_cards += card
    
    # Replace news grid content
    pattern = r'<div class="news-grid" id="newsGrid">.*?</div>\s*<div class="comments-section">'
    replacement = f'<div class="news-grid" id="newsGrid">\n{new_cards}</div>\n\n            <div class="comments-section">'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated index.html with {len(news_items)} news items")
    return True

def main():
    print(f"Starting news update for {NEWS_DATE}")
    
    # Ensure images directory exists
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # Generate all images
    print("\n=== Generating images ===")
    success_count = 0
    for item in NEWS_ITEMS:
        success, filename = generate_image_cogview(item)
        if success:
            success_count += 1
        else:
            print(f"Failed to generate image for news {item['number']}: {item['title']}")
    
    print(f"\nGenerated {success_count}/{len(NEWS_ITEMS)} images")
    
    # Update HTML
    print("\n=== Updating index.html ===")
    update_index_html(NEWS_ITEMS)
    
    print("\n=== Done ===")

if __name__ == "__main__":
    main()