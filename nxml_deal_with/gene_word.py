# coding: utf-8
# 用来匹配基因, 关键字的模块
import re
import string
from data import all_xing_file, all_gene_file


def getXing():
    with open(all_xing_file, "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line.strip()


def make_word():  # 全部的基因名字
    with open(all_gene_file, 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            if not re.match(r'Glyma\d{2}[gG]\d+(\.\d*)?', line) and len(line) > 2:
                yield line.strip()


need_genge = dict()
for word in make_word():
    need_genge[word] = word


def deal_word(words, dir, is_title=False):
    need_xing = dict()
    for line in getXing():
        need_xing[line.lower()] = line
    need_xing["resistance"] = "resistance"

    _name = dir.split("_")[1].strip()
    xings = _name.split()
    if _name.lower() == "cold resistance":
        xings = [_name]
    elif _name.lower() == "seed glycinin and beta-conglycinin content":
        xings = ['seed', 'glycinin', 'beta-conglycinin', 'content']

    need_xing.pop(_name.lower())

    # 首先将性状全部匹配了, 因为有空格, 而单词是按空格切分的, 之后会匹配不到, 这两行位置不能错了
    words = ' '.join(words)
    for __xing in need_xing.keys():
        re.sub(re.escape(__xing), "关键字>"+__xing+"<关键字", words, 0, re.IGNORECASE)
    words = words.split()

    for _xing in xings:
        try:
            need_xing[_xing.lower()] = _xing
        except KeyError:
            pass

    buffer = []

    if is_title:
        # 如果是标题, 进行第一个单词首字母模糊匹配
        head = words[0][0].lower()
        Head = head + words[0][1:]
        try:
            if need_genge[Head]:
                _word = "基因$" + words[0] + "$基因"
                buffer.append(_word)
        except KeyError:
            try:
                if need_genge[words[0]]:
                    _word = "基因$" + words[0] + "$基因"
                    buffer.append(_word)
            except KeyError:
                buffer.append(words[0])
        words = words[1:]

    for word in words:
        try:
            if re.match(r'Glyma\d{2}[gG]\d+(\.\d*)?',
                        word.strip(string.punctuation)) \
                    or re.match(r'LOC\d{9}', word.strip(string.punctuation)) or re.match(
                r'Os\d{2}g\d{7}', word.strip(string.punctuation)) \
                    or re.match(r'SAMN\d{8}', word.strip(string.punctuation)) or re.match(
                r'BAN.{3}g\d{5}D', word.strip(string.punctuation)) \
                    or re.match(r'Glyma\.\d{2}[Gg]\d{6}',
                                word.strip(string.punctuation)) or re.match(
                r'Vigan\.\d{2}G\d{6}', word.strip(string.punctuation)) \
                    or re.match(r'GSBRNA2T\d{11}', word.strip(string.punctuation)) or re.match(
                r'WBb.{5}\.\d{2}', word.strip(string.punctuation)) \
                    or re.match(r'P0.{6}\.\d{2}', word.strip(string.punctuation)) or re.match(
                r'Gm-BamyTkm\d', word.strip(string.punctuation)) \
                    or re.match(r'Gm-Bamy.{3}', word.strip(string.punctuation)) or re.match(
                r'EF1Bgamma\d', word.strip(string.punctuation)) \
                    or re.match(r'LOC\d{5}', word.strip(string.punctuation)) or re.match(
                r'HSP\d{2}(\.)+\d-.', word.strip(string.punctuation)) \
                    or re.match(r'GlmaxMp\d{2}', word.strip(string.punctuation)) or re.match(
                r'GmFAD2-.{2}', word.strip(string.punctuation)) \
                    or re.match(r'GmMYB29.{2}', word.strip(string.punctuation)) or re.match(
                r'Avh1b-.{3}', word.strip(string.punctuation)) \
                    or re.match(r'At1g\d{5}', word.strip(string.punctuation)) or re.match(
                r'G[Mm].+', word.strip(string.punctuation)) or need_genge[word]:
                word = "基因$" + word + "$基因"
        except KeyError:
            try:
                if need_xing[word.strip(string.punctuation).lower()]:
                    word = "关键字$" + word + "$关键字"
            except KeyError:
                pass
        buffer.append(word)

    return ' '.join(buffer)
