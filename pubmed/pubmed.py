#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pubmed.wrappers import MultiDict
import os
from pubmed.init_txt import deal_line
import warnings
from pubmed.templite import Templite
from pubmed.serving import Jay, render_template_by_template
from cgi import escape
import re
from pubmed.nxml_token import nxml_deal


class Article(MultiDict):

    _has_keys = False

    def _find_keys(self, res):
        """
        这个方法是为了给文章标注关键词, 用html标签来标注出来
        :res: 处理的字符串
        return: 返回处理完毕字符串
        """
        for _key in self._keys:
            if self._ignore:
                keys = re.findall(re.escape(_key), res, re.I)
            else:
                keys = re.findall(re.escape(_key), res)
            keys = set(keys)
            for key in keys:
                res = res.replace(
                    key, '<span class="trait">' + key + '</span>')
        if hasattr(self, '_values'):
            for _value in self._values:
                if self._ignore:
                    keys = re.findall(re.escape(_value), res, re.I)
                else:
                    keys = re.findall(re.escape(_value), res)
                keys = set(keys)
                for key in keys:
                    res = res.replace(
                        key, '<span class="gene">' + key + '</span>')
        return res

    def add_keys(self, keys, values=None, ignore=False):
        """
        增加标注单词的方法, 秩序调用此方法, 之后在生成页面是关键词就是标注好的
        :keys: list, set, tuple 关键词
        :values: list, set, tuple 关键词
        :ignore: 是否忽略大小写
        """
        if not isinstance(keys, (list, tuple, set)):
            raise TypeError('参数必须为list, tuple, set之一!')
        self._keys = keys
        if values:
            self._values = values
        self._has_keys = True
        self._ignore = ignore

    def to_str(self, key):
        res = self.get(key)
        if res:
            if not self.nxml:
                res = escape('. '.join(res))
            else:
                res = '. '.join(res)
            if self._has_keys:
                res = self._find_keys(res)
            return res
        return ""

    def to_str_pmid(self):
        return self.to_str("PMID")

    def to_str_pmcid(self):
        return self.to_str("PMCID")

    def to_str_title(self):
        return self.to_str("标题")

    def to_str_summary(self):
        return self.to_str("摘要")

    def to_str_time(self):
        return self.to_str("时间")

    def to_str_home(self):
        return self.to_str("地址")

    def to_str_author(self):
        return self.to_str("作者")

    def to_str_other(self):
        return self.to_str("其他")

    def to_str_doi(self):
        return self.to_str("DOI")

    def to_str_msg(self):
        return self.to_str("信息")

    def to_str_content(self):
        return self.to_str("正文")


def add_path_info_to_article(file_path, article):
    """
    给文章增加路径属性
    :param file_path: 文件路径
    :param article: 文章, Article类型
    :retuen: 文章
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError("该%r文件不存在!" % file_path)
    if not isinstance(article, Article):
        raise TypeError("文章%r必须为Article类型" % article)

    if "/" in file_path:
        file_name = file_path.split("/")[-1]  # 文件名
    else:
        file_name = file_path.split("\\")[-1]

    no_dot_file_name = ''.join(file_name.split(".")[:-1])  # 无后缀文件名

    article.path = file_path
    article.file_name = file_name
    if "." in file_name:  # 如果有后缀增加无后缀文件名属性
        article.no_dot_file_name = no_dot_file_name
    return article


def get_key_value_by_line(line):
    """
    通过一行文字, 得到这行对应的key和value, 没有得到就返回None, None
    :param line: 一行文字
    :return: key和value
    """
    if not isinstance(line, str):
        raise TypeError("%r 必须是str类型" % line)

    if line.strip() == "" or ":" not in line:
        return None, None
    key, value = line.strip().split(":", 1)
    return key, value


class NotPrimaryException(AttributeError):
    """没有主键的错误"""
    pass


class OneFilePubmud(dict):
    def __init__(self, path, save_file_name=False):
        """
        一个Pubmed摘要文件的处理类
        :param path: 摘要文件
        :param save_file_name: 是否每篇文章都保存此文章的路径属性
        """
        if isinstance(path, OneFilePubmud):
            dict.__init__(self, ((k, l) for k, l in path.items()))
        elif isinstance(path, dict):
            dict.__init__(self, path)
        elif isinstance(path, str):
            if not os.path.isfile(path):
                raise FileNotFoundError("该路径%r不存在文件!" % path)
            self._init_deal_path(path, save_file_name)
            if not save_file_name:  # 如果父类调用来处理多文件, 不应该添加此属性
                self.path = path
                if "/" in path:
                    self.file_name = path.split("/")[-1]  # 文件名
                else:
                    self.file_name = path.split("\\")[-1]
                if "." in self.file_name:
                    self.no_dot_file_name = ''.join(
                        self.file_name.split(".")[:-1])  # 无后缀文件名
        else:
            raise TypeError("初始化参数确保是以下之一"
                            "1. 文件路径字符串类型"
                            "2. OneFilePubmud类型"
                            "3. dict类型")

    def _init_deal_path(self, path, save_file_name):
        """
        处理path路径下的文章初始化
        :param path: 文件路径
        :param save_file_name: 为布尔值
        """
        if not os.path.isfile(path):
            raise FileNotFoundError("该%r文件不存在!" % path)

        article = Article()
        is_nxml = False

        # 这里判断处理的是nxml还是普通的摘要txt文件
        if path.endswith('.nxml'):
            my_deal_line = nxml_deal
            is_nxml = True
        else:
            my_deal_line = deal_line

        # for line in lines:
        for line in my_deal_line(path):
            key, varlue = get_key_value_by_line(line)
            if key:
                article.add(key, varlue)
            elif article:
                if save_file_name:  # 如果是处理多文件, 添加额外的文件属性
                    article = add_path_info_to_article(path, article)
                    if is_nxml:
                        article.nxml = True
                    else:
                        article.nxml = False
                try:
                    self.save_article(article)
                except NotPrimaryException as msg:
                    warnings.warn("在" + path + "路径下,", msg)
                article = Article()

    def save_article(self, article):
        """
        保存文章, 默认用pmid为主键, pmid不存在用pmcid为主键, 都不存在就不保存
        :param article: Article类型
        """
        if not isinstance(article, Article):
            raise TypeError("保存文章出错, 文章%r必须为Article类型" % article)

        pmid_key = article.get("PMID")
        pmc = article.get("PMCID")

        # 如果pmcid存在, 说明是有正文的, 只有摘要的是没有pmcid的, 摘要是以"内容"为关键词
        # 麻烦的就是, 如果正文摘要都存在, 那么正文的关键词会是"正文"
        # 但是只有正文时, 正文的关键词是"内容", 与摘要一样了, 所以要把它改成正文
        # 这里相当的蛋疼, 就是因为最开始的关键词命名有问题, 现在一直在加这种莫名奇妙的补丁
        # if pmc:
        #     content = article.get("正文")
        #     if not content:
        #         _content_ = article.poplist("内容")
        #         article.add("正文", _content_)
        # =============================================================================

        if pmid_key:
            primary_key = pmid_key[0].strip().split()[0]  # 这里是为了得到纯数字字符串
            self.add_article(primary_key, article)
        elif pmc:
            primary_key = pmc[0].strip().split()[0]
            self.add_article(primary_key, article)
        else:
            raise NotPrimaryException("文章没有主键, 保存失败")

    def add_article(self, key, value):
        """
        增加PubMed文章的方法
        :param key: 主键
        :param value: 文章内容, 为Article类型
        """
        if not isinstance(value, Article):
            raise ValueError("确保值的类型为Article")
        if self.get(key):
            warnings.warn("原始文章的内容已被替换")
        self[key] = value

    def get_value(self, primary, key):
        """通过主键和key来获取key对应的value"""
        article = self.get(primary)
        if not article:
            warnings.warn("没有%r对应的文章" % primary)
        else:
            if isinstance(key, (list, tuple, set)):
                return [''.join(article.getlist(one)) for one in key]
            value = article.get(key)
            if value:
                return value[0]
            return ''

    def yield_all(self, element="标题"):
        """通过key,yield出所有文章的value"""
        for primary in self.keys():
            yield self.get_element(primary, element)

    def get_all(self, element="标题"):
        """通过key, 返回所有文章的value的list"""
        tem = []
        for value in self.yield_all(element):
            tem.append(value)
        return tem

    def yield_element(self, primarys, element="标题"):
        """
        生成器, 生成文章具体信息
        :param primarys: 主键, 可以是单个主键或者多个主键的list, tuple, set
        :param element: 需要获得的类型, 默认为"标题", 可以是多个类型的list, tuple, set
        :param need_pmid: 是否需要以PMID为前缀, bool型
        :return: 以列表形式返回
        """
        if not isinstance(primarys, (list, tuple, set)):
            primarys = [primarys]

        for primary in primarys:
            value = self.get_value(primary, element)
            if not value:
                warnings.warn("没有得到%r文章的%r属性" % (primary, element))
            # 如果需要主键信息
            if value:
                yield value

    def get_element(self, primarys, element="标题"):
        """
        :param primarys: 主键, 可以是单个主键或者多个主键的list, tuple, set
        :param element: 需要获得的类型, 默认为"标题", 可以是多个类型的list, tuple, set
        :param need_pmid: 是否需要以PMID为前缀, bool型
        :return: 一个结果列表
        """
        if not isinstance(primarys, (list, tuple, set)):
            primarys = [primarys]
        tem = []
        for value in self.yield_element(primarys, element):
            tem.append(value)
        if len(tem) == 1:
            tem = tem[0]
        return tem

    def yield_content(self, pmids):
        """实际调用yield_element, 但是第二个参数为"正文"
        """
        return self.yield_element(pmids, "正文")

    def yield_summary(self, pmids):
        """实际调用yield_element, 但是第二个参数为"摘要"
        """
        return self.yield_element(pmids, "摘要")

    def yield_title(self, pmids):
        """实际调用yield_element, 但是第二个参数为"标题"
        """
        return self.yield_element(pmids, "标题")

    def yield_pmc(self, pmids):
        """实际调用yield_element, 但是第二个参数为"PMCID"
        """
        return self.yield_element(pmids, "PMCID")

    def yield_author(self, pmids):
        """实际调用yield_element, 但是第二个参数为"作者"
        """
        return self.yield_element(pmids, "作者")

    def yield_time(self, pmids):
        """实际调用yield_element, 但是第二个参数为"时间"
        """
        return self.yield_element(pmids, "时间")

    def yield_journal(self, pmids):
        """实际调用yield_element, 但是第二个参数为"期刊"
        """
        return self.yield_element(pmids, "期刊")

    def get_content(self, pmids):
        """实际调用get_element, 但是第二个参数为"正文"
        """
        return self.get_element(pmids, "正文")

    def get_summary(self, pmids):
        """实际调用get_element, 但是第二个参数为"摘要"
        """
        return self.get_element(pmids, "摘要")

    def get_title(self, pmids):
        """实际调用get_element, 但是第二个参数为"标题"
        """
        return self.get_element(pmids, "标题")

    def get_pmc(self, pmids):
        """实际调用get_element, 但是第二个参数为"PMCID"
        """
        return self.get_element(pmids, "PMCID")

    def get_author(self, pmids):
        """实际调用get_element, 但是第二个参数为"作者"
        """
        return self.get_element(pmids, "作者")

    def get_time(self, pmids):
        """实际调用get_element, 但是第二个参数为"时间"
        """
        return self.get_element(pmids, "时间")

    def get_journal(self, pmids):
        """实际调用get_element, 但是第二个参数为"期刊"
        """
        return self.get_element(pmids, "期刊")

    def copy(self):
        """复制一个实例"""
        return self.__class__(self)

    def add_keys(self, article, keys, values=None, ignore=False):
        article.add_keys(keys, values, ignore)

    def yield_keys_values(self, keys, values=None, ignore=False):
        """
        生成器, 生成有关键词的文章的pmid-articel
        :keys: 关键词列表
        :values: 关键词列表
        :ignore: 是否忽略大小写
        """
        for key, article in self.items():
            self.add_keys(article, keys, values, ignore)
            content = article.get('摘要')
            title = article.get('标题')
            if content:
                content = escape(''.join(content))
            if title:
                title = escape(''.join(title))
            main_con = article.get('正文')
            if content or title or main_con:
                if content:
                    content = article._find_keys(content)
                    if '>' in content:
                        yield key, article
                        continue
                if title:
                    title = article._find_keys(title)
                    if '>' in title:
                        yield key, article
                        continue
                if main_con:
                    main_con = article._find_keys(main_con)
                    if '<span class=' in main_con:
                        yield key, article

    def make_summarys(self, summary_html=None, keys=None, values=None, ignore=False, filter_article=False):
        """创建自身实例文章的HTML, summary_html是模板的str, 默认找template/summary.model
        会在本地创建HTML文件夹, 实际是一个生成器, 返回主键和HTML内容的元组
        """
        if summary_html is None:
            summary_tem = create_template('summary.model')
        elif not isinstance(summary_html, str):
            raise TypeError("摘要模板类型必须是str")
        else:
            summary_tem = create_template(summary_html)

        if not os.path.exists(os.getcwd() + "/HTML"):
            os.mkdir(os.getcwd() + "/HTML")

        need_pmid = []
        if keys:
            if filter_article:
                self._need_pmid = []
                for key, article in self.yield_keys_values(keys, values, ignore):
                    self._need_pmid.append(key)
                    yield key, make_summary(article, summary_tem)
            else:
                for key, article in self.items():
                    self.add_keys(article, keys, values, ignore)
                    yield key, make_summary(article, summary_tem)
        else:
            for key, article in self.items():
                yield key, make_summary(article, summary_tem)
        if need_pmid:
            self._need_pmid = need_pmid

    def make_index(self, index_html=None, filter_article=False):
        """根据自身全部实例, 创建主页的HTML, 接收的参数是模板的str, 默认是/template/index.model
        返回主页的HTML内容
        """
        if index_html is None:
            index_tem = create_template('index.model')
        elif not isinstance(index_html, str):
            raise TypeError("主页模板类型必须是str")
        else:
            index_tem = create_template(index_html)

        if filter_article:
            articles = []
            for pmid in self._need_pmid:
                articles.append(self[pmid])
            index_txt = index_tem.render({
                "articles": articles
            })
        else:
            index_txt = index_tem.render({
                "articles": self.values()
            })
        return index_txt

    def make_pages(self, make_html=False, index_html=None,
                   summary_html=None, keys=None, values=None, ignore=False, filter_article=False):
        """
        根据自身实例, 创建html页面或者创建本地服务器, 以便在网页展示文章的信息
        默认模板为template/index.model(主页), template/summary.model(文章)
        :param summary_html: 文章模板str
        :param index_html: 主页模板str
        :param make_html: 是否生成html文件, bool值
        """
        if not make_html:
            return self.make_server(index_html=index_html, summary_html=summary_html, keys=keys,
                                    values=values, ignore=ignore, filter_article=filter_article)

        for key, article in self.make_summarys(summary_html, keys, values, ignore, filter_article):
            create_file(article, os.getcwd() + "/HTML/" + key + ".html")

        index_txt = self.make_index(index_html, filter_article=filter_article)
        create_file(index_txt, os.getcwd() + "/index.html")

    def load_static(self, app, path=None):
        """
        加载静态文件
        """
        @app.route(path)
        def index():
            with open(os.path.split(os.path.realpath(__file__))[0] + path) as fin:
                text = fin.read()
            return text

    def make_server(self, index_html=None, summary_html=None, content_html=None, keys=None,
                    values=None, ignore=False, filter_article=False):
        """创建本地服务器"""
        app = Jay()
        need_pmid = []
        self.load_static(app, "/js/jquery.js")

        index_html = create_index_html(index_html)
        summary_html = create_summary_html(summary_html)
        content_html = create_content_html(content_html)

        if keys:
            if filter_article:
                for key, article in self.yield_keys_values(keys, values, ignore):
                    need_pmid.append(key)
                    self.create_summary_content(
                        app, key, summary_html=summary_html, article=article, content_html=content_html)
            else:
                for key, article in self.items():
                    article = self[key]
                    self.add_keys(article, keys, values, ignore)
                    self.create_summary_content(
                        app, key, keys=keys, values=values, ignore=ignore,
                        summary_html=summary_html, content_html=content_html)
        else:
            for pmid in self.yield_all("PMID"):
                self.create_summary_content(app, pmid, keys=keys, values=values,
                                            ignore=ignore, summary_html=summary_html, content_html=content_html)
        if need_pmid:
            self._need_pmid = need_pmid
        self._make_index(app, need_pmid, filter_article, index_html=index_html)
        app.run()

    def create_summary_content(self, app, pmid, keys=None, values=None,
                               ignore=False, article=None, summary_html=None, content_html=None):
        self._make_detail(app, pmid, keys=keys, values=values, ignore=ignore,
                          article=article, summary_html=summary_html)
        self._make_detail(app, pmid, keys=keys, values=values, ignore=ignore,
                          article=article, content_html=content_html)

    def _make_index(self, app, need_pmid, filter_article, index_html):
        """注册主页
        """
        @app.route('/')
        def index():
            if filter_article:
                articles = []
                if need_pmid:
                    for pmid in need_pmid:
                        articles.append(self[''.join(pmid)])
            else:
                articles = self.values()
            return render_template_by_template(index_html, articles=articles)

    def _make_detail(self, app, pmid, summary_html=None, keys=None, values=None, ignore=False, article=None, content_html=None):
        """注册创建文章详情页
        """
        if content_html is not None:
            route = '/HTML/content/' + ''.join(pmid) + '.html'
        else:
            route = '/HTML/' + ''.join(pmid) + '.html'

        @app.route(route)
        def index():
            if article:
                if content_html:
                    return render_template_by_template(content_html, article=article)
                return render_template_by_template(summary_html, article=article)
            my_article = self[''.join(pmid)]
            if keys:
                my_article.add_keys(keys, values, ignore)
            if content_html:
                return render_template_by_template(content_html, article=my_article)
            return render_template_by_template(summary_html, article=my_article)


def create_index_html(index_html):
    if index_html is None:
        return create_template('index.model')
    return index_html


def create_summary_html(summary_html):
    if summary_html is None:
        return create_template('summary.model')
    return summary_html


def create_content_html(content_html):
    if content_html is None:
        return create_template('content.model')
    return content_html


def create_template(html_name):
    path = os.path.split(os.path.realpath(__file__))[
        0] + "/template/" + html_name
    if_exist = os.path.exists(path)
    if if_exist:
        try:
            with open(path, "rb") as fin:
                html = fin.read().decode("utf8")
            text = Templite(html)
        except IOError:
            raise
    return text


def make_summary(article, summary_tem):
    """
    生成一篇文章的HTML页面
    :param summary_html: 文章模板, 没有就默认为template下的summary.model
    :param article: Article类
    :param path: 完整输出路径, 没有就默认输出当前目录下的HTML文件夹中, 以PMID or PMCID为文件名
    """
    if not isinstance(article, Article):
        raise TypeError("文章类型必须是Article")

    summary_txt = summary_tem.render({
        "article": article
    })
    return summary_txt


def create_file(text, path):
    """根据内容和路径创建文件"""
    try:
        with open(path, "w", encoding="utf8") as fin:
            fin.write(text)
    except IOError:
        raise


class MultiFilePubmud(OneFilePubmud):
    def __init__(self, path):
        """
        初始化多个文件, 即该文件夹的Pubmed信息
        :param path: 文件夹的绝对路径
        """
        if isinstance(path, (OneFilePubmud, MultiFilePubmud)):
            dict.__init__(self, ((k, l) for k, l in path.items()))
        elif isinstance(path, dict):
            dict.__init__(self, path)
        elif isinstance(path, str):
            if not os.path.isdir(path):
                raise NotADirectoryError("没有发现此文件夹")
            all_files = os.listdir(path)
            for file in all_files:
                if file.endswith(".txt") or file.endswith('.nxml'):
                    _tem = OneFilePubmud(path + "/" + file, True)
                    self.update(_tem)
        else:
            raise TypeError("初始化参数确保是以下之一"
                            "1. 文件夹路径字符串类型"
                            "2. OneFilePubmud类型"
                            "3. MultiFilePubmud类型"
                            "4. dict类型")
