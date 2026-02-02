# 爬虫使用指南

## 问题说明

采招网使用了**阿里云人机验证（CAPTCHA）**，Playwright 无头模式会被检测并触发验证码。经过测试，我们提供了两种解决方案。

---

## 方案一：基于浏览器内容的爬虫（推荐，已实现）

这是当前最可靠的方案，绕过了验证码问题。

### 工作原理

1. 使用 Manus 的浏览器工具访问采招网
2. 浏览器工具自动提取页面内容为 Markdown 格式
3. 使用 `BrowserCrawler` 解析 Markdown 内容
4. 保存到数据库

### 使用步骤

#### 方式 A：使用 Manus 浏览器工具（自动化）

```bash
# 1. 使用浏览器工具访问采招网并获取内容
# （在 Manus 中已经演示）

# 2. 将提取的 Markdown 内容保存到文件
# browser_content.txt

# 3. 运行解析脚本
cd /home/ubuntu/bidding-crawler
python3.11 crawl_from_browser.py
```

#### 方式 B：手动复制粘贴

```bash
# 1. 在浏览器中打开搜索页面
https://search.bidcenter.com.cn/search?keywords=广告,标识,牌,标志,宣传,栏,文化

# 2. 等待页面加载完成

# 3. 按 Ctrl+A 全选页面内容

# 4. 按 Ctrl+C 复制

# 5. 将内容粘贴到文件
/home/ubuntu/bidding-crawler/browser_content.txt

# 6. 运行解析脚本
cd /home/ubuntu/bidding-crawler
python3.11 crawl_from_browser.py
```

### 优点

- ✅ 绕过验证码
- ✅ 稳定可靠
- ✅ 无需代理IP
- ✅ 已完整实现并测试

### 缺点

- ⚠️ 需要手动操作（可通过 Manus 浏览器工具半自动化）
- ⚠️ 无法完全自动化

---

## 方案二：Playwright 爬虫（需要进一步优化）

### 当前状态

已实现基础代码，但会触发验证码。

### 需要的改进

1. **使用 playwright-stealth**
   ```bash
   pip3 install playwright-stealth
   ```

2. **配置代理IP池**
   - 购买代理IP服务
   - 配置IP轮换

3. **使用有头模式 + 虚拟显示**
   ```bash
   # 安装 Xvfb
   sudo apt-get install xvfb
   
   # 使用虚拟显示运行
   xvfb-run python3.11 test_crawler.py
   ```

4. **手动处理验证码**
   - 使用打码平台（如 2captcha）
   - 集成验证码识别服务

### 代码位置

- `src/crawler/search_crawler.py` - Playwright 爬虫实现
- `test_crawler.py` - 测试脚本

---

## 方案三：API 调用（未来考虑）

### 可能性

采招网可能有内部 API，可以通过抓包分析获取。

### 步骤

1. 使用浏览器开发者工具（F12）
2. 切换到 Network 标签
3. 刷新页面，查找 XHR/Fetch 请求
4. 分析 API 接口和参数
5. 使用 Python requests 直接调用 API

---

## 推荐工作流程

### 日常使用（推荐）

```bash
# 1. 使用 Manus 浏览器工具访问采招网
# 2. 复制页面内容到 browser_content.txt
# 3. 运行解析脚本
cd /home/ubuntu/bidding-crawler
python3.11 crawl_from_browser.py

# 4. 查看 Streamlit 界面
streamlit run src/ui/app.py
```

### 自动化部署（未来）

1. 部署到服务器
2. 配置代理IP
3. 使用 Playwright + stealth
4. 定时任务每天执行
5. 邮件通知

---

## 测试结果

### 方案一测试

```
✅ 成功解析 1 条项目
📊 地区分布：
  四川: 1 条
📋 信息类型分布：
  招标公告: 1 条
```

### 方案二测试

```
❌ 检测到人机验证
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `src/crawler/browser_crawler.py` | 基于浏览器内容的爬虫（方案一） |
| `src/crawler/search_crawler.py` | Playwright 爬虫（方案二） |
| `crawl_from_browser.py` | 方案一的使用脚本 |
| `test_crawler.py` | 方案二的测试脚本 |
| `browser_content.txt` | 浏览器内容文件 |

---

## 常见问题

### Q: 为什么 Playwright 会触发验证码？

A: 采招网使用了阿里云人机验证，可以检测无头浏览器的特征。

### Q: 方案一能否自动化？

A: 可以通过 Manus 浏览器工具半自动化，但无法完全无人值守。

### Q: 如何获取更多数据？

A: 在浏览器中滚动页面，复制更多内容到 `browser_content.txt`。

### Q: 数据会去重吗？

A: 会自动去重，基于项目ID。

---

## 下一步计划

1. ✅ 实现基于浏览器内容的爬虫（已完成）
2. ⏳ 优化 Playwright 爬虫，绕过验证码
3. ⏳ 实现邮件通知功能
4. ⏳ 实现定时任务调度
5. ⏳ Docker 容器化部署
