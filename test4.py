#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# test4.py
import os
from pubmed import MultiFilePubmud

path = '/home/aiyane/桌面/html20/HTML'
files = [one[:-5] for one in os.listdir(path)]
txt_path = '/home/aiyane/桌面/摘要'
root = MultiFilePubmud(txt_path)

all_txt = []
for txt in root.yield_element(files, ['PMID', '摘要']):
    all_txt.append(':\n'.join(txt))
text = '\n\n'.join(all_txt)
with open('/home/aiyane/桌面/summary.txt', 'w', encoding="utf8") as f:
    f.write(text)
