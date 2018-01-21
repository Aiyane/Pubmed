#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Aiyane"
import os
import re
from multiprocessing import Pool


def initWord():
    with open(
            "C:\\Users\\Administrator\\Desktop\\other_test\\fiest_name.txt",
            "r",
            encoding="utf8") as fin:
        for line in fin.readlines():
            yield line.strip()


neeed_words = tuple(line for line in initWord())


def getGenge(file):
    res = []
    with open("D:\\code\\shuju\\备用\\" + file, "r", encoding="utf8") as fin:
        for line in fin.readlines():
            line = line.split()
            line = ''.join(tuple(word for word in getWord(line))) + "\n"
            res.append(line)
    with open("D:\\code\\shuju\\基因\\" + file, "a", encoding="utf8") as f:
        f.write(''.join(res))
        res.clear()


def getWord(line):
    for word in line:
        if word.lower() in neeed_words:
            word = "基因>" + word.strip() + "<基因"
        yield word+" "


if __name__ == "__main__":
    pool = Pool()
    for (path, dirs, files) in os.walk("D:\\code\\shuju\\备用"):
        pool.map(getGenge, files)
    pool.close()
    pool.join()
