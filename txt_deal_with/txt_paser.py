#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _txt_paser.py

__author__ = 'Aiyane'
import txt_token
from gene_word import deal_word
from data import output_path, need_del_pmid


def getRes(file, path):
    fin_res = []
    with open(path + "\\" + file, "r", encoding="utf8") as fin:
        AST = txt_token.AllDoc(fin)

    for block in AST.kid:
        _res = deal_block(block, file)
        if _res is not None:
            fin_res.append(_res + "\n")

    with open(
            output_path + "\\" + file[:-4].strip() + ".txt", "w",
            encoding="utf8") as f:
        f.write(''.join(fin_res))


def deal_block(block, file):
    Res = []
    for token in block.kid:
        if isinstance(token, txt_token.AuthorToken):
            Res.append(token.content + '\n')
        elif isinstance(token, txt_token.IDToken):
            _res = token.content.split(":")[1].strip()
            if _res.split()[0].strip() in need_del_pmid:
                return None
            Res.append(token.content + '\n')
        elif isinstance(token, txt_token.TimeToken):
            Res.append(token.content + '\n')
        elif isinstance(token, txt_token.TitleToken):
            words = token.content[3:].split()
            content = deal_word(words, file[:-4], True)
            Res.append("标题:" + content + "\n")
        elif isinstance(token, txt_token.ContentToken):
            for line in token.content:
                line = line.split()
                _content = deal_word(line, file[:-4])
                if "基" not in _content or "关" not in _content:
                    continue
                else:
                    Res.append("内容:" + _content + '.\n')

    result = ''.join(Res)
    if "基" in result and "关" in result:
        return result
