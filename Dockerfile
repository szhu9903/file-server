FROM python:3.10.14-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到容器内
COPY app /app/app
COPY gunicorn.config.py .

# 暴露端口
EXPOSE 8051

# 启动 Gunicorn
CMD ["gunicorn", "-c", "gunicorn.config.py", "app.main:app"]
