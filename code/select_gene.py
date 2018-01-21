# coding: utf-8


def getGene():
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\allGene.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line


def geneAndLocus():
    for line in getGene():
        line = line.split('$')
        line = [line[0], line[2], line[3], line[4], line[5]]
        if line[0] or line[1] or line[2] or line[3] or line[4]:
            yield ' $ '.join(line)+'\n'


res = tuple(res for res in geneAndLocus())
with open("C:\\Users\\Administrator\\Desktop\\other_test\\geneAndLocus.txt", "w", encoding="utf8") as f:
    f.write(''.join(res))
