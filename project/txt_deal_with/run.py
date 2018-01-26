#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# run.py

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
