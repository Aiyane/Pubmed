# coding: utf-8

import os

for (path, dirs, files) in os.walk("D:\\我的文档\\res"):
    for file in files:
        Res = []
        with open(path+"\\"+file, "r", encoding="utf8") as fin:
            for line in fin.readlines():
                Res.append(line)
        with open("C:\\Users\\Administrator\\Desktop\\基因_摘要\\"+file, "a", encoding="utf8") as f:
            f.write(''.join(Res))
