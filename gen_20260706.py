#!/usr/bin/env python3
"""Generate news images and update index.html for 2026年07月06日"""

import base64
import json
import os
import re
import requests
import time
import urllib.request

# Configuration
DATE = "20260706"
DATE_CN = "2026年07月06日"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
IMAGES_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
INDEX_PATH = "/home/swg/.openclaw/workspace/news-blog/index.html"

# News content for July 6, 2026
NEWS_ITEMS = [
    {
        "number": "01",
        "title": "世界杯决赛阿根廷点球夺冠 法国前锋姆巴佩罚失关键点球",
        "summary": "2026年美加墨世界杯决赛在迈阿密上演，阿根廷通过点球大战5-3战胜法国，成功卫冕。法国前锋姆巴佩在点球大战中罚失关键点球，遗憾落败。35岁的梅西赛后宣布从国家队退役，全球超过25亿观众见证了这一历史性时刻。法国总统马克龙现场观战，赛后称赞法国队展现了拼搏精神。",
        "tag": "体育",
        "image_prompt": "A dramatic soccer stadium scene at night with floodlights illuminating the pitch, two teams locked in intense competition, Argentine and French players in the final moments of a penalty shootout, fans with national flags cheering emotionally, photorealistic, ultra detailed, 8K, high resolution, sports photography"
    },
    {
        "number": "02",
        "title": "中俄\"海上联合-2026\"演习在青岛正式启动 规模创历年之最",
        "summary": "中俄\"海上联合-2026\"联合演习在山东青岛正式启动，这是两国海军首次在此地举行如此大规模演习。中方派出驱逐舰、护卫舰、潜艇等多型舰艇参演，俄方舰艇编队也已抵达青岛军港。演习将重点围绕海上联合补给、联合反潜、防空等科目展开，旨在深化两国海军务实合作。",
        "tag": "国际",
        "image_prompt": "A naval port with Chinese and Russian warships docked side by side, naval personnel in uniform standing at attention during a military ceremony, flags of both countries waving, harbor cranes in background, photorealistic, ultra detailed, 8K, high resolution, naval military scene"
    },
    {
        "number": "03",
        "title": "特朗普与普京通话 提议调解俄乌战争 北约峰会前引关注",
        "summary": "美国前总统特朗普与俄罗斯总统普京通话后表示，愿意帮助结束俄乌战争。克里姆林宫发言人称这次通话\"具有建设性\"。乌克兰总统泽连斯基表示，他与特朗普通话讨论了1200公里的前线局势。北约峰会将于下周召开，各方就如何结束冲突展开密集外交斡旋。",
        "tag": "国际",
        "image_prompt": "Diplomatic meeting scene with two world leaders in formal suits shaking hands across a mahogany table, American and Russian flags side by side, translators and advisors in background, serious expressions, photorealistic, ultra detailed, 8K, high resolution, political diplomacy"
    },
    {
        "number": "04",
        "title": "中国海军舰艇编队穿越日本四大海峡 7艘舰艇部署西太平洋",
        "summary": "日本防卫省发布消息，中国海军舰艇编队近日穿越吐噶喇海峡、冲绳本岛与宫古岛之间海域、大隅海峡和对马海峡等日本四大要道。目前至少有7艘中国舰艇部署在西太平洋海域，活动频率和规模创近年新高。日本自卫队全程跟踪监视，并已向中方表达关切。",
        "tag": "军事",
        "image_prompt": "Chinese naval warships sailing in formation through ocean strait, Japanese coast guard patrol vessels observing from distance, vast blue Pacific Ocean, mountains on distant coastline, warships with Chinese flags, photorealistic, ultra detailed, 8K, high resolution, naval fleet"
    },
    {
        "number": "05",
        "title": "智谱AI发布GLM-5.3多模态大模型 视频理解能力超越GPT-5",
        "summary": "中国人工智能企业智谱AI发布新一代多模态大模型GLM-5.3，在视频理解、图像分析和文本生成等多项基准测试中超越GPT-5。该模型首次实现对长视频的完整理解与分析，支持一键生成专业级视频解说词。智谱AI同时宣布GLM-5.3 API价格仅为GPT-5的十分之一。",
        "tag": "科技",
        "image_prompt": "Futuristic AI technology concept with glowing neural network visualization, holographic display showing multimodal AI processing video images and text simultaneously, Chinese tech lab setting with researchers working on advanced AI system, photorealistic, ultra detailed, 8K, high resolution, technology innovation"
    },
    {
        "number": "06",
        "title": "比特币重返11万美元关口 机构资金持续涌入加密市场",
        "summary": "比特币价格今日反弹至11万美元以上，24小时涨幅达8%。贝莱德、富达等机构管理的现货比特币ETF净流入连续五周超过50亿美元。分析师指出，美联储降息预期升温和比特币减半后的供需关系改善是主要推动因素。以太坊跟随上涨突破3800美元。",
        "tag": "金融",
        "image_prompt": "Bitcoin cryptocurrency concept with golden BTC coin on digital trading charts showing upward trend, holographic stock market graphs in background, glowing cryptocurrency symbols floating, photorealistic, ultra detailed, 8K, high resolution, finance technology"
    },
    {
        "number": "07",
        "title": "全球AI推理芯片市场突破1.2万亿美元 中国企业市占率提升",
        "summary": "市场研究机构最新数据显示，全球AI芯片市场规模今年突破1.2万亿美元，其中推理芯片占比超过60%。英伟达凭借H200和B200系列占据市场主导，中国企业华为昇腾和壁仞科技的推理芯片在国产大模型应用中获得广泛采用，国产化率已提升至45%。",
        "tag": "科技",
        "image_prompt": "Advanced semiconductor chips arranged in server rack, glowing blue LED indicators, AI computing data center corridor with cooling systems, photorealistic, ultra detailed, 8K, high resolution, technology hardware infrastructure"
    },
    {
        "number": "08",
        "title": "SpaceX星舰完成第12次试飞 成功实现助推器回收",
        "summary": "SpaceX星舰完成第12次综合测试飞行，顺利完成超级重型助推器的着陆回收任务。本次试飞实现了从星舰分离到助推器返回发射场的完整流程，为未来载人登月任务奠定基础。马斯克表示，首次载人登月任务可能在2027年实现。NASA对测试结果表示满意。",
        "tag": "科技",
        "image_prompt": "SpaceX Starship rocket launching from launch pad at sunrise, massive rocket exhaust plume, futuristic aerospace technology, starship upper stage separating from booster, photorealistic, ultra detailed, 8K, high resolution, space exploration"
    },
    {
        "number": "09",
        "title": "中国释放北京锡安教会金明日牧师 中美外交讨论成果",
        "summary": "被中国当局羁押九个月的北京锡安教会创办人金明日牧师获释。家属于人权组织确认了这一消息。分析认为，这是中美两国元首此前会唔时讨论的成果之一。人权组织对金明日的获释表示欢迎，但呼吁中国保障宗教自由。",
        "tag": "社会",
        "image_prompt": "Church building with cross on roof in Beijing cityscape, peaceful congregation gathering, people shaking hands in reconciliation scene, photorealistic, ultra detailed, 8K, high resolution, religious freedom theme"
    },
    {
        "number": "10",
        "title": "欧盟通过最严AI监管法案配套细则 违规罚款最高7%全球营收",
        "summary": "欧盟理事会正式通过《人工智能法案》配套法规细则，对高风险AI系统进行更明确定义。违规企业面临最高全球营业额7%的罚款，谷歌、微软已宣布调整欧盟区AI产品策略以符合新规。AI实名认证制度要求所有聊天机器人在对话开始时必须明确告知用户其机器身份。",
        "tag": "科技",
        "image_prompt": "European Union parliament building in Brussels with EU flags, digital AI regulation symbols and legal documents floating, tech companies logos being regulated, photorealistic, ultra detailed, 8K, high resolution, legal technology regulation"
    },
    {
        "number": "11",
        "title": "联合国气候峰会达成新协议 各国承诺加速碳减排",
        "summary": "联合国气候峰会在日内瓦闭幕，120个国家达成新的碳减排协议。主要经济体承诺在2035年前将碳排放量在2020年基础上减少50%。发展中国家获得更多气候融资支持，绿色气候基金规模扩大至2000亿美元。中国和美国宣布建立气候对话机制。",
        "tag": "国际",
        "image_prompt": "United Nations building in Geneva with national flags from many countries, globe with green leaves growing from it, world leaders signing climate agreement at conference table, photorealistic, ultra detailed, 8K, high resolution, international diplomacy climate"
    },
    {
        "number": "12",
        "title": "日本福岛核废水第三轮排放启动 周边国家抗议不断",
        "summary": "日本东京电力公司开始第三轮福岛核废水排海作业，计划排放约7800吨处理后的核废水。中韩等国政府再次表达强烈抗议，限制日本水产品进口的措施持续。中国外交部表示，日本应当立即停止排海行为，建立邻国充分参与的国际监测机制。",
        "tag": "国际",
        "image_prompt": "Pacific Ocean coastline with Fukushima nuclear plant in background, seawater and industrial pipes, anti-nuclear protest demonstration with signs, diplomatic tension scene, photorealistic, ultra detailed, 8K, high resolution, environmental controversy"
    },
    {
        "number": "13",
        "title": "美联储维持利率不变 暗示9月可能降息",
        "summary": "美联储宣布维持联邦基金利率在5.25%至5.5%不变，符合市场预期。美联储主席鲍威尔在记者会上表示，若通胀数据持续改善，9月降息是可能的选项。最新CPI数据显示美国通胀率回落至2.8%，接近2%的目标。华尔街对美联储表态反应积极。",
        "tag": "金融",
        "image_prompt": "Federal Reserve building in Washington DC with American flag, Federal Reserve chairman at press conference podium with microphones, stock market screens showing upward trend in background, photorealistic, ultra detailed, 8K, high resolution, central bank monetary policy"
    },
    {
        "number": "14",
        "title": "中国经济上半年GDP增长5.8% 消费贡献率首超投资",
        "summary": "国家统计局公布数据显示，上半年中国GDP同比增长5.8%，其中二季度增长5.7%。消费对经济增长的贡献率首次超过资本形成总额，达54.6%。新能源汽车、锂电池和光伏产品出口继续领跑，机电产品出口占比提升至62%。房地产市场出现积极变化。",
        "tag": "经济",
        "image_prompt": "Modern Beijing cityscape with skyscrapers and Chinese national flag, bustling commercial district with shoppers, economic growth charts and graphs, photorealistic, ultra detailed, 8K, high resolution, economic development"
    },
    {
        "number": "15",
        "title": "巴黎奥运会倒计时一周年 筹备进入最后冲刺",
        "summary": "2028年洛杉矶夏季奥运会倒计时一周年活动在巴黎举行，展示了场馆建设成果和赛程安排。巴黎奥组委表示，所有场馆翻新工作已完成95%，运动员村已具备入住条件。本届奥运会将首次引入无人机开幕式表演，并大幅增加女性运动员参赛项目。",
        "tag": "体育",
        "image_prompt": "Eiffel Tower in Paris with Olympic rings display, athletes training in modern stadium, Olympic torch relay ceremony, French and international flags celebration, photorealistic, ultra detailed, 8K, high resolution, Olympic games preparation"
    },
    {
        "number": "16",
        "title": "OpenAI推出ChatGPT情感交互2.0 用户满意度提升至92%",
        "summary": "OpenAI发布ChatGPT新版本，全面升级情感识别和共情回应功能。AI现在可以实时感知用户情绪状态，包括焦虑、悲伤、愤怒等，并自动调整回应策略。用户满意度测试从65%提升至92%，成为史上最受好评的版本更新。该版本已向全球Plus用户推送。",
        "tag": "科技",
        "image_prompt": "Person interacting with AI chatbot interface showing emotional recognition graphics, holographic conversation bubbles with empathetic expressions, modern office setting with user smiling at screen, photorealistic, ultra detailed, 8K, high resolution, AI conversation technology"
    },
    {
        "number": "17",
        "title": "全球海洋塑料污染达严重水平 60国签署减排公约",
        "summary": "国际海洋污染峰会公布数据，全球海洋塑料污染已达严重水平，每年约1100万吨塑料流入海洋。60个国家在峰会期间签署《海洋塑料减排公约》，承诺在2030年前将塑料流入海洋的数量减少80%。公约还要求主要塑料生产国建立生产者责任延伸制度。",
        "tag": "社会",
        "image_prompt": "Ocean beach covered in plastic waste, sea turtle entangled in plastic, environmental cleanup workers collecting garbage on tropical beach, blue ocean water, photorealistic, ultra detailed, 8K, high resolution, environmental pollution"
    },
    {
        "number": "18",
        "title": "俄罗斯发射新一代北极航道监控卫星 提升航运安全能力",
        "summary": "俄罗斯从东方航天发射场成功发射新一代北极航道监控卫星系统。该系统由6颗卫星组成，可实现对北极航道的全天候监控。俄罗斯表示将在2026年底前完成系统部署，届时可为通过北极航道的船只提供实时气象和冰情信息。",
        "tag": "科技",
        "image_prompt": "Russian rocket launching into polar night sky from snowy launch facility, aurora borealis over Arctic landscape, satellite in orbit above Earth polar region, photorealistic, ultra detailed, 8K, high resolution, aerospace satellite"
    },
    {
        "number": "19",
        "title": "马斯克脑机接口人体试验获FDA批准 招募首例志愿者",
        "summary": "美国食品药品监督管理局批准Neuralink公司开展脑机接口人体临床试验。Neuralink已启动首例志愿者招募工作，面向因脊髓损伤或渐冻症导致瘫痪的患者。试验将测试脑机接口的安全性和有效性，患者可通过意念控制电脑或手机。马斯克表示，长期愿景是实现人类与AI的共生。",
        "tag": "科技",
        "image_prompt": "Futuristic brain-computer interface concept, neural network connections glowing inside human brain silhouette, patient using thought to control computer cursor, medical technology laboratory setting, photorealistic, ultra detailed, 8K, high resolution, medical innovation"
    },
    {
        "number": "20",
        "title": "德国发生严重高速公路车祸 涉及40辆汽车致12人死亡",
        "summary": "德国A9高速公路发生严重连环车祸，涉及约40辆汽车，已造成12人死亡、50多人受伤。事故发生在能见度较低的大雾天气条件下，多辆卡车连环追尾。德国总理对遇难者表示哀悼，承诺全力进行救援和善后工作。事故引发对高速公路安全标准的讨论。",
        "tag": "社会",
        "image_prompt": "Emergency scene on German highway with multiple vehicles crashed, fire trucks and ambulances with flashing lights, foggy weather conditions, emergency responders helping injured people, photorealistic, ultra detailed, 8K, high resolution, traffic accident emergency"
    }
]

def generate_image(news_num, prompt, retries=2):
    """Generate image using CogView-3-Flash API"""
    filename = f"{IMAGES_DIR}/news_{DATE}_{news_num}.png"
    
    # Check if image already exists
    if os.path.exists(filename):
        print(f"Image {filename} already exists, skipping generation")
        return filename
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = json.dumps({
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }, ensure_ascii=False).encode("utf-8")
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                API_URL,
                data=data,
                headers=headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                content = result["choices"][0]["message"]["content"]
            
            # Handle different response formats
            image_url = None
            if isinstance(content, list):
                # Format: [{"url": "https://..."}]
                image_url = content[0].get("url")
            elif isinstance(content, str):
                if "data:image" in content:
                    b64_data = content.split("data:image/png;base64,")[1]
                    image_data = base64.b64decode(b64_data)
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    print(f"Generated image for news {news_num}: {filename}")
                    return filename
                elif "http" in content:
                    # Could be a URL string
                    image_url = content
            
            if image_url:
                # Download the image
                print(f"Downloading image from: {image_url[:60]}...")
                with urllib.request.urlopen(image_url, timeout=60) as img_resp:
                    image_data = img_resp.read()
                    with open(filename, "wb") as f:
                        f.write(image_data)
                    print(f"Generated image for news {news_num}: {filename}")
                    return filename
            else:
                print(f"Unexpected content format for news {news_num}: {type(content)}, trying again...")
                
        except Exception as e:
            print(f"Error generating image for news {news_num} (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(3)
    
    print(f"Failed to generate image for news {news_num} after {retries} attempts")
    return None


def update_index_html(news_items):
    """Update index.html with new news content"""
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Update title and date in the HTML
    html = re.sub(r"<title>.*?</title>", f"<title>{DATE_CN} 环球新闻</title>", html)
    html = re.sub(
        r'<meta name="description" content=".*?">',
        f'<meta name="description" content="{DATE_CN}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">',
        html
    )
    
    # Update cover subtitle date
    html = re.sub(
        r'<p class="cover-subtitle">.*?</p>',
        f'<p class="cover-subtitle">全球20条热点新闻 · {DATE_CN}</p>',
        html
    )
    
    # Build new news cards HTML
    new_cards = []
    for item in news_items:
        img_path = f"images/news_{DATE}_{item['number']}.png"
        card_html = f'''<article class="news-card" data-tag="{item["tag"]}">
    <img class="news-image" src="{img_path}" alt="{item["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{item["number"]}</span>
        <h3 class="news-title">{item["title"]}</h3>
        <p class="news-summary">{item["summary"]}</p>
        <div><span class="tag">{item["tag"]}</span></div>
    </div>
</article>'''
        new_cards.append(card_html)
    
    new_cards_html = "\n".join(new_cards)
    
    # Replace the news grid section
    pattern = r'<div class="news-grid" id="newsGrid">.*?</div>\s*\n\s*</div>'
    replacement = f'<div class="news-grid" id="newsGrid">\n{new_cards_html}\n</div>\n\n            </div>'
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Updated index.html with {len(news_items)} news items")


def main():
    print(f"Starting news update for {DATE_CN}")
    print(f"=" * 60)
    
    # Generate images for all news items
    print("\nGenerating images...")
    for i, item in enumerate(NEWS_ITEMS):
        print(f"[{i+1}/20] Generating image for news {item['number']}: {item['title'][:30]}...")
        result = generate_image(item['number'], item['image_prompt'])
        if result:
            print(f"  ✓ Success")
        else:
            print(f"  ✗ Failed")
        # Small delay between requests
        if i < len(NEWS_ITEMS) - 1:
            time.sleep(1)
    
    # Update HTML
    print("\nUpdating index.html...")
    update_index_html(NEWS_ITEMS)
    
    print(f"\n{'=' * 60}")
    print(f"News update for {DATE_CN} complete!")
    print(f"Images saved to: {IMAGES_DIR}/news_{DATE}_*.png")


if __name__ == "__main__":
    main()