#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复招投标数据的三个问题：
1. 移除标题中的关键词标注
2. 确保关键词位置字段存在
3. 过滤过期和中标结果项目
"""

import json
import re
from datetime import datetime


def fix_data():
    """修复数据"""
    
    # 读取原始数据
    with open('data/bidding_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"原始数据: {len(data)} 条")
    
    fixed_data = []
    removed_count = 0
    today = datetime.now().date()
    
    for item in data:
        # 1. 移除标题中的关键词标注
        title = item.get('title', '')
        # 移除类似 "(广告,标识等在内容中)" 的标注
        clean_title = re.sub(r'\s*\([^)]*在[^)]*\)\s*$', '', title)
        item['title'] = clean_title.strip()
        
        # 2. 确保关键词位置字段存在
        if 'keyword_location' not in item:
            # 从旧的 keyword_location_tag 中提取
            if 'keyword_location_tag' in item:
                tag = item['keyword_location_tag']
                if '标题' in tag:
                    item['keyword_location'] = ['标题']
                elif '内容' in tag:
                    item['keyword_location'] = ['正文']
                else:
                    item['keyword_location'] = ['未知']
            else:
                item['keyword_location'] = ['未知']
        
        # 转换为更友好的显示文本
        keyword_locations = []
        for loc in item.get('keyword_location', []):
            if loc == '正文' or '内容' in loc:
                keyword_locations.append('关键字在内容中')
            elif loc == '标题':
                keyword_locations.append('关键字在标题')
            else:
                keyword_locations.append(loc)
        
        item['keyword_location_display'] = ', '.join(keyword_locations) if keyword_locations else '未知'
        
        # 3. 过滤条件
        # 3.1 移除中标结果
        if item.get('info_type') == '中标结果':
            removed_count += 1
            continue
        
        # 3.2 检查投标截止日期
        deadline = item.get('bidding_deadline')
        if deadline and deadline != '详见内容':
            try:
                # 解析日期
                if isinstance(deadline, str):
                    deadline_date = datetime.strptime(deadline[:10], '%Y-%m-%d').date()
                    # 如果截止日期早于今天，跳过
                    if deadline_date < today:
                        removed_count += 1
                        continue
            except:
                pass  # 日期格式错误，保留该项目
        
        fixed_data.append(item)
    
    print(f"修复后数据: {len(fixed_data)} 条")
    print(f"移除项目: {removed_count} 条")
    
    # 统计关键词位置
    location_stats = {}
    for item in fixed_data:
        loc = item.get('keyword_location_display', '未知')
        location_stats[loc] = location_stats.get(loc, 0) + 1
    
    print("\n关键词位置分布:")
    for loc, count in location_stats.items():
        print(f"  {loc}: {count} 条")
    
    # 保存修复后的数据
    with open('data/bidding_data.json', 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 数据已保存到 data/bidding_data.json")
    
    # 显示几个示例
    print("\n示例数据（前3条）:")
    for i, item in enumerate(fixed_data[:3]):
        print(f"\n{i+1}. {item['title']}")
        print(f"   关键词位置: {item['keyword_location_display']}")
        print(f"   发布日期: {item.get('publish_date', 'N/A')}")
        print(f"   截止日期: {item.get('bidding_deadline', 'N/A')}")
        print(f"   详情页: {item.get('detail_url', 'N/A')[:80]}...")


if __name__ == '__main__':
    fix_data()
