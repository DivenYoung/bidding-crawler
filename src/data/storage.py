"""JSON 文件存储"""
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple
from data.models import BiddingInfo
from data.deduplicator import DataDeduplicator


class JSONStorage:
    """JSON 文件存储"""
    
    def __init__(self, file_path: str):
        """
        初始化存储
        
        Args:
            file_path: JSON 文件路径
        """
        self.file_path = file_path
        self.deduplicator = DataDeduplicator()
    
    def save(self, items: List[BiddingInfo], metadata: Dict) -> None:
        """
        保存数据（全量覆盖）
        
        Args:
            items: 项目列表
            metadata: 元数据
        """
        data = {
            "metadata": metadata,
            "data": [item.to_dict() for item in items]
        }
        
        # 确保目录存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self) -> Tuple[List[BiddingInfo], Dict]:
        """
        加载数据和元数据
        
        Returns:
            Tuple[List[BiddingInfo], Dict]: (项目列表, 元数据)
        """
        if not os.path.exists(self.file_path):
            return [], {}
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        items = [BiddingInfo.from_dict(item) for item in data.get('data', [])]
        metadata = data.get('metadata', {})
        
        return items, metadata
    
    def append(self, items: List[BiddingInfo]) -> int:
        """
        追加新数据（自动去重）
        
        Args:
            items: 新项目列表
            
        Returns:
            int: 实际新增的数量
        """
        existing_items, metadata = self.load()
        
        # 去重
        unique_items = self.deduplicator.deduplicate(items, existing_items)
        
        if not unique_items:
            return 0
        
        # 合并数据
        all_items = existing_items + unique_items
        
        # 更新元数据
        metadata['last_incremental_crawl'] = datetime.now().isoformat()
        metadata['total_count'] = len(all_items)
        
        # 保存
        self.save(all_items, metadata)
        
        return len(unique_items)
    
    def get_last_crawl_time(self) -> datetime:
        """
        获取上次抓取时间
        
        Returns:
            datetime: 上次抓取时间
        """
        _, metadata = self.load()
        
        last_crawl = metadata.get('last_incremental_crawl') or metadata.get('last_full_crawl')
        
        if last_crawl:
            return datetime.fromisoformat(last_crawl)
        
        return None
    
    def is_first_run(self) -> bool:
        """
        判断是否首次运行
        
        Returns:
            bool: True 表示首次运行
        """
        return not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0
