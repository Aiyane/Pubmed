#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# sort_gene1.py
"""
模块功能: 根据基因对文章排序
"""
__author__ = 'Aiyane'

import os
import re
from multiprocessing import Pool


def if_equil(word1, word2):
    # 断言
    assert (isinstance(word1, str))
    assert (isinstance(word2, str))
    word1 = word1.lower()
    word2 = word2.lower()
    if len(word1) > 3 and len(word2) <= 3:
        return False
    if len(word2) > 3 and len(word1) <= 3:
        return False
    if len(word1) <= 3 and len(word2) <= 3:
        if word1 == word2:
            return word1
        else:
            return False

    for _i in range(len(word1)):
        for _j in range(len(word2)):
            if word1[_i:_i + 3] == word2[_j:_j + 3]:
                return word1[_i:_i+3]
            if _j + 3 < len(word2):
                _j += 1
            else:
                break
        if _i + 3 < len(word1):
            _i += 1
        else:
            return False
            

if __name__ == '__main__':
    files = os.listdir("C:\\Users\\Administrator\\Desktop\\sorted")
    pool = Pool()
    with open("C:\\Users\\Administrator\\Desktop\\sorted\\" + file, "r", encoding="utf8") as fin:
        pool.map(main, files)
    pool.close()
    pool.join()