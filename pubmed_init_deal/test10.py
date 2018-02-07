# coding: utf-8
import os
path = "C:/Users/Administrator/Desktop/表/pmid.txt"
pmid = []
with open(path, "r", encoding="utf-8") as fin:
    for line in fin.readlines():
        pmid.append(line.strip())

path_ii = "C:/Users/Administrator/Desktop/res"

path1 = "C:/Users/Administrator/Desktop/表/gene1.txt"
path2 = "C:/Users/Administrator/Desktop/表/gene2.txt"
path3 = "C:/Users/Administrator/Desktop/表/gene3.txt"
path4 = "C:/Users/Administrator/Desktop/表/gene4.txt"
GEN1 = []
GEN2 = []
GEN3 = []
GEN4 = []
with open(path1, "r", encoding="utf-8") as fin:
    for line in fin.readlines():
        GEN1.append(line.strip())
with open(path2, "r", encoding="utf-8") as fin:
    for line in fin.readlines():
        GEN2.append(line.strip())
with open(path3, "r", encoding="utf-8") as fin:
    for line in fin.readlines():
        GEN3.append(line.strip())
with open(path4, "r", encoding="utf-8") as fin:
    for line in fin.readlines():
        GEN4.append(line.strip())

MY = {}
for i, pm in enumerate(pmid):
    if GEN1[i]:
        MY.setdefault(pm, []).append(GEN1[i])
    if GEN2[i] and GEN2[i] != GEN1[i]:
        MY.setdefault(pm, []).append(GEN2[i])
    if GEN3[i] and GEN3[i] != GEN1[i] and GEN3[i] != GEN2[i]:
        MY.setdefault(pm, []).append(GEN3[i])
    if GEN4[i] and GEN4[i] != GEN1[i] and GEN4[i] != GEN2[i] and GEN4[i] != GEN3[i]:
        MY.setdefault(pm, []).append(GEN4[i])

all_file = os.listdir(path_ii)

for file in all_file:
    with open(path_ii+"/"+file, "r", encoding="utf8") as f:
        name = file.split(".")[0]
        if file.endswith(".nxml"):
            buffer = []
            for line in f.readlines():
                buffer.append(line.strip())
            line = ''.join(buffer)
            buffer = []
            for key in MY[name]:
                line = line.replace(key, "基因$" + key + "$基因")
                line = line.replace("基因$基因$", "基因$")
                line = line.replace("$基因$基因", "$基因")
            buffer.append(line)
        else:
            buffer = []
            for line in f.readlines():
                for key in MY[name]:
                    line = line.replace(key, "基因$"+key+"$基因")
                    line = line.replace("基因$基因$", "基因$")
                    line = line.replace("$基因$基因", "$基因")
                buffer.append(line)
        with open("C:/Users/Administrator/Desktop/fin_res/"+file, "w", encoding="utf8") as fin:
            fin.write(''.join(buffer))
