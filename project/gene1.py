# coding: utf-8
# 用来将所有基因按照空格切分, 输出


def getRes():
    with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            words = line.split()
            for word in words:  
                yield word.strip()+"\n"

res = tuple(line for line in getRes())
with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列1.txt", "w", encoding="utf8") as f:
    f.write(''.join(res))
