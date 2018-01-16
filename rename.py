# coding: utf-8
import os
import sys

path = "C:\\Users\\Administrator\\Desktop\\txt2"

file = open("C:\\Users\\Administrator\\Desktop\\guanxi.txt")

mydict = {}

while 1:
    line = file.readline()
    if not line:
        break

    dic = line.split()
    mydict[dic[1] + ".txt"] = dic[0] + ".txt"


for (path, dirs, files) in os.walk(path):
    for filename in files:
        newname = mydict[filename]
        os.rename(path + "\\" + filename, "C:\\Users\\Administrator\\Desktop\\txt2" + "\\" + newname)
