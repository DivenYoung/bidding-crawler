"""从浏览器内容抓取数据的实用工具

使用步骤：
1. 在浏览器中打开采招网搜索页面
2. 复制页面内容（Ctrl+A, Ctrl+C）
3. 将内容粘贴到 browser_content.txt 文件中
4. 运行此脚本解析数据

或者：
直接运行此脚本，它会自动使用浏览器工具抓取数据
"""

import sys
sys.path.insert(0, '/home/ubuntu/bidding-crawler/src')

import yaml
import structlog
from datetime import datetime

from crawler.browser_crawler import BrowserCrawler
from data.storage import JSONStorage
from data.models import BiddingInfo
from data.matcher import KeywordMatcher

# 配置日志
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer()
    ]
)

logger = structlog.get_logger()


def load_config():
    """加载配置文件"""
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main():
    """主函数"""
    logger.info("tool.start", message="从浏览器内容抓取数据")
    
    # 加载配置
    config = load_config()
    
    # 初始化爬虫
    crawler = BrowserCrawler(keywords=config['crawler']['keywords'])
    matcher = KeywordMatcher(config['crawler']['keywords'])
    
    # 检查是否有浏览器内容文件
    import os
    content_file = '/home/ubuntu/bidding-crawler/browser_content.txt'
    
    if os.path.exists(content_file):
        logger.info("file.found", path=content_file)
        print(f"\n📄 发现浏览器内容文件: {content_file}")
        print("正在解析...")
        
        # 从文件解析
        results = crawler.parse_from_file(
            content_file,
            region_filter=config['crawler']['search']['region']
        )
    else:
        logger.info("file.not_found", message="未找到浏览器内容文件")
        print(f"\n❌ 未找到文件: {content_file}")
        print("\n请按以下步骤操作：")
        print("1. 在浏览器中打开: https://search.bidcenter.com.cn/search?keywords=广告,标识,牌,标志,宣传,栏,文化")
        print("2. 等待页面加载完成")
        print("3. 按 Ctrl+A 全选页面内容")
        print("4. 按 Ctrl+C 复制")
        print(f"5. 将内容粘贴到文件: {content_file}")
        print("6. 再次运行此脚本")
        return
    
    logger.info("parse.results", count=len(results))
    
    if not results:
        logger.warning("no_results", message="未解析到数据")
        print("\n⚠️  未解析到数据，请检查文件内容格式")
        return
    
    # 转换为 BiddingInfo 对象并匹配关键字
    bidding_items = []
    for item in results:
        # 匹配关键字
        text = f"{item['title']}"
        matched_keywords = matcher.match(text)
        item['keywords_matched'] = matched_keywords
        
        # 创建 BiddingInfo 对象
        bidding_info = BiddingInfo(**item)
        bidding_items.append(bidding_info)
    
    # 显示统计信息
    print(f"\n{'='*60}")
    print(f"✅ 成功解析 {len(bidding_items)} 条项目")
    print(f"{'='*60}")
    
    # 按地区统计
    region_stats = {}
    for item in bidding_items:
        region = item.province or "未知"
        region_stats[region] = region_stats.get(region, 0) + 1
    
    print("\n📊 地区分布：")
    for region, count in sorted(region_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {region}: {count} 条")
    
    # 按信息类型统计
    type_stats = {}
    for item in bidding_items:
        info_type = item.info_type or "未知"
        type_stats[info_type] = type_stats.get(info_type, 0) + 1
    
    print("\n📋 信息类型分布：")
    for info_type, count in sorted(type_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {info_type}: {count} 条")
    
    # 显示前5条结果
    print(f"\n📝 前5条项目预览：")
    for i, item in enumerate(bidding_items[:5], 1):
        print(f"\n{i}. {item.title}")
        print(f"   类型: {item.info_type}")
        print(f"   地区: {item.province} {item.city or ''}")
        print(f"   预算: {item.budget_amount or '未知'}")
        print(f"   日期: {item.publish_date.strftime('%Y-%m-%d') if item.publish_date else '未知'}")
        print(f"   关键字: {', '.join(item.keywords_matched) if item.keywords_matched else '无'}")
    
    # 询问是否保存
    print(f"\n{'='*60}")
    save = input("是否保存到数据库？(y/n): ").strip().lower()
    
    if save == 'y':
        storage = JSONStorage(config['storage']['json_path'])
        
        # 检查是否首次运行
        is_first = storage.is_first_run()
        
        if is_first:
            # 首次运行，全量保存
            metadata = {
                "last_full_crawl": datetime.now().isoformat(),
                "total_count": len(bidding_items),
                "keywords": config['crawler']['keywords'],
                "region": config['crawler']['search']['region']
            }
            storage.save(bidding_items, metadata)
            logger.info("data.saved", mode="full", count=len(bidding_items))
            print(f"\n✅ 已保存 {len(bidding_items)} 条数据（全量）")
        else:
            # 增量保存
            added_count = storage.append(bidding_items)
            logger.info("data.appended", count=added_count)
            print(f"\n✅ 已追加 {added_count} 条新数据")
        
        print(f"\n🚀 现在可以运行 Streamlit 查看数据:")
        print(f"   streamlit run src/ui/app.py")
    else:
        logger.info("data.not_saved")
        print("\n数据未保存")
    
    logger.info("tool.complete")


if __name__ == "__main__":
    main()
