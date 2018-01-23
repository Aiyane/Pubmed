# coding: utf-8
from multiprocessing import Pool
import re
import os
import txt_token


def make_word():  # 全部的基因名字
    with open('C:\\Users\\Administrator\\Desktop\\other_test\\第二列.txt', 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            words = line.lower().strip().split()
            for word in words:
                if not re.match(r'Glyma\d{2}[gG]\d+(\.\d*)?', word):
                    yield word.strip()
    with open("C:\\Users\\Administrator\\Desktop\\other_test\\第一列.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line.strip()


def getXing():
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\PMID"):  # 全部的性状名字
        for file in files:
            word = file.split("_")[1][:-4].strip()
            yield word

need_xing = dict()
for line in getXing():
    need_xing[line.lower()] = line
need_genge = dict()
for word in make_word():
    need_genge[word.lower()] = word


def getRes(name):
    # path 父目录, dirs 所有文件夹, files所有文件名
    # 元组的速度会快一些, 占用内存小
    Res = []
    with open("C:\\Users\\Administrator\\Desktop\\处理后的摘要\\"+name, "r", encoding="utf8") as fin:  # 全部的摘要目录
        xing = name.split("_")[1][:-4].strip()
        reg = re.compile(re.escape(xing), re.IGNORECASE)
        need_xing.pop(xing.lower())
        AST = txt_token.AllDoc(fin)
        for block in AST.children:
            for kid in block.children:
                if isinstance(kid, txt_token.TimeToken):
                    Res.append("时间: " + kid.content + "\n")
                elif isinstance(kid, txt_token.IdToken):
                    Res.append("PMID: "+kid.content + "\n\n")
                elif isinstance(kid, txt_token.AuthorToken):
                    Res.append("作者: "+kid.content+"\n")
                elif isinstance(kid, txt_token.AuthorMessageToken):
                    continue
                elif isinstance(kid, txt_token.TitleToken):
                    words = kid.content.split()
                    content = []
                    for word in words:
                        try:
                            if need_genge[word.lower()] or re.match(r'Glyma\d{2}[gG]\d+(\.\d*)?', word):
                                word = "基因>"+word+"<基因"
                        except KeyError:
                            try:
                                if need_xing[word.lower()]:
                                    word = "关键字>" + word + "<关键字"
                            except KeyError:
                                pass
                        content.append(word)
                    result = ' '.join(content)
                    result = reg.sub("关键字>" + xing + "<关键字", result)
                    Res.append("标题: "+result+"\n")
                elif isinstance(kid, txt_token.Content):
                    words = kid.content.split()
                    content = []
                    for word in words:
                        try:
                            if need_genge[word.lower()] or re.match(r'Glyma\d{2}[gG]\d+(\.\d*)?', word):
                                word = "基因>" + word + "<基因"
                        except KeyError:
                                try:
                                    if need_xing[word.lower()]:
                                        word = "关键字>" + word + "<关键字"
                                except KeyError:
                                    pass
                        content.append(word)
                    result = ' '.join(content)
                    result = reg.sub("关键字>" + xing + "<关键字", result)
                    Res.append("内容: " + result + "\n")
    with open("C:\\Users\\Administrator\\Desktop\\基因_摘要\\"+name, "w", encoding="utf8") as f:  # 摘要结果目录
        f.write(''.join(Res))


if __name__ == '__main__':
    pool = Pool()
    for (path, dirs, files_name) in os.walk("C:\\Users\\Administrator\\Desktop\\处理后的摘要"):  # 全部摘要目录
        pool.map(getRes, files_name)
    pool.close()
    pool.join()
