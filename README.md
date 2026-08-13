# file_server_v2

基于 FastAPI 的文件上传网关服务，支持 Nextcloud WebDAV 和 MinIO 两种存储后端。

## 技术栈

- **Python 3.10** / **FastAPI** — 异步 Web 框架
- **Uvicorn + Gunicorn** — ASGI 服务（开发/生产）
- **MinIO** — S3 兼容对象存储
- **Nextcloud WebDAV** — 文件存储与共享链接
- **httpx + aiofiles** — 异步 HTTP 客户端与文件 I/O
- **Docker + Kubernetes** — 容器化部署

## 项目结构

```
├── server.py                  # 开发启动入口
├── gunicorn.config.py         # Gunicorn 生产配置
├── requirements.txt           # Python 依赖
├── Dockerfile                 # 容器构建文件
├── k8s/                       # Kubernetes 部署清单
└── app/
    ├── main.py                # FastAPI 应用工厂
    ├── config.py              # 配置管理（.env 自动加载）
    ├── routers/
    │   └── file_upload.py     # 上传 API 路由 + 鉴权
    ├── services/
    │   ├── file_service.py    # Nextcloud WebDAV 上传
    │   ├── minio_client.py    # MinIO 客户端单例
    │   └── minio_service.py   # MinIO 上传 + 文件校验
    └── utils/
        └── setup_logging.py   # 日志初始化
```

## 快速开始

### 1. 环境配置

复制 `.env` 文件并按实际环境修改配置项：

```env
API_KEY=your_api_key_here

# Nextcloud
NEXTCLOUD_URL=https://your-nextcloud.example.com
NEXTCLOUD_USERNAME=your_username
NEXTCLOUD_PASSWORD=your_password
UPLOAD_FOLDER=/uploads/

# MinIO
MINIO_URL=http://your-minio.example.com
MINIO_ENDPOINT=192.168.1.100:9000
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
MINIO_BUCKET_NAME=your_bucket
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 开发模式启动

```bash
python server.py
# 服务运行在 http://0.0.0.0:8000
```

### 4. Docker 部署

```bash
docker build -t file-server-v2 .
docker run -d -p 8051:8051 --env-file .env file-server-v2
```

## API 接口

所有上传接口需要在请求头中携带 `X-API-KEY` 进行鉴权。

### POST /upload/minio/

上传图片到 MinIO，返回文件访问 URL。

- **允许格式**：png、jpg、jpeg、gif
- **大小限制**：100MB
- **请求**：`multipart/form-data`，字段名 `file`

```bash
curl -X POST "http://localhost:8000/upload/minio/" \
  -H "X-API-KEY: your_api_key" \
  -F "file=@image.png"
```

### POST /upload/（已暂停）

上传文件到 Nextcloud WebDAV 并生成共享链接预览。当前接口已暂停服务（返回 500）。

## 安全

- **API Key 鉴权**：所有上传接口通过 `X-API-KEY` 请求头校验身份
- **文件校验**：MinIO 上传仅允许图片格式，校验 MIME 类型及文件大小
- **凭据隔离**：敏感配置通过 `.env` 文件注入，不硬编码
