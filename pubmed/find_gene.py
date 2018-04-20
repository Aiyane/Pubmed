#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# gene_word.py
# 用来匹配基因, 关键字的模块
from pubmed import OneFilePubmud, MultiFilePubmud
import re
import os
import string

all_xing_file = "/home/aiyane/dir/全部性状.txt"
# all_gene_file = "/home/aiyane/dir/geneprimary.set.txt"


def getXing():
    with open(all_xing_file, "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line.strip()


# def getGene():
#     with open(all_gene_file, 'r', encoding="utf8") as fin:
#         for line in fin.readlines():
#             if len(line) > 2:
#                 yield line.strip()


pattern_list = [
    r'Glyma.*\d{2}[gG]\d+(\.\d*)?',
    # r'LOC\d+',
    # r'Os\d{2}g\d{7}',
    # r'SAMN\d{8}',
    # r'BAN.{3}g\d{5}D',
    # r'MYB\d+',
    # r'GSBRNA2T\d{11}',
    # r'WBb.{5}\.\d{2}',
    # r'P0.{6}\.\d{2}',
    # r'EF1Bgamma\d',
    # r'LOC\d{5}',
    # r'HSP\d{2}(\.)+\d-.',
    r'GlmaxMp\d{2}',
    # r'Avh1b-.{3}',
    # r'At1g\d{5}',
    r'G[Mm].+',
]


# need_gene 全部基因的字典
# need_xing 全部性状的字典
# re_list 全部的正则
# need_gene = dict((k, k) for k in getGene())
need_xing = dict((k.lower(), k) for k in getXing())
re_list = [re.compile(pattern) for pattern in pattern_list]


def deal_word(words, is_title=False):

    all_gene = []
    all_trait = []
    if is_title:
        Head = words[0][0].lower() + words[0][1:]
        words = words[1:]

    for word in words:
        for pattern in re_list:
            if pattern.match(word.strip(string.punctuation)):
                all_gene.append(word.strip(string.punctuation))
                break
        else:
            if need_xing.get(word.strip(string.punctuation).lower()):
                all_trait.append(word.strip(string.punctuation).lower())

    return all_gene, all_trait


def get_gene_trait_root(file_path, trait=False):
    if os.path.isfile(file_path):
        root = OneFilePubmud(file_path)
    elif os.path.isdir(file_path):
        root = MultiFilePubmud(file_path, trait)
    else:
        raise NotADirectoryError("路径出错")

    all_gene = []
    all_trait = []
    for article in root.yield_all("摘要"):
        if isinstance(article, list):
            article = '\n'.join(article).split()
        else:
            article = article.split()
        genes, traits = deal_word(article)
        all_gene.extend(genes)
        all_trait.extend(traits)

    for article in root.yield_all("标题"):
        article = article.split()
        genes, traits = deal_word(article, True)
        all_gene.extend(genes)
        all_trait.extend(traits)

    return set(all_gene), set(all_trait), root
