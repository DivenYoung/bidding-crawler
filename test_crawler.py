"""测试真实爬虫功能"""
import sys
sys.path.insert(0, '/home/ubuntu/bidding-crawler/src')

import yaml
import structlog
from datetime import datetime

from crawler.search_crawler import SearchCrawler, CrawlerConfig
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
    """测试爬虫"""
    logger.info("test.start", message="开始测试真实爬虫")
    
    # 加载配置
    config = load_config()
    
    # 初始化爬虫
    crawler_config = CrawlerConfig(
        min_delay=config['crawler']['anti_crawl']['min_delay'],
        max_delay=config['crawler']['anti_crawl']['max_delay'],
        max_retries=config['crawler']['anti_crawl']['max_retries']
    )
    
    crawler = SearchCrawler(
        keywords=config['crawler']['keywords'],
        config=crawler_config
    )
    
    # 初始化关键字匹配器
    matcher = KeywordMatcher(config['crawler']['keywords'])
    
    logger.info("crawler.initialized", keywords=config['crawler']['keywords'])
    
    # 执行搜索
    logger.info("crawler.searching", message="正在抓取采招网数据...")
    results = crawler.search_full(
        time_range="近三月",
        region=config['crawler']['search']['region'],
        info_types=config['crawler']['search']['info_types']
    )
    
    logger.info("crawler.results", count=len(results))
    
    if not results:
        logger.warning("no_results", message="未抓取到数据，请检查网络或页面结构")
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
    
    # 显示前3条结果
    logger.info("sample_results", message=f"显示前3条结果:")
    for i, item in enumerate(bidding_items[:3], 1):
        print(f"\n{'='*60}")
        print(f"项目 {i}:")
        print(f"  ID: {item.id}")
        print(f"  标题: {item.title}")
        print(f"  类型: {item.info_type}")
        print(f"  发布日期: {item.publish_date.strftime('%Y-%m-%d')}")
        print(f"  地区: {item.province} {item.city or ''} {item.district or ''}")
        print(f"  匹配关键字: {', '.join(item.keywords_matched)}")
        print(f"  来源: {item.source_url}")
    
    # 询问是否保存
    print(f"\n{'='*60}")
    print(f"共抓取到 {len(bidding_items)} 条数据")
    save = input("\n是否保存到数据库？(y/n): ").strip().lower()
    
    if save == 'y':
        storage = JSONStorage(config['storage']['json_path'])
        
        # 保存数据
        metadata = {
            "last_full_crawl": datetime.now().isoformat(),
            "total_count": len(bidding_items),
            "keywords": config['crawler']['keywords'],
            "region": config['crawler']['search']['region']
        }
        
        storage.save(bidding_items, metadata)
        
        logger.info("data.saved", 
                   count=len(bidding_items), 
                   path=config['storage']['json_path'])
        print(f"\n✅ 已保存 {len(bidding_items)} 条数据到 {config['storage']['json_path']}")
        print(f"\n🚀 现在可以运行 Streamlit 查看数据:")
        print(f"   streamlit run src/ui/app.py")
    else:
        logger.info("data.not_saved", message="用户选择不保存")
        print("\n数据未保存")
    
    logger.info("test.complete")


if __name__ == "__main__":
    main()
