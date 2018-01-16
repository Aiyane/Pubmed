# coding: utf-8
from multiprocessing import Pool
import time
import re
import os


def make_word():
    # 将性状全部存在need_words列表中, 并且去掉首尾空格, 全部转换成小写
    with open('C:\\Users\\Administrator\\Desktop\\need.txt', 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            word = line.lower().strip()
            yield word


# 通过协程将所有性状同时进行搜索, IO操作才是拖慢时间的罪魁祸首!!
def getLine(file, pattern):
    with open("C:\\Users\\Administrator\\Desktop\\test\\" + file, 'r', encoding="utf8") as fin:
        # 使用repr函数包裹字符串会让速度变快, 不知道为啥?
        for Line in fin.readlines():
            if pattern.match(Line.lower()):
                yield (repr(file) + "$" + repr(Line.strip()) + "\n")


def getRes(word):
    # path 父目录, dirs 所有文件夹, files所有文件名
    # 元组的速度会快一些, 占用内存小
    res = tuple()
    pattern = re.compile(r'.*{word}.*$'.format(word=word.strip()))
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\test"):
        for file in files:
            res = tuple(line for line in getLine(file, pattern))
    if res:
        try:
            with open("C:\\Users\\Administrator\\Desktop\\res\\" + word.replace(' ', '_') + ".txt", "w", encoding="utf8") as f:
                f.write(''.join(res))
        except IOError:
            print(word.replace(' ', '_') + ".txt读入: " + ''.join(res) + " 出错")
        del res

if __name__ == '__main__':
    start = time.clock()
    need_words = tuple(word for word in make_word())
    pool = Pool()
    pool.map(getRes, need_words)
    pool.close()
    pool.join()
    end = time.clock()
    print("time: " + str(end - start))
