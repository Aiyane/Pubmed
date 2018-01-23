# coding: utf-8
# 合并去重后的基因, 包括xxx_yyy格式与不是这种格式的

Res = []
with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列4.txt", "r", encoding="utf8") as fin:
    for line in fin.readlines():
        Res.append(line)

with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列6.txt", "r", encoding="utf8") as fin:
    for line in fin.readlines():
        Res.append(line)

with open("C:\\Users\\Administrator\\Desktop\\基因处理\\第二列7.txt", "w", encoding="utf8") as f:
    f.write(''.join(Res))
