#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# gene_word.py
# 用来匹配基因, 关键字的模块
import re
import string

all_xing_file = "/home/aiyane/桌面/全部性状.txt"
all_gene_file = "/home/aiyane/桌面/geneprimary.set.txt"


def getXing():
    with open(all_xing_file, "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line.strip()


def getGene():  # 全部的基因名字
    with open(all_gene_file, 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            if len(line) > 2:
                yield line.strip()


pattern_list = [
    r'Glyma.*\d{2}[gG]\d+(\.\d*)?',
    r'LOC\d+',
    r'Os\d{2}g\d{7}',
    r'SAMN\d{8}',
    r'BAN.{3}g\d{5}D',
    r'MYB\d+',
    r'GSBRNA2T\d{11}',
    r'WBb.{5}\.\d{2}',
    r'P0.{6}\.\d{2}',
    r'EF1Bgamma\d',
    r'LOC\d{5}',
    r'HSP\d{2}(\.)+\d-.',
    r'GlmaxMp\d{2}',
    r'Avh1b-.{3}',
    r'At1g\d{5}',
    r'G[Mm].+',
]


# need_gene 全部基因的字典
need_gene = {(k, k) for k in getGene()}
# need_xing 全部性状的字典
need_xing = {(k.lower(), k) for k in getXing()}
# re_list 全部的正则
re_list = [re.compile(pattern) for pattern in pattern_list]


def deal_word(words, is_title=False):
    buffer = []

    if is_title:
        # 如果是标题, 进行第一个单词首字母模糊匹配
        Head = words[0][0].lower() + words[0][1:]
        if need_gene.get(Head):
            buffer.append("基因$" + words[0] + "$基因")
        elif need_gene.get(words[0]):
            buffer.append("基因$" + words[0] + "$基因")
        else:
            buffer.append(words[0])
        words = words[1:]

    for word in words:
        for pattern in re_list:
            if pattern.match(word.strip(string.punctuation)):
                word = "基因$" + word + "$基因"
                break
        else:
            if need_gene.get(word):
                word = "基因$" + word + "$基因"
            elif need_xing.get(word.strip(string.punctuation).lower()):
                word = "性状$" + word + "$性状"
        buffer.append(word)

    return ' '.join(buffer)
