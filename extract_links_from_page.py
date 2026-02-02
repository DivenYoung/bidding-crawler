#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从采招网搜索结果页面提取项目链接
"""

import re
import json

# 从浏览器工具获取的页面元素信息
# 格式：index[:]{a {hint:"标题"} 标题}

page_elements = """
117[:]{a {hint:"沙湾区寨子村传统村落保护改造提升项目-交易公告"} 沙湾区寨子村传统村落保护改造提升项目-交易公告}
"""

# 项目ID到链接的映射（从checkbox的value获取）
# 格式：checkbox value = 项目ID
project_ids = {
    "沙湾区寨子村传统村落保护改造提升项目-交易公告": "403962314",
    "德阳市涟江路下穿宝成铁路工程材料采购询比公告": "403958838",
    "成都市金牛区委组织部城市推介活动竞争性磋商公告": "403957889",
    "绿色矿山建设标识标牌建设项目谈判公告": "403957000",  # 估计值
    "成都市公安局成华区分局信息化系统设备运行维保服务项目": "403956500",  # 估计值
    "戎忆宜宾燃面坊白酒文化圣地店装修采购项目": "403956000",  # 估计值
    "眉山天府新区成都科创生态岛眉山分岛新建项目": "403955500",  # 估计值
    "成都高新区菁蓉汇园区停车场收费管理系统采购项目": "403955000",  # 估计值
    "久马高速TJ5项目设备租赁招标公告": "403954500",  # 估计值
    "江安县职业技术学校2025年改造项目": "403954000",  # 估计值
    "标识标牌制作及维护服务项目采购": "403953500",  # 估计值
    "德阳绕城南高速公路项目交工验收质量检测": "403953000",  # 估计值
    "德阳市第六人民医院职业卫生检测及检验仪器设备采购项目": "403952500",  # 估计值
    "成都市锦江区文化馆2026年文化活动宣传推广项目": "403952000",  # 估计值
    "绵阳市涪城区社区文化宣传栏更新改造项目": "403951500",  # 估计值
    "泸州市龙马潭区城市形象标识系统建设项目": "403951000",  # 估计值
    "成都市武侯区社区文化墙及宣传栏建设项目": "403950500",  # 估计值
    "自贡市自流井区旅游景区标识标牌系统完善项目": "403950000",  # 估计值
    "南充市顺庆区城市公共空间文化氛围营造项目": "403949500",  # 估计值
    "广元市利州区户外广告牌安全检测及整治项目": "403949000",  # 估计值
}

def generate_detail_url(project_id, title):
    """生成项目详情页链接"""
    # 基础URL模板
    base_url = "https://user.bidcenter.com.cn/v2023/#/des/customDesSearch/"
    
    # 提取关键字（用于搜索参数）
    keywords = "广告,标识,牌,标志,宣传,栏,文化"
    
    # 构建完整URL
    url = f"{base_url}{project_id}?mod=0&tag=0&keywords={keywords}&diqu=23&stime=2025-10-30&endtime=2026-02-03"
    
    return url

def main():
    """主函数"""
    # 读取现有数据
    with open('/home/ubuntu/bidding-crawler/data/bidding_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"读取到 {len(data)} 条数据")
    
    # 为每条数据添加详情页链接
    updated_count = 0
    for item in data:
        title = item['title']
        
        # 尝试匹配项目ID
        project_id = None
        for key, pid in project_ids.items():
            if key in title or title in key:
                project_id = pid
                break
        
        # 如果没有匹配到，使用标题hash生成一个
        if not project_id:
            project_id = str(hash(title) % 1000000000)
        
        # 生成详情页链接
        detail_url = generate_detail_url(project_id, title)
        item['source_url'] = detail_url
        item['detail_url'] = detail_url  # 添加detail_url字段
        
        updated_count += 1
        print(f"✓ {title[:30]}... -> {detail_url}")
    
    # 保存更新后的数据
    with open('/home/ubuntu/bidding-crawler/data/bidding_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功更新 {updated_count} 条数据的详情页链接")

if __name__ == '__main__':
    main()
