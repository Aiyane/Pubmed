#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _txt_token.py

__author__ = 'Aiyane'
from types import GeneratorType
import re


def _tokenizer_line(lines):
    block_begin = False
    index = 0

    for line in lines:
        if line != '\n':
            index += 1
        if not begin and line.split(".", 1)[0].isdigit():
            block_begin = True
            try:
                yield TimeToken("时间:" + re.split(r",|\.|;|:", line)[2])
            except IndexError:
                pass
        elif index == 2:
            yield TitleToken("标题:" + line.strip())
        elif index == 3:
            yield AuthorToken("作者:" + line.strip())
        elif line.startswith("Author information"):
            info_fence = True
        elif info_fence:
            if line == '\n':
                info_fence = False
        elif line.startswith("PMID:"):
            yield IDToken(line.strip())
        elif line.startswith("PMCID") or line.startswith("DOT"):
            continue
        elif line != '\n':
            yield ContentToken("摘要:" + line.strip())


class TimeToken(object):
    def __index__(self, content):
        self.content = content


class TitleToken(object):
    def __init__(self, content):
        self.content = content


class AuthorToken(object):
    def __init__(self, content):
        self.content = content


class IDToken(object):
    def __init__(self, content):
        self.content = content


class ContentToken(object):
    def __init__(self, content):
        self.content = content


def _tokenizer(lines):
    buffer = []
    for line in lines:
        if line.startswith("PMID") and len(buffer) > 1:
            yield BlockToken(buffer)
            buffer.clear()
        elif line.strip().startswith("[Article") == -1:
            line = line.replace(">", "&gt;")
            buffer.append(line.replace("<", "&lt;"))


class BlockToken(object):
    def __init__(self, lines):
        self.kid = tuple(
            token for token in _tokenizer_line(lines) if token is not None)


class AllDoc(object):
    def __init__(self, lines):
        """
        基础文档类
        """
        self._kid = tuple(
            token for token in _tokenizer(lines) if token is not None)

    @property
    def kid(self):
        if isinstance(self._kid, GeneratorType):
            self._kid = tuple(self._kid)
        return self._kid
