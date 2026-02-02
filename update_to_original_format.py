#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新数据，保留采招网原始的关键字位置标注
"""

import json
import re

def extract_location_tag(title: str) -> str:
    """
    从标题中提取原始的位置标注
    
    Args:
        title: 项目标题
        
    Returns:
        位置标注字符串，如 "(广告,标识等在内容中)"
    """
    # 提取括号中的内容
    match = re.search(r'\(([^)]*(?:广告|标识|牌|标志|宣传|栏|文化)[^)]*)\)', title)
    if match:
        return f"({match.group(1)})"
    
    # 如果标题中直接包含关键字但没有括号标注
    keywords = ['广告', '标识', '牌', '标志', '宣传', '栏', '文化']
    for keyword in keywords:
        if keyword in title:
            return ""  # 关键字在标题中，不需要标注
    
    return ""


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
        
        # 提取原始位置标注
        location_tag = extract_location_tag(title)
        
        # 添加到数据中
        item['keyword_location_tag'] = location_tag
        
        # 判断是否有附件或标书
        item['has_attachments'] = '附件' in location_tag
        item['has_bidding_docs'] = '标书' in location_tag
        
        updated_count += 1
        
        # 显示更新信息
        if location_tag:
            print(f"✓ {title[:50]}...")
            print(f"  标注: {location_tag}")
        else:
            print(f"✓ {title[:50]}... (关键字在标题中)")
    
    # 保存更新后的数据
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功更新 {updated_count} 条数据")
    
    # 统计信息
    with_tag_count = sum(1 for item in data if item.get('keyword_location_tag'))
    attachment_count = sum(1 for item in data if item.get('has_attachments'))
    bidding_docs_count = sum(1 for item in data if item.get('has_bidding_docs'))
    
    print("\n📊 统计信息：")
    print(f"有位置标注: {with_tag_count} 条")
    print(f"关键字在标题: {len(data) - with_tag_count} 条")
    print(f"包含附件: {attachment_count} 条")
    print(f"包含标书: {bidding_docs_count} 条")


if __name__ == '__main__':
    main()
