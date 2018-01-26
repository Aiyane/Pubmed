#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# run.py

__author__ = 'Aiyane'

"""
output_path: 输出路径
input_path: 输入路径
all_xing_file: 所有性状文件
all_gene_file: 所有基因文件
need_del_pmid: 需要删除的pmid号
"""
import os
from txt_paser import getRes

output_path = ""
input_path = ""
need_del_pmid = {}
all_xing_file = ""
all_gene_file = ""

for (path, _dirs, files) in os.walk(input_path):
    for file in files:
        getRes(path, file)
