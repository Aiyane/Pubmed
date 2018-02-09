# coding: utf-8
import os

path = "C:/Users/Administrator/Desktop/fin_res2"
path4 = "C:/Users/Administrator/Desktop/表/4.txt"
path5 = "C:/Users/Administrator/Desktop/表/5.txt"
path6 = "C:/Users/Administrator/Desktop/表/6.txt"
path10 = "C:/Users/Administrator/Desktop/表/10.txt"
path3 = "C:/Users/Administrator/Desktop/表/3.txt"

gene = dict()
with open(path3, "r", encoding="utf8") as fin:
    lines3 = fin.readlines()
res3 = []
for line3 in lines3:
    res3.append(line3.strip())

with open(path4, "r", encoding="utf8") as fin:
    lines4 = fin.readlines()
res4 = []
for line4 in lines4:
    res4.append(line4.strip())

with open(path5, "r", encoding="utf8") as fin:
    lines5 = fin.readlines()
res5 = []
for line5 in lines5:
    res5.append(line5.strip())

with open(path6, "r", encoding="utf8") as fin:
    lines6 = fin.readlines()
res6 = []
for line6 in lines6:
    res6.append(line6.strip())

with open(path10, "r", encoding="utf8") as fin:
    lines10 = fin.readlines()
res10 = []
for line10 in lines10:
    res10.append(line10.strip())

for i, tem in enumerate(res3):
    gene.update({tem: [res4[i], res5[i], res6[i], res10[i]]})

files = os.listdir(path)
for file in files:
    Res = []
    with open("C:/Users/Administrator/Desktop/fin_res2/" + file, "r", encoding="utf8") as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith("摘要"):
            if gene[file[:-4]][0]:
                line = line.replace(gene[file[:-4]][0], "基因$"+gene[file[:-4]][0]+"$基因")
            if gene[file[:-4]][1]:
                line = line.replace(gene[file[:-4]][1], "基因$"+gene[file[:-4]][1]+"$基因")
                line = line.replace("基因$基因$", "基因$")
                line = line.replace("$基因$基因", "$基因")
            if gene[file[:-4]][2]:
                line = line.replace(gene[file[:-4]][2], "基因$" + gene[file[:-4]][2] + "$基因")
                line = line.replace("基因$基因$", "基因$")
                line = line.replace("$基因$基因", "$基因")
            if gene[file[:-4]][3]:
                line = line.replace(gene[file[:-4]][3], "性状$" + gene[file[:-4]][3] + "$性状")
        Res.append(line)
    with open("C:/Users/Administrator/Desktop/fin_res3/" + file, "w", encoding="utf8") as f:
        f.write(''.join(Res))
