# coding: utf-8
import os
path = "C:/Users/Administrator/Desktop/output_need_id.txt"

PMID = set()
with open(path, "r", encoding="utf8") as fin:
    for line in fin.readlines():
        if line[0] == "E":
            PMID.add(line.split()[1].strip())

print(len(PMID))

output_path = "C:/Users/Administrator/Desktop/nxml全文"
nxml_pmid = set()
for file in os.listdir(output_path):
    nxml_pmid.add(file[-5])

finID = PMID - nxml_pmid

with open("C:/Users/Administrator/Desktop/output3.txt", "w", encoding="utf8") as f:
    f.write('\n'.join(finID))
