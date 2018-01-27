#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# copy_file_to_bottom.py
"""
模块功能: 合并全文nxml处理后的文件和摘要txt处理后的文件
"""
__author__ = 'Aiyane'


import os

for (path, dirs, files) in os.walk("D:\\我的文档\\res"):
    for file in files:
        Res = []
        with open(path+"\\"+file, "r", encoding="utf8") as fin:
            for line in fin.readlines():
                Res.append(line)
        with open("C:\\Users\\Administrator\\Desktop\\基因_摘要\\"+file, "a", encoding="utf8") as f:
            f.write(''.join(Res))
