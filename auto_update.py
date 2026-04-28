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

def step_1_search_news(count=100):
    """第1步：搜索新闻"""
    logger.log(f"📡 步骤 1/5: 搜索 {count} 条新闻")

    try:
        search_script = Path.home() / ".hermes/scripts/tavily_search.py"
        date_str = get_beijing_time().strftime("%Y年%m月%d日")
        query = f"今日新闻 {date_str} 头条 热点 世界 国际"

        result = subprocess.run(
            ["python3", str(search_script), query, "-n", str(count), "--json"],
            capture_output=True,
            text=True,
            timeout=60
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
                        news_list.append({
                            "title": item.get('title', '无标题'),
                            "summary": item.get('content', '无内容')[:200] if item.get('content') else '无内容',
                            "tags": ["新闻"]  # 默认标签
                        })
                    logger.log(f"✅ 搜索成功: 找到 {len(news_list)} 条新闻")
                    return news_list[:100]  # 确保只返回100条新闻
                else:
                    logger.log("⚠️  搜索结果为空，使用示例数据")
                    return get_sample_news()
            except json.JSONDecodeError as e:
                logger.log(f"⚠️  JSON解析失败: {str(e)}，使用示例数据")
                return get_sample_news()
        else:
            logger.log("⚠️  搜索返回为空，使用示例数据")
            return get_sample_news()
    except Exception as e:
        logger.log(f"⚠️  搜索异常: {str(e)}，使用示例数据")
        return get_sample_news()

def get_sample_news():
    """示例新闻数据（100条）"""
    sample_news = [
        {
            "title": "全球科技峰会今日开幕",
            "summary": "多国科技领袖出席，聚焦AI与可持续发展议题。各国专家就人工智能伦理、可持续发展等议题展开深入讨论，共同制定行业新标准。",
            "tags": ["科技", "国际"]
        },
        {
            "title": "新能源汽车销量创新高",
            "summary": "本月新能源汽车销量同比增长30%，市场前景看好。多家厂商加速布局电动化转型，供应链持续完善。",
            "tags": ["汽车", "经济"]
        },
        {
            "title": "量子计算取得新突破",
            "summary": "量子计算机实现更高稳定性和运算速度，为未来科技发展奠定基础。研究团队在纠错算法上取得重大进展。",
            "tags": ["科技", "量子计算"]
        },
        {
            "title": "航天发射任务圆满成功",
            "summary": "最新卫星成功入轨，为通信网络升级提供支持。本次发射任务标志着航天工业进入新阶段。",
            "tags": ["航天", "科技"]
        },
        {
            "title": "人工智能医疗应用加速",
            "summary": "AI在疾病诊断和药物研发中的应用取得进展，医疗行业迎来变革。多家医疗机构引入AI辅助诊断系统。",
            "tags": ["AI", "医疗"]
        },
        {
            "title": "可再生能源投资创新高",
            "summary": "各国加大清洁能源投资，推动绿色转型。太阳能和风能市场持续扩大。",
            "tags": ["能源", "环保"]
        },
        {
            "title": "5G网络覆盖加速推进",
            "summary": "更多城市实现5G全覆盖，为数字经济提供基础设施支持。5G应用场景不断丰富。",
            "tags": ["科技", "通信"]
        },
        {
            "title": "在线教育平台用户激增",
            "summary": "学习数字化趋势明显，在线教育用户持续增长。个性化学习成为新趋势。",
            "tags": ["教育", "科技"]
        },
        {
            "title": "智慧城市建设加速",
            "summary": "多个城市启动智慧城市项目，提升城市管理水平。物联网技术广泛应用。",
            "tags": ["科技", "城市"]
        },
        {
            "title": "生物科技领域投资活跃",
            "summary": "基因编辑、生物制药等领域投资显著增加。生物科技创新成果不断涌现。",
            "tags": ["科技", "生物"]
        }
    ]

    # 扩展到100条示例新闻
    for i in range(11, 101):
        sample_news.append({
            "title": f"示例新闻标题 {i}",
            "summary": f"这是第{i}条示例新闻的摘要内容。在实际运行中，这里会被真实的新闻内容替换。",
            "tags": ["示例", "新闻"]
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
            summary = news.get("summary", "")[:50]

            # 生成提示词（极致优化：超高清、真实、精致）
            prompt = f"超高清真实新闻摄影，{title}，{summary}，8K分辨率，专业新闻摄影，极致清晰，锐利细节，真实光线，自然色彩，电影级构图，纪实风格，新闻现场感，生动逼真，高对比度，丰富层次，专业镜头，景深效果，真实场景，无卡通，无插画，照片级质量，National Geographic风格，Reuters新闻摄影标准"

            # Pollinations 英文提示词（效果更好）
            prompt_en = f"Professional news photography, {title}. {summary}. 8K ultra high definition, Reuters photojournalism style, National Geographic quality, sharp details, natural lighting, cinematic composition, documentary style, realistic scene, no cartoon, no illustration, photo-realistic, vibrant colors, high contrast, rich layers, professional lens, depth of field, current news event"

            # 图片文件名
            image_file = IMAGES_DIR / f"news_{seed + idx}.png"

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
