# coding: utf-8
# 用来过滤排列好的基因中xxx_yyy的基因然后输出
import re


def getRes():
    reg = re.compile(r'.*_.*')
    with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列1.txt", "r", encoding="utf8") as fin:
        for word in fin.readlines():
            if reg.match(word):
                yield word

res = tuple(word for word in getRes())
with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列2.txt", "w", encoding="utf8") as f:
    f.write(''.join(res))
