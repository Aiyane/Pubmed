#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# deal_line.py
import nltk
from nltk import word_tokenize
import pickle

# path = '/home/aiyane/桌面/line.txt'
# with open(path, "r", encoding="utf8") as f:
#     lines = f.readlines()

# tem = []
# all_txt = {}
# for line in lines:
#     if line[0].isdigit():
#         pmid = line.strip()
#     elif not line.strip():
#         all_txt[pmid] = tem
#         tem = []
#     else:
#         tem.append(line.strip())

# f = open('/home/aiyane/桌面/pmid_line.txt', "wb")
# resb = pickle.dumps(all_txt)
# f.write(resb)
# f.close()

with open('/home/aiyane/桌面/pmid_line.txt', 'rb') as f:
    all_txt = pickle.load(f)

with open('/home/aiyane/桌面/pmid_gene_not_blank.txt', 'rb') as f:
    pmid_gene = pickle.load(f)

grammar = r"""
  NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
  PP: {<IN><NP>}               # Chunk prepositions followed by NP
  VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
  CLAUSE: {<NP><VP>}           # Chunk NP, VP
  """
cp = nltk.RegexpParser(grammar)

res = {}
for key, value in all_txt.items():
    temp = []
    for line in value:
        text = word_tokenize(line)
        tagged_txt = nltk.pos_tag(text)
        tem_tagged_txt = []
        for word, tag in tagged_txt:
            if word in pmid_gene[key]:
                tag = 'GENE'
            tem_tagged_txt.append((word, tag))
        tree = cp.parse(tem_tagged_txt)
        temp.append(tree)
    res[key] = temp

f = open('/home/aiyane/桌面/tree.txt', "wb")
resb = pickle.dumps(res)
f.write(resb)
f.close()
