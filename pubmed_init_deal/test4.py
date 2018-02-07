# coding: utf-8
import os
init_path = "C:/Users/Administrator/Desktop/合并后的内容"

path = "C:/Users/Administrator/Desktop/output3.txt"
PMID = set()
with open(path, "r", encoding="utf8") as fin:
    for line in fin.readlines():
        PMID.add(line.strip())

all_file = os.listdir(init_path)
res = {}
for file in all_file:
    buffer = []
    with open(init_path+"/"+file, "r", encoding="utf8") as fin:
        save_it = ''
        for line in fin.readlines():
            if line != "\n":
                buffer.append(line)
                if line.startswith("PMI"):
                    ID = line.split(":", 1)[1].strip().split()[0]
                    if ID in PMID:
                        save_it = ID
            elif buffer and save_it:
                res.update({save_it: ''.join(buffer)})
                save_it = ''
            else:
                buffer.clear()

for key, value in res.items():
    with open("C:/Users/Administrator/Desktop/txt全文2/"+key+".txt", "w", encoding="utf8") as f:
        f.write(value)
