# coding: utf-8
def getID():
    with open("C:\\Users\\Administrator\\Desktop\\大豆PMID.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line


res = tuple(line for line in getID())
for i in range(16):
    j = i + 1
    with open("C:\\Users\\Administrator\\Desktop\\test" + str(j) + ".txt", "w", encoding="utf8") as f:
        if j == 16:
            f.write(''.join(res[j*1000-1000:]))
        else:
            f.write(''.join(res[j*1000-1000:j*1000]))
