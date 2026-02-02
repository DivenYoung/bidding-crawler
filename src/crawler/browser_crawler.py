"""基于浏览器工具的爬虫方案

由于采招网有严格的反爬机制，Playwright 无头模式会被检测。
这个模块提供了一个基于浏览器工具的替代方案。

使用方法：
1. 手动在浏览器中打开采招网搜索页面
2. 将页面内容复制到文本文件
3. 使用此模块解析文本内容
"""

import re
from datetime import datetime
from typing import List, Dict, Optional
import structlog

logger = structlog.get_logger()


class BrowserCrawler:
    """基于浏览器内容的爬虫"""
    
    def __init__(self, keywords: List[str]):
        """
        初始化爬虫
        
        Args:
            keywords: 搜索关键字列表
        """
        self.keywords = keywords
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """解析日期字符串"""
        if not date_str:
            return None
        
        try:
            date_str = date_str.strip()
            
            if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                return datetime.strptime(date_str[:10], "%Y-%m-%d")
            
            match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_str)
            if match:
                year, month, day = match.groups()
                return datetime(int(year), int(month), int(day))
                
        except Exception as e:
            logger.warning("date_parse_failed", date_str=date_str, error=str(e))
        
        return None
    
    def parse_content(self, content: str, region_filter: str = None) -> List[Dict]:
        """
        从浏览器复制的内容中解析项目列表
        
        Args:
            content: 浏览器页面内容
            region_filter: 地区筛选（如"四川"）
            
        Returns:
            List[Dict]: 解析后的项目列表
        """
        items = []
        lines = content.strip().split('\n')
        
        current_item = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测新项目的开始
            info_types = ['招标公告', '中标结果', '招标变更', '采购信息', '拟在建项目', '拍卖转让', '招标预告']
            
            # 检测新项目
            found_new_item = False
            for info_type in info_types:
                if line.startswith(info_type):
                    # 保存上一个项目
                    if current_item and current_item.get('title'):
                        items.append(current_item)
                    
                    # 开始新项目
                    current_item = {
                        'id': None,
                        'title': '',
                        'info_type': info_type,
                        'publish_date': None,
                        'province': None,
                        'city': None,
                        'district': None,
                        'owner_unit': None,
                        'budget_amount': None,
                        'procurement_type': None,
                        'bidding_deadline': None,
                        'keywords_matched': [],
                        'project_address': None,
                        'attachments': [],
                        'source_url': ''
                    }
                    
                    # 提取标题
                    title = line[len(info_type):].strip()
                    title = re.sub(r'\s*\([^)]*\)\s*$', '', title)
                    current_item['title'] = title.strip()
                    found_new_item = True
                    break
            
            if not found_new_item and current_item:
                # 解析采购预算
                if '采购预算：' in line or '中标金额：' in line:
                    match = re.search(r'[采购预算|中标金额]：(.+?)(?:\s|$)', line)
                    if match:
                        current_item['budget_amount'] = match.group(1).strip()
                
                # 解析采购方式
                if '采购方式：' in line:
                    match = re.search(r'采购方式：(.+?)(?:\s|$)', line)
                    if match:
                        current_item['procurement_type'] = match.group(1).strip()
                
                # 解析截止时间
                if '截止时间：' in line:
                    match = re.search(r'截止时间：(.+?)(?:\s|$)', line)
                    if match:
                        deadline_str = match.group(1).strip()
                        current_item['bidding_deadline'] = self._parse_date(deadline_str)
                
                # 解析地区
                provinces = ['四川', '北京', '上海', '天津', '重庆', '河北', '山西', '辽宁', '吉林', 
                           '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', 
                           '湖南', '广东', '海南', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', 
                           '内蒙古', '广西', '西藏', '宁夏', '新疆']
                
                if line in provinces:
                    current_item['province'] = line
                
                # 解析日期
                date_match = re.match(r'(\d{4}-\d{2}-\d{2})$', line)
                if date_match:
                    current_item['publish_date'] = self._parse_date(date_match.group(1))
        
        # 保存最后一个项目
        if current_item and current_item.get('title'):
            items.append(current_item)
        
        # 生成项目ID
        for i, item in enumerate(items):
            if not item['id']:
                item['id'] = f"browser_{int(datetime.now().timestamp())}_{i}"
            
            if not item['source_url']:
                item['source_url'] = f"https://search.bidcenter.com.cn/search?keywords={','.join(self.keywords)}"
        
        # 地区筛选
        if region_filter:
            items = [item for item in items if item.get('province') == region_filter]
        
        logger.info("parse.complete", total=len(items), region=region_filter)
        
        return items
    
    def parse_from_file(self, file_path: str, region_filter: str = None) -> List[Dict]:
        """
        从文件中解析项目列表
        
        Args:
            file_path: 文本文件路径
            region_filter: 地区筛选
            
        Returns:
            List[Dict]: 解析后的项目列表
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.parse_content(content, region_filter)


# 使用示例
if __name__ == "__main__":
    # 示例：从浏览器复制的内容解析
    sample_content = """
招标公告 沙湾区寨子村传统村落保护改造提升项目-交易公告 (广告,标识在内容中)
采购预算：27218.16万元 
 采购方式：比选 截止时间：详见内容 
四川
2026-02-02
招标公告 江门市蓬江区棠下镇仁和路与建棠路交叉口北侧地块项目设计招标公告 (广告,标识在内容中)
采购预算：详见内容 采购方式：比选 截止时间：详见内容 
广东
2026-02-02
    """
    
    crawler = BrowserCrawler(['广告', '标识'])
    items = crawler.parse_content(sample_content, region_filter='四川')
    
    print(f"解析到 {len(items)} 条项目")
    for item in items:
        print(f"- {item['title']}")
