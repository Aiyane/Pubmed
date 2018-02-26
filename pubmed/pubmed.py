#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理的文件: 合并后的摘要, 即全文与摘要都在都处理了的, 在没有摘要只有全文的文章里, 关键字以内容开头
在有摘要有全文的文章里, 关键字以内容为摘要以正文为全文, 在只有摘要的文章里, 摘要以内容为关键字
目标: 构建摘要的树型结构使得以后可以当作基础数据结构直接调用解析

一个简单的应用例子:

    from getSummary import OneFilePubmud

    path = "C:/Users/Administrator/Desktop/摘要文件.txt"
    summary = OneFilePubmud(path)

    # 提供的方法, 这里的 "xxx" 可以替换成 "标题", "摘要", "时间", "作者", "期刊", "PMCID", "正文", 不填就默认为 "标题"
    summary.get_element('15067400', "xxx")  # 通过pmid得到元素,
    summary.get_element(['15067400', '15067400'], "xxx") # 通过list得到元素
    summary.get_element(('15067400', '15067400'), "xxx") # 通过tuple得到元素
    summary.get_element({'15067400', '15067401'}, "xxx") # 通过set得到元素

    summary.get_summary('15067400')  # 通过pmid获取摘要
    summary.get_summary(['15067400', '15067400'])  # 通过pmid列表获取摘要
    summary.get_summary(('15067400', '15067400'))  # 通过pmid集合获取摘要

    summary.get_content()  # 通过pmid获取正文(筛选出来的正文), 用法同摘要
    summart.get_pmc()  # 通过pmid获取pmcid, 用法同摘要
    summary.get_author()  # 通过pmid获取作者, 用法同摘要
    summary.get_title()  # 通过pmid获取标题, 用法同摘要
    summary.get_time()  # 通过pmid获取时间, 用法同摘要
    summary.get_journal()  # 通过pmid获取期刊, 用法同摘要
    # 以上函数都有第三个参数, 接收布尔值, 表明是否需要将"{pmid}: "作为开头一同返回, 即 key: value 格式返回

    summary['15067400']  # 显示一篇文章的全部信息

    summary['15067400']["内容"]  # 显示一篇文章的摘要
    summary['15067400']["时间"]  # 显示一篇文章的时间
    summary['15067400']["标题"]  # 显示一篇文章的标题
    summary['15067400']["正文"]  # 显示一篇文章的正文
    summary['15067400']["PMCID"]  # 显示一篇文章的PMCID
    summary['15067400']["期刊"]  # 显示一篇文章的期刊
    summary['15067400']["PMID"]  # 显示一篇文章的PMID
    summary['15067400']["作者"]  # 显示一篇文章的作者

    # 与上面类似的为有yield_element()方法, 区别是上述方法返回一个列表, 而yield开头的方法是一个生成器, 用于for循环,
    # 可以一个个的得到这些值而不是得到一个庞大的list占内存, 以下是用法, 第一个参数可接受list, tuple, set当然还有单个pmid字符串
    # 这里的 "xxx" 可以替换成 "标题", "摘要", "时间", "作者", "期刊", "PMCID", "正文", 不填就默认为 "标题"
    for title in summary.yield_element(['15067400', '15067401'], "xxx"):
        print(title)
    # 同理以下也是生成器
    summary.yield_content()
    summary.yield_time()
    summary.yield_journal()
    summary.yield_summary()
    summary.yield_pmc()
    summary.yield_author()
    summary.yield_title()

    summary.path  # 为单文件路径
    summary.file_name  # 为单文件名
    summary.no_dot_file_name  # 为无后缀文件名

    new_sum = OneFilePubmud(summary)  # 这样拷贝summary
    new_sum = OneFilePubmud.copy()  # 或者调用此方法

    # 当然把这个类当作普通的字典也完全可以
    my_dict = OneFilePubmud({"key": "value", "key2": "value2"})
    # 所以可以看出此类初始化参数类型可以是
    # 1. 文件路径字符串类型
    # 2. OneFilePubmud类型
    # 3. dict类型

MultiFilePubmud类的用法与OneFilePubmud的用法基本一致, 区别在于初始化的参数为
1. 文件夹路径字符串类型
2. OneFilePubmud类型
3. MultiFilePubmud类型
4. dict类型

另外MultiFilePubmud的实例没有 "path", "file_name", "no_dot_file_name" 三个key, 但是可以对每一篇文章查找这些key,
以下是例子:
    from getSummary import MultiFilePubmud

    path = "C:/Users/Administrator/Desktop/摘要文件夹"
    summary = MultiFilePubmud(path)

    summary['15067400'].path  # 这是此文章的全路径
    summary['15067400'].file_name  # 这是此文章的文件名
    summary['15067400'].no_dot_file_name  # 这是此文章无后缀文件名

"""
from pubmed.wrappers import MultiDict
import os
from pubmed.init_txt import deal_line
import warnings
from pubmed.templite import Templite
from pubmed.serving import Jay, render_template_by_template
from cgi import escape
import re


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
                res = res.replace(key, '<span class="trait">' + key + '</span>')
        if hasattr(self, '_values'):
            for _value in self._values:
                if self._ignore:
                    keys = re.findall(re.escape(_value), res, re.I)
                else:
                    keys = re.findall(re.escape(_value), res)
                keys = set(keys)
                for key in keys:
                    res = res.replace(key, '<span class="gene">' + key + '</span>')
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
            res = escape('. '.join(res))
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
        # for line in lines:
        for line in deal_line(path):
            key, varlue = get_key_value_by_line(line)
            if key:
                article.add(key, varlue)
            elif article:
                if save_file_name:  # 如果是处理多文件, 添加额外的文件属性
                    article = add_path_info_to_article(path, article)
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
                return [''.join(article.get(one)) for one in key]
            return article.get(key)[0]

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
            if content or title:
                if (content and '>' in article._find_keys(content)) or (title and '>' in article._find_keys(title)):
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
            return self.make_server(index_html=index_html, summary_html=summary_html, keys=keys, values=values, ignore=ignore, filter_article=filter_article)
        
        for key, article in self.make_summarys(summary_html, keys, values, ignore, filter_article):
            create_file(article, os.getcwd() + "/HTML/" + key + ".html")

        index_txt = self.make_index(index_html, filter_article=filter_article)
        create_file(index_txt, os.getcwd() + "/index.html")

    def make_server(self, index_html=None, summary_html=None, keys=None, values=None, ignore=False, filter_article=False):
        """创建本地服务器"""
        app = Jay()
        need_pmid = []

        if index_html is None:
            index_html = create_template('index.model')
        if summary_html is None:
            summary_html = create_template('summary.model')

        if keys:
            if filter_article:
                for key, article in self.yield_keys_values(keys, values, ignore):
                    need_pmid.append(key)
                    self._make_detail(app, key, summary_html=summary_html, article=article)
            else:
                for key, article in self.items():
                    article = self[key]
                    self.add_keys(article, keys, values, ignore)
                    self._make_detail(app, key, keys=keys, values=values, ignore=ignore, summary_html=summary_html)
        else:
            for pmid in self.yield_all("PMID"):
                self._make_detail(app, pmid, keys=keys, values=values, ignore=ignore, summary_html=summary_html)
        if need_pmid:
            self._need_pmid = need_pmid
        self._make_index(app, need_pmid, filter_article, index_html=index_html)
        app.run()

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


    def _make_detail(self, app, pmid, summary_html, keys=None, values=None, ignore=False, article=None):
        """注册创建文章详情页
        """
        @app.route('/HTML/' + ''.join(pmid) + '.html')
        def index():
            if article:
                return render_template_by_template(summary_html, article=article)
            my_article = self[''.join(pmid)]
            if keys:
                my_article.add_keys(keys, values, ignore)
            return render_template_by_template(summary_html, article=my_article)


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
                if file.endswith(".txt"):
                    _tem = OneFilePubmud(path + "/" + file, True)
                    self.update(_tem)
        else:
            raise TypeError("初始化参数确保是以下之一"
                            "1. 文件夹路径字符串类型"
                            "2. OneFilePubmud类型"
                            "3. MultiFilePubmud类型"
                            "4. dict类型")
