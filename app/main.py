#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：file_server_v2 
@File    ：main.py
@Author  ：szhu9903
@Date    ：2025/2/28 15:05 
'''

from fastapi import FastAPI
from app.config import Settings
from app.utils.setup_logging import setup_logging
from app.routers import file_upload

def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.app_title,
        version=settings.app_version
    )
    # 初始化日志
    setup_logging()

    # 包含路由
    app.include_router(file_upload.router)

    return app

# 创建应用实例并传入配置
settings = Settings()
app = create_app(settings)
