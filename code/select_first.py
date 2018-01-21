# coding: utf-8


def getRes():
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\geneAndLocus.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            line = line.split("$")
            if line[0]:
                yield line[0] + "\n"


res = tuple(line for line in getRes())
with open("C:\\Users\\Administrator\\Desktop\\other_test\\select_gene.txt", "w", encoding="utf8") as f:
    f.write(''.join(res))
