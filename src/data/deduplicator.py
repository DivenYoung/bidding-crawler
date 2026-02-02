"""数据去重器"""
from typing import List
from data.models import BiddingInfo


class DataDeduplicator:
    """数据去重器"""
    
    def deduplicate(
        self, 
        new_items: List[BiddingInfo], 
        existing_items: List[BiddingInfo]
    ) -> List[BiddingInfo]:
        """
        去除重复项（基于项目ID）
        
        Args:
            new_items: 新抓取的数据
            existing_items: 已存在的数据
            
        Returns:
            List[BiddingInfo]: 去重后的新数据
        """
        # 构建已存在项目的ID集合
        existing_ids = {item.id for item in existing_items}
        
        # 过滤出不重复的新项目
        unique_items = [
            item for item in new_items 
            if item.id not in existing_ids
        ]
        
        return unique_items
