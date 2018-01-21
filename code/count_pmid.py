# coding: utf-8
import os
from multiprocessing import Pool
import shutil


def had_id():
    all_pmid = get_pmid()
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\need_file"):
        for dir in dirs:
            all_pmid.remove(dir)
    for pmid in all_pmid:
        shutil.copyfile("C:\\Users\\Administrator\\Desktop\\PMID\\" + pmid,
                        "C:\\Users\\Administrator\\Desktop\\need_pmid\\" + pmid)


def get_pmid():
    Res = []
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\PMID"):
        for file in files:
            Res.append(file)
    return Res


had_id()
