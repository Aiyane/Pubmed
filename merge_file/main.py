#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# main.py
"""
模块功能: 将全文nxml处理文件合并到响应的摘要txt处理文件后, 然后将pmid相同的摘要与全文归并一起
"""
__author__ = 'Aiyane'
import os


def _tokenizer(lines):
    buffer = []
    for line in lines:
        if line == '\n' and len(buffer) > 1:
            yield Block(buffer)
            buffer.clear()
        else:
            buffer.append(line)


class AllDoc(object):
    def __init__(self, lines):
        self.kid = tuple(
            token for token in _tokenizer(lines) if token is not None)
        self.PMID = dict()
        for token in self.kid:
            try:
                if token._pmid not in self.PMID.keys():
                    self.PMID[token._pmid] = token
                else:
                    token.summary = self.PMID[token._pmid].content
                    _content = [
                        line.replace("内容", "正文") for line in token.content
                    ]
                    token.content = _content
                    self.PMID[token._pmid] = token
            except AttributeError:
                self.PMID[token.title] = token


class Block(object):
    def __init__(self, buffer):
        _content = []
        for line in buffer:
            if line.startswith("时间"):
                self.time = line
            elif line.startswith("作者"):
                self.author = line
            elif line.startswith("内容"):
                _content.append(line)
                self.content = _content
            elif line.startswith("标题"):
                self.title = line
            elif line.startswith("PMCID"):
                self.pmcid = line
            elif line.startswith("期刊"):
                self.jou = line
            elif line.startswith("PMID"):
                self.pmid = line
                _pmid = line.split(":")[1].strip().split()[0].strip()
                self._pmid = _pmid


for (path, dirs, files) in os.walk("D:\\我的文档\\res"):
    for file in files:
        Res = []
        with open(path + "\\" + file, "r", encoding="utf8") as fin:
            for line in fin.readlines():
                Res.append(line)
        with open(
                "C:\\Users\\Administrator\\Desktop\\基因_摘要\\" + file,
                "a",
                encoding="utf8") as f:
            f.write(''.join(Res))

AST = None
for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\基因_摘要"):
    for file in files:
        Res = []
        with open(path + "\\" + file, "r", encoding="utf8") as fin:
            AST = AllDoc(fin)

        for token in AST.PMID.values():
            for param in dir(token):
                if param.startswith("_"):
                    continue
                elif param == "time":
                    Res.append(token.time)
                elif param == "jou":
                    Res.append(token.jou)
                elif param == "pmid":
                    Res.append(token.pmid)
                elif param == "pmcid":
                    Res.append(token.pmcid)
                elif param == "title":
                    Res.append(token.title)
                elif param == "author":
                    Res.append(token.author)
                elif param == "content":
                    Res.append(''.join(token.content))
                elif param == "summary":
                    Res.append(''.join(token.summary))
            Res.append("\n")

        with open(
                "C:\\Users\\Administrator\\Desktop\\合并后的内容\\" + file,
                "w",
                encoding="utf8") as f:
            f.write(''.join(Res))
