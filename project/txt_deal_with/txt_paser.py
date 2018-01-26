#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _txt_paser.py

__author__ = 'Aiyane'

import re
import string

import txt_token
from gene_word import deal_word
from run import output_path, need_del_pmid


def getRes(path, file):
    fin_res = []
    AST = None
    with open(path+"\\"+file, "r", encoding="utf8") as fin:
        AST = _txt_token.AllDoc(fin.read())
    
    for block in AST.kid:
        _res = deal_block(block, file)+"\n"
        if _res is not None:
            fin_res.append(_res)
    
    with open(output_path, "w", encoding="utf8") as f:
        f.write(''.join(fin_res))
    
def deal_block(block, file):
    Res = []
    for token in block.kid:
        if isinstance(token, _txt_token.AuthorToken):
            Res.append(token.content+'\n')
        elif isinstance(token, _txt_token.IDToken:
            if token.content.split(":")[1].strip() in need_del_pmid:
                return None
            Res.append(token.content+'\n')
        elif isinstance(token, _txt_token.TimeToken):
            Res.append(token.content+'\n')
        elif isinstance(token, _txt_token.TitleToken):
            words = token.content[3:].split()
            content = deal_word(words, file[:-4], True)
            Res.append("标题:"+content+"\n")
        elif isinstance(token, _txt_token.ContentToken):
            words = toekn.content[3:].split()
            content = deal_word(words, file[:-4])
            if "基" in content and "关" in content:
                Res.append("摘要:"+content+'\n')
    return ''.join(Res)
