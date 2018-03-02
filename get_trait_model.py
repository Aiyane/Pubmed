#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
from gensim.models import word2vec
import os
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

path = '/home/aiyane/桌面/摘要'
files = os.listdir(path)
tem = []
for one in files:
    with open(path + "/" + one, "r", encoding="utf8") as f:
        tem.append(f.read())
with open('/home/aiyane/桌面/all_summary.txt', "w", encoding="utf8") as f:
    f.write('\n'.join(tem))

sentences = word2vec.Text8Corpus('/home/aiyane/桌面/all_summary.txt')
for i in range(300,1000,200):
    model = word2vec.Word2Vec(sentences, size=i, sg=1, hs=1)  # sg=1:训练skip-gram模型; 默认window=5; hs=1 hierarchical softmax被使用
    # 保存模型，以便重用
    model.save("/home/aiyane/桌面/model/"+ str(i) + "_size.model")
