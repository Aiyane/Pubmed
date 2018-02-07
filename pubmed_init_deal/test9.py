# coding: utf-8
import os
import re

path1 = "C:/Users/Administrator/Desktop/new_file"
path2 = "C:/Users/Administrator/Desktop/nxml_res"
gene_file = "C:/Users/Administrator/Desktop/gene.txt"

files1 = os.listdir(path1)
files2 = os.listdir(path2)

GEN = set()
with open(gene_file, "r", encoding="utf8") as fi:
    for ine in fi.readlines():
        if ine != "\n":
            GEN.add(ine.strip())

for file1 in files1:
    with open(path1+"/"+file1, "r", encoding="utf8") as fin:
        tem = ["内容: "]
        for line in fin.readlines():
            line = line.replace("$基因", "")
            line = line.replace("基因$", "")
            line = line.replace("关键字$", "")
            line = line.replace("$关键字", "")
            # for gen in GEN:
            #     line = line.replace(gen, "基因$"+gen+"$基因")
            tem.append(line)
        with open("C:/Users/Administrator/Desktop/res/"+file1, "w", encoding="utf8") as ff:
            ff.write(''.join(tem))

for file2 in files2:
    with open(path2+"/"+file2, "r", encoding="utf8") as fin:
        tem = ["内容: "]
        for line in fin.readlines():
            line = line.replace("$基因", "")
            line = line.replace("基因$", "")
            line = line.replace("关键字$", "")
            line = line.replace("$关键字", "")
            # for gen in GEN:
            #     line = line.replace(gen, "基因$" + gen + "$基因")
            tem.append(line)
        with open("C:/Users/Administrator/Desktop/res/"+file2, "w", encoding="utf8") as ff:
            ff.write(''.join(tem))
