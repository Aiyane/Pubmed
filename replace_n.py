# coding: utf-8
import os

# path 父目录, dirs 所有文件夹, files所有文件名
string = ''
for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\txt2"):
    for file in files:
        with open("C:\\Users\\Administrator\\Desktop\\txt2\\"+file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if line != '\n':
                    line = line.strip()
                else:
                    line = '\n\n'
                string = string + line
        with open("C:\\Users\\Administrator\\Desktop\\txt2\\" + file, "w", encoding="utf-8") as f:
            f.write(string)
        string = ''
