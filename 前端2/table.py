# coding: utf-8
"""
用来生成主页的数据表
"""
import os
from templite import Templite

# 这是数据表的那11列数据的文件夹
path = "C:/Users/Administrator/Desktop/表"

fs = os.listdir(path)

my = {}
for i, f in enumerate(fs):
    tem = []
    with open(path+"/"+f, "r", encoding="utf8") as fin:
        for line in fin.readlines():
            tem.append(line.strip())
    my.update({i: tem})

LL = []
for i in range(len(my[0])):
    zi = {"key": my[4][i], "value": [my[0][i], my[3][i], my[4][i], "摘要", "全文", my[5][i], my[6][i], my[7][i], my[8][i], my[9][i], my[10][i], my[1][i], my[2][i]]}
    LL.append(zi)

with open("D:/我的文档/Documents/GitHub/Pubmed/pubmed_init_deal/template/model.html", "r", encoding="utf8") as fi:
    html = fi.read()

tem = Templite(html)

res = tem.render({
    "LL": LL
})

with open("D:/我的文档/Documents/GitHub/Pubmed/pubmed_init_deal/index.html", "w", encoding="utf8") as fou:
    fou.write(res)
