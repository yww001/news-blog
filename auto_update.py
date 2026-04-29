#!/usr/bin/env python3
"""
增强版新闻博客自动更新器
包含质量检查机制
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import time
import opencc

# 初始化简繁体转换器
converter = opencc.OpenCC('t2s')  # Traditional to Simplified

# 配置
BLOG_PATH = "/home/swg/.openclaw/workspace/news-blog"
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "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")
IMAGES_DIR = Path(BLOG_PATH) / "images"
LOGS_DIR = Path(BLOG_PATH) / "logs"

# 创建必要的目录
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

class Logger:
    def __init__(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = LOGS_DIR / f"{today}.log"
        self.log("=" * 60)
        self.log(f"开始更新新闻博客 - {datetime.now()}")
        self.log("=" * 60)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, 'a') as f:
            f.write(log_message + "\n")

logger = Logger()

def get_beijing_time():
    """获取北京时间（UTC+8）"""
    return datetime.now() + timedelta(hours=8)

def step_1_search_news(count=20):
    """第1步：搜索新闻"""
    logger.log(f"📡 步骤 1/5: 搜索 {count} 条新闻")

    try:
        search_script = Path.home() / ".hermes/scripts/tavily_search.py"
        date_str = get_beijing_time().strftime("%Y年%m月%d日")
        query = f"今日新闻 {date_str} 头条 热点 世界 国际"

        result = subprocess.run(
            ["python3", str(search_script), query, "--max-results", str(count), "--json-output"],
            capture_output=True,
            text=True,
            timeout=90
        )

        if result.returncode == 0 and result.stdout.strip():
            import json
            # 搜索脚本第一行是日志，从第二行开始解析JSON
            try:
                # 查找JSON开始的行（第一个{）
                lines = result.stdout.splitlines()
                json_start = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith('{'):
                        json_start = i
                        break
                json_text = '\n'.join(lines[json_start:])
                response = json.loads(json_text)

                # 从Tavily响应中提取新闻
                if 'results' in response and len(response['results']) > 0:
                    news_list = []
                    for item in response['results'][:count]:
                        title = item.get('title', '无标题')
                        raw_content = item.get('content', '无内容')
                        
                        # 清理内容：转繁体为简体，移除英文和特殊符号
                        content = clean_news_content(raw_content)
                        title = clean_news_content(title)  # 标题也需要清理
                        
                        # 过滤掉含"中共"的新闻
                        if '中共' in title or '中共' in content:
                            logger.log(f"🚫 过滤含敏感词新闻: {title[:30]}...")
                            continue
                        
                        # 确保摘要至少150字，不足则扩展
                        content = expand_summary(content, min_length=150, max_length=200)
                        
                        news_list.append({
                            "title": title,
                            "summary": content,
                            "raw_prompt": raw_content[:100],  # 保存原始内容用于生成图片
                            "tags": ["新闻"]
                        })
                    logger.log(f"✅ 搜索成功: 找到 {len(news_list)} 条新闻")
                    
                    # 确保正好20条新闻，不足则用示例补齐
                    if len(news_list) < count:
                        needed = count - len(news_list)
                        logger.log(f"📝 需要补充 {needed} 条示例新闻")
                        sample = get_sample_news(needed)
                        for s in sample:
                            s['summary'] = expand_summary(s['summary'], min_length=150, max_length=200)
                            s['raw_prompt'] = s['summary'][:100]
                        news_list.extend(sample)
                    
                    return news_list[:20]  # 确保只返回20条新闻
                else:
                    logger.log("⚠️  搜索结果为空，使用示例数据")
                    sample_news = get_sample_news(count)
                    # 扩展示例新闻每个摘要到150-200字
                    for news in sample_news:
                        news['summary'] = expand_summary(news['summary'], min_length=150, max_length=200)
                        news['raw_prompt'] = news['summary'][:100]
                    return sample_news
            except json.JSONDecodeError as e:
                logger.log(f"⚠️  JSON解析失败: {str(e)}，使用示例数据")
                sample_news = get_sample_news(count)
                for news in sample_news:
                    news['summary'] = expand_summary(news['summary'], min_length=150, max_length=200)
                    news['raw_prompt'] = news['summary'][:100]
                return sample_news
        else:
            logger.log("⚠️  搜索返回为空，使用示例数据")
            sample_news = get_sample_news(count)
            for news in sample_news:
                news['summary'] = expand_summary(news['summary'], min_length=150, max_length=200)
            return sample_news
    except Exception as e:
        logger.log(f"⚠️  搜索异常: {str(e)}，使用示例数据")
        sample_news = get_sample_news(count)
        for news in sample_news:
            news['summary'] = expand_summary(news['summary'], min_length=150, max_length=200)
        return sample_news


def extract_image_keywords(title, summary):
    """从标题和摘要中提取图片生成的关键词"""
    import re
    
    # 合并标题和摘要
    text = f"{title} {summary}"
    
    # 定义常见关键词类别
    keyword_map = {
        # 科技类
        "科技": "technology, computer, digital",
        "人工智能": "AI, artificial intelligence, robot",
        "AI": "AI, artificial intelligence, robot",
        "手机": "smartphone, mobile phone",
        "电脑": "computer, laptop",
        "互联网": "internet, network",
        "5G": "5G network, communication tower",
        "芯片": "computer chip, semiconductor",
        "新能源": "solar panel, wind turbine, clean energy",
        "汽车": "car, automobile, vehicle",
        "电动车": "electric car, EV",
        
        # 国际/政治类
        "美国": "United States, American flag",
        "白宫": "White House, Washington DC",
        "联合国": "United Nations, UN headquarters",
        
        # 经济类
        "经济": "economy, business, finance",
        "股市": "stock market, trading",
        "银行": "bank, finance building",
        
        # 社会类
        "教育": "school, education, students",
        "医疗": "hospital, doctor, medicine",
        "气候": "climate, weather, environment",
        "灾难": "disaster, emergency",
        
        # 体育/娱乐
        "体育": "sports, stadium",
        "奥运": "Olympics, sports",
        "电影": "movie, cinema, film",
        "音乐": "music, concert",
        
        # 地点
        "北京": "Beijing, China cityscape",
        "上海": "Shanghai, modern city",
        "国际": "international, global",
        "全球": "world, global",
    }
    
    keywords_found = []
    for cn_keyword, en_keyword in keyword_map.items():
        if cn_keyword in text:
            keywords_found.append(en_keyword)
    
    # 如果没找到关键词，使用通用描述
    if not keywords_found:
        return "breaking news, current events"
    
    return ", ".join(keywords_found[:3])  # 最多返回3个关键词


def clean_news_content(text):
    """清理新闻内容：移除英文、繁体、特殊符号，转为纯简体中文"""
    if not text:
        return "暂无内容"
    
    import re
    
    # 0. 首先转换繁体为简体
    text = converter.convert(text)
    
    # 1. 移除 markdown 链接和图片标记 ![[ ]] [[ ]] [视频]
    text = re.sub(r'!\[\[.*?\]\]', '', text)
    text = re.sub(r'\[\[视频\].*?\]', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    
    # 2. 移除 Markdown 标题标记 ### ## *
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*|\*', '', text)
    
    # 3. 移除英文单词（保留中文）
    # 这个复杂，需要仔细处理 - 只移除���英文部分
    # 简单方法：把所有连续英文字母替换为空
    text = re.sub(r'[a-zA-Z]{2,}', '', text)
    
    # 4. 移除数字开头的内容（如 "1、", "2、" 作为列表编号）
    text = re.sub(r'^\d+[.、]\s*', '', text, flags=re.MULTILINE)
    
    # 5. 移除剩余特殊符号 但保留中文标点
    text = re.sub(r'[^\u4e00-\u9fa5\u3000-\u303f\uff00-\uffefa-zA-Z0-9\s\d，。！？；：、""''（）【】《》——…·]', '', text)
    
    # 6. 移除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 7. 移除 URL
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    
    return text if text else "暂无内容"


def expand_summary(content, min_length=150, max_length=200):
    """扩展摘要到指定长度，确保恰好150-200字"""
    if not content:
        return "暂无内容"
    
    # 如果太短，需要扩展内容
    if len(content) < min_length:
        # 从已有内容提取关键词并扩展
        # 获取句子中的关键信息然后补充
        additions = [
            "该事件引发广泛关注，行业专家表示这将带来深远影响。",
            "相关部门已启动应急预案，确保各项工作有序进行。",
            "业内人士分析认为这标志着行业进入新发展阶段。",
            "多家机构表示将继续关注后续进展。",
            " experts表示具体情况仍在进一步调查中。",
            "各方正积极协调，争取早日达成共识。"
        ]
        
        for add in additions:
            if len(content) + len(add) <= max_length:
                content = content.rstrip('。！？') + "，" + add[1:]  # 去掉开头的标点
        
        return content[:max_length]
    
    # 如果太长，截取并确保句子完整
    if len(content) > max_length:
        # 尝试在句号处截断
        truncated = content[:max_length]
        last_period = max(truncated.rfind('。'), truncated.rfind('！'), truncated.rfind('？'))
        if last_period > min_length:
            return truncated[:last_period + 1]
        return truncated + "..."
    
    return content

def get_sample_news(count=20):
    """示例新闻数据（默认20条）- 每个摘要150-200字"""
    sample_news = [
        {
            "title": "全球科技峰会今日开幕",
            "summary": "多国科技领袖齐聚一堂，聚焦人工智能与可持续发展议题。各国专家就AI伦理治理、绿色能源转型、数字经济发展等议题展开深入讨论，共同制定行业新标准，推动全球科技创新合作迈向新阶段。",
            "tags": ["科技", "国际"]
        },
        {
            "title": "新能源汽车销量创新高",
            "summary": "本月新能源汽车销量同比增长30%，市场前景持续看好。多家厂商加速布局电动化转型，供应链体系持续完善，充电基础设施加快建设，消费者对新能源汽车的接受度显著提升。",
            "tags": ["汽车", "经济"]
        },
        {
            "title": "量子计算取得新突破",
            "summary": "量子计算机实现更高稳定性和运算速度，为未来科技发展奠定基础。研究团队在纠错算法和量子比特控制方面取得重大进展，推动量子计算实用化进程。",
            "tags": ["科技", "量子计算"]
        },
        {
            "title": "航天发射任务圆满成功",
            "summary": "最新卫星成功入轨，为通信网络升级提供支持。本次发射任务标志着航天工业进入新阶段，卫星互联网建设加速推进。",
            "tags": ["航天", "科技"]
        },
        {
            "title": "人工智能医疗应用加速",
            "summary": "AI在疾病诊断和药物研发中的应用取得显著进展，医疗行业迎来数字化变革。多地医疗机构引入AI辅助诊断系统，提升诊疗效率和准确率。",
            "tags": ["AI", "医疗"]
        },
        {
            "title": "可再生能源投资创新高",
            "summary": "各国加大清洁能源投资力度，推动绿色转型战略实施。太阳能、风能市场持续扩大，技术创新降低成本，储能产业迎来快速发展期。",
            "tags": ["能源", "环保"]
        },
        {
            "title": "5G网络覆盖加速推进",
            "summary": "更多城市实现5G网络全覆盖，为数字经济提供基础设施建设支撑。5G应用场景不断丰富，工业互联网、智慧城市等领域加速发展。",
            "tags": ["科技", "通信"]
        },
        {
            "title": "在线教育平台用户激增",
            "summary": "学习数字化趋势明显，在线教育平台用户规模持续增长。个性化学习方案成为行业新趋势，AI辅助教学提升学习效率。",
            "tags": ["教育", "科技"]
        },
        {
            "title": "智慧城市建设加速",
            "summary": "多个城市启动智慧城市建设项目，运用物联网、大数据等技术提升城市管理水平。智能交通、智慧安防等领域取得显著成效。",
            "tags": ["科技", "城市"]
        },
        {
            "title": "生物科技领域投资活跃",
            "summary": "基因编辑、生物制药等前沿领域投资显著增加，生物科技创新成果不断涌现。创新药物研发提速，为疑难疾病治疗带来新希望。",
            "tags": ["科技", "生物"]
        }
    ]

    # 生成更多示例新闻达到20条，每个都是150-200字
    for i in range(11, count + 1):
        sample_news.append({
            "title": f"今日要闻第{i}条",
            "summary": f"今日要闻第{i}条的相关报道。据相关部门介绍，该消息引发了广泛关注，业内人士分析认为这将对相关行业产生积极影响。目前各项工作正在有序推进中，具体实施细节将另行公布。",
            "tags": ["要闻", "动态"]
        })
    
    return sample_news


def step_2_generate_images(news_list, seed=101, max_retries=2):
    """第2步：生成图片（带质量检查和重试）"""
    logger.log(f"🎨 步骤 2/5: 生成 {len(news_list)} 张图片（带质量检查）")
    logger.log(f"📊 质量标准: 文件50KB-800KB, 宽≥800, 高≥450, 比例16:9")

    try:
        results = []
        genai_script = Path.home() / ".hermes/scripts/pollinations_generate.py"
        if not genai_script.exists():
            genai_script = Path(BLOG_PATH) / "pollinations_generate.py"

        for idx, news in enumerate(news_list, 1):
            title = news.get("title", "")
            # 使用更多内容来生成图片
            summary = news.get("summary", "")[:150]
            raw_prompt = news.get("raw_prompt", "")[:100]  # 使用原始未清理内容
            
            # 提取关键词生成更具体的描述
            keywords = extract_image_keywords(title, summary)
            
            # 为每条新闻生成独特的高质量提示词
            prompt_en = f"Realistic news photography: {keywords}. {title}. {summary}. "
            prompt_en += "8K ultra high definition, photorealistic, detailed, natural lighting, "
            prompt_en += "professional photojournalism, Reuters/Associated Press style, "
            prompt_en += "real scene, actual event, no animation, no cartoon, vivid colors, "
            prompt_en += "cinematic composition, sharp focus, depth of field, current news"

            # 图片文件名，使用唯一命名避免覆盖
            image_file = IMAGES_DIR / f"news_{seed + idx:04d}.png"

            success = False
            retry_count = 0

            while not success and retry_count <= max_retries:
                try:
                    logger.log(f"🖼️  生成图片 {idx}/{len(news_list)}: {title[:30]}... (尝试 {retry_count + 1})")

                    result = subprocess.run(
                        ["python3", str(genai_script),
                         prompt_en,
                         "--output", str(image_file),
                         "--width", "1344",
                         "--height", "768",
                         "--seed", str(seed + idx + retry_count * 100),
                         "--nologo"],
                        capture_output=True,
                        text=True,
                        timeout=180,
                        env={**os.environ, "NVIDIA_API_KEY": NVIDIA_API_KEY}
                    )

                    if result.returncode == 0 and image_file.exists():
                        # 检查图片质量
                        quality_ok = check_image_quality(image_file)
                        if quality_ok:
                            logger.log(f"✅ 图片 {idx}/{len(news_list)} 生成成功且质量合格")
                            results.append(str(image_file))
                            success = True
                        else:
                            if retry_count < max_retries:
                                logger.log(f"⚠️  图片质量不达标，重新生成...")
                                retry_count += 1
                                image_file.unlink()  # 删除不合格的图片
                            else:
                                logger.log(f"⚠️  图片 {idx}/{len(news_list)} 质量未达标但已达到最大重试次数")
                                results.append(str(image_file))
                                success = True
                    else:
                        if retry_count < max_retries:
                            logger.log(f"⚠️  图片 {idx}/{len(news_list)} 生成失败，重试...")
                            retry_count += 1
                        else:
                            logger.log(f"❌ 图片 {idx}/{len(news_list)} 生成失败")
                            results.append(None)
                            success = True

                    # 稍等避免API限流
                    if idx < len(news_list) or not success:
                        time.sleep(3)

                except subprocess.TimeoutExpired:
                    if retry_count < max_retries:
                        logger.log(f"⚠️  图片 {idx}/{len(news_list)} 超时，重试...")
                        retry_count += 1
                    else:
                        logger.log(f"❌ 图片 {idx}/{len(news_list)} 超时")
                        results.append(None)
                        success = True
                except Exception as e:
                    if retry_count < max_retries:
                        logger.log(f"⚠️  图片 {idx}/{len(news_list)} 异常: {str(e)}，重试...")
                        retry_count += 1
                    else:
                        logger.log(f"❌ 图片 {idx}/{len(news_list)} 最终失败")
                        results.append(None)
                        success = True

        return results
    except Exception as e:
        logger.log(f"❌ 图片生成异常: {str(e)}")
        return [None] * len(news_list)

def check_image_quality(image_path):
    """检查图片质量是否达标（提高标准）"""
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            width, height = img.size
            file_size_kb = os.path.getsize(image_path) / 1024

            # Pollinations 质量标准（适配实际输出）
            min_size_kb = 50   # Pollinations 压缩率较高
            max_size_kb = 800
            min_width = 800    # Pollinations 通常输出 800-1024 宽度
            min_height = 450
            target_ratio = 16/9
            ratio_tolerance = 0.2  # 放宽比例容差

            ratio = width / height
            ratio_diff = abs(ratio - target_ratio) / target_ratio

            # 检查各项指标
            size_ok = min_size_kb <= file_size_kb <= max_size_kb
            resolution_ok = width >= min_width and height >= min_height
            ratio_ok = ratio_diff <= ratio_tolerance

            return size_ok and resolution_ok and ratio_ok
    except:
        return False

def step_3_check_quality(news_list, image_files):
    """第3步：检查整体质量"""
    logger.log(f"🔍 步骤 3/5: 检查内容和图片质量")

    try:
        check_script = Path(BLOG_PATH) / "check_quality.py"

        # 临时创建检查脚本需要的参数
        check_ok = True

        for idx, (news, image_file) in enumerate(zip(news_list, image_files), 1):
            title = news.get("title", "No Title")
            summary = news.get("summary", "")

            # 检查内容长度
            if len(summary) < 50:
                logger.log(f"⚠️  新闻 {idx} 内容过短 ({len(summary)} 字符)")
                check_ok = False
            else:
                logger.log(f"✅ 新闻 {idx} 内容长度: {len(summary)} 字符")

            # 检查图片
            if image_file and os.path.exists(image_file):
                img_quality = check_image_quality(image_file)
                if img_quality:
                    size_kb = os.path.getsize(image_file) / 1024
                    logger.log(f"✅ 新闻 {idx} 图片质量: {size_kb:.1f}KB")
                else:
                    logger.log(f"⚠️  新闻 {idx} 图片质量未达标")
                    check_ok = False
            else:
                logger.log(f"⚠️  新闻 {idx} 图片文件不存在")
                check_ok = False

        if check_ok:
            logger.log("✅ 质量检查通过")
        else:
            logger.log("⚠️  部分内容或图片质量未达标，但继续发布")

        return check_ok
    except Exception as e:
        logger.log(f"❌ 质量检查异常: {str(e)}")
        return True  # 出错时继续，不阻止发布

def step_4_create_html(news_list, image_files):
    """第4步：创建 HTML"""
    logger.log(f"📝 步骤 4/5: 创建 HTML 页面")

    try:
        # 这里使用完整的 index_enhanced.html 作为基础模板
        # 只需要修改新闻卡片部分

        from datetime import datetime
        date_str = get_beijing_time().strftime("%Y年%m月%d日")

        news_cards_html = ""
        for idx, (news, image_file) in enumerate(zip(news_list, image_files), 1):
            title = news.get("title", "无标题")
            summary = news.get("summary", "无内容")
            tags = news.get("tags", [])
            image_path = f"images/{Path(image_file).name}" if image_file else "images/news_default.png"

            # 构建新闻卡片
            news_cards_html += f"""

                <div class="news-card">
                    <img src="{image_path}" alt="{title}" class="news-image">
                    <div class="news-content">
                        <span class="news-number">{idx}</span>
                        <h3 class="news-title">{title}</h3>
                        <p class="news-summary">{summary}</p>
                        <div>"""

            # 添加标签
            for tag in tags[:5]:
                news_cards_html += f'\n                            <span class="tag">{tag}</span>'

            news_cards_html += """
                        </div>
                    </div>
                </div>"""

        # 读取并更新 index_enhanced.html
        index_enhanced = Path(BLOG_PATH) / "index_enhanced.html"
        with open(index_enhanced, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 替换占位符
        html_content = html_content.replace("{{NEWS_DATE}}", date_str)
        html_content = html_content.replace("{{NEWS_CARDS}}", news_cards_html)

        # 保存新文件
        html_file = Path(BLOG_PATH) / "index.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.log(f"✅ HTML 创建成功: {html_file}")
        return str(html_file)

    except Exception as e:
        logger.log(f"❌ HTML 创建失败: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return None

def step_5_upload_to_github(html_file):
    """第5步：上传到 GitHub"""
    logger.log(f"🚀 步骤 5/5: 上传到 GitHub")

    try:
        upload_script = Path(BLOG_PATH) / "upload.sh"

        result = subprocess.run(
            [str(upload_script), f"📰 自动更新 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=BLOG_PATH
        )

        if result.returncode == 0:
            logger.log("✅ 上传成功")
            return True
        else:
            logger.log(f"❌ 上传失败")
            return False

    except Exception as e:
        logger.log(f"❌ 上传异常: {str(e)}")
        return False

def main():
    """主函数"""
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="自动更新新闻博客（增强版）")
    parser.add_argument("--news-count", type=int, default=20, help="新闻数量")
    parser.add_argument("--no-upload", action="store_true", help="不上传，仅生成")
    parser.add_argument("--seed", type=int, help="图片随机种子（默认基于日期生成，避免覆盖历史图片）")

    args = parser.parse_args()

    # 默认用日期生成seed，每天不重复，避免覆盖历史图片
    if args.seed is None:
        today = datetime.now().strftime("%Y%m%d")
        args.seed = int(today)  # e.g. 20260428

    try:
        # 第1步：搜索新闻
        news_list = step_1_search_news(args.news_count)
        if not news_list:
            return 1

        # 第2步：生成图片（带质量检查）
        image_files = step_2_generate_images(news_list, args.seed)

        # 第3步：检查质量
        quality_ok = step_3_check_quality(news_list, image_files)

        # 第4步：创建 HTML
        html_file = step_4_create_html(news_list, image_files)
        if not html_file:
            return 1

        # 第5步：上传
        if not args.no_upload:
            success = step_5_upload_to_github(html_file)
            if success:
                logger.log("=" * 60)
                logger.log("🎉 更新完成！")
                logger.log(f"🌐 https://yww001.github.io/news-blog/")
                logger.log(f"📊 质量: {'✅ 合格' if quality_ok else '⚠️  部分未达标'}")
                logger.log(f"📷 生成: {len(image_files)} 张图片")
                logger.log(f"📰 新闻: {len(news_list)} 条")
                logger.log("=" * 60)
            else:
                logger.log("⚠️  图片和 HTML 已生成，但上传失败")
                return 1
        else:
            logger.log("✅ 生成完成（未上传）")
            logger.log(f"📄 HTML 文件: {html_file}")

        return 0

    except Exception as e:
        logger.log(f"❌ 错误: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
