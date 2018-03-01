# coding: utf-8
import os
import re


def init_txt(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError("没有%r文件" % file_path)

    with open(file_path, "r", encoding="utf8") as fin:
        lines = fin.readlines()

    tem_line = ''
    for line in lines:
        if line.strip() == "":
            if tem_line:
                yield tem_line
                tem_line = ''
            yield "\n\n"
        elif line.startswith(("PMCID", "DOI")):
            yield line
        elif line.strip():
            tem_line += line.strip()+" "


def deal_line(file_path):
    """
    关键字: DOI, PMCID, PMID, 时间, 标题, 住址, 作者, 信息, 摘要, 其他
    :param file_path: 文件路径
    """
    count = 0
    jump_title = False
    for line in init_txt(file_path):
        count += 1
        if line.startswith(("DOI", "PMCID")):
            yield line.strip()
            count = 0
        elif line.startswith("PMID"):
            line = line.split(":", 1)[1].strip()
            line = "PMID:" + line.split()[0]
            yield line.strip()
            count = 0
            yield "\n"
        elif line.strip() == "":
            count -= 1
        elif count == 1:
            if line.startswith("#"):
                line = line[1:]
            if line.split(".", 1)[0].isdigit():
                try:
                    line = re.split(r",|\.|;|:", line)
                    yield "时间:" + line[2].strip()
                except IndexError:
                    count -= 1
                    jump_title = True
            elif jump_title:
                line = re.split(r",|\.|;|:", line)
                yield "时间:" + line[1].strip()
                jump_title = False
            else:
                count -= 1
        elif count == 2:
            yield "标题:" + line.strip()
        elif count == 3:
            if line.startswith("[Article in"):
                yield "住址:" + line.strip()
                count -= 1
            else:
                yield "作者:" + line.strip()
        elif count == 4:
            if line.startswith("Author information:"):
                yield "信息:" + line.strip()
                count -= 1
            else:
                try:
                    _line = re.split(r"\.|;", line)
                    words = _line[1].strip().split(' ')
                    if len(words[0].strip()) == 4 and words[0].strip().isdigit() and \
                            words[1] in Moth:
                        yield "时间:" + ' '.join(words)
                        count -= 1
                    else:
                        yield "摘要:" + line.strip()
                except IndexError:
                    yield "摘要:" + line.strip()
        elif count == 5:
            yield "其他:" + line.strip()


Moth = ('Oct', 'Jan', 'Feb', 'Mar', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
