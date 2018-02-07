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
    
    summary["path"]  # 为单文件路径
    summary["file_name"]  # 为单文件名
    summary["no_dot_file_name"]  # 为无后缀文件名
    
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
    
    summary['15067400']['path']  # 这是此文章的全路径
    summary['15067400']['file_name']  # 这是此文章的文件名
    summary['15067400']['no_dot_file_name']  # 这是此文章无后缀文件名

"""
from wrappers import MultiDict
import os


class OneFilePubmud(dict):
    def __init__(self, path, save_file_name=False):
        """
        初始化一个文件成一个OnedFilePubmud类
        :param path: Pubmud文件的绝对路径
        """

        if isinstance(path, OneFilePubmud):
            dict.__init__(self, ((k, l) for k, l in path.items()))
        elif isinstance(path, dict):
            dict.__init__(self, path)

        elif isinstance(path, str):
            if not os.path.isfile(path):
                raise FileNotFoundError("该路径不存在文件!")

            file_name = path.split("/")[-1]
            no_dot_file_name = ''.join(file_name.split(".")[:-1])

            _temp = MultiDict()
            try:
                with open(path, "r", encoding="utf8") as f:
                    for _line in f.readlines():
                        try:
                            key, value = _line.strip().split(":", 1)
                        except ValueError:
                            key = None
                        if key:
                            _temp.add(key, value)
                        elif _line == "\n" and _temp:

                            if save_file_name:  # 如果是处理多文件, 添加此属性
                                _temp.add("path", path)
                                _temp.add("file_name", file_name)
                                _temp.add("no_dot_file_name", no_dot_file_name)
                            pmid_key = _temp.get("PMID")

                            # 如果pmcid存在, 说明是有正文的, 但是正文也是以"内容"为关键字, 有摘要的才是以"正文"为关键字
                            pmc = _temp.get("PMCID", None)
                            if pmc:
                                content = _temp.get("正文")
                                if not content:
                                    _content_ = _temp.poplist("内容")
                                    _temp.add("正文", _content_)

                            if pmid_key:  # 没有pmid号的都不要
                                pmid_key = pmid_key[0].strip().split()[0]  # 这里是为了得到纯数字字符串
                                self[pmid_key] = _temp
                            _temp = MultiDict()
            except IOError:
                raise IOError("该文件不可读")

            if not save_file_name:  # 如果父类调用来处理多文件, 不应该添加此属性
                self["path"] = path
                self["file_name"] = file_name
                self["no_dot_file_name"] = no_dot_file_name

        else:
            raise TypeError("初始化参数确保是以下之一"
                            "1. 文件路径字符串类型"
                            "2. OneFilePubmud类型"
                            "3. dict类型")
        
    def yield_element(self, pmids, element="标题", need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
            pmids: list, tuple, set, str
            return: list
        """
        if element == "摘要":  # 保持接口正确
            element = "内容"
        if isinstance(pmids, (list, tuple, set)):
            _error = {}
            _pmid = []
            for pmid in pmids:
                res = self.get(pmid)
                if res and pmid not in _pmid:
                    _res = res.get(element)
                    if _res:
                        if need_pmid:
                            _res = pmid + ": " + ''.join(_res)
                        yield _res
                    else:
                        _value = _error.get(pmid)
                        if _value:
                            _error["Error: " + pmid][0] += 1
                            _error["Error: " + pmid].append("该文章没有" + element)
                        else:
                            _error["Error: " + pmid] = [0, "该文章没有" + element]
                        print("Error: " + pmid)
                        print(_error["Error: " + pmid])
                        yield "Error: " + pmid
                else:
                    _value = _error.get(pmid)
                    if _value:
                        _error["Error: " + pmid][0] += 1
                    elif res:
                        _error["Error: " + pmid] = [1]
                    else:
                        _error["Error: " + pmid] = [0, "没有该文章"]
                    print("Error: " + pmid)
                    print(_error["Error: " + pmid])
                    yield "Error: " + pmid
                _pmid.append(pmid)
        elif isinstance(pmids, str):
            res = self.get(pmids)
            if res:
                _res = res.get(element)
                if _res:
                    if need_pmid:
                        _res = pmids + ": " + ''.join(_res)
                    yield _res
                else:
                    raise AttributeError("该文章没有" + element)
            else:
                raise AttributeError("没有该PMID的文章")
        else:
            raise TypeError("PMID类型错误! 确保是字符串")
    
    def yield_content(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        :param pmids: 
        :return: 
        """
        return self.yield_element(pmids, "正文", need_pmid)

    def yield_summary(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
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
        tem = []
        for elem in self.yield_element(pmids, "正文", need_pmid):
            tem.append(''.join(elem))
        return tem

    def get_summary(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        tem = []
        for elem in self.yield_element(pmids, "摘要", need_pmid):
            tem.append(''.join(elem))
        return tem

    def get_title(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        tem = []
        for elem in self.yield_element(pmids, "标题", need_pmid):
            tem.append(''.join(elem))
        return tem

    def get_pmc(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        tem = []
        for elem in self.yield_element(pmids, "PMCID", need_pmid):
            tem.append(''.join(elem))
        return tem

    def get_author(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        tem = []
        for elem in self.yield_element(pmids, "作者", need_pmid):
            tem.append(''.join(elem))
        return tem

    def get_time(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        tem = []
        for elem in self.yield_element(pmids, "时间", need_pmid):
            tem.append(''.join(elem))
        return tem

    def get_journal(self, pmids, need_pmid=False):
        """
        若传参为list或tuple或set
        则打印的错误信息是一个字典, key为PMID
        value是一个列表, 列表第一个元素代表重复的次数
        """
        tem = []
        for elem in self.yield_element(pmids, "期刊", need_pmid):
            tem.append(''.join(elem))
        return tem

    def copy(self):
        return self.__class__(self)


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
                    _tem = OneFilePubmud(path+"/"+file, True)
                    self.update(_tem)
        else:
            raise TypeError("初始化参数确保是以下之一"
                            "1. 文件夹路径字符串类型"
                            "2. OneFilePubmud类型"
                            "3. MultiFilePubmud类型"
                            "4. dict类型")
