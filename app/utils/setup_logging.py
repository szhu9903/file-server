#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：file_server_v2 
@File    ：setup_logging.py
@Author  ：szhu9903
@Date    ：2025/2/28 15:13 
'''

import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("置日志记录")
