# coding: utf-8
"""
用来生成markdown文档
"""
import os


def getDoc(test_file="test.py"):
    path = os.getcwd() + "/" + test_file

    with open(path, "r", encoding="utf8") as fin:
        lines = fin.readlines()

    codefence = False
    yield "## " + lines[0][3:-4]
    for line in lines[1:]:
        if line.startswith("#"):
            if codefence:
                yield "```\n"
                codefence = False
            yield line[2:]
            yield '\n'
        elif line.startswith('"""'):
            if codefence:
                yield "```\n"
                codefence = False
            yield "### " + line[3:-4]
            yield "\n"
        elif line == "\n":
            if codefence:
                yield "```\n"
                codefence = False
            yield line
        else:
            if not codefence:
                yield "```py\n"
                codefence = True
            yield line
    if codefence:
        yield "```\n"


def main(file="doc.md", test_file="test.py"):
    with open(os.getcwd() + "/" + file, "w", encoding="utf8") as f:
        for line in getDoc(test_file):
            f.write(line)

if __name__ == '__main__':
    main()
