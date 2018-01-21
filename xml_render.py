# coding: utf-8
import re
import shutil
from multiprocessing import Pool
import os


# 构造全部大豆PMID的tuple, tuple会快一些
def getAllID():
    with open('C:\\Users\\Administrator\\Desktop\\大豆PMID.txt', 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            yield line.strip()
all_id = tuple(pmid for pmid in getAllID())
pattern = re.compile(r'.*pmid.*')


def getPMID(path, file):
    with open(path + "\\" + file, 'r', encoding="utf8") as fin:
        context = fin.read()
        context = re.split(r'(?s)(<.*?>)', context)
    stop = False
    for line in context:
        if stop:
            stop = False
            if line in all_id:
                stop = True
            break
        if pattern.match(line.lower()):
            stop = True
            continue
    if stop:
        shutil.copyfile(path + "\\" + file, 'C:\\Users\\Administrator\\Desktop\\大豆\\' + file)


# 遍历全部文件夹的全部文件
def wark_dir(dir):
    for (path, _dirs, files) in os.walk("D:\\code\\shuju\\" + dir):
        for file in files:
            getPMID(path, file)


if __name__ == '__main__':
    # path 父目录, dirs 所有文件夹, files所有文件名
    pool = Pool()
    for (_path, dirs, _files) in os.walk("D:\\code\\shuju"):
        pool.map(wark_dir, dirs)
    pool.close()
    pool.join()
