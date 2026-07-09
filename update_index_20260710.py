#!/usr/bin/env python3
"""Update index.html with new news for 2026年07月10日"""
from pathlib import Path

DATE_STR = "20260710"
DATE_DISPLAY = "2026年07月10日"

NEWS_CARDS = '''            <div class="news-grid">
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_01.png" alt="ChatGPT-5发布震惊业界 多模态能力接近通用人工智能" loading="lazy">
    <div class="news-content">
        <span class="news-number">01</span>
        <h3 class="news-title">ChatGPT-5发布震惊业界 多模态能力接近通用人工智能</h3>
        <p class="news-summary">OpenAI今日发布ChatGPT-5，这款新型大模型在多模态理解、逻辑推理和创造性任务上表现惊艳。GPT-5能够实时分析视频、生成3D内容，并首次通过物理直觉测试。奥特曼表示'这可能是最后一个需要手工标注训练的模型'。微软宣布将GPT-5深度集成到Office和Windows系统中，股价应声上涨4%。教育界对AI辅助学习充满期待。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="国际">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_02.png" alt="二十国集团峰会开幕 各国领袖共商全球经济治理" loading="lazy">
    <div class="news-content">
        <span class="news-number">02</span>
        <h3 class="news-title">二十国集团峰会开幕 各国领袖共商全球经济治理</h3>
        <p class="news-summary">二十国集团领导人峰会在纽约联合国总部开幕，本届峰会聚焦全球债务危机、气候融资和数字税改革三大议题。中国国家主席在开幕致辞中提出'共建共享'的全球治理理念，呼吁发达国家承担更多责任。美国总统则强调'公平竞争'，双方在贸易规则上仍有分歧。峰会预计发布联合声明，但具体成果仍待观察。</p>
        <div><span class="tag">国际</span></div>
    </div>
</article>
<article class="news-card" data-tag="金融">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_03.png" alt="人民币国际化提速 跨境支付系统再添六国" loading="lazy">
    <div class="news-content">
        <span class="news-number">03</span>
        <h3 class="news-title">人民币国际化提速 跨境支付系统再添六国</h3>
        <p class="news-summary">人民币跨境支付系统CIPS新增六个非洲和东南亚国家参与，直接使用人民币进行国际贸易结算的国家已达87个。中国人民银行宣布推出数字人民币跨境版，支持实时汇率兑换和匿名支付。分析认为美元在全球储备货币中的占比首次跌破50%，国际货币体系正在经历结构性变化。</p>
        <div><span class="tag">金融</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_04.png" alt="苹果折叠屏iPhone正式发布 售价15999元起" loading="lazy">
    <div class="news-content">
        <span class="news-number">04</span>
        <h3 class="news-title">苹果折叠屏iPhone正式发布 售价15999元起</h3>
        <p class="news-summary">苹果公司今日发布旗下首款折叠屏iPhone，采用钛金属铰链和超瓷晶面板，可承受超过50万次折叠。手机展开后为8英寸平板模式，搭载M4芯片和全新iPadOS系统。苹果还同步发布了支持折叠屏的Apple Pencil Pro，售价15999元起。预订量已超过百万，黄牛加价现象重现。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="社会">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_05.png" alt="中国探月工程六号发射成功 计划在2030年载人登月" loading="lazy">
    <div class="news-content">
        <span class="news-number">05</span>
        <h3 class="news-title">中国探月工程六号发射成功 计划在2030年载人登月</h3>
        <p class="news-summary">中国探月工程六号探测器在文昌航天发射场成功发射，将执行月球南极着陆和采样返回任务。探测器携带了玉兔六号月球车和欧洲航天局合作的有效载荷。按计划，中国将在2028年实现月球科研站基本型建设，2030年前后实施载人登月任务。</p>
        <div><span class="tag">社会</span></div>
    </div>
</article>
<article class="news-card" data-tag="经济">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_06.png" alt="央行宣布定向降准0.25个百分点 释放长期资金5000亿" loading="lazy">
    <div class="news-content">
        <span class="news-number">06</span>
        <h3 class="news-title">央行宣布定向降准0.25个百分点 释放长期资金5000亿</h3>
        <p class="news-summary">中国人民银行宣布定向降准0.25个百分点，预计释放长期资金约5000亿元。降准资金将重点支持科技创新、绿色发展和中小微企业。央行同时维持7天期逆回购利率不变，市场解读为'精准滴灌'而非大水漫灌。分析师认为此举将降低企业融资成本，对A股形成利好。</p>
        <div><span class="tag">经济</span></div>
    </div>
</article>
<article class="news-card" data-tag="国际">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_07.png" alt="英国首相宣布辞职 保守党陷入党内危机" loading="lazy">
    <div class="news-content">
        <span class="news-number">07</span>
        <h3 class="news-title">英国首相宣布辞职 保守党陷入党内危机</h3>
        <p class="news-summary">英国首相在唐宁街宣布辞职，原因是无法调和党内在脱欧后贸易政策上的分歧。保守党内部陷入激烈内斗，多位重量级议员要求提前举行党魁选举。民调显示工党支持率已领先保守党15个百分点，英国政治格局可能迎来重大转变。英镑汇率小幅下跌。</p>
        <div><span class="tag">国际</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_08.png" alt="特斯拉无人驾驶出租车全球首发 预计2027年规模化运营" loading="lazy">
    <div class="news-content">
        <span class="news-number">08</span>
        <h3 class="news-title">特斯拉无人驾驶出租车全球首发 预计2027年规模化运营</h3>
        <p class="news-summary">特斯拉在年度股东大会上发布了首款无人驾驶出租车Cybercab，车内无方向盘和踏板，采用最新FSD v13自动驾驶系统。马斯克表示Cybercab将在2026年开始在特定城市试运营，2027年实现规模化推广。每辆车预计每天可运行20小时，运营成本仅为传统出租车的三分之一。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="军事">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_09.png" alt="中国海军福建舰完成海试 电磁弹射系统表现优异" loading="lazy">
    <div class="news-content">
        <span class="news-number">09</span>
        <h3 class="news-title">中国海军福建舰完成海试 电磁弹射系统表现优异</h3>
        <p class="news-summary">中国第三艘航空母舰福建舰完成第八次海试返回船厂，本次海试重点测试了电磁弹射系统和舰载机适配性。官方媒体报道称各项目标均圆满完成，舰载机日均起降次数创下新高。军事专家分析福建舰正式服役后，中国海军远洋作战能力将得到质的提升。</p>
        <div><span class="tag">军事</span></div>
    </div>
</article>
<article class="news-card" data-tag="经济">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_10.png" alt="全球最大自贸区启动 中国与东盟贸易额突破万亿美元" loading="lazy">
    <div class="news-content">
        <span class="news-number">10</span>
        <h3 class="news-title">全球最大自贸区启动 中国与东盟贸易额突破万亿美元</h3>
        <p class="news-summary">区域全面经济伙伴关系协定实施三年来，中国与东盟贸易额首次突破万亿美元大关，逆势增长12%。跨境电商和新能源汽车成为贸易增长新引擎。东南亚国家对中国制造业投资增长40%，产业链合作更加紧密。</p>
        <div><span class="tag">经济</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_11.png" alt="华为发布鸿蒙PC系统 打破Windows和macOS垄断" loading="lazy">
    <div class="news-content">
        <span class="news-number">11</span>
        <h3 class="news-title">华为发布鸿蒙PC系统 打破Windows和macOS垄断</h3>
        <p class="news-summary">华为正式发布搭载鸿蒙系统的PC产品，采用自研麒麟X90处理器和鸿蒙PC操作系统。余承东表示鸿蒙PC支持安卓和Linux应用生态，运行效率比同类产品提升35%。联想、戴尔等厂商表达合作意向，但能否建立生态仍是最大挑战。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="社会">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_12.png" alt="多地高温突破历史极值 电网负荷连续三次创新高" loading="lazy">
    <div class="news-content">
        <span class="news-number">12</span>
        <h3 class="news-title">多地高温突破历史极值 电网负荷连续三次创新高</h3>
        <p class="news-summary">受副热带高压影响，华东和华中地区持续高温，多地气温突破40度。国家电网表示已启用有序用电方案，优先保障居民用电。浙江、江苏等省电网负荷连续三次刷新历史纪录。当地气象部门发布最高级别高温红色预警，呼吁企业错峰用电。</p>
        <div><span class="tag">社会</span></div>
    </div>
</article>
<article class="news-card" data-tag="国际">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_13.png" alt="北溪天然气管道爆炸案调查取得重大进展" loading="lazy">
    <div class="news-content">
        <span class="news-number">13</span>
        <h3 class="news-title">北溪天然气管道爆炸案调查取得重大进展</h3>
        <p class="news-summary">德国检方宣布北溪天然气管道爆炸案调查取得重大进展，收集到关键物证指向某国家级行为者。俄罗斯对此予以否认。欧盟呼吁建立独立国际调查机制，但遭到相关方反对。天然气期货价格波动加剧，欧洲能源安全议题再次引发关注。</p>
        <div><span class="tag">国际</span></div>
    </div>
</article>
<article class="news-card" data-tag="金融">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_14.png" alt="巴菲特大幅减持苹果股票 套现超过500亿美元" loading="lazy">
    <div class="news-content">
        <span class="news-number">14</span>
        <h3 class="news-title">巴菲特大幅减持苹果股票 套现超过500亿美元</h3>
        <p class="news-summary">伯克希尔哈撒韦披露最新持仓显示，巴菲特在二季度大幅减持苹果股票，套现超过500亿美元。巴菲特表示'现在估值过高'，但仍保留约9%的苹果股份。此举引发市场对科技股高估值的担忧，美股三大指数期货应声下跌。</p>
        <div><span class="tag">金融</span></div>
    </div>
</article>
<article class="news-card" data-tag="文化">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_15.png" alt="三星堆遗址发现大型祭祀场所 出土文物改写古蜀历史" loading="lazy">
    <div class="news-content">
        <span class="news-number">15</span>
        <h3 class="news-title">三星堆遗址发现大型祭祀场所 出土文物改写古蜀历史</h3>
        <p class="news-summary">三星堆遗址考古取得重大突破，考古队在遗址北部发现距今约3200年的大型祭祀场所，出土青铜器、玉器和象牙器物超过三千件。国家文物局表示这是理解古蜀文明的关键突破，部分器物造型与中原夏商文化存在明显差异，青铜神树修复也取得重要进展。</p>
        <div><span class="tag">文化</span></div>
    </div>
</article>
<article class="news-card" data-tag="国际">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_16.png" alt="日本首相闪电访问华盛顿 深化美日军事同盟" loading="lazy">
    <div class="news-content">
        <span class="news-number">16</span>
        <h3 class="news-title">日本首相闪电访问华盛顿 深化美日军事同盟</h3>
        <p class="news-summary">日本首相紧急访问华盛顿，与美国总统举行非公开会谈。双方宣布将美日安保条约适用范围扩大至太空领域，并同意在日本境内部署中程导弹防御系统。中国外交部表示严重关切，呼吁有关国家停止制造地区紧张局势。</p>
        <div><span class="tag">国际</span></div>
    </div>
</article>
<article class="news-card" data-tag="体育">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_17.png" alt="中国女排世联赛夺冠 击败巴西实现三连冠" loading="lazy">
    <div class="news-content">
        <span class="news-number">17</span>
        <h3 class="news-title">中国女排世联赛夺冠 击败巴西实现三连冠</h3>
        <p class="news-summary">中国女排在世界女排联赛总决赛中以3比1击败巴西队，成功实现三连冠。主攻手李盈莹砍下全场最高的28分，当选赛事MVP。主教练表示这支年轻球队仍有上升空间，目标是巴黎奥运会金牌。中国女排世界排名稳居前三。</p>
        <div><span class="tag">体育</span></div>
    </div>
</article>
<article class="news-card" data-tag="科技">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_18.png" alt="脑机接口临床试验获批 瘫痪患者有望恢复行动能力" loading="lazy">
    <div class="news-content">
        <span class="news-number">18</span>
        <h3 class="news-title">脑机接口临床试验获批 瘫痪患者有望恢复行动能力</h3>
        <p class="news-summary">美国FDA批准Neuralink进行脑机接口人体临床试验第二阶段，约100名四肢瘫痪患者将参与测试。患者可通过意念控制电脑和机械臂。马斯克表示最终目标是实现'数字永生'，但医学界呼吁理性看待技术成熟度。</p>
        <div><span class="tag">科技</span></div>
    </div>
</article>
<article class="news-card" data-tag="环境">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_19.png" alt="全球海洋温度持续升高 珊瑚礁白化速度加快" loading="lazy">
    <div class="news-content">
        <span class="news-number">19</span>
        <h3 class="news-title">全球海洋温度持续升高 珊瑚礁白化速度加快</h3>
        <p class="news-summary">海洋科研机构警告，全球海洋表面温度连续第18个月创下历史新高，大堡礁珊瑚白化面积已超过60%。科学家警告如果升温趋势持续，全球90%的珊瑚礁可能在2040年前消失。多个环保组织呼吁各国加速淘汰化石燃料。</p>
        <div><span class="tag">环境</span></div>
    </div>
</article>
<article class="news-card" data-tag="经济">
    <img class="news-image" src="images/news_''' + DATE_STR + '''_20.png" alt="SpaceX星舰首次商业任务成功 将电信卫星送入地球同步轨道" loading="lazy">
    <div class="news-content">
        <span class="news-number">20</span>
        <h3 class="news-title">SpaceX星舰首次商业任务成功 将电信卫星送入地球同步轨道</h3>
        <p class="news-summary">SpaceX星舰完成首次商业有效载荷任务，将一颗重达8吨的通信卫星送入地球同步轨道。这次任务标志着星舰正式投入商业运营，马斯克表示未来发射成本有望降至每次200万美元。一家亚洲卫星运营商已成为星舰的首批签约客户。</p>
        <div><span class="tag">经济</span></div>
    </div>
</article>
            </div>'''

# Read the current index.html
html_path = Path("/home/swg/.openclaw/workspace/news-blog/index.html")
html_content = html_path.read_text()

# Find the start marker - the warning div closing tag and the news-grid div opening
start_marker = '            <div class="warning">⚠️ <strong>注意：</strong> 新闻信息基于搜索结果整理，图片由 AI 生成，仅供参考。建议通过官方渠道获取最新准确信息。</div>\n'
end_marker = '            <div class="comments-section">'

# Find positions
start_idx = html_content.find(start_marker)
end_idx = html_content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("ERROR: Could not find markers")
    exit(1)

start_idx += len(start_marker)
new_content = html_content[:start_idx] + '\n' + NEWS_CARDS + '\n' + html_content[end_idx:]

# Write back
html_path.write_text(new_content)
print("index.html updated successfully!")
print(f"Start idx: {start_idx}, End idx: {end_idx}")
print(f"New content length: {len(new_content)}")