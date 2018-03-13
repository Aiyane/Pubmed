#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# filter_more.py

with open('/home/aiyane/dir/table/2Category2副本.txt', "r", encoding="utf8") as fin:
    tem = set()
    for line in fin.readlines():
        if line != 'Category2':
            tem.add(line.strip())

with open('/home/aiyane/dir/table/trait_result.txt', "w", encoding="utf-8") as f:
    for one in tem:
        ones = one.split(' ')
        f.write('\n'.join(ones))
        f.write('\n')
