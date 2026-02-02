#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新现有数据，添加关键字位置信息
"""

import json
import re

# 关键字位置映射规则
# 基于采招网页面的标注格式
LOCATION_PATTERNS = {
    r'在内容中': ['正文'],
    r'在内容或附件中.*附件': ['正文', '附件'],
    r'在内容或标书中.*标书': ['正文', '标书'],
    r'在标题中': ['标题'],
}

def extract_keyword_location(title: str) -> tuple:
    """
    从标题中提取关键字位置信息
    
    Args:
        title: 项目标题
        
    Returns:
        (keyword_location, has_attachments, has_bidding_docs)
    """
    keyword_location = []
    has_attachments = False
    has_bidding_docs = False
    
    # 检查标题中是否包含关键字
    keywords = ['广告', '标识', '牌', '标志', '宣传', '栏', '文化']
    title_lower = title
    
    # 检查关键字是否在标题中（不在括号内）
    title_without_brackets = re.sub(r'\([^)]*\)', '', title)
    for keyword in keywords:
        if keyword in title_without_brackets:
            if '标题' not in keyword_location:
                keyword_location.append('标题')
            break
    
    # 检查括号中的位置标注
    bracket_match = re.search(r'\(([^)]+)\)', title)
    if bracket_match:
        bracket_content = bracket_match.group(1)
        
        # 检查是否在正文中
        if '在内容中' in bracket_content or '在正文中' in bracket_content:
            if '正文' not in keyword_location:
                keyword_location.append('正文')
        
        # 检查是否在附件中
        if '附件' in bracket_content:
            if '正文' not in keyword_location:
                keyword_location.append('正文')
            keyword_location.append('附件')
            has_attachments = True
        
        # 检查是否在标书中
        if '标书' in bracket_content:
            if '正文' not in keyword_location:
                keyword_location.append('正文')
            keyword_location.append('标书')
            has_bidding_docs = True
    
    # 如果没有任何位置信息，默认为正文
    if not keyword_location:
        keyword_location = ['正文']
    
    return keyword_location, has_attachments, has_bidding_docs


def main():
    """主函数"""
    # 读取现有数据
    data_file = '/home/ubuntu/bidding-crawler/data/bidding_data.json'
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"读取到 {len(data)} 条数据")
    
    # 更新每条数据
    updated_count = 0
    for item in data:
        title = item['title']
        
        # 提取关键字位置信息
        keyword_location, has_attachments, has_bidding_docs = extract_keyword_location(title)
        
        # 更新数据
        item['keyword_location'] = keyword_location
        item['has_attachments'] = has_attachments
        item['has_bidding_docs'] = has_bidding_docs
        
        updated_count += 1
        
        # 显示更新信息
        location_str = ', '.join(keyword_location)
        flags = []
        if has_attachments:
            flags.append('📎附件')
        if has_bidding_docs:
            flags.append('📋标书')
        flags_str = ' '.join(flags) if flags else ''
        
        print(f"✓ {title[:40]}...")
        print(f"  位置: {location_str} {flags_str}")
    
    # 保存更新后的数据
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功更新 {updated_count} 条数据的关键字位置信息")
    
    # 统计信息
    location_stats = {}
    attachment_count = 0
    bidding_docs_count = 0
    
    for item in data:
        for loc in item['keyword_location']:
            location_stats[loc] = location_stats.get(loc, 0) + 1
        if item['has_attachments']:
            attachment_count += 1
        if item['has_bidding_docs']:
            bidding_docs_count += 1
    
    print("\n📊 统计信息：")
    print(f"关键字位置分布：")
    for loc, count in sorted(location_stats.items()):
        print(f"  {loc}: {count} 条")
    print(f"包含附件: {attachment_count} 条")
    print(f"包含标书: {bidding_docs_count} 条")


if __name__ == '__main__':
    main()
