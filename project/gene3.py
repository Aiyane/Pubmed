# coding: utf-8
# 用来删除以glysoja和GLYMA开头的单词


def getRes():
    with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列2.txt", "r", encoding="utf8") as fin:
        glysoja = 0
        GLYMA = 0
        for word in fin.readlines():
            if word.startswith("glysoja"):
                glysoja += 1
            elif word.startswith("GLYMA"):
                GLYMA += 1
            else:
                yield word
    print(glysoja)  # 26448
    print(GLYMA)  # 75703

res = tuple(word for word in getRes())
with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列3.txt", "w", encoding="utf8") as f:
    f.write(''.join(res))
