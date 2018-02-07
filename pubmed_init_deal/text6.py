# coding: utf-8
import os
path = "C:/Users/Administrator/Desktop/txt全文2"
path2 = "C:/Users/Administrator/Desktop/nxml全文"

TXT = set()
NXML = set()

for txt in os.listdir(path):
    TXT.add(txt[:-4])

for nxml in os.listdir(path2):
    NXML.add(nxml[:-5])

for n in NXML:
    if n not in TXT:
        print(n)