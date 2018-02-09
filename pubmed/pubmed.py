# coding: utf-8
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
from wrappers import MultiDict
import os
from init_txt import deal_line
import warnings
from templite import Templite


class Article(MultiDict):
    
    def to_str(self, key):
        res = self.get(key)
        if res:
            return ''.join(res)
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
                    self.no_dot_file_name = ''.join(self.file_name.split(".")[:-1])  # 无后缀文件名
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
            return article.get(key)

    def yield_all(self, element="标题", need_pmid=False):
        if not isinstance(need_pmid, bool):
            raise TypeError("第二个参数必须为bool值")

        for primary in self.keys():
            yield self.get_element(primary, element, need_pmid)

    def get_all(self, element="标题", need_pmid=False):
        if not isinstance(need_pmid, bool):
            raise TypeError("第二个参数必须为bool值")

        tem = []
        for value in self.yield_all(element, need_pmid):
            tem.append('\n'.join(value))
        return tem

    def yield_element(self, primarys, element="标题", need_pmid=False):
        """
        生成器, 生成文章具体信息
        :param primarys: 主键, 可以是单个主键或者多个主键的list, tuple, set
        :param element: 需要获得的类型, 默认为"标题", 可以是多个类型的list, tuple, set
        :param need_pmid: 是否需要以PMID为前缀, bool型
        :return: 以列表形式返回
        """
        if not isinstance(need_pmid, bool):
            raise TypeError("need_pmid参数必须为bool型")
        if not isinstance(primarys, (list, tuple, set)):
            primarys = [primarys]

        for primary in primarys:
            value = self.get_value(primary, element)
            if not value:
                warnings.warn("没有得到%r文章的%r属性" % (primary, element))
            # 如果需要主键信息
            elif need_pmid:
                value = [primary + ": " + '\n'.join(value)]
            if value:
                yield value

    def get_element(self, primarys, element="标题", need_pmid=False):
        """
        :param primarys: 主键, 可以是单个主键或者多个主键的list, tuple, set
        :param element: 需要获得的类型, 默认为"标题", 可以是多个类型的list, tuple, set
        :param need_pmid: 是否需要以PMID为前缀, bool型
        :return: 一个结果列表
        """
        if not isinstance(need_pmid, bool):
            raise TypeError("need_pmid参数必须为bool型")
        if not isinstance(primarys, (list, tuple, set)):
            primarys = [primarys]
        tem = []
        for value in self.yield_element(primarys, element, need_pmid):
            tem.append('\n'.join(value))
        return tem

    def yield_content(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        :param need_pmid: 
        :param pmids: 
        :return: 
        """
        return self.yield_element(pmids, "正文", need_pmid)

    def yield_summary(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        :param need_pmid: 
        :param pmids: 
        :return: 
        """
        return self.yield_element(pmids, "摘要", need_pmid)

    def yield_title(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.yield_element(pmids, "标题", need_pmid)

    def yield_pmc(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.yield_element(pmids, "PMCID", need_pmid)

    def yield_author(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.yield_element(pmids, "作者", need_pmid)

    def yield_time(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.yield_element(pmids, "时间", need_pmid)

    def yield_journal(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.yield_element(pmids, "期刊", need_pmid)

    def get_content(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.get_element(pmids, "正文", need_pmid)

    def get_summary(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.get_element(pmids, "摘要", need_pmid)

    def get_title(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.get_element(pmids, "标题", need_pmid)

    def get_pmc(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.get_element(pmids, "PMCID", need_pmid)

    def get_author(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.get_element(pmids, "作者", need_pmid)

    def get_time(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.get_element(pmids, "时间", need_pmid)

    def get_journal(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        return self.get_element(pmids, "期刊", need_pmid)

    def copy(self):
        return self.__class__(self)

    def make_summarys(self, summary_html=None):
        if not isinstance(summary_html, str):
            raise TypeError("摘要模板类型必须是str")

        if not summary_html:
            try:
                with open(os.getcwd() + "/template/summary.model", "r", encoding="utf8") as fin:
                    summary_html = fin.read()
            except IOError:
                raise FileNotFoundError("模板丢失!")

        if not os.path.exists(os.getcwd() + "/HTML"):
            os.mkdir(os.getcwd() + "/HTML")

        for key, article in self.items():
            yield key, make_summary(article, summary_html)

    def make_index(self, index_html=None):
        if not isinstance(index_html, str):
            raise TypeError("主页模板类型必须是str")

        if not index_html:
            try:
                with open(os.getcwd() + "/template/index.model", "r", encoding="utf8") as fin:
                    index_html = fin.read()
            except IOError:
                raise FileNotFoundError("模板丢失!")

        index_tem = Templite(index_html)
        index_txt = index_tem.render({
            "articles": self.values()
        })
        return index_txt

    def make_pages(self, make_html=True):
        if not os.path.exists(os.getcwd() + "/template/index.model") \
                or not os.path.exists(os.getcwd() + "/template/summary.model"):
            raise FileNotFoundError("模板丢失!")

        with open(os.getcwd() + "/template/index.model", "r", encoding="utf8") as fin:
            index_html = fin.read()
        with open(os.getcwd() + "/template/summary.model", "r", encoding="utf8") as fin:
            summary_html = fin.read()

        index_txt = self.make_index(index_html)
        if make_html:
            for key, article in self.make_summarys(summary_html):
                create_file(article, os.getcwd() + "/HTML/" + key + ".html")
            create_file(index_txt, os.getcwd() + "/index.html")

    def server_summary(self, pmid):
        article = self.get(pmid)
        if article:
            pass


def make_summary(article, summary_html=None):
    """
    生成一篇文章的HTML页面
    :param summary_html: 文章模板, 没有就默认为template下的summary.model
    :param article: Article类
    :param path: 完整输出路径, 没有就默认输出当前目录下的HTML文件夹中, 以PMID or PMCID为文件名
    """
    if summary_html:
        if not isinstance(summary_html, str):
            raise TypeError("摘要模板类型必须是str")
    else:
        try:
            with open(os.getcwd() + "/template/summary.model", "r", encoding="utf8") as fin:
                summary_html = fin.read()
        except IOError:
            raise FileNotFoundError("模板丢失!")

    if not isinstance(article, Article):
        raise TypeError("文章类型必须是Article")
    summary_tem = Templite(summary_html)
    summary_txt = summary_tem.render({
        "article": article
    })

    # if not path:
    #     name = article.get("PMID")
    #     if not name:
    #         name = article.get("PMCID")
    #     if not name:
    #         warnings.warn("没有正确的输出路径")
    #         return
    #     if not os.path.exists(os.getcwd() + "/HTML"):
    #         os.mkdir(os.getcwd() + "/HTML")
    #     path = os.getcwd() + "HTML" + ''.join(name) + ".html"

    return summary_txt


def create_file(text, path):
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
