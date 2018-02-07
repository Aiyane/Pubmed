#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# _txt_token.py

__author__ = 'Aiyane'
from types import GeneratorType
import re


def _tokenizer_line(lines):
    block_begin = False
    info_fence = False
    index = 0
    title_fence = False
    author_fence = False

    for line in lines:
        if line != '\n' and line != '':
            index += 1
        if not block_begin and line.split(".", 1)[0].isdigit():
            block_begin = True
            try:
                line = re.split(r",|\.|;|:", line)
                yield TimeToken("时间:" + line[2].strip())
            except IndexError:
                pass
        elif not title_fence and index == 2:
            title_fence = True
            yield TitleToken("标题:" + line.strip())
        elif not author_fence and index == 3:
            author_fence = True
            yield AuthorToken("作者:" + line.strip())
        elif line.startswith("Author information"):
            info_fence = True
        elif info_fence:
            if line == '\n':
                info_fence = False
        elif line.startswith("PMID:"):
            yield IDToken(line.strip())
        elif line.startswith("PMCID") or line.startswith("DOI"):
            continue
        elif line != '\n':
            yield ContentToken(line.strip())


class TimeToken(object):
    def __init__(self, content):
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
        content = content.split(".")
        self.content = content


def _tokenizer(lines):
    buffer = []
    for line in lines:
        if line.startswith("PMID") and len(buffer) > 1:
            buffer.append(line)
            yield BlockToken(buffer)
            buffer.clear()
        elif not line.strip().startswith("[Article"):
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
