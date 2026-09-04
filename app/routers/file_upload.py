#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：file_server_v2 
@File    ：file_upload.py
@Author  ：szhu9903
@Date    ：2025/2/28 15:16 
'''

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.security import APIKeyHeader
from app.services.file_service import upload_file_to_nextcloud
from app.services.minio_client import get_minio_client
from app.services.minio_service import upload_file_to_minio
from app.config import Settings, get_settings
from minio import Minio

router = APIRouter()

# API密钥验证
api_key_header = APIKeyHeader(name="X-API-KEY")

@router.post("/upload/")
async def upload_file(
        file: UploadFile = File(...),
        settings: Settings = Depends(get_settings),
        api_key: str = Depends(api_key_header)
):
    return HTTPException(status_code=500, detail='暂停服务')
    # if api_key != settings.api_key:
    #     raise HTTPException(status_code=403, detail="API 密钥无效")
    #
    # try:
    #     # 调用服务层上传文件并获取共享链接
    #     link_url = await upload_file_to_nextcloud(file, settings)
    #     return {"link_url": link_url}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload/minio/")
async def upload_file(
        file: UploadFile = File(...),
        settings: Settings = Depends(get_settings),
        api_key: str = Depends(api_key_header),
        minio_client: Minio = Depends(get_minio_client)
):
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="API 密钥无效")

    try:
        # 调用服务层上传文件并获取共享链接
        link_url = await upload_file_to_minio(file, settings, minio_client)
        return {"link_url": link_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))