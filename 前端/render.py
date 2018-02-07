# coding: utf-8
from templite import Templite
import os


class Render(object):
    def __init__(self, html, html2, my_dict, path):
        """
        摘要文件的名字为 大类_性状.txt ,这个类批量生成HTML文件
        模板需要存放在templites中, 渲染的文件全在HTML文件夹中
        :param html: 详情页模板名
        :param html2: 主页模板名
        :param my_dict: 摘要关键字的字典, key为摘要中关键字, value为模板中变量名
        :param path: 摘要的路径
        """
        self.path = path
        self.files = os.listdir(path)
        self.my_dict = my_dict
        self.genge = []
        self.loc = os.getcwd()

        with open(
                self.loc + "\\templites\\" + html, "r", encoding="utf8") as f:
            self.tem = Templite(f.read())

        with open(
                self.loc + "\\templites\\" + html2, "r",
                encoding="utf8") as fin:
            self.tem2 = Templite(fin.read())

    def __trans(self, line):
        """
        关键字替换函数
        :param line: 具有关键字的一行
        :return: 替换结果
        """
        _str1 = line.replace("关键字$", "<span class=\"trait\">")
        _str2 = _str1.replace("$关键字", "</span>")
        _str3 = _str2.replace("基因$", "<span class=\"gene\">")
        _str4 = _str3.replace("$基因", "</span>")
        return _str4

    def __getArticle(self, lines):
        """
        返回一篇文章的结果, 接收一篇文章的列表
        :param lines: 一篇文章的列表行
        :return: 一篇文章的结果
        """
        article = dict()
        my_con = []
        my_all = []
        _main = ''
        _begin = True
        for line in lines:
            if _begin and line.startswith("正文"):
                _main = line.split(":", 1)[1].strip()
                _begin = False
            elif line.startswith("内容") and _main != '':
                if _main[:50] == line.split(":", 1)[1].strip()[:50]:
                    article["main"].pop(0)
            for k in self.my_dict.keys():
                if line.startswith(k):
                    cstring = line.split(":", 1)[1].strip()
                    if k == "标题":
                        cstring = self.__trans(cstring)
                    elif k == "内容":
                        my_con.append(self.__trans(cstring))
                        cstring = my_con
                    elif k == "正文":
                        my_all.append(self.__trans(cstring))
                        cstring = my_all
                    article[self.my_dict[k]] = cstring
                    break
        for key in self.my_dict.values():
            if key not in article.keys():
                article[key] = "未知"

        if article["content"] == "未知":
            article["content"] = ["未知"]
        if article["main"] != "未知":
            article["if_full"] = False
            article["if_summ"] = False
            article["if_all"] = True
        elif article["pmcid"] != "未知":
            article["if_full"] = True
            article["if_summ"] = False
            article["if_all"] = False
        else:
            article["if_full"] = False
            article["if_all"] = False
            article["if_summ"] = True
        return article

    def __getRes(self, file):
        """
        处理全部文章
        :param file: 一个性状的文件名
        """
        with open(self.path + "\\" + file, "r", encoding="utf8") as fin:
            _content = []
            for line in fin.readlines():
                _content.append(line)
                # if line == "\n" and len(_content) > 1:
                #     self.genge.append(self.__getArticle(_content))
                #     _content.clear()
            if len(_content) > 1:
                self.genge.append(self.__getArticle(_content))
                _content.clear()

    def __render(self, path, context):
        """
        渲染一个性状的函数
        :param path: 文件路径
        :param content: 上下文
        """
        _text1 = self.tem.render(context)

        with open(path, "w", encoding="utf8") as f:
            f.write(_text1)

    def __render_index(self, length):
        _xings = dict()
        _xing = []
        Res = []
        _lei = ''
        for file in self.files:
            _articles = dict()
            # _name = file.split("_")[1][:-4].strip()
            _name = file.split(".", 1)[0]
            lei = file.split("_")[0]
            if lei != _lei and _lei != '':
                _xings.update({"xing": _xing, "lei": _lei})
                Res.append(_xings)
                _xing = []
                _xings = dict()
            _lei = lei
            _articles.update({"name": _name})
            _articles.update({"url": _name + ".html"})
            _articles.update({"num": length[_name]})
            _xing.append(_articles)
        _xings.update({"xing": _xing, "lei": _lei})
        Res.append(_xings)

        _text2 = self.tem2.render({
            "Res": Res,
        })

        with open(self.loc + "\\index.html", "w", encoding="utf8") as fout:
            fout.write(_text2)

    def render(self):
        """
        调用渲染的接口
        """
        _length = dict()
        for file in self.files:
            # name = file.split("_")[1][:-4].strip()
            name = file.split(".", 1)[0]
            self.__getRes(file)
            _length.update({name: len(self.genge)})
            self.__render(self.loc + "\\HTML\\" + name + ".html", {
                "name": name,
                "genge": self.genge,
            })
            self.genge.clear()

        self.__render_index(_length)
