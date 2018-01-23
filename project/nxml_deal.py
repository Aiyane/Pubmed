# coding: utf-8
# 处理nxml全文, 但是应该改, 程序有问题
from multiprocessing import Pool
import re
import os


def init_paper(text):
    context = re.split(r'(?s)(<.*?>)', text)
    return context


def make_word():
    # 将性状全部存在need_words列表中, 并且去掉首尾空格, 全部转换成小写
    with open(
            '/home/wutbio006/hey/dataset/need.txt', 'r',
            encoding="utf8") as fin:
        for line in fin.readlines():
            word = line.lower().strip()
            yield word


# IO操作才是拖慢时间的罪魁祸首!!
def getLine(files, pattern, word):
    for file in files:
        with open(
                "/home/wutbio006/hey/dataset/soybean/" + file,
                'r',
                encoding="utf8") as fin:
            # 使用repr函数包裹字符串会让速度变快, 不知道为啥?
            buffer = ''
            context = init_paper(fin.read())
            pattern2 = r'(Glyma\d{2}[Gg]\d+(\.\d*)?)'
            reg = re.compile(re.escape(word), re.IGNORECASE)

            strat_MCID, start_MID = False, False
            frist_id, frist_cid = True, True
            MID = []
            CID = []

            jou = []
            first_jou = True
            start_jou = False

            title = []
            first_title = True
            start_title = False

            author = []
            contrib = False
            first_contrib = True

            data = []
            start_data = False
            first_data = True
            for Line in context:
                if frist_cid and Line.startswith(
                        '<article-id pub-id-type="pmc">'):
                    strat_MCID = True
                    continue
                elif strat_MCID:
                    if Line.startswith("</article-id>"):
                        strat_MCID = False
                        frist_cid = False
                    elif not Line.startswith("<"):
                        CID.append(Line.strip() + " ")
                    continue
                elif frist_id and Line.startswith(
                        '<article-id pub-id-type="pmid">'):
                    start_MID = True
                    continue
                elif start_MID:
                    if Line.startswith("</article-id>"):
                        start_MID = False
                        frist_id = False
                    elif not Line.startswith("<"):
                        MID.append(Line.strip() + " ")
                    continue
                elif first_jou and Line.startswith("<journal-title>"):
                    start_jou = True
                    continue
                elif start_jou:
                    if Line.startswith("</journal-title>"):
                        start_jou = False
                        first_jou = False
                    elif not Line.startswith("<"):
                        jou.append(Line.strip() + " ")
                    continue

                elif first_title and Line.startswith("<article-title>"):
                    start_title = True
                    continue
                elif start_title:
                    if Line.startswith("</article-title>"):
                        start_title = False
                        first_title = False
                    elif not Line.startswith("<"):
                        title.append(Line.strip() + " ")
                    continue

                elif first_data and Line.startswith(
                        '<date date-type="accepted">'):
                    start_data = True
                    continue
                elif start_data:
                    if Line.startswith("</date>"):
                        start_data = False
                        first_data = False
                    elif not Line.startswith("<") and Line.isdigit():
                        data.append(Line.strip() + " ")
                    continue

                elif first_contrib and Line.startswith("<contrib-group>"):
                    contrib = True
                    continue
                elif contrib:
                    if Line.startswith("</contrib-group>"):
                        contrib = False
                        first_contrib = False
                    elif not Line.startswith("<") and Line.isalpha(
                    ) and len(Line) > 1:
                        author.append(Line.strip() + " ")
                    continue

                elif not Line.startswith("<"):
                    buffer = buffer + Line.strip()
                elif Line.startswith("<"):
                    if pattern.match(buffer.lower()):
                        gene_name = re.search(pattern2, buffer)
                        Line = reg.sub("关键词>" + word + "<关键词", Line)
                        if gene_name:
                            buffer = re.sub(pattern2,
                                            "基因>" + gene_name.group(1) + "<基因",
                                            buffer)
                        yield ("PMID:" + repr(''.join(MID)) + "\n" + "PMCID:" +
                               repr(''.join(CID)) + "\n" + "期刊:" +
                               repr(''.join(jou)) + "\n"
                               "标题:" + repr(''.join(title)) + "\n" + "作者:" +
                               repr(''.join(author)) + "\n" + "时间:" + repr(
                                   ''.join(data)) + "\n" + "内容:" + repr(
                                       buffer.strip()) + "\n\n")
                    buffer = ''


def getRes(word):
    # path 父目录, dirs 所有文件夹, files所有文件名
    # 元组的速度会快一些, 占用内存小
    files = []
    pattern = re.compile(r'[\s\S]*{word}[\s\S]*$'.format(word=word.strip()))
    for (__path, dirs,
         __files) in os.walk("/home/wutbio006/hey/dataset/soybean"):
        for _dir in dirs:
            for (_path, _dirs, _files) in os.walk(__path + "/" + _dir):
                for file in _files:
                    if file.endswith(".nxml"):
                        files.append(_dir + "/" + file)
    res = tuple(line for line in getLine(files, pattern, word))
    if res:
        try:
            with open(
                    "/home/wutbio006/hey/dataset/soyResult/" + word + ".txt",
                    "w",
                    encoding="utf8") as f:
                f.write(''.join(res))
        except IOError:
            print(word.replace(' ', '_') + ".txt读入: " + ''.join(res) + " 出错")
        del res


if __name__ == '__main__':
    need_words = tuple(word for word in make_word())
    pool = Pool()
    pool.map(getRes, need_words)
    pool.close()
    pool.join()
