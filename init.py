# coding: utf-8
global line
f = open("C:\\Users\\Administrator\\Desktop\\find.txt")
lines = f.readlines()
myList = []
for line in lines:
    myList.append(line)

mySet = set(myList)
for yuansu in mySet:
    with open("C:\\Users\\Administrator\\Desktop\\find1.txt", "a") as f:
        f.write(yuansu)
