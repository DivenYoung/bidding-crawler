# Streamlit Cloud 部署说明

## 部署步骤

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 使用 GitHub 账号登录
3. 点击 "New app"
4. 选择仓库：`DivenYoung/bidding-crawler`
5. 选择分支：`v1.3-dev`（或 `main`）
6. 主文件路径：`src/ui/app.py`
7. 点击 "Deploy!"

## 配置文件

- `requirements.txt`: Python 依赖包
- `.streamlit/config.toml`: Streamlit 配置
- `src/ui/app.py`: 主应用文件
- `data/bidding_data.json`: 数据文件

## 数据更新

数据文件存储在 `data/bidding_data.json`，需要定期更新：
1. 运行爬虫脚本更新数据
2. 提交并推送到 GitHub
3. Streamlit Cloud 会自动重新部署

## 注意事项

- 免费版有资源限制（1GB RAM）
- 数据文件不要超过 100MB
- 支持自动从 GitHub 同步更新
