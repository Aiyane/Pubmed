# coding: utf-8
import os
import re
import shutil
from multiprocessing import Pool

pattern = re.compile(r'pmid">(\d+)')


def get_file(file):
    Res = False
    goal = ''
    pmid = ''
    with open("/home/wutbio006/hey/dataset/soybean/" + file, "r", encoding="utf") as fin:
        for line in fin.readlines():
            res = pattern.search(line)
            if res:
                pmid = res.group(1).strip()
                goal = if_need(pmid)
                if goal is not None:
                    Res = True
    if Res:
        isExists = os.path.exists("/home/wutbio006/hey/dataset/need_file/" + goal)
        if not isExists:
            os.mkdir("/home/wutbio006/hey/dataset/need_file/" + goal)
        shutil.copyfile("/home/wutbio006/hey/dataset/soybean/" + file,
                        "/home/wutbio006/hey/dataset/need_file/" + goal + "/" + pmid + ".nxml")


def if_need(pmid):
    for (path, dirs, files) in os.walk("/home/wutbio006/hey/dataset/need_pmid"):
        for file in files:
            with open("/home/wutbio006/hey/dataset/need_pmid" + file, "r", encoding="utf8") as fin:
                for line in fin.readlines():
                    if pmid == line.strip():
                        return file
    return None


def get_dir(dir):
    for (path, dirs, files) in os.walk("/home/wutbio006/hey/dataset/soybean/" + dir):
        for file in files:
            if file.endswith(".nxml"):
                get_file(dir+"/"+file)

if __name__ == '__main__':
    pool = Pool()
    for (path, dirs, files) in os.walk("/home/wutbio006/hey/dataset/soybean"):
        pool.map(get_dir, dirs)
    pool.close()
    pool.join()
