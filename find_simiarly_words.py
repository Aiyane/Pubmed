#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# find_simiarly_words.py
from gensim.models import word2vec
import logging
import os

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

path = '/home/aiyane/dir/result_word_embedding'


trait_path = '/home/aiyane/dir/table/trait_result.txt'
with open(trait_path, 'r') as fin:
    trait_list = fin.read().split('\n')

for i in range(300, 1000, 200):
    model = word2vec.Word2Vec.load(
        "/home/aiyane/dir/model/" + str(i) + "_size.model")
    with open(path + "/" + str(i) + "_size_result.txt", "w") as f:
        for trait in trait_list:
            try:
                words = model.most_similar(trait, topn=10)
                print('和术语' + trait + "最相关的词找到: ")
                f.write(trait + '\n')
                for word in words:
                    f.write(word[0] + '\t' + str(word[1]) + '\n')
                    print(word[0], word[1])
                print("------------------")
            except (KeyError, UnicodeEncodeError):
                continue
            f.write("\n")
