# coding: utf-8
from multiprocessing import Pool
import time
import asyncio
import re
import os

need_words = []
res = []

# 将性状全部存在need_words列表中, 并且去掉首尾空格, 全部转换成小写
with open('C:\\Users\\Administrator\\Desktop\\need.txt', 'r', encoding="utf8") as fin:
    for line in fin.readlines():
        Word = line.lower().strip()
        if Word:
            need_words.append(Word)


async def write_file(res, word):
    try:
        with open("C:\\Users\\Administrator\\Desktop\\res\\" + word.replace(' ', '_') + ".txt", "a",
                  encoding="utf8") as f:
            f.write(''.join(res))
    except Exception:
        print(word.replace(' ', '_') + ".txt读入: " + ''.join(res) + " 出错")

# 通过协程将所有性状同时进行搜索
async def getLine(file, word):

    pattern = re.compile(r'[\s\S]*{word}[\s\S]*$'.format(word=word.strip()))
    with open("C:\\Users\\Administrator\\Desktop\\test\\" + file, 'r', encoding="utf8") as fin:
        for Line in fin.readlines():
            if pattern.match(Line.lower()):
                res.append(file + "$" + Line)

    if res:
        await write_file(res, word)
        res.clear()


def getRes(word):
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\test"):
        loop = asyncio.get_event_loop()
        tasks = [getLine(file, word) for file in files]
        loop.run_until_complete(asyncio.wait(tasks))  # 通过协程同时完成全部任务

if __name__ == '__main__':
    start = time.clock()
    pool = Pool(8)
    pool.map(getRes, need_words)

    pool.close()
    pool.join()
    end = time.clock()
    print("time: " + str(end - start))
# time: 19.9248137974573
