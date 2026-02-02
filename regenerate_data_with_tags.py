#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成数据，为标题添加原始的位置标注
"""

import json
from datetime import datetime

# 根据项目特征添加位置标注
def add_location_tag(title: str, has_keyword_in_title: bool) -> str:
    """
    为标题添加位置标注
    
    Args:
        title: 原始标题
        has_keyword_in_title: 标题中是否直接包含关键字
        
    Returns:
        带位置标注的完整标题
    """
    # 如果标题中直接包含关键字，不添加标注
    if has_keyword_in_title:
        return title
    
    # 否则添加 "(广告,标识等在内容中)" 标注
    return f"{title} (广告,标识等在内容中)"


def main():
    """主函数"""
    # 读取现有数据
    data_file = '/home/ubuntu/bidding-crawler/data/bidding_data.json'
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"读取到 {len(data)} 条数据")
    
    # 关键字列表
    keywords = ['广告', '标识', '牌', '标志', '宣传', '栏', '文化']
    
    # 更新每条数据
    updated_count = 0
    for item in data:
        original_title = item['title']
        
        # 检查标题中是否直接包含关键字
        has_keyword_in_title = any(kw in original_title for kw in keywords)
        
        # 添加位置标注
        full_title = add_location_tag(original_title, has_keyword_in_title)
        
        # 更新标题
        item['title'] = full_title
        
        # 提取位置标注信息
        if has_keyword_in_title:
            item['keyword_location_tag'] = ""
        else:
            item['keyword_location_tag'] = "(广告,标识等在内容中)"
        
        updated_count += 1
        
        # 显示更新信息
        if has_keyword_in_title:
            print(f"✓ {original_title[:50]}... [关键字在标题]")
        else:
            print(f"✓ {original_title[:50]}... [添加标注]")
    
    # 保存更新后的数据
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功更新 {updated_count} 条数据")
    
    # 统计信息
    with_tag_count = sum(1 for item in data if item.get('keyword_location_tag'))
    in_title_count = len(data) - with_tag_count
    
    print("\n📊 统计信息：")
    print(f"关键字在标题: {in_title_count} 条")
    print(f"关键字在内容: {with_tag_count} 条")


if __name__ == '__main__':
    main()
