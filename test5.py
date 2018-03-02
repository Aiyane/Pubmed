#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# test5.py
from pubmed import MultiFilePubmud
import os
import re
import pickle
path = '/home/aiyane/桌面/nxml_content166.txt'

with open(path, "r", encoding="utf8") as f:
    lines = f.readlines()

with open('/home/aiyane/桌面/pmid_gene.txt', 'rb') as f:
    key_words = pickle.load(f) 

all_txt = {}
start = False
pmid = ''
tem = []
for line in lines:
    if not line.strip():
        start = True
        if pmid:
            all_txt[pmid] = tem
            tem.clear()
    elif start:
        pmid = line.strip()[:-1]
        start = False
    else:
        tem.append(line.strip())

res = {}
for key in all_txt.keys():
    marks = key_words[key]
    txt = all_txt[key]
    for _txt in txt:
        txts = re.split(r'((?! )(?! \w))[\.\?] (?!\))', _txt)
        for line in txts:
            for mark in marks:
                if mark and mark in line:
                    res.setdefault(key, []).append(line)
                    break
    
with open('/home/aiyane/桌面/nxml_line.txt', "w", encoding="utf8") as f:
    for key, value in res.items():
        f.write(key + '\n')
        f.write('\n'.join(value) + '\n\n')