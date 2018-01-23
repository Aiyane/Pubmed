# coding: utf-8
# 计算全部不是xxx_yyy的其他基因出现的个数, 然后输出(去重)

Res = dict()
with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列5.txt", "r", encoding="utf8") as fin:
    for word in fin.readlines():
        try:
            Res[word] += 1
        except KeyError:
            Res[word] = 1

with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列6.txt", "w", encoding="utf8") as f:
    res = []
    for key in Res.keys():
        res.append(key)
    f.write(''.join(res))

with open("C:\\Users\\Administrator\\Desktop\\基因处理\\非特殊记录.txt", "w", encoding="utf8") as f:
    res = []
    for k, y in Res.items():
        res.append(k.strip() + " " + str(y) + "\n")
    f.write(''.join(res))
