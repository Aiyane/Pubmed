#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# run.py
"""
在data.py中将all_xing_file改成所有性状的文件路径, 里面的性状是一行一个
2. 在data.py中将all_gene_file改成所有基因的路径, 里面的基因是一行一个
3. 在data.py中将input_path改成你的nxml文件根目录, 注意看上面注释!!! 其子目录的格式要求
4. 在data.py中将output_path改成你的输出路径, 提示: 最好是空目录
5. 在data.py中将需要删除的pmid添加到need_del_pmid集合中去
6. 改完以后点击运行 run.py 即可
"""

__author__ = 'Aiyane'
import os
from txt_paser import getRes
from data import input_path
from multiprocessing import Pool
from functools import partial

# for (path, _dirs, files) in os.walk(input_path):
#     for file in files:
#         getRes(path, file)
if __name__ == '__main__':
    pool = Pool()
    for (path, _dirs, files) in os.walk(input_path):
        getRes = partial(getRes, path=path)
        pool.map(getRes, files)
    pool.close()
    pool.join()
