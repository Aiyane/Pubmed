# coding: utf-8
from multiprocessing import Pool
import time
import re
import os


# 将全部性状构造成一个元组的正则表达式, 并且去掉首尾空格, 全部转换成小写
# 经实验, 元组是最快的, 另外利用生成器也是最快的
def make_tuple():
    with open('C:\\Users\\Administrator\\Desktop\\need.txt', 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            Word = line.lower().strip()
            yield (r'(.*({word}).*$)'.format(word=Word.strip()))
patterns_tuple = tuple(re.compile(pattern) for pattern in make_tuple())


def getRes(file):
    with open("C:\\Users\\Administrator\\Desktop\\test\\" + file, 'r', encoding="utf8") as fin:
        for Line in fin.readlines():
            for pattern in patterns_tuple:
                _a = pattern.match(Line.lower())
                # 这一行没匹配到的话进都不用进去了
                if _a:
                    try:
                        with open("C:\\Users\\Administrator\\Desktop\\res\\" + _a.group(2).replace(' ', '_') + ".txt", "a",
                                  encoding="utf8") as f:
                            # 用repr函数写入速度会变快, 不知道为啥?
                            f.write(repr(file) + " $ " + repr(Line.strip())+"\n")
                    except Exception:
                        print(_a.group(2).replace(' ', '_') + ".txt读入: " + Line + " 出错")


if __name__ == '__main__':
    start = time.clock()
    pool = Pool()

    # 对大数量的论文用进程池来并发处理
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\test"):
        pool.map(getRes, files)
    pool.close()
    pool.join()
    end = time.clock()
    print("time: " + str(end - start))
# time: 12.979454806698195
