#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：file_server_v2 
@File    ：file_service.py
@Author  ：szhu9903
@Date    ：2025/2/28 15:33 
'''

import datetime
import httpx
import aiofiles
from fastapi import HTTPException
from app.config import Settings
import xml.etree.ElementTree as ET

async def upload_file_to_nextcloud(file, settings: Settings):
    # 文件名
    now_date = datetime.datetime.now()
    file_name = now_date.strftime("%Y%m%d%H%M%S%f") + file.filename

    # 临时存储文件
    temp_path = f"/tmp/{file_name}"

    # 使用 aiofiles 异步写文件
    async with aiofiles.open(temp_path, "wb") as f:
        content = await file.read()  # 异步读取上传的文件
        await f.write(content)

    # 使用 httpx 异步上传文件
    async with httpx.AsyncClient() as client:
        webdav_url = f"{settings.nextcloud_url}/remote.php/webdav{settings.upload_folder}{file_name}"

        # 使用 aiofiles 读取文件并异步上传
        async with aiofiles.open(temp_path, "rb") as f:
            response = await client.put(
                webdav_url,
                data=f,
                auth=(settings.nextcloud_username, settings.nextcloud_password),
            )

        if response.status_code != 201:
            raise HTTPException(status_code=500, detail="将文件上传到 Nextcloud 时出错")

        # 获取共享链接
        share_url = f"{settings.nextcloud_url}/ocs/v2.php/apps/files_sharing/api/v1/shares"
        share_response = await client.post(
            share_url,
            headers={"OCS-APIRequest": "true"},
            data={
                "path": f"{settings.upload_folder}{file_name}",
                "shareType": 3,  # 公共链接
                # "permissions": 1 #
            },
            auth=(settings.nextcloud_username, settings.nextcloud_password),
        )

        if share_response.status_code != 200:
            raise HTTPException(status_code=500, detail="创建共享链接时出错")

        # 获取 URL 路径
        root = ET.fromstring(share_response.content)
        url = root.find('.//url').text
        return f'{url}/preview'
