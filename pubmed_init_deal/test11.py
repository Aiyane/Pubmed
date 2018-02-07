import os
from pubmed import MultiFilePubmud

init_path = "C:/Users/Administrator/Desktop/合并后的内容"
path = "C:/Users/Administrator/Desktop/fin_res"

all_file = os.listdir(path)

root = MultiFilePubmud(init_path)

for file in all_file:
    name = file.split(".")[0]
    time = root[name].get("时间")
    author = root[name].get("作者")
    pmid = root[name].get("PMID")
    jou = root[name].get("期刊")
    title = root[name].get("标题")

    with open(path + "/" + file, "a", encoding="utf8") as f:
        if time:
            f.write("\n")
            f.write("时间: " + ''.join(time))
        if author:
            f.write("\n")
            f.write("作者: " + ''.join(author))
        if pmid:
            f.write("\n")
            f.write("PMID: " + ''.join(pmid))
        if jou:
            f.write("\n")
            f.write("期刊: " + ''.join(jou))
        if title:
            f.write("\n")
            f.write("标题: " + ''.join(title))