# coding: utf-8
# 处理摘要语法树, 遍历所有子结点, 用来标注全部的基因, 标注全部的性状
import os
import re
import string
from multiprocessing import Pool

import txt_token

need_del_pmid = {'10947181', '29305230', '29287393', '27794206', '26601587', '18096944', '29293767', '29290449',
                 '28562076', '28938771', '28709434', '28496985', '28373120', '27822738', '27746355', '27718430'}


def make_word():  # 全部的基因名字
    with open('C:\\Users\\Administrator\\Desktop\\基因处理\\geneprimary.set.txt', 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            if not re.match(r'Glyma\d{2}[gG]\d+(\.\d*)?', line) and len(line) > 2:
                yield line.strip()


def getXing():
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\PMID"):  # 全部的性状名字
        for file in files:
            word = file.split("_")[1][:-4].strip()
            yield word


need_genge = dict()
for word in make_word():
    need_genge[word] = word


def getRes(name):
    Res = []
    _res = []

    need_xing = dict()
    for line in getXing():
        # need_xing[line.lower()] = line
    need_xing["resistance"] = "resistance"

    with open("C:\\Users\\Administrator\\Desktop\\处理后的摘要\\" + name, "r", encoding="utf8") as fin:  # 全部的摘要目录
        _name = name.split("_")[1][:-4].strip()
        xings = _name.split()
        if _name.lower() == "cold resistance":
            xings = [_name]
        elif _name.lower() == "seed glycinin and beta-conglycinin content":
            xings = ['seed', 'glycinin', 'beta-conglycinin', 'content']

        need_xing.pop(_name.lower())
        for _xing in xings:
            try:
                need_xing[_xing.lower()] = _xing
            except KeyError:
                pass

        AST = txt_token.AllDoc(fin)
        for block in AST.children:
            has_content = True
            for kid in block.children:
                if isinstance(kid, txt_token.TimeToken):
                    _res.append("时间: " + kid.content + "\n")
                elif isinstance(kid, txt_token.IdToken):
                    if kid.content in need_del_pmid:
                        _res.clear()
                        break
                    _res.append("PMID: " + kid.content + "\n\n")
                    __res = ''.join(_res)
                    if "关" in __res and "基" in __res:
                        Res.append(__res)
                        _res = []
                    else:
                        _res.clear()
                elif isinstance(kid, txt_token.AuthorToken):
                    _res.append("作者: " + kid.content + "\n")
                elif isinstance(kid, txt_token.AuthorMessageToken):
                    continue
                elif isinstance(kid, txt_token.TitleToken):
                    words = kid.content.split()
                    content = []

                    head = words[0][0].lower()
                    Head = head + words[0][1:]
                    try:
                        if need_genge[Head]:
                            _word = "基因$" + words[0] + "$基因"
                            content.append(_word)
                    except KeyError:
                        try:
                            if need_genge[words[0]]:
                                _word = "基因$" + words[0] + "$基因"
                                content.append(_word)
                        except KeyError:
                            content.append(words[0])
                    for word in words[1:]:
                        try:
                            if re.match(r'Glyma\d{2}[gG]\d+(\.\d*)?',
                                        word.strip(string.punctuation)) \
                                    or re.match(r'LOC\d{9}', word.strip(string.punctuation)) or re.match(
                                r'Os\d{2}g\d{7}', word.strip(string.punctuation)) \
                                    or re.match(r'SAMN\d{8}', word.strip(string.punctuation)) or re.match(
                                r'BAN.{3}g\d{5}D', word.strip(string.punctuation)) \
                                    or re.match(r'Glyma\.\d{2}[Gg]\d{6}', word.strip(string.punctuation)) or re.match(
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
                        content.append(word)
                    result = ' '.join(content)
                    # i = 0
                    # for reg in regs:
                    #     result = reg.sub("关键字$" + xings[i] + "$关键字", result)
                    #     i += 1
                    _res.append("标题: " + result + "\n")
                elif isinstance(kid, txt_token.Content) and has_content:
                    has_content = False
                    words = kid.content.split()
                    content = []
                    for word in words:
                        try:
                            if re.match(r'Glyma\d{2}[gG]\d+(\.\d*)?',
                                        word.strip(string.punctuation)) \
                                    or re.match(r'LOC\d{9}', word.strip(string.punctuation)) or re.match(
                                r'Os\d{2}g\d{7}', word.strip(string.punctuation)) \
                                    or re.match(r'SAMN\d{8}', word.strip(string.punctuation)) or re.match(
                                r'BAN.{3}g\d{5}D', word.strip(string.punctuation)) \
                                    or re.match(r'Glyma\.\d{2}[Gg]\d{6}', word.strip(string.punctuation)) or re.match(
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
                        content.append(word)
                    result = ' '.join(content)
                    # i = 0
                    # for reg in regs:
                    #     result = reg.sub("关键字$" + xings[i] + "$关键字", result)
                    #     i += 1
                    _res.append("内容: " + result + "\n")

    with open("C:\\Users\\Administrator\\Desktop\\基因_摘要\\" + name.split("_")[0] + "_" + name.split("_")[1][
                                                                                        :-4].strip() + ".txt", "w",
              encoding="utf8") as f:  # 摘要结果目录
        f.write(''.join(Res))


if __name__ == '__main__':
    pool = Pool()
    for (path, dirs, files_name) in os.walk("C:\\Users\\Administrator\\Desktop\\处理后的摘要"):  # 全部摘要目录
        pool.map(getRes, files_name)
    pool.close()
    pool.join()
