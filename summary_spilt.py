# coding: utf-8
import os

# path 父目录, dirs 所有文件夹, files所有文件名
maxline = ''
for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\文档\\国创\\摘要"):
    for file in files:
        with open("C:\\Users\\Administrator\\Desktop\\文档\\国创\\摘要\\"+file, "r", encoding="utf-8") as f:
            maxl = 0
            for line in f.readlines():
                if len(line) > maxl:
                    maxl = len(line)
                    maxline = line
        with open("C:\\Users\\Administrator\\Desktop\\文档\\国创\\摘要\\" + file, "w", encoding="utf-8") as f:
            f.write(maxline)
        maxline = ''
