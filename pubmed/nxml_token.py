#!/usr/bin/python3
# coding: utf-8
"""
这一个文件处理的是nxml文件的解析
"""
from types import GeneratorType
import re
import os


def _tokenizer(lines):
    fence = False
    pmc_close = True
    pmid_close = True
    jou_close = True
    time_close = True
    title_close = True
    author_close = True
    zai_close = True
    is_zai = True
    buffer = []
    for line in lines:
        if fence:
            if line.startswith('</abstract>'):
                yield ''.join(buffer)
                buffer.clear()
                fence = False
                is_zai = True
                continue
            elif line.startswith('</article-id>'):
                yield ''.join(buffer)
                buffer.clear()
                fence = False
                continue
            elif line.startswith('</journal-title>'):
                yield ''.join(buffer)
                buffer.clear()
                fence = False
                continue
            elif line.startswith('</article-title>'):
                yield ''.join(buffer)
                buffer.clear()
                fence = False
                continue
            elif line.startswith('</date>'):
                yield ''.join(buffer)
                buffer.clear()
                fence = False
                continue
            elif line.startswith('</contrib-group>'):
                yield ''.join(buffer)
                buffer.clear()
                fence = False
                continue
            elif is_zai and line.startswith('</p>'):
                yield ''.join(buffer)
                buffer.clear()
                fence = False
                continue
            buffer.append(line)

        elif zai_close and line.startswith('<abstract>'):
            zai_close = False
            buffer.append("摘要:")
            fence = True
            is_zai = False
        elif pmc_close and line.startswith('<article-id pub-id-type="pmc">'):
            buffer.append("PMCID:")
            pmc_close = False
            fence = True
        elif pmid_close and line.startswith('<article-id pub-id-type="pmid">'):
            buffer.append("PMID:")
            pmid_close = False
            fence = True
        elif jou_close and line.startswith('<journal-title>'):
            buffer.append("期刊:")
            jou_close = False
            fence = True
        elif title_close and line.startswith('<article-title>'):
            title_close = False
            buffer.append("标题:")
            fence = True
        elif time_close and line.startswith('<date date-type="accepted">'):
            time_close = False
            buffer.append("时间:")
            fence = True
        elif author_close and line.startswith('<contrib-group>'):
            author_close = False
            buffer.append("作者:")
            fence = True
        elif line.startswith('<p>'):
            buffer.append("正文:")
            fence = True


def init_deal(text):
    return re.split(r'(?s)(<.*?>)', text)


def nxml_deal(path):
    if not os.path.isfile(path) or not path.endswith(".nxml"):
        raise FileNotFoundError("%r文件不存在", path)

    with open(path, "r", encoding="utf8") as fin:
        text = fin.read()
    for line in _tokenizer(init_deal(text)):
        yield line
    yield '\n'