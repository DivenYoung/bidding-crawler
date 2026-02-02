"""主执行脚本"""
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
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()


def load_config():
    """加载配置文件"""
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_mock_data():
    """创建模拟数据用于演示"""
    mock_items = [
        BiddingInfo(
            id="mock_001",
            title="成都市锦江区文化宣传栏及标识牌采购项目招标公告",
            info_type="招标公告",
            publish_date=datetime(2026, 2, 1),
            province="四川",
            city="成都",
            district="锦江区",
            owner_unit="成都市锦江区文化旅游局",
            budget_amount="150万元",
            procurement_type="公开招标",
            bidding_deadline=datetime(2026, 2, 20, 17, 0),
            keywords_matched=["文化", "宣传", "标识", "牌"],
            project_address="四川省成都市锦江区",
            attachments=["https://example.com/attachment1.pdf"],
            source_url="https://www.bidcenter.com.cn/mock/001"
        ),
        BiddingInfo(
            id="mock_002",
            title="绵阳市涪城区户外广告牌制作安装项目",
            info_type="招标公告",
            publish_date=datetime(2026, 2, 2),
            province="四川",
            city="绵阳",
            district="涪城区",
            owner_unit="绵阳市涪城区城市管理局",
            budget_amount="80万元",
            procurement_type="询比",
            bidding_deadline=datetime(2026, 2, 18, 17, 0),
            keywords_matched=["广告", "牌"],
            project_address="四川省绵阳市涪城区",
            attachments=[],
            source_url="https://www.bidcenter.com.cn/mock/002"
        ),
        BiddingInfo(
            id="mock_003",
            title="德阳市旌阳区文化广场标识导视系统采购",
            info_type="招标公告",
            publish_date=datetime(2026, 2, 3),
            province="四川",
            city="德阳",
            district="旌阳区",
            owner_unit="德阳市旌阳区文化体育局",
            budget_amount="120万元",
            procurement_type="公开招标",
            bidding_deadline=datetime(2026, 2, 25, 17, 0),
            keywords_matched=["文化", "标识"],
            project_address="四川省德阳市旌阳区",
            attachments=["https://example.com/attachment3.pdf"],
            source_url="https://www.bidcenter.com.cn/mock/003"
        ),
        BiddingInfo(
            id="mock_004",
            title="成都市武侯区社区宣传栏更新改造项目",
            info_type="招标公告",
            publish_date=datetime(2026, 1, 28),
            province="四川",
            city="成都",
            district="武侯区",
            owner_unit="成都市武侯区民政局",
            budget_amount="60万元",
            procurement_type="竞争性磋商",
            bidding_deadline=datetime(2026, 2, 15, 17, 0),
            keywords_matched=["宣传", "栏"],
            project_address="四川省成都市武侯区",
            attachments=[],
            source_url="https://www.bidcenter.com.cn/mock/004"
        ),
        BiddingInfo(
            id="mock_005",
            title="泸州市龙马潭区文化墙及标志牌设计制作项目",
            info_type="招标公告",
            publish_date=datetime(2026, 1, 25),
            province="四川",
            city="泸州",
            district="龙马潭区",
            owner_unit="泸州市龙马潭区宣传部",
            budget_amount="200万元",
            procurement_type="公开招标",
            bidding_deadline=datetime(2026, 2, 22, 17, 0),
            keywords_matched=["文化", "标志", "牌"],
            project_address="四川省泸州市龙马潭区",
            attachments=["https://example.com/attachment5.pdf"],
            source_url="https://www.bidcenter.com.cn/mock/005"
        )
    ]
    
    return mock_items


def main():
    """主函数"""
    logger.info("app.start")
    
    # 加载配置
    config = load_config()
    
    # 初始化存储
    storage = JSONStorage(config['storage']['json_path'])
    
    # 检查是否首次运行
    is_first_run = storage.is_first_run()
    
    if is_first_run:
        logger.info("first_run_detected", message="创建模拟数据用于演示")
        
        # 创建模拟数据
        mock_items = create_mock_data()
        
        # 保存数据
        metadata = {
            "last_full_crawl": datetime.now().isoformat(),
            "total_count": len(mock_items),
            "keywords": config['crawler']['keywords'],
            "region": config['crawler']['search']['region']
        }
        
        storage.save(mock_items, metadata)
        
        logger.info("mock_data_created", count=len(mock_items))
        print(f"\n✅ 已创建 {len(mock_items)} 条模拟数据")
        print(f"📁 数据文件: {config['storage']['json_path']}")
        print(f"\n🚀 现在可以运行 Streamlit 查看数据:")
        print(f"   cd /home/ubuntu/bidding-crawler")
        print(f"   streamlit run src/ui/app.py")
    else:
        logger.info("data_exists", message="数据文件已存在")
        items, metadata = storage.load()
        print(f"\n📊 当前数据统计:")
        print(f"   总项目数: {len(items)}")
        print(f"   上次更新: {metadata.get('last_full_crawl', '未知')}")
        print(f"\n🚀 运行 Streamlit 查看数据:")
        print(f"   cd /home/ubuntu/bidding-crawler")
        print(f"   streamlit run src/ui/app.py")
    
    logger.info("app.complete")


if __name__ == "__main__":
    main()
