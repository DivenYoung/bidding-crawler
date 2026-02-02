"""关键字匹配引擎"""
from typing import List, Dict


class KeywordMatcher:
    """关键字匹配引擎"""
    
    def __init__(self, keywords: List[str]):
        """
        初始化匹配器
        
        Args:
            keywords: 关键字列表
        """
        self.keywords = keywords
    
    def match(self, text: str) -> List[str]:
        """
        在文本中匹配关键字
        
        Args:
            text: 待匹配文本
            
        Returns:
            List[str]: 匹配到的关键字列表
        """
        if not text:
            return []
        
        matched = []
        for keyword in self.keywords:
            if keyword in text:
                matched.append(keyword)
        
        return matched
    
    def is_relevant(self, item: Dict) -> bool:
        """
        判断项目是否相关（至少匹配一个关键字）
        
        Args:
            item: 项目信息字典
            
        Returns:
            bool: True 表示相关，False 表示不相关
        """
        title = item.get('title', '')
        content = item.get('content', '')
        
        # 在标题和内容中搜索关键字
        text = f"{title} {content}"
        matched = self.match(text)
        
        return len(matched) > 0
