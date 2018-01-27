# coding: utf-8
# 这是处理nxml全文的模块, 将nxml文件构成的树型结构进行解析成序列化结构
import os
import re

import nxml_token
from gene_word import deal_word
from data import need_del_pmid


def init_deal(text):
    return re.split(r'(?s)(<.*?>)', text)


def getRes(dir, path, goal):
    fin_res = []
    files = os.listdir(path+"\\"+dir)
    for file in files:
        if_jump = False
        Res = []
        with open(path+"\\"+dir+"\\"+file, "r", encoding="utf8") as fin:
            lines = init_deal(fin.read())
            AST = nxml_token.AllDoc(lines)

            for token in AST.kid:
                if isinstance(token, nxml_token.AuthorToken):
                    Res.append(token.content+"\n")
                elif isinstance(token, nxml_token.TimeToken):
                    Res.append(token.content+"\n")
                elif isinstance(token, nxml_token.IDToken):
                    if token.content.split(":")[1].strip() in need_del_pmid:
                        if_jump = True
                        break
                    Res.append(token.content+"\n")
                elif isinstance(token, nxml_token.JouToken):
                    Res.append(token.content+"\n")
                elif isinstance(token, nxml_token.TitleToken):
                    words = token.content[3:].split()
                    content = deal_word(words, dir, True)
                    Res.append("标题:"+content+"\n")
                elif isinstance(token, nxml_token.ContentToken):
                    words = token.content[3:].split()
                    content = deal_word(words, dir)
                    if "基" in content and "关" in content:
                        Res.append("内容:"+content+"\n")

        if if_jump:
            continue
        result = ''.join(Res)
        if "基" in result and "关" in result:
            fin_res.append(result+"\n")
    with open(goal+"\\"+dir+".txt", "w", encoding="utf8") as f:
        f.write(''.join(fin_res))
        fin_res.clear()
