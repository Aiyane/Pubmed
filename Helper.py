# coding: utf-8

import random
import string

need_words = []

# 将性状全部存在need_words列表中, 并且去掉首尾空格, 全部转换成小写
with open('C:\\Users\\Administrator\\Desktop\\need.txt', 'r', encoding="utf8") as fin:
    for line in fin.readlines():
        if line.strip():
            need_words.append(line.lower())

for i in range(1000):
    with open('C:\\Users\\Administrator\\Desktop\\test\\test' + str(i) + ".txt", 'a', encoding="utf8") as f:
        for _r in range(100):
            if random.randint(0, 9) % 2 == 0:
                f.write(''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 8)) + '\n')
            else:
                f.write(''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 4)) + need_words[random.randint(0, 113)].strip() +
                        ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 4)) + '\n')
