# coding: utf-8
import os
with open(os.getcwd()+"/test.py", "r", encoding="utf8") as fin:
    lines = fin.readlines()

res = []
codefence = False
for line in lines:
    if line.startswith("#"):
        if codefence:
            res.append("```\n")
            codefence = False
        res.append(line[2:])
        res.append('\n')
    elif line.startswith('"""'):
        if codefence:
            res.append("```\n")
            codefence = False
        res.append("### " + line[3:-4])
        res.append("\n")
    elif line == "\n":
        if codefence:
            res.append("```\n")
            codefence = False
        res.append(line)
    else:
        if not codefence:
            res.append("```py\n")
            codefence = True
        res.append(line)
if codefence:
    res.append("```\n")

with open(os.getcwd()+"/doc.md", "w", encoding="utf8") as f:
    f.write(''.join(res))
