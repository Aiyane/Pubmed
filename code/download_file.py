# coding: utf-8
import os
import re
import shutil
from multiprocessing import Pool


def initId():
    with open("/home/wutbio006/hey/dataset/need_pmid.txt", "r", encoding="utf8") as fin:
        for line in fin.readlines():
            yield line.strip()

need_words = tuple(word for word in initId())


def getFile(dir):
    xml_file = ''
    pdf_file = ''
    for (_path, _dirs, _files) in os.walk("/home/wutbio006/hey/dataset/soybean/"+dir):
        for file in _files:
            if file.endswith(".nxml"):
                xml_file = file
            elif file.endswith(".pdf"):
                pdf_file = file
        getLine(xml_file, _path, pdf_file)


def init_paper(text):
    context = re.split(r'(?s)(<.*?>)', text)
    return context


def getLine(file, path, pdf_file):
    Copy = False
    with open(path+"/"+file, "r", encoding="utf8") as fin:
        context = init_paper(fin.read())
        start_id = False
        for line in context:
            if line.startswith('<article-id pub-id-type="pmid">'):
                start_id = True
                continue
            elif start_id:
                if line.startswith("</article-id>"):
                    break
                elif not line.startswith("<"):
                    line = line.strip()
                    if line in need_words:
                        Copy = True
    if Copy:
        shutil.copyfile(path+"/"+pdf_file, "/home/wutbio006/hey/dataset/need_pdf_file/"+file)


if __name__ == '__main__':
    pool = Pool()
    for (path, dirs, files) in os.walk("/home/wutbio006/hey/dataset/soybean"):
        pool.map(getFile, dirs)
    pool.close()
    pool.join()