# Git 提交记录

## 仓库信息

- **仓库地址**: https://github.com/DivenYoung/bidding-crawler
- **仓库类型**: Private（私有）
- **当前版本**: v1.2.0
- **分支**: main

---

## 提交历史

### 1. feat: 项目初始化 (1b3c3bc)

**提交内容**：
- 添加 `.gitignore` 忽略规则
- 添加 `requirements.txt` 依赖列表
- 添加 `config.yaml` 配置文件模板
- 添加 `pytest.ini` 测试配置

**文件**：
- `.gitignore`
- `requirements.txt`
- `config.yaml`
- `pytest.ini`

---

### 2. feat: 实现数据模型和基础数据处理模块 (4c87e55)

**提交内容**：
- 添加 `BiddingInfo` 数据模型，支持招投标信息结构化存储
- 实现 `KeywordMatcher` 关键字匹配器
- 实现 `DataDeduplicator` 数据去重器
- 实现 `JSONStorage` JSON 存储层
- 支持关键字位置标注（标题、正文、附件、标书）
- 支持详情页链接存储

**文件**：
- `src/data/models.py`
- `src/data/matcher.py`
- `src/data/deduplicator.py`
- `src/data/storage.py`

---

### 3. test: 添加单元测试（TDD 实践） (b901a72)

**提交内容**：
- 添加 `KeywordMatcher` 单元测试
- 添加 `DataDeduplicator` 单元测试
- 添加 `JSONStorage` 单元测试
- 测试覆盖率：12 个测试用例全部通过
- 遵循 TDD 开发实践

**文件**：
- `tests/unit/test_keyword_matcher.py`
- `tests/unit/test_deduplicator.py`
- `tests/unit/test_storage.py`

---

### 4. feat: 实现爬虫模块 (abb627b)

**提交内容**：
- 添加 `SearchCrawler` 基于 Playwright 的爬虫实现
- 添加 `BrowserCrawler` 基于浏览器内容的爬虫方案
- 支持采招网动态页面抓取
- 支持关键字搜索和地区筛选
- 包含反爬策略（User-Agent 轮换、请求延迟）

**文件**：
- `src/crawler/search_crawler.py`
- `src/crawler/browser_crawler.py`

---

### 5. feat: 实现 Streamlit Web 可视化界面 (7b62427)

**提交内容**：
- 添加数据展示表格（9 个字段）
- 实现多维度筛选（时间、城市、类型、关键字位置）
- 支持 CSV/JSON 数据导出
- 显示项目统计信息
- 显示原始关键字位置标注
- 支持详情页链接跳转

**文件**：
- `src/ui/app.py`

---

### 6. feat: 添加工具脚本 (56cc50f)

**提交内容**：
- `main.py`: 主执行脚本
- `test_crawler.py`: 爬虫测试脚本
- `crawl_from_browser.py`: 基于浏览器内容的爬虫工具
- `update_keyword_locations.py`: 更新关键字位置信息
- `update_to_original_format.py`: 更新为原始格式
- `regenerate_data_with_tags.py`: 重新生成带位置标注的数据
- `extract_links_from_page.py`: 提取项目详情页链接
- `convert_real_data.py`: 转换真实数据格式

**文件**：
- `main.py`
- `test_crawler.py`
- `crawl_from_browser.py`
- `update_keyword_locations.py`
- `update_to_original_format.py`
- `regenerate_data_with_tags.py`
- `extract_links_from_page.py`
- `convert_real_data.py`

---

### 7. feat: 添加 Docker 容器化部署配置 (139d55a)

**提交内容**：
- `Dockerfile`: 构建 Python 应用镜像
- `docker-compose.yml`: 一键部署配置
- 支持 Streamlit 服务
- 包含数据持久化卷配置

**文件**：
- `Dockerfile`
- `docker-compose.yml`

---

### 8. docs: 添加项目文档 (3f3e705)

**提交内容**：
- `README.md`: 项目说明和快速开始指南
- `CRAWLER_GUIDE.md`: 爬虫使用详细指南
- `DELIVERY.md`: 项目交付文档
- 包含功能说明、使用方法、部署指南

**文件**：
- `README.md`
- `CRAWLER_GUIDE.md`
- `DELIVERY.md`

---

### 9. data: 添加真实招投标数据 (d779305)

**提交内容**：
- 20 条四川省招投标项目数据
- 数据来源：采招网
- 包含完整的关键字位置标注
- 包含项目详情页链接
- 时间范围：近三月
- 更新 `.gitignore` 允许提交示例数据

**文件**：
- `data/bidding_data.json`
- `.gitignore`

---

## 版本标签

### v1.2.0

**发布日期**: 2026-02-02

**功能特性**：
- 采招网数据抓取（四川省）
- 关键字匹配（广告、标识、牌、标志、宣传、栏、文化）
- 原始位置标注保留
- Streamlit Web 界面
- 多维度筛选和数据导出
- Docker 容器化部署
- 完整的单元测试（12个测试用例）

**技术栈**：
- Python 3.11
- Playwright / BeautifulSoup4
- Streamlit
- Docker

---

## 提交规范

本项目遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `test`: 测试相关
- `refactor`: 代码重构
- `style`: 代码格式调整
- `chore`: 构建/工具链相关
- `data`: 数据相关

---

## 后续迭代计划

### v1.3.0（计划中）
- 实现邮件通知功能
- 添加定时任务调度
- 优化 Playwright 爬虫绕过验证码

### v2.0.0（计划中）
- PostgreSQL 持久化
- NLP 语义匹配
- 企业微信/钉钉机器人集成
- 详情页深度抓取

---

## 克隆仓库

```bash
git clone https://github.com/DivenYoung/bidding-crawler.git
cd bidding-crawler
```

## 查看提交历史

```bash
# 查看简洁的提交历史
git log --oneline

# 查看详细的提交历史
git log --stat

# 查看图形化提交历史
git log --graph --oneline --decorate --all
```

## 切换到特定版本

```bash
# 切换到 v1.2.0
git checkout v1.2.0

# 返回最新版本
git checkout main
```
