# coding: utf-8
import os

path = "C:/Users/Administrator/Desktop/new_error.txt"

Res = set()
with open(path, "r", encoding="utf8") as fin:
    for line in fin.readlines():
        if line.startswith("E"):
            l = line.split()[1].strip()
            Res.add(l)

print(len(Res))

TXT = set()
path = "C:/Users/Administrator/Desktop/txt全文2"
for txt in os.listdir(path):
    TXT.add(txt[:-4])

for res in Res:
    if res not in TXT:
        print(res)
