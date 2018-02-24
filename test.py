#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# test.py
from pubmed import OneFilePubmud

content = OneFilePubmud('pubmed.txt')
content.make_pages(make_html=False, keys=['soybean'], ignore=True, filter_article=True)