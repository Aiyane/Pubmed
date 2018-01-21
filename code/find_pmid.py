# coding: utf-8
import os
import re
import shutil
from multiprocessing import Pool


def getAllID():
    with open('C:\\Users\\Administrator\\Desktop\\deal\\大豆PMID.txt', 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            yield line.strip()
all_id = tuple(pmid for pmid in getAllID())


# 遍历全部文件夹的全部文件
def wark_dir(dir):
    for (path, _dirs, files) in os.walk("D:\\code\\shuju\\" + dir):
        for file in files:
            getPMID(path, file)
pattern = r'pmid">((\d)+)<'


def getPMID(path, file):
    with open(path + "\\" + file, 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            gene_name = re.search(pattern, line)
            if gene_name:
                if gene_name.group(1) in all_id:
                    shutil.copyfile(path + "\\" + file, 'C:\\Users\\Administrator\\Desktop\\deal\\大豆\\' + file)
                    break

if __name__ == '__main__':
    # path 父目录, dirs 所有文件夹, files所有文件名
    pool = Pool()
    for (_path, dirs, _files) in os.walk("D:\\code\\shuju"):
        pool.map(wark_dir, dirs)
    pool.close()
    pool.join()
