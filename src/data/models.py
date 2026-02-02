"""数据模型定义"""
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional, List, Dict


@dataclass
class BiddingInfo:
    """招投标信息实体"""
    
    # 唯一标识
    id: str
    
    # 基本信息
    title: str
    info_type: str
    publish_date: datetime
    
    # 地理信息
    province: str
    city: Optional[str] = None
    district: Optional[str] = None
    
    # 项目详情
    owner_unit: Optional[str] = None
    budget_amount: Optional[str] = None
    procurement_type: Optional[str] = None
    
    # 时间节点
    bidding_deadline: Optional[datetime] = None
    
    # 内容与附件
    keywords_matched: List[str] = field(default_factory=list)
    keyword_location: List[str] = field(default_factory=list)  # 新增：关键字出现位置
    project_address: Optional[str] = None
    attachments: List[str] = field(default_factory=list)
    
    # 附件标识
    has_attachments: bool = False  # 新增：是否有附件
    has_bidding_docs: bool = False  # 新增：是否有标书
    
    # 元数据
    source_url: str = ""
    detail_url: str = ""  # 新增：详情页链接
    crawled_at: datetime = None
    
    def __post_init__(self):
        """初始化默认值"""
        if self.crawled_at is None:
            self.crawled_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        data = asdict(self)
        # 转换 datetime 为 ISO 格式字符串
        if isinstance(data['publish_date'], datetime):
            data['publish_date'] = data['publish_date'].isoformat()
        if data['bidding_deadline'] and isinstance(data['bidding_deadline'], datetime):
            data['bidding_deadline'] = data['bidding_deadline'].isoformat()
        if isinstance(data['crawled_at'], datetime):
            data['crawled_at'] = data['crawled_at'].isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BiddingInfo':
        """从字典创建实例"""
        # 处理可能缺失的新字段
        if 'keyword_location' not in data:
            data['keyword_location'] = []
        if 'has_attachments' not in data:
            data['has_attachments'] = False
        if 'has_bidding_docs' not in data:
            data['has_bidding_docs'] = False
        if 'detail_url' not in data:
            data['detail_url'] = data.get('source_url', '')
        
        # 转换 ISO 格式字符串为 datetime
        if isinstance(data.get('publish_date'), str):
            data['publish_date'] = datetime.fromisoformat(data['publish_date'])
        if data.get('bidding_deadline') and isinstance(data['bidding_deadline'], str):
            data['bidding_deadline'] = datetime.fromisoformat(data['bidding_deadline'])
        if isinstance(data.get('crawled_at'), str):
            data['crawled_at'] = datetime.fromisoformat(data['crawled_at'])
        return cls(**data)
