# coding: utf-8
from multiprocessing import Pool
import re
import os


def init_paper(text):
    context = re.split(r'(?s)(<.*?>)', text)
    return context


def make_word():
    # 将性状全部存在need_words列表中, 并且去掉首尾空格, 全部转换成小写
    with open('C:\\Users\\Administrator\\Desktop\\deal\\need.txt', 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            word = line.lower().strip()
            yield word


# IO操作才是拖慢时间的罪魁祸首!!
def getLine(files, pattern):
    for file in files:
        with open("C:\\Users\\Administrator\\Desktop\\deal\\大豆\\" + file, 'r', encoding="utf8") as fin:
            # 使用repr函数包裹字符串会让速度变快, 不知道为啥?
            context = init_paper(fin.read())
            pattern2 = r'(Glyma\d{2}[Gg]\d+(\.\d*)?)'
            for Line in context:
                if pattern.match(Line.lower()):
                    gene_name = re.search(pattern2, Line)
                    if gene_name:
                        Line = re.sub(pattern2, "基因: "+gene_name.group(1), Line)
                    yield ("PMCID: " + repr(file) + "内容: " + repr(Line.strip()) + "\n")


def getRes(word):
    # path 父目录, dirs 所有文件夹, files所有文件名
    # 元组的速度会快一些, 占用内存小
    res = tuple()
    pattern = re.compile(r'[\s\S]*{word}[\s\S]*$'.format(word=word.strip()))
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\deal\\大豆"):
        res = tuple(line for line in getLine(files, pattern))
    if res:
        try:
            with open("C:\\Users\\Administrator\\Desktop\\deal\\quan_res\\" + word.replace(' ', '_') + ".txt", "w", encoding="utf8") as f:
                f.write(''.join(res))
        except IOError:
            print(word.replace(' ', '_') + ".txt读入: " + ''.join(res) + " 出错")
        del res

if __name__ == '__main__':
    need_words = tuple(word for word in make_word())
    pool = Pool()
    pool.map(getRes, need_words)
    pool.close()
    pool.join()
