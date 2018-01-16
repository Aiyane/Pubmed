# coding: utf-8
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

# 通过协程将所有性状同时进行搜索
async def getLine(file, word):

    # 第一段if是判断word是否以数字开头, 以数字开头的去掉开头的数字
    if word[0].isdigit():
        name = []
        for Char in word:
            if Char.isdigit():
                continue
            else:
                name.append(Char)
            word = ''.join(name)

    pattern = re.compile(r'[\s\S]*{word}[\s\S]*$'.format(word=word.strip()))
    with open("C:\\Users\\Administrator\\Desktop\\test\\" + file, 'r', encoding="utf8") as fin:
        for Line in fin.readlines():
            if pattern.match(Line.lower()):
                res.append(file + "$" + Line)

    if res:
        try:
            with open("C:\\Users\\Administrator\\Desktop\\res\\" + word.replace(' ', '_') + ".txt", "a", encoding="utf8") as f:
                f.write(''.join(res))
        except Exception:
            print(word.replace(' ', '_') + ".txt读入: " + ''.join(res) + " 出错")
        res.clear()

async def getRes(word):
    # path 父目录, dirs 所有文件夹, files所有文件名
    for (path, dirs, files) in os.walk("C:\\Users\\Administrator\\Desktop\\test"):
        for file in files:
            await getLine(file, word)


loop = asyncio.get_event_loop()

tasks = [getRes(word) for word in need_words]  # 将每一个性状都当作参数传递到处理函数中, 打包成一个任务列表
# task = loop.create_task(tasks)
# try:
#     loop.run_until_complete(asyncio.wait(tasks))
# except SystemExit:
#     print("caught SystemExit!")
#     task.exception()
#     raise
# finally:
#     loop.close()
loop.run_until_complete(asyncio.wait(tasks))  # 通过协程同时完成全部任务
loop.close()
