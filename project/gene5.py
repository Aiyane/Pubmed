# coding: utf-8
# 用来筛选不是xxx_yyy这样格式的基因到另一个文件
import re


def getRes():
    reg = re.compile(r'.*_.*')
    with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列1.txt", "r", encoding="utf8") as fin:
        for word in fin.readlines():
            if not reg.match(word):
                yield word

res = tuple(word for word in getRes())
with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列5.txt", "w", encoding="utf8") as f:
    f.write(''.join(res))
