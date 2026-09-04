#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：file_server_v2 
@File    ：config.py
@Author  ：szhu9903
@Date    ：2025/2/28 15:07 
'''

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_title: str = "FastAPI Application"
    app_version: str = "1.0.0"
    api_key: str = ''

    nextcloud_url: str = ''
    nextcloud_username: str = ''
    nextcloud_password: str = ''
    upload_folder: str = ''

    minio_url: str = ''
    minio_endpoint: str = ''
    minio_access_key: str = ''
    minio_secret_key: str = ''
    minio_bucket_name: str = ''

    # database_url: str = "sqlite:///./test.db"
    # secret_key: str = "your_secret_key"

    class Config:
        env_file = ".env"  # 配置从 .env 文件读取环境变量

# 返回 Pydantic 的配置实例
def get_settings() -> Settings:
    return Settings()
