#!/usr/bin/env python3
"""Generate news and images for 2026年07月07日"""
import base64
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# Constants
DATE = "20260707"
DATE_CN = "2026年07月07日"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
REPO_DIR = Path("/home/swg/.openclaw/workspace/news-blog")
IMAGES_DIR = REPO_DIR / "images"

# News data for July 7, 2026
NEWS_ITEMS = [
    {
        "number": "01",
        "title": "世界杯决赛：阿根廷点球大战击败法国 梅西宣布从国家队退役",
        "summary": "2026年美加墨世界杯决赛在迈阿密硬石体育场精彩落幕，阿根廷通过点球大战5-3战胜法国，成功卫冕世界杯冠军。法国前锋姆巴佩在点球大战中罚失关键点球，35岁的梅西赛后正式宣布从国家队退役。全球超过25亿观众通过直播见证了这一历史性时刻，法国总统马克龙现场观战并称赞法国队的拼搏精神。",
        "tag": "体育",
        "prompt": "A dramatic football stadium scene at night, World Cup final match, Argentine players celebrating with trophy, fireworks display, crowd of 80000 spectators, photorealistic, ultra detailed, 8K, high resolution, no text or watermarks"
    },
    {
        "number": "02",
        "title": "中俄\"海上联合-2026\"演习在青岛启动 规模创历年之最",
        "summary": "中俄\"海上联合-2026\"联合演习在山东青岛正式启动，这是两国海军首次在青岛举行如此大规模演习。中方派出驱逐舰、护卫舰、潜艇等多型主战舰艇参演，俄方舰艇编队也已抵达青岛军港。演习将重点围绕海上联合补给、联合反潜、防空等科目展开，旨在深化两国海军务实合作，提升协同作战能力。",
        "tag": "国际",
        "prompt": "Naval warships at a busy military port, Chinese and Russian navies conducting joint maritime exercises, destroyers and frigates docked, naval officers on deck, Qingdao China, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "03",
        "title": "特朗普与普京通话提议调解俄乌战争 北约峰会前引发国际关注",
        "summary": "美国前总统特朗普与俄罗斯总统普京进行电话会谈后表示，愿意帮助调解结束俄乌战争。克里姆林宫发言人称这次通话\"具有建设性意义\"。乌克兰总统泽连斯基随后表示已与特朗普通话，讨论了长达1200公里的前线局势。北约峰会即将召开，各方就如何结束冲突展开密集外交斡旋，国际社会对此高度关注。",
        "tag": "国际",
        "prompt": "Diplomatic meeting scene, two world leaders shaking hands, international summit setting with flags, serious expressions, photorealistic, ultra detailed, 8K, no text or watermarks"
    },
    {
        "number": "04",
        "title": "中国海军舰艇编队穿越日本四大海峡 7艘舰艇部署西太平洋",
        "summary": "日本防卫省统合幕僚监部发布消息，中国海军舰艇编队近日穿越吐噶喇海峡、冲绳本岛与宫古岛之间海域、大隅海峡和对马海峡等日本四大要道。目前至少有7艘中国舰艇部署在西太平洋海域，活动频率和规模创近年新高。日本自卫队全程跟踪监视，并已通过外交渠道向中方表达关切。",
        "tag": "军事",
        "prompt": "Chinese naval fleet warships sailing in formation through ocean strait, Japanese coastline visible in background, military vessels with flags, open sea, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "05",
        "title": "智谱AI发布GLM-5.3多模态大模型 视频理解能力超越GPT-5",
        "summary": "中国人工智能企业智谱AI发布新一代多模态大模型GLM-5.3，在视频理解、图像分析和文本生成等多项国际基准测试中超越GPT-5。该模型首次实现对长视频的完整理解与深度分析，支持一键生成专业级视频解说词。智谱AI同时宣布GLM-5.3 API价格仅为GPT-5的十分之一，将大幅降低企业AI应用成本。",
        "tag": "科技",
        "prompt": "Futuristic AI technology laboratory, researchers working with holographic displays showing neural network visualizations, cutting-edge server rooms, Chinese tech company setting, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "06",
        "title": "比特币重返11万美元关口 机构资金持续涌入加密货币市场",
        "summary": "比特币价格重返11万美元关口，为2026年以来首次创下历史新高。机构投资者持续涌入加密货币市场，贝莱德、富达等资管巨头的比特币ETF持仓量持续增加。分析师认为美联储降息预期、比特币减半效应以及机构采用率提升是本轮上涨的主要驱动力。加密货币总市值突破3.5万亿美元。",
        "tag": "金融",
        "prompt": "Digital cryptocurrency concept art, Bitcoin coin with glowing effect, financial trading charts on screens, modern trading floor with holographic displays, photorealistic, ultra detailed, 8K, no text watermarks"
    },
    {
        "number": "07",
        "title": "达沃斯科技峰会2026在辽宁开幕 全球科技领袖共商AI伦理",
        "summary": "达沃斯科技峰会2026在辽宁省大连市隆重开幕，主题为\"在变局中构建科技未来\"。全球2000多名科技领袖、企业家和学者参会，重点讨论人工智能伦理治理、量子计算突破、太空商业化等议题。中国领导人出席开幕式并发表主旨演讲，强调构建开放包容的全球科技治理体系。",
        "tag": "科技",
        "prompt": "International technology summit conference venue, large auditorium with global tech leaders on stage, holographic displays showing AI and quantum computing visuals, WEF Davos style event in China, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "08",
        "title": "南欧野火肆虐迫使数万人撤离 环法自行车赛被迫改道",
        "summary": "野火在法国南部、西班牙和意大利多地持续蔓延，迫使数万居民紧急撤离家园。法国政府宣布南部四省进入紧急状态，环法自行车赛因途经火区被迫更改路线。欧盟启动民防机制，协调成员国消防资源支援。极端高温天气加剧了火势蔓延，气象部门警告未来几天风险依然很高。",
        "tag": "国际",
        "prompt": "Wildfire burning in Southern European countryside, flames through forests near mountains, firefighters battling blaze, evacuating families with luggage, orange sky, smoke clouds, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "09",
        "title": "乌克兰无人机深入袭击俄罗斯最大炼油厂 距边境2500公里",
        "summary": "乌克兰无人机袭击了俄罗斯西伯利亚地区最大的炼油厂，该设施距离乌克兰边境超过2500公里。此前该炼油厂是俄罗斯十大炼油企业中唯一未被乌军无人机触及的企业。袭击导致炼油厂部分设施起火，俄罗斯防空系统未能有效拦截。能源专家表示，这将影响俄罗斯国内燃油供应和出口能力。",
        "tag": "军事",
        "prompt": "Military drone aircraft in night sky over Russian industrial facility, explosions and fires at oil refinery below, distant battlefield scene, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "10",
        "title": "日本首相高市早苗访问印度 推进经济与安全战略合作",
        "summary": "日本首相高市早苗访问印度新德里，与印度总理莫迪举行会谈，双方探讨深化经济安全与战略合作。两国签署多项合作协议，涉及半导体供应链、清洁能源和国防技术领域。高市早苗表示，日本将加大对印度制造业投资，支持印度成为全球供应链重要一环。舆论认为此举旨在应对地区格局变化。",
        "tag": "国际",
        "prompt": "Japanese Prime Minister meeting with Indian counterpart at official government palace, bilateral summit, flags of both nations, diplomatic setting in New Delhi, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "11",
        "title": "阿里巴巴禁止员工使用Anthropic编程工具 被指进行模型蒸馏",
        "summary": "据多家媒体报道，阿里巴巴将禁止员工使用Anthropic的编程工具Claude Code，该禁令将于7月10日起生效。Anthropic此前已禁止中国公司及在华外资企业使用其模型。报道称阿里巴巴被指控对其Claude模型进行\"蒸馏\"提取能力。阿里随后发表声明否认违规使用，双方关系趋于紧张。",
        "tag": "科技",
        "prompt": "Modern technology company office, programmers working at computers with code on screens, Chinese tech company interior, legal documents and AI chip on desk, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "12",
        "title": "德国\"隐形冠军\"中小企业面临中国竞争压力 寻求政府支持",
        "summary": "德国中小企业群体被称为\"隐形冠军\"，长期是德国经济支柱和出口主力。然而，中国制造业快速升级对这些细分市场龙头形成激烈竞争。德国工业协会呼吁政府加大对中小企业的研发补贴和税收优惠，帮助它们在数字化和绿色转型中保持竞争力。企业主们表示正在积极拥抱新技术应对挑战。",
        "tag": "经济",
        "prompt": "Traditional German precision manufacturing factory interior, workers operating CNC machines, industrial robots assembling components, Mittelstand company workshop, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "13",
        "title": "斯坦福大学发布AI就业报告 75%毕业生使用AI工具完成学业",
        "summary": "斯坦福大学发布2026年AI与就业报告，显示75%的应届毕业生在学业中广泛使用AI工具。报告指出AI正在重塑人类技能结构，部分重复性工作机会减少但新岗位涌现。教育专家呼吁改革课程设置，将AI素养纳入基础培养。调查显示学生们对AI既兴奋又担忧，希望在变革中找准自身定位。",
        "tag": "科技",
        "prompt": "Stanford University campus with iconic redwood trees, students using laptops and AI assistants in modern library, Silicon Valley backdrop, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "14",
        "title": "金饰价格年内跌幅超500元/克 央行购金节奏放缓",
        "summary": "国际金价持续回调，国内金饰价格年内跌幅已超过500元/克。目前10年期美债收益率升至4.6%以上，实际利率回落降低了黄金吸引力。分析指出金饰价格阶段性见顶，央行购金与实物需求中长期配置逻辑未变但短期节奏放缓。消费者观望情绪浓厚，婚庆刚需成为为数不多的支撑因素。",
        "tag": "金融",
        "prompt": "Gold jewelry display in luxury jewelry store, various gold necklaces and bracelets under spotlight, elegant interior, photorealistic, ultra detailed, 8K, no text watermarks"
    },
    {
        "number": "15",
        "title": "王毅与芬兰外长瓦尔托宁会谈 中芬战略伙伴关系持续深化",
        "summary": "当地时间7月5日，中共中央政治局委员、外交部长王毅在赫尔辛基与芬兰外长瓦尔托宁举行会谈。王毅表示，芬兰是最早同新中国建交的西方国家之一，也是第一个同中国签订政府间贸易协定的西方国家。双方就深化经贸合作、应对气候变化、维护多边贸易体系等议题深入交换意见。",
        "tag": "国际",
        "prompt": "Diplomatic meeting in Helsinki government building, Chinese and Finnish foreign ministers shaking hands, flags of both nations on walls, formal diplomatic setting, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "16",
        "title": "欧盟关注中国贸易失衡问题 冯德莱恩重申对话解决立场",
        "summary": "欧盟委员会主席冯德莱恩就欧盟与中国贸易关系发表讲话，表示欧盟应继续就贸易失衡问题同中国进行对话，将明确提出中国过剩商品涌入欧洲市场等问题。欧方呼吁中国采取措施平衡双边贸易，避免部分行业产能过剩冲击欧洲企业。分析认为欧盟寻求务实解决而非对抗的态度。",
        "tag": "国际",
        "prompt": "European Union flag waving in front of European Commission building in Brussels, trade negotiation meeting room inside, diplomats discussing, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "17",
        "title": "日本股市泡沫破裂 央行政策收紧后一年蒸发50%市值",
        "summary": "日本股市经历剧烈调整，主要股指较高点回落超过50%，引发市场对泡沫破裂的担忧。日本央行此前持续收紧货币政策，推动日元升值并压缩出口企业利润。分析认为前期涨幅过大、估值过高是调整主因，日元套利交易平仓加剧了跌势。投资者期待政府采取措施稳定市场情绪。",
        "tag": "金融",
        "prompt": "Tokyo Stock Exchange trading floor with falling stock price displays, worried investors looking at screens, red LED numbers showing decline, photorealistic, ultra detailed, 8K, no text watermarks"
    },
    {
        "number": "18",
        "title": "DeepSeek发布AI推理新突破 效率提升10倍成本下降90%",
        "summary": "中国AI初创公司DeepSeek发布新型推理技术，在保持模型能力的同时将推理效率提升10倍，计算成本下降90%。该公司此前发表相关技术论文后，谷歌也采用类似技术路径。这一突破有望改变AI推理市场的竞争格局，降低中小企业应用AI的门槛，推动生成式AI更广泛落地。",
        "tag": "科技",
        "prompt": "Chinese AI startup office with breakthrough technology visualization, neural network efficiency diagram on screen, data center servers, innovative tech atmosphere, photorealistic, ultra detailed, 8K, no watermarks"
    },
    {
        "number": "19",
        "title": "OpenAI完成新一轮融资 估值达4000亿美元超越Stripe",
        "summary": "人工智能领军企业OpenAI完成新一轮超过100亿美元融资，估值达到4000亿美元，超越Stripe成为全球估值最高的私营科技公司。微软继续跟投，软银愿景基金首次入股。本轮融资将主要用于提升算力资源、招聘顶级AI人才，以及加速GPT-5等下一代模型研发。",
        "tag": "科技",
        "prompt": "Modern tech company headquarters lobby, OpenAI logo visible, venture capital funding concept, digital art showing growth chart, San Francisco office interior, photorealistic, ultra detailed, 8K, no text watermarks"
    },
    {
        "number": "20",
        "title": "耐克大中华区营收连续八季下滑 跌幅超3%加剧市场担忧",
        "summary": "运动品牌耐克公布2026财年第四季度财报，大中华区营收连续第八个季度下滑，跌幅超过3%。耐克表示中国消费者偏好国产品牌、电商竞争加剧以及库存问题是主要挑战。公司宣布加大对中国市场技术投入，但分析师对其扭转颓势持谨慎态度。耐克股价在盘后交易中下跌超过3%。",
        "tag": "经济",
        "prompt": "Nike store interior in shopping mall, sports apparel displays, Chinese consumers shopping, modern retail environment, photorealistic, ultra detailed, 8K, no text watermarks"
    },
]

def generate_image_cogview(news: dict, output_path: Path, retry: int = 2) -> bool:
    """Generate image using CogView-3-Flash API"""
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {news['prompt']}"}]
    }
    
    for attempt in range(retry):
        try:
            result = subprocess.run(
                ["curl", "-s", "-X", "POST", API_URL,
                 "-H", f"Authorization: Bearer {API_KEY}",
                 "-H", "Content-Type: application/json",
                 "-d", json.dumps(payload)],
                capture_output=True, text=True, timeout=120
            )
            
            resp = json.loads(result.stdout)
            if "choices" in resp and resp["choices"]:
                content = resp["choices"][0]["message"]["content"]
                if isinstance(content, list) and len(content) > 0:
                    img_url = content[0].get("url", "")
                    if img_url:
                        # Download image from URL
                        dl_result = subprocess.run(
                            ["curl", "-s", "-o", str(output_path), img_url],
                            capture_output=True, text=True, timeout=60
                        )
                        if dl_result.returncode == 0 and output_path.exists():
                            size = output_path.stat().st_size
                            if size > 1000:  # Valid image
                                print(f"  ✓ {output_path.name} ({size} bytes)")
                                return True
                print(f"  ✗ Attempt {attempt+1} failed: unexpected content format")
            else:
                print(f"  ✗ Attempt {attempt+1} failed: no choices in response")
        except Exception as e:
            print(f"  ✗ Attempt {attempt+1} exception: {e}")
        time.sleep(3)
    
    return False

def main():
    os.chdir(REPO_DIR)
    IMAGES_DIR.mkdir(exist_ok=True)
    
    print(f"=== Generating news and images for {DATE_CN} ===\n")
    
    # Step 1: Generate all 20 images
    print("Step 1: Generating images with CogView-3-Flash...")
    failed = []
    for i, news in enumerate(NEWS_ITEMS):
        num = news["number"]
        img_path = IMAGES_DIR / f"news_{DATE}_{num}.png"
        print(f"  [{i+1}/20] Generating news_{DATE}_{num}.png...", end=" ", flush=True)
        success = generate_image_cogview(news, img_path)
        if not success:
            failed.append((i, news))
            print(f"FAILED")
        time.sleep(2)  # Rate limiting
    
    # Retry failed images
    if failed:
        print(f"\nRetrying {len(failed)} failed images...")
        for i, news in failed:
            num = news["number"]
            img_path = IMAGES_DIR / f"news_{DATE}_{num}.png"
            print(f"  Retrying news_{DATE}_{num}.png...", end=" ", flush=True)
            success = generate_image_cogview(news, img_path)
            if success:
                failed.remove((i, news))
                print("OK")
            else:
                print("FAILED")
            time.sleep(3)
    
    if failed:
        print(f"\n⚠️ {len(failed)} images still failed")
    
    print(f"\n✓ All images done!")
    
    # Step 2: Generate news HTML content
    print("\nStep 2: Generating news HTML content...")
    news_cards = []
    for news in NEWS_ITEMS:
        card = f'''<article class="news-card" data-tag="{news["tag"]}">
    <img class="news-image" src="images/news_{DATE}_{news["number"]}.png" alt="{news["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{news["number"]}</span>
        <h3 class="news-title">{news["title"]}</h3>
        <p class="news-summary">{news["summary"]}</p>
        <div><span class="tag">{news["tag"]}</span></div>
    </div>
</article>'''
        news_cards.append(card)
    
    news_grid_html = "\n".join(news_cards)
    
    # Step 3: Read and update index.html
    print("\nStep 3: Updating index.html...")
    with open(REPO_DIR / "index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Update date in title
    html = html.replace("2026年07月06日", DATE_CN)
    html = html.replace("2026年07月05日", DATE_CN)
    
    # Update meta description
    old_desc = '<meta name="description" content="2026年07月06日全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">'
    new_desc = f'<meta name="description" content="{DATE_CN}全球20条热点新闻，涵盖科技、政治、军事、经济等领域的最新动态">'
    html = html.replace(old_desc, new_desc)
    
    # Replace news grid content
    import re
    pattern = r'<div class="warning">.*?</div>\s*<div class="news-grid" id="newsGrid">\s*.*?</div>\s*</div>\s*<div class="comments-section">'
    replacement = f'<div class="warning">⚠️ <strong>注意：</strong> 新闻信息基于搜索结果整理，图片由 AI 生成，仅供参考。建议通过官方渠道获取最新准确信息。</div>\n                        <div class="news-grid" id="newsGrid">\n{news_grid_html}\n                    </div>\n                    <div class="comments-section">'
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    with open(REPO_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✓ index.html updated!")
    
    # Step 4: Git operations
    print("\nStep 4: Git operations...")
    result = subprocess.run(
        ["git", "add", "index.html"] + [f"images/news_{DATE}_{str(i).zfill(2)}.png" for i in range(1, 21)],
        cwd=REPO_DIR, capture_output=True, text=True
    )
    print(f"  Git add: done")
    
    commit_msg = f"更新首页：2026-07-07"
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        cwd=REPO_DIR, capture_output=True, text=True,
        env={**os.environ, "GIT_SSH_COMMAND": "ssh -i ~/.ssh/id_ed25519"}
    )
    print(f"  Commit: {result.stdout.strip()}")
    if result.stderr:
        print(f"  Stderr: {result.stderr.strip()[:200]}")
    
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=REPO_DIR, capture_output=True, text=True,
        env={**os.environ, "GIT_SSH_COMMAND": "ssh -i ~/.ssh/id_ed25519"}
    )
    if "error" in result.stderr.lower() or "failed" in result.stderr.lower():
        print(f"  Push FAILED: {result.stderr.strip()[:300]}")
    else:
        print(f"  Push: success")
    
    print("\n=== ALL DONE ===")

if __name__ == "__main__":
    main()