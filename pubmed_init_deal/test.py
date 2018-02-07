# coding: utf-8
from pubmed import OneFilePubmud, MultiFilePubmud

# 原生Pubmed的Abstract摘要文件的路径
init_path = "C:/Users/Administrator/Desktop/摘要/高产_Photoperiod sensitivity.txt"
# 很多Pubmed摘要文件的文件夹路径
path = "C:/Users/Administrator/Desktop/摘要"

# 以下是例子, text_root和root就是可操作的对象了
text_root = OneFilePubmud(init_path)
root = MultiFilePubmud(path)
