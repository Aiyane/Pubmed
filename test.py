#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# test.py
from pubmed import OneFilePubmud
root = OneFilePubmud('pubmed.txt')
words = ['soybean']
words2 = ['information']

root.make_pages(keys=words, values=words2, filter_article=True)