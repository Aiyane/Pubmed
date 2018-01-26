#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# main.py
"""
模块功能: 
"""
__author__ = 'Aiyane'


def _tokenizer(lines):
    buffer = []
    for line in lines:
        if line == '\n' and len(buffer) > 1:
            yield Block(buffer)
            buffer.clear()
        else:
            buffer.append(line)


def _tokenizer_line(buffer):
    for line in buffer:
        if line.startswith("时间"):
            yield TimeToken(line)
        elif line.startswith("作者"):
            yield AuthorToken(line)
        elif line.startswith("内容"):
            yield ContentToken(line)


class AllDoc(object):
    def __init__(self, lines):
        self.kid = tuple(token for token in _tokenizer(lines))


class Block(object):
    def __init__(self, buffer):
        self.kid = (token for token in _tokenizer_line(buffer))
