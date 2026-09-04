#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：file_server_v2 
@File    ：minio_service.py
@Author  ：szhu9903
@Date    ：2025/3/18 22:30 
'''

import re
import datetime
import aiofiles
from datetime import timedelta
from app.config import Settings
from fastapi import HTTPException
from minio import Minio
from minio.error import S3Error

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB


def validate_file(file):
    # 校验扩展名
    ext = file.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "不支持的文件类型")

    # 校验MIME类型
    if not re.match(r'image/.*', file.content_type):
        raise HTTPException(400, "非法文件格式")

    # 校验文件大小
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise HTTPException(413, "文件过大")

async def upload_file_to_minio(file, settings: Settings, client: Minio):
    """
    上传文件到 MinIO，并返回共享 URL
    """

    validate_file(file)

    # 生成唯一文件名
    now_date = datetime.datetime.now()
    file_name = now_date.strftime("%Y%m%d%H%M%S%f") + file.filename

    # 临时存储文件
    # temp_path = f"../tmp/{file_name}"

    try:
        # # 使用 aiofiles 异步写文件
        # async with aiofiles.open(temp_path, "wb") as f:
        #     content = await file.read()  # 异步读取上传的文件
        #     await f.write(content)
        # 使用流式上传避免内存溢出
        client.put_object(
            bucket_name = settings.minio_bucket_name,
            object_name = file_name,
            data = file.file,
            length = file.size,  # 自动计算大小
            content_type = file.content_type
        )
        # 生成可直接访问的预览 URL
        file_url = f"{settings.minio_url}/{settings.minio_bucket_name}/{file_name}"
        return file_url
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO 错误: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {e}")





