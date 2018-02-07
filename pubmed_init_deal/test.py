# coding: utf-8
from pubmed import MultiFilePubmud

pmid_file_path = "C:/Users/Administrator/Desktop/new_id.txt"
init_path = "C:/Users/Administrator/Desktop/合并后的内容"
output_path = "C:/Users/Administrator/Desktop/new_output.txt"

PMID = set()
with open(pmid_file_path, "r", encoding="utf8") as fin:
    for line in fin.readlines():
        PMID.add(line.strip())

print(len(PMID))
root = MultiFilePubmud(init_path)
res = root.get_summary(PMID, True)

with open(output_path, "w", encoding="utf8") as f:
    f.write('\n\n'.join(res))
