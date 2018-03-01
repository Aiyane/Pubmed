#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# test3.py
from pubmed import MultiFilePubmud
import os
init_path = '/home/aiyane/桌面/html20/HTML'
init_files = [one[:-5] for one in os.listdir(init_path)]

path = '/home/aiyane/桌面/xing'
files = os.listdir(path)

root = MultiFilePubmud({})
for one_file in files:
    root1 = MultiFilePubmud(path + '/' + one_file)
    for article in root1.values():
        article.add('性状', one_file)
    root.update(root1)

all_txt = []
for txt in root.yield_element(init_files, ['PMID', '正文']):
    all_txt.append(':\n'.join(txt))
text = '\n\n'.join(all_txt)

with open('/home/aiyane/桌面/nxml_content.txt', 'w', encoding="utf8") as f:
    f.write(text)