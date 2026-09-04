#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：file_server_v2 
@File    ：minio_client.py
@Author  ：szhu9903
@Date    ：2025/3/19 16:20 
'''

from minio import Minio
from app.config import get_settings

settings = get_settings()  # 读取 MinIO 配置

# 创建 MinIO 客户端（全局单例）
minio_client = Minio(
    endpoint=settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=False  # 如果是 HTTPS，设置为 True
)

# 定义 FastAPI 依赖项
def get_minio_client() -> Minio:
    return minio_client

