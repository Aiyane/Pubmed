# coding: utf-8
from multiprocessing import Pool
import re
import my_token


def make_word():
    # 将性状全部存在need_words列表中, 并且去掉首尾空格, 全部转换成小写
    with open('C:\\Users\\Administrator\\Desktop\\deal\\need.txt', 'r', encoding="utf8") as fin:
        for line in fin.readlines():
            words = line.lower().strip()
            yield words


# IO操作才是拖慢时间的罪魁祸首!!
def getLine(tokens, pattern):
    if_yield = False
    for token in tokens.children:
        if isinstance(token, my_token.Content) and pattern.match(token.content.lower()):
            if_yield = True
            break
    return if_yield


def getRes(word):
    # path 父目录, dirs 所有文件夹, files所有文件名
    # 元组的速度会快一些, 占用内存小

    pattern = re.compile(r'.*{word}.*$'.format(word=word.strip()))
    with open("C:\\Users\\Administrator\\Desktop\\summary.txt", "r", encoding="utf8") as fin:
        AST = my_token.AllDoc(fin)
    for children in AST.children:
        if getLine(children, pattern):
            try:
                with open("D:\\code\\shuju\\111111\\" + word + ".txt", "a", encoding="utf8") as f:
                    for token in children.children:
                        if isinstance(token, my_token.TimeToken):
                            f.write("时间: "+str(token.time))
                        elif isinstance(token, my_token.AuthorToken):
                            f.write("作者: "+str(token.author))
                        elif isinstance(token, my_token.Content):
                            reg = re.compile(re.escape(word), re.IGNORECASE)
                            token.content = reg.sub("关键词>"+word+"<关键词", token.content)
                            gene_name = re.search(r'(Glyma\d{2}[Gg]\d+(\.\d*)?)', token.content)
                            if gene_name:
                                token.content = re.sub(r'(Glyma\d{2}[Gg]\d+(\.\d*)?)', "基因>" +
                                                       gene_name.group(1) + "<基因", token.content, re.IGNORECASE)
                            f.write("内容: "+str(token.content))
                        elif isinstance(token, my_token.IdToken):
                            f.write("PMID: "+str(token.id))
                        elif isinstance(token, my_token.TitleToken):
                            f.write("标题: "+str(token.title))
                    f.write("\n\n")
            except IOError:
                print(word + ".txt读入: " + token.__class__.__name__ + " 出错")


if __name__ == '__main__':
    need_words = tuple(word for word in make_word())
    pool = Pool()
    pool.map(getRes, need_words)
    pool.close()
    pool.join()
