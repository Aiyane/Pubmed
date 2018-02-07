# coding: utf-8

out_path = "C:/Users/Administrator/Desktop/new_file"
path = "C:/Users/Administrator/Desktop/new_output.txt"

with open(path, "r", encoding="utf8") as f:
    for line in f.readlines():
        if line[0] == "E" or line == "\n":
            continue
        con = line.split(":", 1)[1].strip()
        name = line.split(":", 1)[0]
        with open(out_path+"/"+name+".txt", "w", encoding="utf8") as fin:
            fin.write(con)