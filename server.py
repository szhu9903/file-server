#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：file_server_v2 
@File    ：server.py
@Author  ：szhu9903
@Date    ：2025/2/28 20:39 
'''
import uvicorn
from app.main import create_app
from app.config import Settings

settings = Settings()

app = create_app(settings)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)