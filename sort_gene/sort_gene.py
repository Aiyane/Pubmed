#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# sort_gene.py
"""
模块功能: 给输出的文章进行排序
"""
__author__ = 'Aiyane'
import os
import re


def if_equil(word1, word2):
    # 断言
    assert (isinstance(word1, str))
    assert (isinstance(word2, str))
    word1 = word1.lower()
    word2 = word2.lower()
    if len(word1) > 3 and len(word2) <= 3:
        return False
    if len(word2) > 3 and len(word1) <= 3:
        return False
    if len(word1) <= 3 and len(word2) <= 3:
        if word1 == word2:
            return True
        else:
            return False

    for _i in range(len(word1)):
        for _j in range(len(word2)):
            if word1[_i:_i + 3] == word2[_j:_j + 3]:
                return True
            if _j + 3 < len(word2):
                _j += 1
            else:
                break
        if _i + 3 < len(word1):
            _i += 1
        else:
            return False


# 测试
# word1 = "123-aiyane"
# word2 = "haha -23- njsx"
# print(if_equil(word1, word2))

# local_dict = dict()
# local_list = []
# gene_dict = dict()
# gene_list = []

# def getCom(pages):
#     for page in pages:
#         page = page.split("\n")
#         for line in page:
#             if line.startswith("内容") or line.startswith("标题"):
#                 genes = re.findall(r'基因$(.*)$基因', line)
#                 for gene in genes:
#                     gene = gene[3:-3]
#                     if gene <= 3:
#                         try:
#                             if local_dict[gene]:
#                                 continue
#                         except KeyError:
#                             local_dict[gene] = True
#                             try:
#                                 if gene_dict[gene]:
#                                     gene_dict[gene] += 1
#                             except KeyError:
#                                 gene_dict[gene] = 1
#                     else:
#                         is_equil = False
#                         is_equil_all = False
#                         out_equil_gene = ''
#                         for _gen in local_list:
#                             if if_equil(gene, _gen):
#                                 is_equil = True
#                                 break
#                         if not is_equil:
#                             for _g in gene_list:
#                                 if if_equil(_g, gene):
#                                     is_equil_all = True
#                                     out_equil_gene = _g
#                                     break
#                             if not is_equil_all:
#                                 gene_dict[gene] = 1
#                             else:
#                                 gene_dict[out_equil_gene] += 1
#                         local_list.append(gene)
#                 gene_list.extend(local_list)


class Block(object):
    def __init__(self, buffer):
        self.content = buffer
        self.gene_nums = 0
        self.gene_name = []
        self.init()

    def init(self):
        for line in self.content:
            if line.startswith("内容") or line.startswith("标题"):
                genes = re.findall(r'基因\$(.*)\$基因', line)
                if len(genes) == 1:
                    self.gene_name.append(genes[0])
                    self.gene_nums += 1
                for _i in range(len(genes) - 1):
                    gene = genes[_i]
                    error_gene = False
                    for _gene in genes[_i + 1:]:
                        if if_equil(_gene, gene):
                            error_gene = True
                            break
                    if not error_gene:
                        self.gene_name.append(gene)
                        self.gene_nums += 1

    def getGeneName(self):
        return self.gene_name


def getRes(path, file):
    with open(path + "\\" + file, "r", encoding="utf8") as fin:
        buffer = []
        for line in fin.readlines():
            if line == "\n" and len(buffer) > 1:
                yield buffer
                buffer = []
            else:
                buffer.append(line)


def getObject(path, file):
    my_blocks = []
    for buffer in getRes(path, file):
        a = Block(buffer)
        my_blocks.append(a)
    return my_blocks


block_list = []
for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\合并后的内容"):
    for file in files:
        gene_dict = dict()
        gene_count = dict()
        blocks = getObject(path, file)
        all_gene = []
        for block in blocks:
            for block_gene in block.getGeneName():
                gene_dict[block_gene] = block
                all_gene.append(block_gene)

        for gene in all_gene:
            count = 1
            genes = all_gene[:]
            if len(genes) > 1 and genes is not None:
                genes.remove(gene)
                for other_gene in genes:
                    if if_equil(gene, other_gene):
                        count += 1
                gene_count[gene] = count
            else:
                gene_count[gene] = count

        with open("C:\\Users\\Administrator\\Desktop\\sorted\\" + file, "w", encoding="utf8") as f:
            res_list = sorted(gene_count.items(), key=lambda g: g[1], reverse=True)
            for res in res_list:
                _block = gene_dict[res[0]]
                if _block not in block_list:
                    f.write(''.join(_block.content) + "\n")
                block_list.append(_block)
