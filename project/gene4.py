# coding: utf-8
# 计算全部xxx_yyy中xxx出现的个数, 然后输出

Res = dict()
with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列3.txt", "r", encoding="utf8") as fin:
    for line in fin.readlines():
        word = line.split("_")[0]
        try:
            Res[word] += 1
        except KeyError:
            Res[word] = 1

with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列4.txt", "w", encoding="utf8") as f:
    res = []
    for key in Res.keys():
        res.append(key+"\n")
    f.write(''.join(res))

with open("C:\\Users\\Administrator\\Desktop\\基因处理\\记录.txt", "a", encoding="utf8") as f:
    res = []
    for k, y in Res.items():
        res.append(k+" "+str(y)+"\n")
    f.write(''.join(res))
