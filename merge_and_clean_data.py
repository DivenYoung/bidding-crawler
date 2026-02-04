#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并新旧数据，过滤过期项目
"""

import json
from datetime import datetime, timedelta


def merge_and_clean_data():
    """合并并清理数据"""
    
    # 读取新数据
    with open('/tmp/bidding-crawler/data/bidding_data_new.json', 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    
    print(f"新数据: {len(new_data)} 条")
    
    # 读取旧数据（如果存在）
    try:
        with open('/tmp/bidding-crawler/data/bidding_data.json', 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        print(f"旧数据: {len(old_data)} 条")
    except:
        old_data = []
        print("旧数据: 0 条（文件不存在）")
    
    # 合并数据（使用项目ID去重）
    all_data = {}
    
    # 先添加旧数据
    for item in old_data:
        project_id = item.get('id', '')
        if project_id:
            all_data[project_id] = item
    
    # 再添加新数据（会覆盖旧数据中的同ID项目）
    for item in new_data:
        project_id = item.get('id', '')
        if project_id:
            all_data[project_id] = item
    
    print(f"\n合并后: {len(all_data)} 条（去重）")
    
    # 过滤数据
    today = datetime.now().date()
    three_months_ago = today - timedelta(days=90)
    
    filtered_data = []
    removed_count = 0
    
    for project_id, item in all_data.items():
        # 1. 移除中标结果
        if item.get('info_type') == '中标结果':
            removed_count += 1
            continue
        
        # 2. 检查发布日期（保留3个月内的数据）
        publish_date_str = item.get('publish_date', '')
        if publish_date_str:
            try:
                publish_date = datetime.strptime(publish_date_str[:10], '%Y-%m-%d').date()
                if publish_date < three_months_ago:
                    removed_count += 1
                    continue
            except:
                pass  # 日期格式错误，保留
        
        # 3. 检查投标截止日期（移除已过期的）
        deadline = item.get('bidding_deadline', '')
        if deadline and deadline != '详见内容':
            try:
                deadline_date = datetime.strptime(deadline[:10], '%Y-%m-%d').date()
                if deadline_date < today:
                    removed_count += 1
                    continue
            except:
                pass  # 日期格式错误，保留
        
        filtered_data.append(item)
    
    print(f"过滤后: {len(filtered_data)} 条")
    print(f"移除: {removed_count} 条（中标结果 + 3个月前 + 已过期）")
    
    # 按发布日期排序（最新的在前）
    filtered_data.sort(key=lambda x: x.get('publish_date', ''), reverse=True)
    
    # 保存
    output_file = '/tmp/bidding-crawler/data/bidding_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 数据已保存到 {output_file}")
    
    # 统计信息
    print("\n=== 数据统计 ===")
    
    # 信息类型
    info_type_stats = {}
    for item in filtered_data:
        info_type = item.get('info_type', '未知')
        info_type_stats[info_type] = info_type_stats.get(info_type, 0) + 1
    
    print("\n信息类型：")
    for info_type, count in sorted(info_type_stats.items()):
        print(f"  {info_type}: {count} 条")
    
    # 关键词位置
    keyword_location_stats = {}
    for item in filtered_data:
        loc = item.get('keyword_location_display', '未知')
        keyword_location_stats[loc] = keyword_location_stats.get(loc, 0) + 1
    
    print("\n关键词位置：")
    for loc, count in sorted(keyword_location_stats.items()):
        print(f"  {loc}: {count} 条")
    
    # 发布日期分布
    date_stats = {}
    for item in filtered_data:
        date = item.get('publish_date', '未知')[:10]
        date_stats[date] = date_stats.get(date, 0) + 1
    
    print("\n发布日期分布（最近5天）：")
    for date in sorted(date_stats.keys(), reverse=True)[:5]:
        print(f"  {date}: {date_stats[date]} 条")
    
    # 显示示例
    print("\n=== 示例数据（前3条）===\n")
    for i, item in enumerate(filtered_data[:3]):
        print(f"{i+1}. {item['title']}")
        print(f"   项目ID: {item['id']}")
        print(f"   发布日期: {item.get('publish_date', 'N/A')}")
        print(f"   截止时间: {item.get('bidding_deadline', 'N/A')}")
        print(f"   关键字位置: {item.get('keyword_location_display', 'N/A')}")
        print(f"   详情页: {item.get('detail_url', 'N/A')[:80]}...")
        print()


if __name__ == '__main__':
    merge_and_clean_data()
