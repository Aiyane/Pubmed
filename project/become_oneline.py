#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 处理摘要, 使摘要变成一行

__author__ = 'Aiyane'
import re
import os


def deal_line(lines):
    fence = False
    jump = False
    begin = False
    temp = ''
    for line in lines:
        if fence:
            if line == '\n':
                yield (temp + '\n')
                temp = ''
                fence = False
                yield line
            elif re.match(r"\((.*)\).*", line):
                if re.match(r"\((.*)\).*", line).group(1).isdigit():
                    if temp:
                        yield (temp + '\n')
                    temp = line.strip()
                    continue
                temp = temp + line.strip()
            else:
                temp = temp + line.strip()

        elif not begin and line.split(".", 1)[0].isdigit():
            begin = True
            temp = line.strip()
        elif line.startswith("PMID:"):
            begin = False
            yield (line)
        elif line.startswith("DOI:"):
            yield (line)
        elif line.startswith("PMCID:"):
            yield (line)
        elif line.startswith("Author information:"):
            fence = True
            yield (line)
        elif jump:
            if line == '\n':
                jump = False
        elif begin and line.find("©") == -1:
            if line == '\n':
                yield (temp + '\n')
                yield (line)
                temp = ''
            else:
                temp = temp + ' ' + line.strip()
        elif line == '\n':
            yield line
        elif line.find("©") != -1:
            jump = True


for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\摘要"):
    res = tuple()
    for file in files:
        with open(path + "\\" + file, "r", encoding="utf8") as fin:
            res = tuple(line for line in deal_line(fin))
        with open(
                "C:\\Users\\Administrator\\Desktop\\处理后的摘要\\" + file,
                "w",
                encoding="utf8") as f:
            f.write(''.join(res))
