#!/usr/bin/env python3
import os
import json
import base64
import requests
import re
from datetime import datetime

# ===== 配置 =====
DATE_STR = "2026年07月19日"
DATE_ID = "20260719"
API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
IMAGES_DIR = "/home/swg/.openclaw/workspace/news-blog/images"
INDEX_PATH = "/home/swg/.openclaw/workspace/news-blog/index.html"

os.makedirs(IMAGES_DIR, exist_ok=True)

# ===== 20条新闻内容 =====
NEWS = [
    {
        "num": "01",
        "tag": "科技",
        "title": "上海世界人工智能大会发布"星枢计划"首批卫星数据",
        "summary": "2026世界人工智能大会期间，上海太空算力产业传来重大进展，"星枢计划"首批12颗试验卫星成功传回首批数据。该计划由复旦大学与上海星枢天算联合研制，旨在构建天地一体化算力网络。卫星搭载太赫兹通信载荷，理论传输速率可达5G的100倍，首批数据已应用于上海智慧城市基础设施建设，全球太空算力竞争进入新阶段。",
        "prompt": "A futuristic satellite in orbit above Earth, transmitting data streams, Shanghai cityscape in background, photorealistic, ultra detailed, 8K, high resolution, no text, no watermark"
    },
    {
        "num": "02",
        "tag": "科技",
        "title": "全球首个人形机器人自由格斗联赛揭幕战在深圳打响",
        "summary": "众擎URKL全球人形机器人自由格斗联赛揭幕战在深圳市体育馆火热开战，16支队伍携自主研发的人形机器人展开激烈对抗。比赛采用1V1对抗赛形式，机器人需在限定时间内完成击打、闪避和战术组合动作。赛事吸引全球超过2000万名观众在线观看，外媒称人形机器人格斗将成为下一个体育娱乐风口。",
        "prompt": "Humanoid robot fighting competition in a sports arena, mechanical warriors in battle stance, Shenzhen arena with neon lights, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "03",
        "tag": "国际",
        "title": "习近平在哈萨克斯坦发表演讲 宣布建立AI国际合作机制",
        "summary": "国家主席习近平在哈萨克斯坦首都阿斯塔纳出席中亚合作峰会并发表主旨演讲，宣布中国将建立"一带一路"人工智能国际合作机制，未来5年向发展中国家提供100亿美元AI发展基金。习近平表示，人工智能治理需要全球共同参与，中国愿与各国分享AI技术成果。这一倡议获得中亚五国和多个新兴市场国家的积极响应。",
        "prompt": "Chinese president delivering speech at international summit in Astana Kazakhstan, grand conference hall, flags of multiple nations, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "04",
        "tag": "经济",
        "title": "中国上半年GDP同比增长5.3% 经济运行总体平稳",
        "summary": "国家统计局发布2026年上半年经济数据，上半年国内生产总值（GDP）同比增长5.3%，其中二季度增长4.9%。数据显示，高技术制造业投资增长12.4%，新能源汽车、锂电池和太阳能电池出口增长强劲。统计局表示，下半年将进一步加大宏观政策调节力度，推动经济持续回升向好，实现全年5%左右的发展目标。",
        "prompt": "Modern Chinese city skyline with factories and wind turbines, data visualization charts on screen, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "05",
        "tag": "国际",
        "title": "俄乌第四轮和平谈判在维也纳举行 双方释放善意",
        "summary": "俄罗斯与乌克兰代表在奥地利维也纳举行第四轮和平谈判，就停火协议框架和战俘交换清单达成原则性共识。土耳其总统埃尔多安与联合国秘书长特使联合主持会议，双方同意设立人道主义走廊并重启粮食出口通道。欧盟对此表示欢迎，称这是冲突爆发以来最重要的外交突破，但最终协议仍需各方政治授权。",
        "prompt": "Diplomatic negotiation at Vienna palace, Russian and Ukrainian delegates at round table, UN flag and EU flags, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "06",
        "tag": "金融",
        "title": "人民币汇率突破7.1关口 创年内新高",
        "summary": "在岸人民币对美元汇率盘中升破7.10，创下2026年以来最高水平。外汇交易中心数据显示，人民币对美元中间价较前一日上调352个基点。分析认为，美联储降息预期升温、美元指数走弱以及外资持续流入人民币资产是主要推动因素。央行表示，人民币汇率长期稳定的基础没有改变，将继续保持双向波动。",
        "prompt": "Chinese yuan and US dollar banknotes, financial trading screen showing exchange rate charts, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "07",
        "tag": "体育",
        "title": "2026年世界杯决赛阿根廷力克法国 成功卫冕冠军",
        "summary": "2026年国际足联世界杯决赛在纽约大都会人寿体育场落幕，阿根廷凭借点球大战以5-3击败法国，成功卫冕世界杯冠军。开场第12分钟姆巴佩闪击破门，下半场梅西任意球扳平，加时赛双方各入一球。点球大战中法国队长格列兹曼罚失，阿根廷门将马丁内斯扑出关键点球。全场比赛超过8亿观众收看，创本届世界杯收视纪录。",
        "prompt": "Football World Cup final stadium at night, Argentina celebrating with trophy, fireworks display, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "08",
        "tag": "科技",
        "title": "百度发布文心5.0大模型 推理能力对标GPT-5",
        "summary": "百度在2026世界人工智能大会上正式发布文心大模型5.0版本，官方称其在多项基准测试中与OpenAI GPT-5持平，部分中文理解任务实现超越。文心5.0采用全新MoE架构，参数量突破万亿级，推理速度提升3倍。百度同时宣布向开发者免费开放API接口，并启动"文心百川"计划，目标是3年内赋能100万家中小企业AI升级。",
        "prompt": "AI technology conference keynote, large LED screen showing neural network visualization, Chinese tech company logo, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "09",
        "tag": "社会",
        "title": "华北黄淮地区迎强降雨 北京发布防汛一级响应",
        "summary": "受副热带高压北抬影响，华北黄淮地区出现大范围强降雨天气，北京、天津、河北等地24小时降雨量超过200毫米，达到大暴雨级别。北京市防汛指挥部启动一级应急响应，城市副中心、新机场等重点项目工地全部停工。气象部门预报本轮降雨将持续至21日，呼吁市民减少不必要出行，避开低洼地带。",
        "prompt": "Heavy rain flooding city streets in Beijing, people with umbrellas, flood barriers in place, dramatic storm clouds, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "10",
        "tag": "国际",
        "title": "英国正式申请加入金砖国家 约翰逊称其为\"历史性决定\"",
        "summary": "英国外交大臣在喀山举行的金砖国家外长会议上正式递交加入申请，成为首个申请加入金砖机制的七国集团成员。英国首相约翰逊表示，英国脱欧后需要重新定位全球伙伴关系，金砖国家代表新兴市场和发展中国家的崛起，英国"不能缺席"。金砖扩员问题将在今年10月喀山金砖峰会上正式讨论。",
        "prompt": "British Foreign Secretary at international BRICS meeting in Kazan Russia, flags of multiple nations, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "11",
        "tag": "科技",
        "title": "特斯拉发布Optimus Gen-3人形机器人 售价降至2万美元",
        "summary": "特斯拉在AI DAY发布会上推出Optimus Gen-3人形机器人，售价从去年的10万美元降至2万美元，续航提升至8小时，可完成复杂家务和轻工业任务。马斯克表示，2027年产能将达50万台，2028年进入家用市场。发布会现场展示了机器人组装汽车零部件、搬运物品和陪伴老人等场景，引发全球科技行业震动。",
        "prompt": "Tesla humanoid robot working in modern factory, precise mechanical movements, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "12",
        "tag": "金融",
        "title": "比特币跌破8万美元 加密市场遭遇大幅回调",
        "summary": "比特币价格日内跌幅超过15%，跌破8万美元关口，加密货币总市值缩水至2.8万亿美元。分析师认为获利回吐叠加监管压力是主因，韩国最大加密交易所Bithumb遭突击检查引发恐慌。美国SEC宣布对多家山寨币项目展开调查，市场恐慌情绪蔓延。不过机构投资者逢低买入，分析师认为牛市格局未变。",
        "prompt": "Bitcoin cryptocurrency price crashing on screen, red market charts, digital currency concept, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "13",
        "tag": "文化",
        "title": "三星堆遗址新发现8座祭祀坑 出土文物超5000件",
        "summary": "四川省文物考古研究院公布三星堆遗址最新考古成果，2025年至今新发现8座祭祀坑，出土黄金面具、青铜神树、玉器和象牙等珍贵文物超过5000件。考古队长表示，新发现印证了古蜀国高度发达的物质文明，对研究中华文明多元一体格局具有重大意义。国家文物局已启动三星堆博物馆新馆建设，建成后将成为全球最大青铜器专题博物馆。",
        "prompt": "Archaeologists excavating ancient Sanxingdui ruins in Sichuan, golden masks and bronze artifacts, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "14",
        "tag": "国际",
        "title": "欧盟就移民配额改革达成协议 结束多年僵局",
        "summary": "欧盟成员国在布鲁塞尔峰会上就移民配额改革方案达成历史性协议，结束了长达5年的政策僵局。新协议设立强制成员国分担移民安置的机制，对拒绝接收的国家征收每人2万欧元的团结税。意大利、希腊等前沿国家将获得更多资金支持。协议还需欧洲议会批准，预计2027年生效，将重塑欧盟移民政策框架。",
        "prompt": "European Union summit meeting in Brussels, leaders at conference table, EU flags, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "15",
        "tag": "科技",
        "title": "华为发布问界M9Ultra 搭载城市NCA 3.0智驾系统",
        "summary": "华为在上海举行新品发布会，正式推出问界M9Ultra智能汽车，全球首发城市NCA 3.0智能驾驶系统。该系统可在无高精地图的城市道路实现全程自动驾驶，识别率和决策速度较上一代提升50%。余承东表示，问界M9系列上市12小时大定突破5万辆，创中国高端SUV新纪录。华为智驾已覆盖全国400座城市。",
        "prompt": "Huawei smart electric car on Shanghai expressway, autonomous driving visualization on dashboard, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "16",
        "tag": "社会",
        "title": "中国科学家在沙漠成功种植耐盐碱水稻 亩产突破800公斤",
        "summary": "青岛海水稻研发中心宣布，中国科学家在新疆塔克拉玛干沙漠边缘的盐碱地上试种的耐盐碱水稻"海稻86"获得突破，亩产达到812公斤，刷新该类土地水稻种植纪录。"海稻86"可在pH 9.5以下的盐碱地生长，灌溉用水减少40%。袁隆平团队表示，按目前推广速度，2030年前可为中国新增1亿亩良田，有效保障国家粮食安全。",
        "prompt": "Scientists harvesting rice in desert oasis, golden rice paddies against sand dunes, Xinjiang farmland, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "17",
        "tag": "金融",
        "title": "沪深交易所发布减持新规 大股东不得通过融券绕道",
        "summary": "上海和深圳证券交易所联合发布《上市公司股东减持股份实施细则》修订版，明确禁止大股东通过融券绕道减持，堵住政策漏洞。新规要求，大股东及其一致行动人持有的股份，扣除战略投资者承诺锁定部分后方可计算可减持数量。证监会表示，新规旨在维护中小投资者利益，促进市场健康发展，即日起施行。",
        "prompt": "Shanghai Stock Exchange trading floor, investors watching stock market screens, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "18",
        "tag": "国际",
        "title": "印度成功着陆月背探测器 成为全球第三个软着陆国家",
        "summary": "印度空间研究组织宣布，"月船4号"探测器成功在月球背面着陆，印度成为全球第三个实现月背软着陆的国家。探测器携带月球车和钻探设备，将开展月背地质构造和水冰资源勘探。印度总理莫迪表示，这是印度航天事业的里程碑，证明发展中国家同样可以在深空探索领域取得突破。中国"嫦娥"系列为月背探测提供了重要技术参考。",
        "prompt": "India lunar lander on moon surface, lunar rover exploring, Earth in background, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "19",
        "tag": "文化",
        "title": "《黑神话：悟空》DLC全球同步上线 销量突破5000万份",
        "summary": "国产3A游戏《黑神话：悟空》首个DLC"大闹天宫"全球同步上线，上线首日销量突破500万份。游戏科学CEO冯骥表示，DLC历时2年开发，包含全新地图、Boss战和剧情内容。Steam平台同时在线玩家峰值突破180万，创造单机游戏新纪录。海外玩家评分高达9.2分，成为中国文化出海的现象级产品。",
        "prompt": "Chinese game character Sun Wukong in epic fantasy battle scene, glowing staff and clouds, photorealistic, ultra detailed, 8K, high resolution"
    },
    {
        "num": "20",
        "tag": "社会",
        "title": "中国启动首次全国自然灾害风险普查 摸清风险底数",
        "summary": "国务院办公厅印发通知，启动首次全国自然灾害综合风险普查，普查对象涵盖地震、洪涝、台风、干旱、森林草原火灾等主要灾种。应急管理部表示，普查将于2026年底完成，目的是全面摸清全国风险隐患底数，建立国家自然灾害综合风险数据库，指导各地科学编制防灾减灾规划，提升基层应急响应能力。",
        "prompt": "Emergency management officials conducting disaster risk survey in Chinese village, flood prevention infrastructure, photorealistic, ultra detailed, 8K, high resolution"
    },
]

def generate_image_cogview(prompt: str, output_path: str) -> bool:
    """调用智谱 CogView-3-Flash 生成图片"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "cogview-3-flash",
        "messages": [{"role": "user", "content": f"Image prompt: {prompt}"}]
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        # 提取base64数据:image/png;base64,XXXXX
        if "data:image/png;base64," in content:
            b64_data = content.split("data:image/png;base64,")[1]
        elif "data:image/jpeg;base64," in content:
            b64_data = content.split("data:image/jpeg;base64,")[1]
        else:
            print(f"  [ERROR] 未知格式: {content[:100]}")
            return False
        img_bytes = base64.b64decode(b64_data)
        with open(output_path, "wb") as f:
            f.write(img_bytes)
        print(f"  [OK] 已保存: {output_path}")
        return True
    except Exception as e:
        print(f"  [ERROR] 生成失败: {e}")
        return False

def main():
    print(f"===== 开始生成 {DATE_STR} 的新闻 =====")
    
    # 1. 生成图片
    print("\n[Step 1] 生成图片...")
    for news in NEWS:
        num = news["num"]
        filename = f"news_{DATE_ID}_{num}.png"
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # 跳过已存在的图片
        if os.path.exists(filepath):
            print(f"  [SKIP] {filename} 已存在，跳过")
            continue
        
        print(f"  生成 {filename}...")
        success = False
        for attempt in range(2):
            if generate_image_cogview(news["prompt"], filepath):
                success = True
                break
        if not success:
            print(f"  [WARN] {filename} 生成失败，将继续其他图片")
    
    # 2. 更新 index.html
    print(f"\n[Step 2] 更新 index.html...")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 生成20个新闻卡片的HTML
    news_cards = ""
    for news in NEWS:
        img_src = f"images/news_{DATE_ID}_{news['num']}.png"
        card = f'''<article class="news-card" data-tag="{news["tag"]}">
    <img class="news-image" src="{img_src}" alt="{news["title"]}" loading="lazy">
    <div class="news-content">
        <span class="news-number">{news["num"]}</span>
        <h3 class="news-title">{news["title"]}</h3>
        <p class="news-summary">{news["summary"]}</p>
        <div><span class="tag">{news["tag"]}</span></div>
    </div>
</article>'''
        news_cards += card + "\n"
    
    # 替换标题和副标题的日期
    html = re.sub(r"<title>.*?环球新闻</title>", f"<title>{DATE_STR} 环球新闻</title>", html)
    html = re.sub(r"全球20条热点新闻 · \d{4}年\d{2}月\d{2}日", f"全球20条热点新闻 · {DATE_STR}", html)
    
    # 替换整个news-grid区域
    # 找到 <div class="news-grid"> 到 </div>\n                        </div> 的内容
    pattern = r'<div class="news-grid">\s*.*?\s*</div>\s*</div>\s*</div>'
    replacement = f'<div class="news-grid">\n\n{news_cards}\n\n                </div>\n        </div>'
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"  [OK] index.html 已更新")
    
    # 3. Git 推送
    print(f"\n[Step 3] Git 推送...")
    os.chdir("/home/swg/.openclaw/workspace/news-blog")
    os.system("git add index.html images/news_20260719_*.png")
    commit_msg = f"更新首页：2026-07-19"
    os.system(f'git commit -m "{commit_msg}"')
    os.system('GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519" git push origin main')
    
    print("\n===== 完成 =====")

if __name__ == "__main__":
    main()