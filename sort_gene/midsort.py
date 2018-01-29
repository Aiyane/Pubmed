#!/usr/bin/env python
# coding=utf-8
# author: Haohao Zhang<hyacinth.hao@foxmail.com>
# 2018-01-28 20:34
#
import os
from multiprocessing import Pool

def read_mid(path):
    """
    读取中间结果
    :param path:
    :return:
    """
    result = []
    tmp = ''
    with open(path, encoding="utf8") as f:
        for line in f:
            if line != '\n':
                tmp += line
            else:
                result.append(tmp)
                tmp = ''
    return result


def write_mid(path, mid, index):
    with open(path, 'w', encoding="utf8") as f:
        for i in index:
            f.write(mid[i] + '\n')


def parse_gene(line):
    """
    从中间结果提取去重基因列表
    :param line:
    :return:
    """
    # for i in range(len(line)):
    result = []
    _max_len = len(line)
    i = 0
    while True:
        if line[i:i+3] == '基因$':
            tmp = ''
            j = i + 3
            while True:
                if line[j] != '$':
                    tmp += line[j]
                    j += 1
                else:
                    i = j + 3
                    result.append(tmp)
                    break
        else:
            i += 1
        if i >= _max_len:
            break
    return set_gene(result)


def set_gene(genes):
    """
    基因去重
    :param genes:
    :return:
    """
    result = []
    for g in genes:
        found = False
        for k in result:
            if is_match(g, k):
                found = True
        if not found:
            result.append(g)
    return result


def lcs_dp(input_x, input_y):
    """
    最小子串查找
    :param input_x:
    :param input_y:
    :return:
    """
    dp = [([0] * len(input_y)) for i in range(len(input_x))]
    max_len = max_index = 0
    for i in range(0, len(input_x)):
        for j in range(0, len(input_y)):
            if input_x[i] == input_y[j]:
                if i != 0 and j != 0:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                elif i == 0 or j == 0:
                    dp[i][j] = 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    max_index = i + 1 - max_len
    return input_x[max_index:max_index + max_len]


def is_match(x, y):
    if len(x) < 3 or len(y) < 3:
        return True if x == y else False
    else:
        return True if len(lcs_dp(x, y)) >= 3 else False


def main(trait, output):
    # init
    gene_count = {}
    paper_gene = {}
    result = []

    # read data
    mid = read_mid(trait)

    # parse gene
    for i, v in enumerate(mid):
        genes = parse_gene(v)
        paper_gene[i] = []
        for g in genes:
            found = False
            for k in gene_count:
                if is_match(g, k):
                    gene_count[k] += 1
                    paper_gene[i].append(k)
                    found = True
            if not found:
                gene_count[g] = 1
                paper_gene[i].append(g)

    # sort gene
    while len(gene_count) > 0:
        top_gene = sorted(gene_count, key=lambda x: gene_count[x])[-1]
        for k, v in paper_gene.items():
            if top_gene in v and k not in result:
                result.append(k)
        del gene_count[top_gene]
    # result = set(result)
    write_mid(output, mid, result)


if __name__ == '__main__':
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\合并后的内容"):
        for file in files:
            main(path+"\\"+file, "C:\\Users\\Administrator\\Desktop\\sorted\\"+file)
