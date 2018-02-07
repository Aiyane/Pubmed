# coding: utf-8

import os

path1 = "C:/Users/Administrator/Desktop/PMID"
path = "C:/Users/Administrator/Desktop/output4.txt"

PMID = set()
with open(path, "r", encoding="utf8") as f:
    for line in f.readlines():
        PMID.add(line.strip())

ALL_ID = set()

for file in os.listdir(path1):
    with open(path1+"/"+file, "r", encoding="utf8") as f:
        for line in f.readlines():
            ALL_ID.add(line.strip())

with open("C:/Users/Administrator/Desktop/all_id.txt", "w", encoding="utf8") as f:
    f.write('\n'.join(ALL_ID))

OK_ID = set()
for pmid in PMID:
    if pmid in ALL_ID:
        OK_ID.add(pmid)

with open("C:/Users/Administrator/Desktop/ok_id.txt", "w", encoding="utf8") as f:
    f.write('\n'.join(OK_ID))
