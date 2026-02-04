#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从采招网HTML中提取项目信息和详情页链接
"""

import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import unquote


def parse_html(html_file):
    """解析HTML文件"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有项目列表项
    project_items = soup.find_all('div', class_='ssjg-list_cell')
    
    print(f"找到 {len(project_items)} 个项目\n")
    
    projects = []
    
    for item in project_items:
        try:
            # 提取信息类型
            info_type_elem = item.find('span', class_='ssjg-leixing')
            info_type = info_type_elem.text.strip() if info_type_elem else '未知'
            
            # 提取标题和详情页链接
            title_elem = item.find('a', class_='ssjg-title')
            if not title_elem:
                continue
            
            title = title_elem.get('title', '').strip()
            detail_url = title_elem.get('href', '').strip()
            
            # 提取项目ID (tid属性)
            project_id = title_elem.get('tid', '')
            
            # 清理详情页链接（移除 // 前缀）
            if detail_url.startswith('//'):
                detail_url = 'https:' + detail_url
            
            # 提取关键词位置
            keyword_location_elem = item.find('span', class_='ssjg-title')
            keyword_location_text = ''
            if keyword_location_elem:
                font_elem = keyword_location_elem.find('font')
                if font_elem:
                    parent_text = keyword_location_elem.get_text()
                    if '在内容中' in parent_text:
                        keyword_location_text = '关键字在内容中'
                    elif '在内容或附件中' in parent_text:
                        keyword_location_text = '关键字在内容或附件中'
                    elif '在标题' in parent_text:
                        keyword_location_text = '关键字在标题'
                    else:
                        keyword_location_text = '关键字在内容中'
            
            # 检查是否有附件
            has_attachments = bool(item.find('span', class_='fujian-label'))
            
            # 提取采购预算
            budget_elem = item.find('i', class_='yusuan')
            budget = ''
            if budget_elem:
                budget_text = budget_elem.get_text().strip()
                # 移除 <i class="defaut"> 标签
                budget = re.sub(r'<[^>]+>', '', budget_text).strip()
            
            # 提取采购方式
            procurement_elem = item.find('i', class_='fangshi')
            procurement_type = procurement_elem.text.strip() if procurement_elem else ''
            
            # 提取截止时间
            deadline_elem = item.find('i', class_='jiezhi')
            deadline = deadline_elem.text.strip() if deadline_elem else '详见内容'
            
            # 提取地区
            region_elem = item.find('span', class_='diqu')
            region = region_elem.get('title', '').strip() if region_elem else ''
            
            # 提取发布日期
            publish_date_elem = item.find('span', class_='ssjg-shijian')
            publish_date = publish_date_elem.text.strip() if publish_date_elem else ''
            
            # 构造项目数据
            project = {
                'id': project_id,
                'title': title,
                'info_type': info_type,
                'publish_date': publish_date,
                'province': region if region else '四川',
                'city': '',  # 需要从详情页提取
                'district': '',
                'owner_unit': '',
                'budget_amount': budget,
                'procurement_type': procurement_type,
                'bidding_deadline': deadline,
                'keywords_matched': [],  # 需要匹配关键词
                'project_address': '',
                'attachments': [],
                'source_url': detail_url,
                'detail_url': detail_url,
                'crawled_at': datetime.now().isoformat(),
                'keyword_location': ['正文'] if '内容' in keyword_location_text else ['标题'],
                'keyword_location_display': keyword_location_text,
                'has_attachments': has_attachments,
                'has_bidding_docs': False
            }
            
            projects.append(project)
            
        except Exception as e:
            print(f"解析项目时出错: {e}")
            continue
    
    return projects


def main():
    """主函数"""
    
    # 解析HTML
    projects = parse_html('/home/ubuntu/upload/pasted_content.txt')
    
    print(f"\n成功提取 {len(projects)} 个项目\n")
    
    # 显示前5个项目
    print("前5个项目：\n")
    for i, project in enumerate(projects[:5]):
        print(f"{i+1}. {project['title']}")
        print(f"   项目ID: {project['id']}")
        print(f"   信息类型: {project['info_type']}")
        print(f"   发布日期: {project['publish_date']}")
        print(f"   截止时间: {project['bidding_deadline']}")
        print(f"   关键字位置: {project['keyword_location_display']}")
        print(f"   详情页: {project['detail_url'][:80]}...")
        print()
    
    # 保存到文件
    output_file = '/tmp/bidding-crawler/data/bidding_data_new.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已保存到 {output_file}")
    
    # 统计信息
    info_type_stats = {}
    for project in projects:
        info_type = project['info_type']
        info_type_stats[info_type] = info_type_stats.get(info_type, 0) + 1
    
    print("\n信息类型统计：")
    for info_type, count in info_type_stats.items():
        print(f"  {info_type}: {count} 条")
    
    # 关键词位置统计
    keyword_location_stats = {}
    for project in projects:
        loc = project['keyword_location_display']
        keyword_location_stats[loc] = keyword_location_stats.get(loc, 0) + 1
    
    print("\n关键词位置统计：")
    for loc, count in keyword_location_stats.items():
        print(f"  {loc}: {count} 条")


if __name__ == '__main__':
    main()
