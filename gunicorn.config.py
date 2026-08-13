
# 绑定地址和端口
bind = "0.0.0.0:8051"

# 工作进程数
workers = 2

# 工作进程类型
worker_class = "uvicorn.workers.UvicornWorker"

accesslog = "-"  # 访问日志文件路径
errorlog = "-"  # 错误日志文件路径

# 日志级别
loglevel = "info"
