FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Playwright 浏览器（后续版本使用）
# RUN playwright install chromium
# RUN playwright install-deps

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8501

# 默认命令
CMD ["streamlit", "run", "src/ui/app.py", "--server.port=8501", "--server.headless=true"]
