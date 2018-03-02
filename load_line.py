#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# load_line.py
import pickle
with open('/home/aiyane/桌面/tree.txt', 'rb') as f:
    res = pickle.load(f)
with open('/home/aiyane/桌面/pmid_gene.txt', 'rb') as fin:
    relation = pickle.load(fin)

# genes = {}
# for key, value in relation.items():
#     tem = []
#     for item in value:
#         if item:
#             tem.append(item)
#     genes[key] = tem

# f = open('/home/aiyane/桌面/pmid_gene_not_blank.txt', "wb")
# resb = pickle.dumps(genes)
# f.write(resb)
# f.close()

with open('/home/aiyane/桌面/pmid_gene_not_blank.txt', 'rb') as fin:
    pmid_gene = pickle.load(fin)

print(pmid_gene)