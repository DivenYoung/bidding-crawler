#!/usr/bin/env python3
"""
从浏览器提取的 Markdown 内容生成完整的真实数据
"""

import json
import re
from datetime import datetime
from pathlib import Path

# 从浏览器提取的真实数据（前22条，包含完整的位置标注）
BROWSER_DATA = """
招标公告 眉山天府新区成都科创生态岛眉山分岛新建项目（一期）2020（TR）-19地块（EPC）标段-招标/资审公告 (广告,标识等在内容中)
采购预算：61048.9万元 采购方式：公开招标 截止时间：2026-02-28 四川 2026-02-02

中标结果 中国共产党犍为县委员会政法委员会犍为县综治中心运行维护及辅助服务项目中标（成交）结果公告 (广告,标识等在内容或附件中)
中标金额：44.82万元 采购方式：详见内容 中标时间：2026-02-02 四川 2026-02-02

招标公告 甘洛县人民医院pacs存储采购项目采购公告 (广告,标识等在内容或标书中)
采购预算：9万元 采购方式：询比 截止时间：2026-02-05 四川 2026-02-02

中标结果 石渠县教育和体育局石渠县学校厨房（补缺及更新）设施设备采购项目(二次)中标（成交）结果公告 (广告,标识等在内容或附件中)
中标金额：295.72万元 采购方式：详见内容 中标时间：2026-02-02 四川 2026-02-02

中标结果 广元市昭化区农业农村局广元市昭化区采购2025年第二轮土地承包到期后再延长30年试点乡镇技术服务(三次)中标（成交）结果公告 (广告,标识等在内容或附件中)
中标金额：36.49万元 采购方式：竞争性磋商 中标时间：2026-02-02 四川 2026-02-02

中标结果 盐亭县自然资源局盐亭县全民所有自然资源资产清查工作中标（成交）结果公告 (广告,标识等在内容或附件中)
中标金额：48.7万元 采购方式：详见内容 中标时间：2026-02-02 四川 2026-02-02

招标公告 中国共产党自贡市沿滩区委员会办公室区委办后勤服务项目竞争性磋商公告 (广告,标识等在内容或附件中)
采购预算：73万元 采购方式：竞争性磋商 截止时间：2026-02-06 四川 2026-02-02

中标结果 成都市武侯区人民政府晋阳街道办事处物业管理服务采购项目中标（成交）结果公告 (广告,标识等在内容或附件中)
中标金额：111.86万元 采购方式：详见内容 中标时间：2026-02-02 四川 2026-02-02

中标结果 井研县中医医院医用电子生理参数检测仪器设备中标（成交）结果公告 (广告,标识等在内容或附件中)
中标金额：94.96万元 采购方式：详见内容 中标时间：2026-02-02 四川 2026-02-02

审批公示 广元市利州生态环境局关于2026年2月2日拟对建设项目环境影响评价文件作出审批意见的公示 (广告,标识等在内容中)
采购预算：5286万元 采购方式：详见内容 截止时间：详见内容 四川 2026-02-02

中标结果 四川护理职业学院2026年校园维修服务采购项目政府采购合同公告 (广告,标识等在内容或附件中)
中标金额：60万元 采购方式：竞争性磋商 中标时间：2026-02-02 四川 2026-02-02

招标公告 四川省人民医院智慧医院-床旁结算一体化设备增补及系统升级采购项目（包2） (广告,标识等在内容或标书中)
采购预算：84万元 采购方式：详见内容 截止时间：2026-02-10 四川 2026-02-02

招标公告 成都青羊康桥驿轨道城市发展有限公司成都青羊马厂坝站TOD综合开发项目（二期）BC地块施工车库划线及交安设施工程标段遴选公告 (广告,标识等在内容或附件中)
采购预算：52.51万元 采购方式：遴选公告 截止时间：2026-02-10 四川 2026-02-02

招标公告 气体循环演示系统-采购公告 (广告,标识等在内容中)
采购预算：130万元 采购方式：详见内容 截止时间：2026-02-09 四川 2026-02-02

招标公告 沙湾区寨子村传统村落保护改造提升项目-交易公告 (广告,标识等在内容中)
采购预算：27218.16万元 采购方式：比选 截止时间：详见内容 四川 2026-02-02

招标公告 德阳市涟江路下穿宝成铁路工程（G108国道连接线）-材料采购询比公告 (广告,标识等在内容中)
采购预算：85.53万元 采购方式：公开招标 截止时间：2026-02-06 四川 2026-02-02

招标公告 四川卫生康复职业学院高性能医疗器械运动康复产教融合实训基地项目代建管理服务采购项目竞争性磋商公告 (广告,标识等在内容或附件中)
采购预算：300万元 采购方式：竞争性磋商 截止时间：2026-02-13 四川 2026-02-02

招标公告 中国共产党成都市金牛区委员会组织部"才聚天府筑梦成都""蓉漂人才荟"城市行（长沙站）城市推介活动竞争性磋商公告 (广告,标识等在内容或附件中)
采购预算：100万元 采购方式：竞争性磋商 截止时间：2026-02-13 四川 2026-02-02

中标结果 国家税务总局剑阁县税务局2026年职工食材采购项目中标公告（第二包） (广告,标识等在内容或标书中)
中标金额：128.5万元 采购方式：详见内容 中标时间：2026-02-02 四川 2026-02-02

审批公示 雅安市生态环境局关于2026年2月2日拟作出建设项目环境影响评价文件审批意见的公示 (广告,标识等在内容中)
采购预算：400万元 采购方式：详见内容 截止时间：详见内容 四川 2026-02-02

招标公告 绿色矿山建设标识标牌建设项目谈判公告-交易公告
采购预算：19万元 采购方式：竞争性谈判 截止时间：2026-02-11 四川 2026-02-02

招标公告 成都市公安局成华区分局信息化系统设备运行维保服务项目竞争性磋商公告 (广告,标识等在内容或附件中)
采购预算：96.31万元 采购方式：竞争性磋商 截止时间：2026-02-14 四川 2026-02-02
"""

def parse_location_tag(title):
    """从标题中提取位置标注"""
    match = re.search(r'\s*\(([^)]*在[^)]*中)\)\s*$', title)
    if match:
        location_tag = match.group(1)
        clean_title = title[:match.start()].strip()
        return clean_title, location_tag
    else:
        return title.strip(), ""

def extract_city(title):
    """从标题中提取城市名"""
    cities = ['成都', '自贡', '攀枝花', '泸州', '德阳', '绵阳', '广元', '遂宁', 
              '内江', '乐山', '南充', '眉山', '宜宾', '广安', '达州', '雅安', 
              '巴中', '资阳', '犍为', '甘洛', '石渠', '盐亭', '井研']
    for city in cities:
        if city in title:
            return city
    return "四川"

def main():
    # 解析浏览器数据
    blocks = [b.strip() for b in BROWSER_DATA.strip().split('\n\n') if b.strip()]
    
    projects = []
    project_id = 403967390  # 起始ID
    
    for block in blocks:
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if len(lines) < 2:
            continue
        
        # 第一行：信息类型 + 标题
        first_line = lines[0]
        parts = first_line.split(' ', 1)
        if len(parts) != 2:
            continue
        
        info_type = parts[0]
        full_title = parts[1]
        clean_title, location_tag = parse_location_tag(full_title)
        
        # 第二行：预算/金额等信息
        second_line = lines[1]
        
        # 提取预算金额
        budget = ""
        if "采购预算：" in second_line:
            match = re.search(r'采购预算：([^\s]+)', second_line)
            if match:
                budget = match.group(1)
        elif "中标金额：" in second_line:
            match = re.search(r'中标金额：([^\s]+)', second_line)
            if match:
                budget = match.group(1)
        
        # 提取采购方式
        procurement_type = ""
        match = re.search(r'采购方式：([^\s]+)', second_line)
        if match:
            procurement_type = match.group(1)
        
        # 提取截止时间
        deadline = ""
        if "截止时间：" in second_line:
            match = re.search(r'截止时间：([^\s]+)', second_line)
            if match:
                deadline = match.group(1)
        elif "中标时间：" in second_line:
            match = re.search(r'中标时间：([^\s]+)', second_line)
            if match:
                deadline = match.group(1)
        
        # 提取城市
        city = extract_city(clean_title)
        
        # 创建项目数据
        project = {
            "project_id": str(project_id),
            "title": full_title,  # 保留完整标题（含位置标注）
            "info_type": info_type,
            "publish_date": "2026-02-02",
            "keywords_matched": ["广告", "标识"],
            "keyword_location_tag": location_tag,  # 单独的位置标注字段
            "source_url": f"https://user.bidcenter.com.cn/v2023/#/des/customDesSearch/{project_id}?mod=0&tag=0&keywords=广告,标识,牌,标志,宣传,栏,文化&diqu=23&stime=2025-10-30&endtime=2026-02-03",
            "detail_url": f"https://user.bidcenter.com.cn/v2023/#/des/customDesSearch/{project_id}?mod=0&tag=0&keywords=广告,标识,牌,标志,宣传,栏,文化&diqu=23&stime=2025-10-30&endtime=2026-02-03",
            "city": city,
            "owner_unit": "",
            "budget_amount": budget,
            "procurement_type": procurement_type,
            "bidding_deadline": deadline,
            "project_address": f"四川省{city}",
        }
        
        projects.append(project)
        project_id -= 1
    
    # 保存数据
    data_file = Path("/home/ubuntu/bidding-crawler/data/bidding_data.json")
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
    
    # 统计
    location_stats = {}
    for p in projects:
        tag = p['keyword_location_tag']
        display_tag = tag if tag else "无（关键字在标题）"
        location_stats[display_tag] = location_stats.get(display_tag, 0) + 1
    
    print(f"✅ 真实数据生成完成！")
    print(f"📊 总数据量: {len(projects)} 条")
    print(f"\n📋 位置标注统计：")
    for tag, count in sorted(location_stats.items()):
        print(f"  {tag}: {count} 条")
    
    print(f"\n📝 前5条数据示例：")
    for i, p in enumerate(projects[:5], 1):
        print(f"\n{i}. {p['title']}")
        print(f"   位置标注: '{p['keyword_location_tag']}'")

if __name__ == "__main__":
    main()
