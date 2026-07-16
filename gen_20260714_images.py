#!/usr/bin/env python3
import json
import base64
import urllib.request
import urllib.error
import os
import time

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
DATE = "20260714"
DATE_DISPLAY = "2026年07月14日"
IMAGES_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
INDEX_HTML = "/home/swg/.openclaw/workspace/news-blog/index.html"

os.makedirs(IMAGES_DIR, exist_ok=True)

# News data
NEWS_DATA = [
    {"number": "01", "title": "北约峰会在土耳其闭幕 通过新一轮东扩决策", "summary": "北约峰会在土耳其安卡拉闭幕，会议通过接纳芬兰和瑞典加入北约的议程，并决定在东欧地区部署更多军事力量。峰会联合声明强调加强集体防御能力，美国宣布将向欧洲增派两万兵力。俄罗斯外交部发言人表示，北约继续东扩是危险举动，将采取反制措施。", "tag": "国际", "image_prompt": "NATO summit meeting in Ankara Turkey with flags of member nations, world leaders in formal suits seated at conference table, diplomatic atmosphere, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"},
    {"number": "02", "title": "世界人工智能大会将在上海开幕 展示多项前沿技术", "summary": "2026世界人工智能大会暨人工智能全球治理高级别会议将于7月17日在上海开幕。本届大会以智能伙伴共创未来为主题，将展示超过500项AI前沿技术成果，涵盖大模型、机器人、自动驾驶等领域。特斯拉CEO马斯克、OpenAI CEO奥尔特曼等将出席并发表演讲。", "tag": "科技", "image_prompt": "World AI conference exhibition hall in Shanghai with futuristic robots and holographic displays, visitors interacting with AI-powered devices, grand convention center interior, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "03", "title": "特斯拉全自动驾驶出租车在旧金山开始运营", "summary": "特斯拉在旧金山正式启动全自动驾驶出租车服务，首批投入500辆无人驾驶Model Y。乘客可通过手机APP预约，票价与普通出租车相当。特斯拉表示已获得加州机动车辆管理局商业运营许可，安全驾驶里程超过1亿英里。Waymo和Cruise等竞争对手表示欢迎竞争，共同推动行业标准制定。", "tag": "科技", "image_prompt": "Tesla autonomous taxi self-driving car driving on San Francisco streets with no driver visible, cityscape background, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"},
    {"number": "04", "title": "欧洲多国遭遇极端高温 法国宣布进入紧急状态", "summary": "欧洲多国遭遇罕见热浪，法国、西班牙、意大利气温突破45摄氏度。法国政府宣布进入公共卫生紧急状态，埃菲尔铁塔、卢浮宫等标志性景点缩短开放时间。高温已造成至少200人死亡，电力系统超负荷运转，多国呼吁民众减少不必要外出。", "tag": "国际", "image_prompt": "Extreme heat wave in Europe, scorching sun over Paris with heat haze, people cooling off at fountains, thermal imaging colors, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"},
    {"number": "05", "title": "国际油价持续下跌 布伦特原油跌破75美元", "summary": "国际油价延续下跌趋势，布伦特原油期货价格跌破75美元/桶，创近两年新低。主要产油国增产预期升温和全球需求放缓共同施压石油市场。OPEC+本周将召开会议讨论进一步减产措施，市场预计可能日均减产50万桶以稳定价格。", "tag": "金融", "image_prompt": "Oil price decline visualization, oil tanker ship at sea, falling stock market chart overlay, industrial port background, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"},
    {"number": "06", "title": "中国成功发射天宫空间站扩展舱段", "summary": "中国在文昌航天发射场使用长征五号B运载火箭成功发射天宫空间站扩展舱段。扩展舱将与天宫空间站核心舱对接，新增约50立方米的活动空间和一套出舱活动气闸舱。6名航天员将在轨完成设备安装和调试，为后续载人登月任务做准备。", "tag": "科技", "image_prompt": "Chinese space station Tiangong in orbit above Earth with astronauts in white spacesuits conducting spacewalk, spacecraft docking, cosmic background with stars, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "07", "title": "联合国教科文组织呼吁保护人工智能时代的文化遗产", "summary": "联合国教科文组织发布报告，警告AI技术可能加速文化遗产的流失和失真。报告指出深度伪造、算法生成内容正在模糊历史真实性边界，呼吁各国制定AI时代文化遗产保护标准。教科文组织同时启动数字记忆项目，计划对全球1000处濒危遗产进行高精度数字化保存。", "tag": "文化", "image_prompt": "UNESCO heritage site being digitally preserved, archaeologists using 3D scanning technology on ancient temple ruins, digital hologram overlay, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"},
    {"number": "08", "title": "美国最高法院裁定社交媒体平台须对算法推荐负责", "summary": "美国最高法院以6比3的投票裁定，社交媒体平台对其算法推荐内容负有法律责任，不能以技术中立为由完全免责。裁决要求平台建立更有效的内容审核机制，并赋予用户关闭个性化推荐的权利。Meta、字节跳动等科技巨头表示将上诉，称裁决将摧毁平台商业模式。", "tag": "科技", "image_prompt": "US Supreme Court building with gavel, social media icons and algorithms visualization floating above, phones showing social media feeds, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "09", "title": "德国大众宣布在华投资200亿欧元 押注电动化转型", "summary": "德国大众集团宣布未来五年将在中国投资200亿欧元，重点布局电动汽车和智能驾驶技术。投资将用于新建三座新能源工厂、扩大研发中心规模，并与地平线机器人等中国科技企业深化合作。大众表示中国是其最重要的单一市场，电动化转型已取得实质性进展。", "tag": "经济", "image_prompt": "Volkswagen electric vehicle factory in China with robotic assembly lines, new energy cars on production line, modern automated manufacturing, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "10", "title": "日本发射新型侦察卫星 提升对朝监控能力", "summary": "日本宇宙航空研究开发机构使用H3运载火箭成功发射一枚新型光学侦察卫星情报收集卫星-7。该卫星分辨率达0.3米，可识别地面小型车辆，将显著提升日本对朝鲜半岛及周边地区的监控能力。日本防卫省表示此举旨在应对地区安全环境变化，增强情报收集自主性。", "tag": "军事", "image_prompt": "Japanese H3 rocket launching from Tanegashima Space Center at dusk, satellite separating in orbit above Earth, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"},
    {"number": "11", "title": "全球首个碳中和液化天然气交易完成", "summary": "壳牌与中国石油完成全球首个碳中和液化天然气交易，货物总量约6.5万吨。交易过程中产生的碳排放通过森林碳汇和可再生能源项目进行抵消，符合国际航空碳抵销和减排计划标准。业内人士指出碳中和LNG贸易将逐步成为行业趋势。", "tag": "经济", "image_prompt": "LNG liquefied natural gas tanker ship at sea with sunset, carbon neutrality concept with green forest and renewable energy wind turbines, shipping containers, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "12", "title": "欧盟委员会对苹果处以80亿欧元反垄断罚款", "summary": "欧盟委员会宣布对苹果公司处以80亿欧元反垄断罚款，指控其滥用App Store市场支配地位，强制开发者使用苹果支付系统并收取高额佣金。这是欧盟有史以来对科技公司开出的最大罚单。苹果表示将提起上诉，称处罚无视竞争法的基本事实。", "tag": "经济", "image_prompt": "European Commission building in Brussels with Apple logo, legal documents and Euro banknotes, justice scales balance, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "13", "title": "国际黑客组织对多国金融机构发动协同攻击", "summary": "一个名为影子风暴的国际黑客组织对美洲、欧洲、亚洲多家金融机构发动协同网络攻击，导致部分银行ATM和网上银行服务中断。美联储、欧洲央行等监管机构召开紧急会议，要求受影响机构启动应急响应。美国FBI情报显示攻击与某国家级APT组织存在关联。", "tag": "社会", "image_prompt": "Cybersecurity attack visualization, hacker in dark room with multiple monitors showing code and data streams, bank buildings in background, digital glitch effects, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "14", "title": "巴西登革热疫情持续蔓延 确诊超过500万例", "summary": "巴西卫生部公布数据显示，今年以来登革热确诊病例已突破500万例，死亡人数超过2500人。疫情集中在东南部人口密集地区，医疗系统承受巨大压力。世界卫生组织已派遣紧急医疗队协助抗疫，并呼吁各国加强对蚊媒传染病的监测和防控。", "tag": "社会", "image_prompt": "Hospital in Brazil crowded with patients, doctors in protective gear treating people, tropical climate background with mosquitoes, medical equipment, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "15", "title": "阿根廷宣布重返南美国家联盟 卢拉表示欢迎", "summary": "阿根廷政府正式宣布重新加入南美国家联盟（UNASUR），结束了七年的退群状态。阿根廷外长表示区域合作对应对共同挑战至关重要。阿根廷总统米莱在社交媒体上表示，重返联盟将促进地区贸易一体化和安全合作。巴西总统卢拉对此表示热烈欢迎。", "tag": "国际", "image_prompt": "South American leaders meeting at diplomatic summit, Argentine and Brazilian flags side by side, handshake between presidents, UNASUR emblem, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "16", "title": "OpenAI推出企业级AI助手 瞄准商业市场", "summary": "OpenAI发布企业级AI助手ChatGPT Business，面向企业客户提供定制化服务。企业版支持私有化部署、多模态分析和API深度集成，月费为每用户25美元。ChatGPT企业用户已超过100万，覆盖金融服务、医疗、教育等多个行业。", "tag": "科技", "image_prompt": "OpenAI office with employees using ChatGPT Business on computers, modern tech workplace, AI chatbot interface on screen, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "17", "title": "2026年温网公开赛开幕 多位中国选手晋级", "summary": "2026年温布尔登网球公开赛在伦敦开幕，中国选手郑钦文首轮横扫对手晋级，王欣瑜逆转取胜同样晋级第二轮。男单方面，张之臻因伤退赛。赛会头号种子辛纳表示本届赛事竞争激烈，德约科维奇剑指第八冠。", "tag": "体育", "image_prompt": "Wimbledon tennis championship in London, tennis players on grass court, Centre Court with iconic Tudor architecture, crowd cheering, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "18", "title": "联合国报告显示全球饥饿人口连续第三年上升", "summary": "联合国粮农组织发布《2026年世界粮食安全和营养状况》报告，全球面临饥饿的人口已达7.35亿，连续第三年上升。冲突、气候变化和经济不确定性是主要驱动因素。报告呼吁国际社会增加农业投资，优先支持小农生产者和脆弱国家。", "tag": "国际", "image_prompt": "UN headquarters in New York with globe, families in developing country receiving food aid, agricultural fields with drought, contrast between plenty and scarcity, photorealistic, ultra detailed, 8K, high resolution, no text"},
    {"number": "19", "title": "英伟达发布新一代AI芯片Blackwell Ultra", "summary": "英伟达在加州圣何塞发布新一代AI芯片Blackwell Ultra，性能是前代产品的2.5倍，专为训练超大规模语言模型设计。黄仁勋表示该芯片已获得微软、谷歌、亚马逊等云服务商超过50亿美元的预订单。芯片采用台积电3纳米工艺，将于今年第四季度开始出货。", "tag": "科技", "image_prompt": "NVIDIA GPU chip silicon wafer under microscope, glowing blue circuit traces, futuristic technology background, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"},
    {"number": "20", "title": "中国多省份出现强降雨 防汛应急响应提升至二级", "summary": "受持续强降雨影响，中国水利部将防汛应急响应提升至二级。长江、淮河流域多个水文站超警戒水位，四川、湖北、安徽等地已转移危险区域群众超过50万人。国家防总派出工作组赴重点地区督导防汛工作，要求确保人民生命安全。", "tag": "社会", "image_prompt": "China flood emergency response, soldiers in rain gear rescuing villagers with boats, swollen river with submerged buildings, rescue vehicles with lights, photorealistic, ultra detailed, 8K, high resolution, no text"}
]

def generate_image(news_item, retry=False):
    prompt = news_item["image_prompt"]
    
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            # content is a list with dict containing 'url'
            image_url = content[0]["url"]
            
            # Download image
            img_req = urllib.request.Request(image_url)
            with urllib.request.urlopen(img_req, timeout=120) as img_response:
                image_data = img_response.read()
                filename = f"news_{DATE}_{news_item['number'].zfill(2)}.png"
                filepath = os.path.join(IMAGES_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(image_data)
                print(f"OK: {filename} ({len(image_data)} bytes)")
                return True
                
    except Exception as e:
        print(f"FAIL: news_{DATE}_{news_item['number'].zfill(2)}.png - {e}")
        if not retry:
            print(f"  Retrying...")
            time.sleep(2)
            return generate_image(news_item, retry=True)
        return False

def update_index_html():
    """Update index.html with new news items"""
    import re
    
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Update title and date
    html = re.sub(r"<title>.*?环球新闻</title>", f"<title>{DATE_DISPLAY} 环球新闻</title>", html)
    html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{DATE_DISPLAY}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">', html)
    html = re.sub(r"全球20条热点新闻 · \d{4}年\d{2}月\d{2}日", f"全球20条热点新闻 · {DATE_DISPLAY}", html)
    
    # Generate new news cards HTML
    news_cards = ""
    for item in NEWS_DATA:
        card = f'''<article class="news-card" data-tag="{item["tag"]}">
    <img class="news-image" src="images/news_{DATE}_{item["number"].zfill(2)}.png" alt="{item["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{item["number"]}</span>
        <h3 class="news-title">{item["title"]}</h3>
        <p class="news-summary">{item["summary"]}</p>
        <div><span class="tag">{item["tag"]}</span></div>
    </div>
</article>'''
        news_cards += card + "\n"
    
    # Replace news grid content
    old_pattern = r'<div class="news-grid">.*?</div>\s*<div class="comments-section">'
    new_html = f'<div class="news-grid">\n{news_cards}</div>\n            <div class="comments-section">'
    html = re.sub(old_pattern, new_html, html, flags=re.DOTALL)
    
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Updated index.html with {len(NEWS_DATA)} news items")

def main():
    print(f"Generating news for {DATE_DISPLAY}")
    print("=" * 50)
    
    # Generate all images
    print("\nGenerating images...")
    failed = []
    for item in NEWS_DATA:
        success = generate_image(item)
        if not success:
            failed.append(item)
        time.sleep(1)  # Rate limiting
    
    # Retry failed images once
    if failed:
        print(f"\nRetrying {len(failed)} failed images...")
        time.sleep(3)
        for item in failed[:]:
            success = generate_image(item)
            if success:
                failed.remove(item)
    
    print(f"\n{len(NEWS_DATA) - len(failed)}/{len(NEWS_DATA)} images generated successfully")
    
    if failed:
        for item in failed:
            print(f"  FAILED: {item['title']}")
    
    # Update index.html
    print("\nUpdating index.html...")
    update_index_html()
    print("\nDone!")

if __name__ == "__main__":
    main()