# coding: utf-8


def getRes():
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\select_gene.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            line = list(line.split())
            yield line[0] + "\n"


res = tuple(word for word in getRes())
with open("C:\\Users\\Administrator\\Desktop\\other_test\\fiest_name.txt", "w", encoding="utf8") as f:
    f.write(''.join(res))
