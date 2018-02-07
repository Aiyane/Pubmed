# coding: utf-8

from pubmed import MultiFilePubmud

path2 = "C:/Users/Administrator/Desktop/基因_摘要"
pmid_file_path = "C:/Users/Administrator/Desktop/PMID.txt"
output_path = "C:/Users/Administrator/Desktop/output2.txt"

PMID = set()
with open(pmid_file_path, "r", encoding="utf8") as fin:
    for line in fin.readlines():
        PMID.add(line.strip())

print(len(PMID))
root = MultiFilePubmud(path2)
res = root.get_summary(PMID, True)

with open(output_path, "w", encoding="utf8") as f:
    f.write('\n\n'.join(res))
