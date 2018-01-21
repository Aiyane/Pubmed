# coding: utf-8

count = 0
with open("C:\\Users\\Administrator\\Desktop\\geneAndLocus.txt", "r", encoding="utf8") as f:
    for line in f.readlines():
        res = line.strip().split("$")
        if res[1]:
            count += 1
print(count)
