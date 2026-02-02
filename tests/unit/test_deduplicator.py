"""数据去重器单元测试"""
import sys
sys.path.insert(0, '/home/ubuntu/bidding-crawler/src')

from datetime import datetime
from data.models import BiddingInfo
from data.deduplicator import DataDeduplicator


def test_deduplicate_by_id():
    """测试基于ID去重"""
    existing = [
        BiddingInfo(
            id="1", 
            title="项目A", 
            info_type="招标公告",
            publish_date=datetime.now(),
            province="四川"
        )
    ]
    new = [
        BiddingInfo(
            id="1", 
            title="项目A", 
            info_type="招标公告",
            publish_date=datetime.now(),
            province="四川"
        ),
        BiddingInfo(
            id="2", 
            title="项目B", 
            info_type="招标公告",
            publish_date=datetime.now(),
            province="四川"
        )
    ]
    
    dedup = DataDeduplicator()
    result = dedup.deduplicate(new, existing)
    
    assert len(result) == 1
    assert result[0].id == "2"


def test_deduplicate_all_new():
    """测试全部为新数据"""
    existing = []
    new = [
        BiddingInfo(
            id="1", 
            title="项目A", 
            info_type="招标公告",
            publish_date=datetime.now(),
            province="四川"
        ),
        BiddingInfo(
            id="2", 
            title="项目B", 
            info_type="招标公告",
            publish_date=datetime.now(),
            province="四川"
        )
    ]
    
    dedup = DataDeduplicator()
    result = dedup.deduplicate(new, existing)
    
    assert len(result) == 2


def test_deduplicate_all_duplicate():
    """测试全部为重复数据"""
    existing = [
        BiddingInfo(
            id="1", 
            title="项目A", 
            info_type="招标公告",
            publish_date=datetime.now(),
            province="四川"
        ),
        BiddingInfo(
            id="2", 
            title="项目B", 
            info_type="招标公告",
            publish_date=datetime.now(),
            province="四川"
        )
    ]
    new = [
        BiddingInfo(
            id="1", 
            title="项目A", 
            info_type="招标公告",
            publish_date=datetime.now(),
            province="四川"
        ),
        BiddingInfo(
            id="2", 
            title="项目B", 
            info_type="招标公告",
            publish_date=datetime.now(),
            province="四川"
        )
    ]
    
    dedup = DataDeduplicator()
    result = dedup.deduplicate(new, existing)
    
    assert len(result) == 0
