# coding:utf-8
# 从服务器上筛的nxml与其他人找的nxml, 将不一样的移动
import os
import shutil

my_dict = dict()
for (path, dirs, files) in os.walk("D:\\我的文档\\xing"):
    for dir in dirs:
        for (path1, dirs1, files1) in os.walk(path+"\\"+dir):
            for file in files1:
                my_dict[file] = file

for (path, dirs, _files) in os.walk("C:\\Users\\Administrator\\Desktop\\从服务器上筛的nxml"):
    for dir in dirs:
        for (path2, dirs2, files2) in os.walk(path + "\\" + dir):
            for file in files2:
                try:
                    if my_dict[file]:
                        pass
                except KeyError:
                    if not os.path.exists("D:\\我的文档\\备用\\"+dir[:-4].strip()):
                        os.mkdir("D:\\我的文档\\备用\\"+dir[:-4].strip())
                    shutil.copyfile(path + "\\" + dir + "\\" + file, "D:\\我的文档\\xing\\"+dir[:-4].strip()+"\\"+file)
