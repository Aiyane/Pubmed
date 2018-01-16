# coding: utf-8
path = "C:\\Users\\Administrator\\Desktop\\abstract.txt"
path1 = "C:\\Users\\Administrator\\Desktop\\txt1\\"

with open(path, "r", encoding="utf-8") as f:
    tem = []
    for line in f.readlines():
        tem.append(line)
        if line.startswith("PMID"):
            l = line.split(' ')
            name = l[1]
            with open(path1 + name + ".txt", "w", encoding="utf-8") as f1:
                f1.write(''.join(tem))
                tem.clear()
