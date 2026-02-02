"""
Streamlit Web 应用 - 招投标信息展示
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import re

# 页面配置
st.set_page_config(
    page_title="招投标信息监控系统",
    page_icon="📊",
    layout="wide"
)

# 标题
st.title("📊 招投标信息监控系统")
st.markdown("**数据来源：采招网（四川省）** | 关键字：广告、标识、牌、标志、宣传、栏、文化")

# 加载数据
@st.cache_data
def load_data():
    """加载招投标数据"""
    data_file = Path("/home/ubuntu/bidding-crawler/data/bidding_data.json")
    if not data_file.exists():
        return pd.DataFrame()
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    # 处理标题：移除括号中的位置标注，得到纯净标题
    if 'title' in df.columns:
        df['clean_title'] = df['title'].apply(lambda x: re.sub(r'\s*\([^)]*在[^)]*中)\)\s*$', '', x))
    
    # 处理关键字位置标注：使用真实的完整标注
    if 'keyword_location_tag' in df.columns:
        df['location_display'] = df['keyword_location_tag'].apply(
            lambda x: '标题' if x == '' else x
        )
    
    # 转换日期格式
    if 'publish_date' in df.columns:
        df['publish_date'] = pd.to_datetime(df['publish_date']).dt.date
    
    return df

# 加载数据
df = load_data()

if df.empty:
    st.warning("暂无数据，请先运行爬虫抓取数据")
    st.stop()

# 侧边栏 - 筛选条件
st.sidebar.header("🔍 筛选条件")

# 时间范围筛选
if 'publish_date' in df.columns:
    min_date = df['publish_date'].min()
    max_date = df['publish_date'].max()
    
    date_range = st.sidebar.date_input(
        "发布日期范围",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        df = df[(df['publish_date'] >= date_range[0]) & (df['publish_date'] <= date_range[1])]

# 城市筛选
if 'city' in df.columns:
    cities = ['全部'] + sorted([c for c in df['city'].unique() if c])
    selected_city = st.sidebar.selectbox("城市", cities)
    if selected_city != '全部':
        df = df[df['city'] == selected_city]

# 信息类型筛选
if 'info_type' in df.columns:
    info_types = ['全部'] + sorted(df['info_type'].unique().tolist())
    selected_type = st.sidebar.selectbox("信息类型", info_types)
    if selected_type != '全部':
        df = df[df['info_type'] == selected_type]

# 关键字位置筛选
if 'keyword_location_tag' in df.columns:
    st.sidebar.subheader("关键字位置")
    show_in_title = st.sidebar.checkbox("📄 关键字在标题", value=True)
    show_in_content = st.sidebar.checkbox("📝 关键字在内容中", value=True)
    show_in_attachment = st.sidebar.checkbox("📎 关键字在内容或附件中", value=True)
    show_in_bidding_doc = st.sidebar.checkbox("📋 关键字在内容或标书中", value=True)
    
    # 根据选择筛选
    selected_tags = []
    if show_in_title:
        selected_tags.append("")
    if show_in_content:
        selected_tags.append("广告,标识等在内容中")
    if show_in_attachment:
        selected_tags.append("广告,标识等在内容或附件中")
    if show_in_bidding_doc:
        selected_tags.append("广告,标识等在内容或标书中")
    
    if selected_tags:
        df = df[df['keyword_location_tag'].isin(selected_tags)]

# 关键字筛选
keyword_filter = st.sidebar.text_input("标题关键字")
if keyword_filter:
    df = df[df['clean_title'].str.contains(keyword_filter, case=False, na=False)]

# 统计信息
st.header("📈 数据统计")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("项目总数", len(df))

with col2:
    if 'info_type' in df.columns:
        bidding_count = len(df[df['info_type'] == '招标公告'])
        st.metric("招标公告", bidding_count)

with col3:
    if 'keyword_location_tag' in df.columns:
        in_title_count = len(df[df['keyword_location_tag'] == ""])
        st.metric("关键字在标题", in_title_count)

with col4:
    if 'keyword_location_tag' in df.columns:
        in_content_count = len(df[df['keyword_location_tag'] != ""])
        st.metric("关键字在内容", in_content_count)

# 数据展示
st.header("📋 项目列表")

# 准备展示的数据
display_df = df.copy()

# 选择要展示的列并重命名
column_mapping = {
    'clean_title': '项目标题',
    'publish_date': '发布日期',
    'info_type': '信息类型',
    'location_display': '关键字位置',
    'owner_unit': '业主单位',
    'budget_amount': '预算金额',
    'procurement_type': '采购类型',
    'bidding_deadline': '投标截止时间',
    'keywords_matched': '匹配关键字',
    'project_address': '项目地址',
    'detail_url': '详情链接'
}

# 只保留存在的列
available_columns = [col for col in column_mapping.keys() if col in display_df.columns]
display_df = display_df[available_columns]
display_df = display_df.rename(columns=column_mapping)

# 处理关键字列表显示
if '匹配关键字' in display_df.columns:
    display_df['匹配关键字'] = display_df['匹配关键字'].apply(
        lambda x: ', '.join(x) if isinstance(x, list) else str(x)
    )

# 显示数据表格
st.dataframe(
    display_df,
    use_container_width=True,
    height=600,
    column_config={
        "项目标题": st.column_config.TextColumn(
            "项目标题",
            width="large",
            help="项目的完整标题（已移除位置标注）"
        ),
        "关键字位置": st.column_config.TextColumn(
            "关键字位置",
            width="medium",
            help="关键字出现的具体位置"
        ),
        "预算金额": st.column_config.TextColumn(
            "预算金额",
            width="small",
        ),
        "详情链接": st.column_config.LinkColumn(
            "详情链接",
            display_text="查看详情",
            width="small",
        ),
    }
)

# 导出功能
st.header("📥 数据导出")
col1, col2 = st.columns(2)

with col1:
    # 导出为 CSV
    csv = display_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 导出为 CSV",
        data=csv,
        file_name=f"bidding_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    # 导出为 JSON
    json_str = df.to_json(orient='records', force_ascii=False, indent=2)
    st.download_button(
        label="📥 导出为 JSON",
        data=json_str,
        file_name=f"bidding_data_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )

# 关键字位置说明
st.header("📖 关键字位置说明")

st.markdown("""
| 显示内容 | 含义 | 示例 |
|---------|------|------|
| **标题** | 关键字直接出现在项目标题中 | 绿色矿山建设**标识标牌**建设项目谈判公告 |
| **广告,标识等在内容中** | 关键字出现在项目正文内容中 | 沙湾区寨子村传统村落保护改造提升项目 |
| **广告,标识等在内容或附件中** | 关键字出现在项目正文或附件文件中 | 中国共产党犍为县委员会政法委员会犍为县综治中心运行维护及辅助服务项目 |
| **广告,标识等在内容或标书中** | 关键字出现在项目正文或标书文件中 | 国家税务总局剑阁县税务局2026年职工食材采购项目 |

**说明**：
- "标题"类型的项目通常更相关，关键字直接出现在项目名称中
- "内容"类型的项目需要查看详情页确认相关性
- "附件"或"标书"类型的项目可能包含更详细的技术要求
""")

# 页脚
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: gray;'>
    <p>招投标信息监控系统 v1.4 | 数据来源：采招网</p>
    <p>关键字：广告、标识、牌、标志、宣传、栏、文化 | 地区：四川省</p>
    <p>更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
