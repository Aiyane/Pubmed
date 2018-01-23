# coding: utf-8
# 处理txt的全文, 标注出全部的基因, 标注出全部的性状
import re
import os


def make_word():
    # 将性状全部存在need_words列表中, 并且去掉首尾空格, 全部转换成小写
    with open('C:\\Users\\Administrator\\Desktop\\other_test\\第二列.txt', 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            words = line.lower().strip().split()
            for word in words:
                if not re.match(r'Glyma\d{2}[gG]\d+(\.\d*)?', word):
                    yield word
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\第一列.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line.strip()


def getXing():
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\PMID"):
        for file in files:
            word = file.split("_")[1][:-4]
            yield word.lower()


need_word = dict()
for word in make_word():
    need_word[word.lower()] = word
genge = dict()
for line in getXing():
    genge[line.lower()] = line

with open("C:\\Users\\Administrator\\Desktop\\处理后的测试全文.txt", "r", encoding="utf8") as fin:
    content = []
    Res = []
    for words in fin.readlines():
        words = words.split()
        for word in words:
            try:
                if need_word[word.lower()] or re.match(r'Glyma\d{2}[gG]\d+(\.\d*)?', word):
                    word = "基因>" + word + "<基因"
            except KeyError:
                try:
                    if genge[word.lower()]:
                        word = "关键字>" + word + "<关键字"
                except KeyError:
                    pass
            content.append(word)
        content.append("\n")
    Res.append(' '.join(content))
with open("C:\\Users\\Administrator\\Desktop\\测试全文1.txt", "w", encoding="utf8") as f:
    f.write(''.join(Res))
