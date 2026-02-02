"""存储层单元测试"""
import sys
sys.path.insert(0, '/home/ubuntu/bidding-crawler/src')

import os
import tempfile
from datetime import datetime
from data.models import BiddingInfo
from data.storage import JSONStorage


def test_is_first_run():
    """测试首次运行判断"""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_path = f.name
    
    # 删除临时文件，模拟首次运行
    os.unlink(temp_path)
    
    storage = JSONStorage(temp_path)
    assert storage.is_first_run() == True
    
    # 清理
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def test_save_and_load():
    """测试保存和加载"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
        temp_path = f.name
    
    storage = JSONStorage(temp_path)
    
    items = [
        BiddingInfo(
            id="1",
            title="项目A",
            info_type="招标公告",
            publish_date=datetime(2026, 2, 1),
            province="四川"
        )
    ]
    
    metadata = {
        "last_full_crawl": "2026-02-01T00:00:00",
        "total_count": 1
    }
    
    storage.save(items, metadata)
    
    loaded_items, loaded_metadata = storage.load()
    
    assert len(loaded_items) == 1
    assert loaded_items[0].id == "1"
    assert loaded_items[0].title == "项目A"
    assert loaded_metadata["total_count"] == 1
    
    # 清理
    os.unlink(temp_path)


def test_append_with_dedup():
    """测试追加数据并去重"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
        temp_path = f.name
    
    storage = JSONStorage(temp_path)
    
    # 初始数据
    initial_items = [
        BiddingInfo(
            id="1",
            title="项目A",
            info_type="招标公告",
            publish_date=datetime(2026, 2, 1),
            province="四川"
        )
    ]
    
    metadata = {
        "last_full_crawl": "2026-02-01T00:00:00",
        "total_count": 1
    }
    
    storage.save(initial_items, metadata)
    
    # 追加数据（包含重复和新数据）
    new_items = [
        BiddingInfo(
            id="1",  # 重复
            title="项目A",
            info_type="招标公告",
            publish_date=datetime(2026, 2, 1),
            province="四川"
        ),
        BiddingInfo(
            id="2",  # 新数据
            title="项目B",
            info_type="招标公告",
            publish_date=datetime(2026, 2, 2),
            province="四川"
        )
    ]
    
    added_count = storage.append(new_items)
    
    assert added_count == 1  # 只新增了1条
    
    loaded_items, loaded_metadata = storage.load()
    
    assert len(loaded_items) == 2
    assert loaded_metadata["total_count"] == 2
    
    # 清理
    os.unlink(temp_path)
