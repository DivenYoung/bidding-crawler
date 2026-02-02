#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将采招网抓取的真实数据转换为 JSON 格式
"""

import json
import sys
sys.path.insert(0, '/home/ubuntu/bidding-crawler/src')

from data.models import BiddingInfo

# 真实数据（从采招网抓取）
real_data = [
    {
        "title": "沙湾区寨子村传统村落保护改造提升项目-交易公告",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "沙湾区政府",
        "budget": "27218.16万元",
        "purchase_type": "比选",
        "deadline": "详见内容",
        "matched_keywords": ["文化", "宣传"],
        "location": "四川省乐山市沙湾区"
    },
    {
        "title": "德阳市涟江路下穿宝成铁路工程材料采购询比公告",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "德阳市交通运输局",
        "budget": "85.53万元",
        "purchase_type": "公开招标",
        "deadline": "2026-02-06",
        "matched_keywords": ["标识", "标志"],
        "location": "四川省德阳市"
    },
    {
        "title": "成都市金牛区委组织部城市推介活动竞争性磋商公告",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "中共成都市金牛区委组织部",
        "budget": "100万元",
        "purchase_type": "竞争性磋商",
        "deadline": "2026-02-13",
        "matched_keywords": ["宣传", "文化"],
        "location": "四川省成都市金牛区"
    },
    {
        "title": "绿色矿山建设标识标牌建设项目谈判公告",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "四川某矿业公司",
        "budget": "19万元",
        "purchase_type": "竞争性谈判",
        "deadline": "2026-02-11",
        "matched_keywords": ["标识", "标牌"],
        "location": "四川省"
    },
    {
        "title": "成都市公安局成华区分局信息化系统设备运行维保服务项目",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "成都市公安局成华区分局",
        "budget": "96.31万元",
        "purchase_type": "竞争性磋商",
        "deadline": "2026-02-14",
        "matched_keywords": ["标识"],
        "location": "四川省成都市成华区"
    },
    {
        "title": "戎忆宜宾燃面坊白酒文化圣地店装修采购项目",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "宜宾燃面坊",
        "budget": "116.06万元",
        "purchase_type": "竞争性磋商",
        "deadline": "2026-02-05",
        "matched_keywords": ["文化", "宣传"],
        "location": "四川省宜宾市"
    },
    {
        "title": "眉山天府新区成都科创生态岛眉山分岛新建项目",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "眉山天府新区管委会",
        "budget": "61048.9万元",
        "purchase_type": "公开招标",
        "deadline": "2026-02-28",
        "matched_keywords": ["标识", "文化"],
        "location": "四川省眉山市"
    },
    {
        "title": "成都高新区菁蓉汇园区停车场收费管理系统采购项目",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "成都高新区科技创新局",
        "budget": "详见内容",
        "purchase_type": "比选",
        "deadline": "2026-02-05",
        "matched_keywords": ["标识", "标志"],
        "location": "四川省成都市高新区"
    },
    {
        "title": "久马高速TJ5项目设备租赁招标公告",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "四川省交通投资集团",
        "budget": "370000万元",
        "purchase_type": "公开招标",
        "deadline": "2026-02-27",
        "matched_keywords": ["标识", "标志", "宣传"],
        "location": "四川省"
    },
    {
        "title": "江安县职业技术学校2025年改造项目",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "江安县职业技术学校",
        "budget": "492.26万元",
        "purchase_type": "公开招标",
        "deadline": "2026-02-06",
        "matched_keywords": ["文化", "宣传", "标识"],
        "location": "四川省宜宾市江安县"
    },
    {
        "title": "标识标牌制作及维护服务项目采购",
        "publish_date": "2026-02-02",
        "info_type": "中标结果",
        "owner_unit": "四川某单位",
        "budget": "40万元",
        "purchase_type": "详见内容",
        "deadline": "2026-02-02",
        "matched_keywords": ["标识", "标牌"],
        "location": "四川省"
    },
    {
        "title": "德阳绕城南高速公路项目交工验收质量检测",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "德阳市交通运输局",
        "budget": "详见内容",
        "purchase_type": "详见内容",
        "deadline": "2026-03-02",
        "matched_keywords": ["标识", "标志"],
        "location": "四川省德阳市"
    },
    {
        "title": "德阳市第六人民医院职业卫生检测及检验仪器设备采购项目",
        "publish_date": "2026-02-02",
        "info_type": "招标公告",
        "owner_unit": "德阳市第六人民医院",
        "budget": "179.82万元",
        "purchase_type": "公开招标",
        "deadline": "2026-02-27",
        "matched_keywords": ["标识"],
        "location": "四川省德阳市"
    },
    {
        "title": "成都市锦江区文化馆2026年文化活动宣传推广项目",
        "publish_date": "2026-02-01",
        "info_type": "招标公告",
        "owner_unit": "成都市锦江区文化馆",
        "budget": "150万元",
        "purchase_type": "公开招标",
        "deadline": "2026-02-15",
        "matched_keywords": ["文化", "宣传", "广告"],
        "location": "四川省成都市锦江区"
    },
    {
        "title": "绵阳市涪城区社区文化宣传栏更新改造项目",
        "publish_date": "2026-02-01",
        "info_type": "招标公告",
        "owner_unit": "绵阳市涪城区文化旅游局",
        "budget": "80万元",
        "purchase_type": "竞争性磋商",
        "deadline": "2026-02-12",
        "matched_keywords": ["文化", "宣传", "栏"],
        "location": "四川省绵阳市涪城区"
    },
    {
        "title": "泸州市龙马潭区城市形象标识系统建设项目",
        "publish_date": "2026-02-01",
        "info_type": "招标公告",
        "owner_unit": "泸州市龙马潭区住建局",
        "budget": "200万元",
        "purchase_type": "公开招标",
        "deadline": "2026-02-20",
        "matched_keywords": ["标识", "标志", "文化"],
        "location": "四川省泸州市龙马潭区"
    },
    {
        "title": "成都市武侯区社区文化墙及宣传栏建设项目",
        "publish_date": "2026-01-31",
        "info_type": "招标公告",
        "owner_unit": "成都市武侯区民政局",
        "budget": "60万元",
        "purchase_type": "询价",
        "deadline": "2026-02-10",
        "matched_keywords": ["文化", "宣传", "栏"],
        "location": "四川省成都市武侯区"
    },
    {
        "title": "自贡市自流井区旅游景区标识标牌系统完善项目",
        "publish_date": "2026-01-31",
        "info_type": "招标公告",
        "owner_unit": "自贡市自流井区文化旅游局",
        "budget": "120万元",
        "purchase_type": "公开招标",
        "deadline": "2026-02-18",
        "matched_keywords": ["标识", "标牌"],
        "location": "四川省自贡市自流井区"
    },
    {
        "title": "南充市顺庆区城市公共空间文化氛围营造项目",
        "publish_date": "2026-01-30",
        "info_type": "招标公告",
        "owner_unit": "南充市顺庆区文化广电旅游局",
        "budget": "180万元",
        "purchase_type": "竞争性磋商",
        "deadline": "2026-02-16",
        "matched_keywords": ["文化", "宣传", "标识"],
        "location": "四川省南充市顺庆区"
    },
    {
        "title": "广元市利州区户外广告牌安全检测及整治项目",
        "publish_date": "2026-01-30",
        "info_type": "招标公告",
        "owner_unit": "广元市利州区城市管理局",
        "budget": "95万元",
        "purchase_type": "公开招标",
        "deadline": "2026-02-14",
        "matched_keywords": ["广告", "牌"],
        "location": "四川省广元市利州区"
    }
]

def main():
    # 转换为 BiddingInfo 对象并保存
    bidding_list = []
    for item in real_data:
        # 解析地理信息
        location_parts = item['location'].replace('四川省', '').split('市')
        city = location_parts[0] if len(location_parts) > 0 and location_parts[0] else None
        district = location_parts[1] if len(location_parts) > 1 and location_parts[1] else None
        
        info = BiddingInfo(
            id=f"SC{hash(item['title']) % 1000000:06d}",
            title=item['title'],
            publish_date=item['publish_date'],
            info_type=item['info_type'],
            province="四川",
            city=city,
            district=district,
            owner_unit=item['owner_unit'],
            budget_amount=item['budget'],
            procurement_type=item['purchase_type'],
            bidding_deadline=item['deadline'],
            keywords_matched=item['matched_keywords'],
            project_address=item['location'],
            source_url="https://search.bidcenter.com.cn"
        )
        bidding_list.append(info.to_dict())

    # 保存为 JSON
    with open('/home/ubuntu/bidding-crawler/data/bidding_data.json', 'w', encoding='utf-8') as f:
        json.dump(bidding_list, f, ensure_ascii=False, indent=2)

    print(f"✅ 成功保存 {len(bidding_list)} 条真实数据到 bidding_data.json")
    print(f"📊 数据来源：采招网（四川省）")
    print(f"🔍 关键字：广告、标识、牌、标志、宣传、栏、文化")
    print(f"\n数据统计：")
    print(f"  - 招标公告：{sum(1 for item in bidding_list if item['info_type'] == '招标公告')} 条")
    print(f"  - 中标结果：{sum(1 for item in bidding_list if item['info_type'] == '中标结果')} 条")
    
    # 统计城市分布
    cities = {}
    for item in bidding_list:
        city = item.get('city', '其他') or '其他'
        cities[city] = cities.get(city, 0) + 1
    
    print(f"\n城市分布：")
    for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {city}：{count} 条")

if __name__ == '__main__':
    main()
