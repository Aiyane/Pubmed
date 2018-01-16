# coding: utf-8
from multiprocessing import Pool
import time
import re
import os

need_words = []
res = []

# 将性状全部存在need_words列表中, 并且去掉首尾空格, 全部转换成小写
with open('C:\\Users\\Administrator\\Desktop\\need.txt', 'r', encoding="utf8") as fin:
    for line in fin.readlines():
        Word = line.lower().strip()
        need_words.append(Word)


# 通过协程将所有性状同时进行搜索, IO操作才是拖慢时间的罪魁祸首!!
def getLine(file, pattern):
    with open("C:\\Users\\Administrator\\Desktop\\test\\" + file, 'r', encoding="utf8") as fin:
        # 使用repr函数包裹字符串会让速度变快, 不知道为啥?
        for Line in fin.readlines():
            if pattern.match(Line.lower()):
                res.append(repr(file) + "$" + repr(Line.strip()) + "\n")


def getRes(word):
    # path 父目录, dirs 所有文件夹, files所有文件名
    pattern = re.compile(r'.*{word}.*$'.format(word=word.strip()))
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\test"):
        for file in files:
            getLine(file, pattern)
    if res:
        try:
            with open("C:\\Users\\Administrator\\Desktop\\res\\" + word.replace(' ', '_') + ".txt", "w", encoding="utf8") as f:
                f.write(''.join(res))
        except Exception:
            print(word.replace(' ', '_') + ".txt读入: " + ''.join(res) + " 出错")
        res.clear()

if __name__ == '__main__':
    start = time.clock()
    pool = Pool()
    pool.map(getRes, need_words)
    pool.close()
    pool.join()
    end = time.clock()
    print("time: " + str(end - start))
