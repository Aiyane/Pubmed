# coding: utf-8

My_dict = {}
My_list1 = []
My_list2 = []
res = []
with open('t1.txt', 'r', encoding='utf-8') as fi1:
    for line in fi1.readlines():
        My_list1.append(line.strip())

with open('t2.txt', 'r', encoding='utf8') as fi2:
    for line in fi2.readlines():
        My_list2.append(line.strip())

with open('t0.txt', 'r', encoding='utf8') as fin:
    i = 0
    for line in fin.readlines():
        My_dict[line.strip()] = My_list1[i] + '*' + My_list2[i]
        i += 1

with open('ss.txt', 'r', encoding='utf8') as fin:
    for line in fin.readlines():
        try:
            res.append(My_dict[line.strip()])
        except:
            res.append(' ')
            with open('cuowu.txt', 'a') as f:
                f.write(line)

with open('res1.txt', 'a') as f:
    for line in res:
        line = line.split('*')[0] + '\n'
        f.write(line)

with open('res2.txt', 'a') as f:
    for line in res:
        line = ''.join(line.split('*')[1:]) + '\n'
        f.write(line)
