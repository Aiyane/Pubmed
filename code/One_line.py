# coding: utf-8
import os
from multiprocessing import Pool


def transfor(file):
    temp = ""
    res = []
    with open("C:\\Users\\Administrator\\Desktop\\summary\\" + file, "r", encoding="utf8") as fin:
        for line in fin.readlines():
            if line != "\n":
                temp = temp + line.strip() + " "
            else:
                res.append(temp+"\n\n")
                temp = ""
    write_file(file, res)


def write_file(file, res):
    with open("C:\\Users\\Administrator\\Desktop\\summary_oneline\\" + file, "w", encoding="utf8") as f:
        f.write(''.join(res))

if __name__ == '__main__':
    pool = Pool()
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\summary"):
        pool.map(transfor, files)
    pool.close()
    pool.join()

