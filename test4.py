#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# test4.py
import os
# import re
# from pubmed import MultiFilePubmud
import pickle

# path = '/home/aiyane/桌面/html20/HTML'
# files = [one[:-5] for one in os.listdir(path)]
# txt_path = '/home/aiyane/桌面/摘要'
# root = MultiFilePubmud(txt_path)

# key_words = {}
# table_path = '/home/aiyane/桌面/table'
# tables = os.listdir(table_path)
# for table in tables:
#     if table.startswith('3'):
#         with open(table_path + "/" + table, "r", encoding="utf8") as f:
#             pmids = f.readlines()
#     elif table.startswith('4'):
#         with open(table_path + "/" + table, "r", encoding="utf8") as f:
#             geneNames = f.readlines()
#     elif table.startswith('5'):
#         with open(table_path + "/" + table, "r", encoding="utf8") as f:
#             geneID1s = f.readlines()
#     elif table.startswith('6'):
#         with open(table_path + "/" + table, "r", encoding="utf8") as f:
#             geneID2s = f.readlines()
#     elif table.startswith('10'):
#         with open(table_path + "/" + table, "r", encoding="utf8") as f:
#             traits = f.readlines()

# for pmid, geneName, geneID1, gengID2, trait in zip(pmids, geneNames, geneID1s, geneID2s, traits):
#     key_words.setdefault(pmid.strip(), []).extend([geneName.strip(), geneID1.strip(), gengID2.strip(), trait.strip()])

with open('/home/aiyane/桌面/pmid_gene.txt', 'rb') as f:
    key_words = pickle.load(f)

res = {}
for key, value in key_words.items():
    tem = set()
    for item in value:
        if item:
            tem.add(item)
    res[key] = tem

f = open('/home/aiyane/桌面/pmid_gene_not_blank.txt', 'wb')
resb = pickle.dumps(res)
f.write(resb)
f.close()

# f = open('/home/aiyane/桌面/pmid_gene.txt', "wb")
# resb = pickle.dumps(key_words)
# f.write(resb)
# f.close()

# all_txt = {}
# for txt in root.yield_element(files, ['PMID', '摘要']):
#     all_txt[txt[0]] = txt[1]

# res = {}
# for key in all_txt.keys():
#     marks = key_words[key]
#     txt = all_txt[key]
#     # txts = re.split('.*?[\.\?](?=\s+(?:[A-Z]|$))', txt)
#     txts = re.split(r'((?! )(?! \w))[\.\?] (?!\))', txt)
#     for line in txts:
#         for mark in marks:
#             if mark and mark in line:
#                 res.setdefault(key, []).append(line)
#                 break

# with open('/home/aiyane/桌面/line.txt', "w", encoding="utf8") as f:
#     for key, value in res.items():
#         f.write(key + '\n')
#         f.write('\n'.join(value) + '\n\n')