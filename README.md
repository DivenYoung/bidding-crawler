# 招投标信息爬虫工具

## 项目简介

这是一个针对采招网的招投标信息爬虫工具，专门用于监控四川省的招投标项目。

### 核心功能

- ✅ 关键字匹配（广告、标识、牌、标志、宣传、栏、文化）
- ✅ 数据存储（JSON 格式）
- ✅ Streamlit 可视化界面
- ✅ 数据筛选和导出
- ✅ TDD 开发（12个单元测试全部通过）
- ✅ **真实爬虫实现（基于浏览器内容）**

### 技术栈

- Python 3.11
- Streamlit（Web界面）
- Playwright（浏览器自动化）
- pytest（测试框架）
- structlog（结构化日志）

---

## 快速开始

### 1. 安装依赖

```bash
cd /home/ubuntu/bidding-crawler
pip3 install -r requirements.txt
playwright install chromium
```

### 2. 配置

编辑 `config.yaml` 文件，配置关键字、地区等参数。

### 3. 抓取数据

**推荐方式：使用浏览器内容爬虫**

```bash
# 方式 A：使用 Manus 浏览器工具
# 1. 在 Manus 中使用浏览器工具访问采招网
# 2. 复制提取的 Markdown 内容到 browser_content.txt
# 3. 运行解析脚本
python3.11 crawl_from_browser.py

# 方式 B：手动复制粘贴
# 1. 在浏览器中打开: https://search.bidcenter.com.cn/search?keywords=广告,标识,牌,标志,宣传,栏,文化
# 2. 按 Ctrl+A 全选，Ctrl+C 复制
# 3. 粘贴到 browser_content.txt
# 4. 运行解析脚本
python3.11 crawl_from_browser.py
```

**备选方式：Playwright 爬虫（会触发验证码）**

```bash
python3.11 test_crawler.py
```

> ⚠️ **注意**：采招网使用了阿里云人机验证，Playwright 无头模式会被检测。详见 [爬虫使用指南](CRAWLER_GUIDE.md)。

### 4. 启动 Web 界面

```bash
streamlit run src/ui/app.py --server.port=8501
```

访问 http://localhost:8501 查看界面。

---

## 项目结构

```
bidding-crawler/
├── src/
│   ├── crawler/          # 爬虫模块
│   │   ├── search_crawler.py      # Playwright 爬虫
│   │   └── browser_crawler.py     # 浏览器内容爬虫（推荐）
│   ├── data/             # 数据层
│   │   ├── models.py     # 数据模型
│   │   ├── storage.py    # 存储层
│   │   ├── matcher.py    # 关键字匹配
│   │   └── deduplicator.py
│   ├── notification/     # 通知模块（待实现）
│   ├── ui/               # UI层
│   │   └── app.py        # Streamlit应用
│   └── scheduler/        # 调度器（待实现）
├── tests/
│   ├── unit/             # 单元测试
│   └── integration/      # 集成测试
├── data/
│   └── bidding_data.json # 数据文件
├── logs/                 # 日志目录
├── config.yaml           # 配置文件
├── main.py               # 主执行脚本（模拟数据）
├── test_crawler.py       # Playwright 爬虫测试
├── crawl_from_browser.py # 浏览器内容爬虫（推荐）
├── browser_content.txt   # 浏览器内容文件
├── CRAWLER_GUIDE.md      # 爬虫使用指南
└── README.md
```

---

## 运行测试

```bash
# 运行所有单元测试
pytest tests/unit/ -v

# 运行测试并查看覆盖率
pytest tests/unit/ --cov=src --cov-report=html
```

---

## 配置说明

### config.yaml

```yaml
crawler:
  keywords:              # 搜索关键字
    - 广告
    - 标识
    - 牌
    - 标志
    - 宣传
    - 栏
    - 文化
  
  search:
    region: 四川         # 地区筛选
    info_types:
      - 招标公告         # 信息类型
    time_range_full: 近三月
    time_range_incremental: 近一天
  
  anti_crawl:
    min_delay: 2.0       # 最小延迟（秒）
    max_delay: 5.0       # 最大延迟（秒）
    max_retries: 3       # 最大重试次数

storage:
  type: json
  json_path: ./data/bidding_data.json

ui:
  title: "四川省招投标信息监控系统"
  page_size: 50
```

---

## 爬虫方案对比

| 方案 | 优点 | 缺点 | 状态 |
|------|------|------|------|
| **浏览器内容爬虫** | 绕过验证码、稳定可靠 | 需要手动操作 | ✅ 已实现 |
| **Playwright 爬虫** | 可自动化 | 触发验证码 | ⚠️ 需优化 |
| **API 调用** | 高效稳定 | 需要逆向工程 | ⏳ 未实现 |

详细说明请查看 [爬虫使用指南](CRAWLER_GUIDE.md)。

---

## 数据字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| id | 项目唯一标识 | browser_1738491312_0 |
| title | 项目标题 | 沙湾区寨子村传统村落保护改造提升项目 |
| info_type | 信息类型 | 招标公告 |
| publish_date | 发布日期 | 2026-02-02 |
| province | 省份 | 四川 |
| city | 城市 | 乐山 |
| owner_unit | 业主单位 | （需进入详情页获取） |
| budget_amount | 预算金额 | 27218.16万元 |
| procurement_type | 采购类型 | 比选 |
| bidding_deadline | 投标截止时间 | 2026-02-20 17:00 |
| keywords_matched | 匹配的关键字 | ["广告", "标识"] |
| project_address | 项目地址 | 四川省乐山市沙湾区 |
| source_url | 来源链接 | https://search.bidcenter.com.cn/... |

---

## 使用示例

### 示例 1：抓取四川省招标信息

```bash
# 1. 访问采招网搜索页面
# 2. 复制内容到 browser_content.txt
# 3. 运行脚本
python3.11 crawl_from_browser.py

# 输出：
# ✅ 成功解析 1 条项目
# 📊 地区分布：
#   四川: 1 条
```

### 示例 2：查看 Streamlit 界面

```bash
streamlit run src/ui/app.py

# 界面功能：
# - 查看项目列表
# - 按时间/城市/关键字筛选
# - 导出为 CSV
```

---

## 开发日志

### 2026-02-02

#### MVP 阶段
- ✅ 完成 SDD 需求文档
- ✅ 搭建项目骨架
- ✅ 实现数据模型（BiddingInfo）
- ✅ 实现关键字匹配器（KeywordMatcher）
- ✅ 实现数据去重器（DataDeduplicator）
- ✅ 实现 JSON 存储层（JSONStorage）
- ✅ 实现 Streamlit UI
- ✅ 编写 12 个单元测试（全部通过）
- ✅ 创建模拟数据演示

#### 真实爬虫实现
- ✅ 调研采招网数据结构
- ✅ 实现 Playwright 爬虫（基础版）
- ⚠️ 发现人机验证问题
- ✅ 实现基于浏览器内容的爬虫（方案一）
- ✅ 测试并验证数据解析
- ✅ 编写爬虫使用指南

---

## 常见问题

### Q: 如何添加新的关键字？
A: 编辑 `config.yaml` 文件中的 `crawler.keywords` 列表。

### Q: 如何更改监控地区？
A: 编辑 `config.yaml` 文件中的 `crawler.search.region` 字段。

### Q: 数据存储在哪里？
A: 默认存储在 `./data/bidding_data.json`，可在配置文件中修改。

### Q: 如何导出数据？
A: 在 Streamlit 界面中点击"导出为 CSV"按钮。

### Q: 为什么 Playwright 爬虫会失败？
A: 采招网使用了阿里云人机验证，无头浏览器会被检测。请使用基于浏览器内容的爬虫方案。详见 [爬虫使用指南](CRAWLER_GUIDE.md)。

### Q: 如何获取更多数据？
A: 在浏览器中滚动页面，复制更多内容到 `browser_content.txt`，然后运行解析脚本。

---

## 后续迭代计划

### V1.1（1-2周）
- ✅ 实现真实爬虫（基于浏览器内容）
- ⏳ 优化 Playwright 爬虫，绕过验证码
- ⏳ 添加邮件通知功能
- ⏳ 实现定时任务调度

### V2.0（1-2个月）
- ⏳ PostgreSQL 持久化
- ⏳ NLP 语义匹配
- ⏳ 企业微信/钉钉机器人
- ⏳ Docker 容器化部署
- ⏳ API 逆向工程

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

---

## 许可证

MIT License

---

## 联系方式

如有问题或建议，请联系开发团队。
