# coding: utf-8
# 排序结果, 短的在前面, 按字母表排在前面

Res = dict()
with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列7.txt", "r", encoding="utf8") as fin:
    for line in fin.readlines():
        length = len(line) - 1
        try:
            Res[length] += line
        except KeyError:
            Res[length] = line

with open("C:\\Users\\Administrator\\Desktop\\基因处理\\结果.txt", "w", encoding="utf8") as f:
    res = []
    for i in range(25):
        try:
            words = Res[i].split()
        except KeyError:
            continue
        for word in sorted(words):
            res.append(word)

    f.write('\n'.join(res))
# 3 6 7 5 4 9 12 10 8 15 2 11 13 14 16 1 17 24 19
