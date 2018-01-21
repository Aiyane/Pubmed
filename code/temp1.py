# coding: utf-8
import re
import os
from multiprocessing import Pool

pattern = re.compile(r'PMID: (\d+)')


def getRes(file):
    pmid = []
    with open("C:\\Users\\Administrator\\Desktop\\summary_oneline\\" + file, "r", encoding="utf8") as fin:
        for line in fin.readlines():
            if line != '\n':
                try:
                    pmid.append(pattern.search(line).group(1).strip()+'\n')
                except AttributeError:
                    print(line)
                    print(file)
    with open("C:\\Users\\Administrator\\Desktop\\PMID\\"+file, "w", encoding="utf8") as f:
        f.write(''.join(pmid))

if __name__ == '__main__':
    pool = Pool()
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\summary_oneline"):
        pool.map(getRes, files)
    pool.close()
    pool.join()