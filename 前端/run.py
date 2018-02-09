# coding: utf-8
from render import Render
"""
在本地目录下建立一个templites文件夹用来存放模板html, 渲染时默认会寻找这个文件夹
在本地目录下建立一个HTML文件夹, 渲染结果默认输出在HTML文件夹中
运行后会在当前目录找到index.html即为主页

将path改成全部摘要的路径
将detail_model改成详情页模板名
将index_model改成主页模板名

my_dict为摘要的关键字与模板的变量名对照字典

"""

path = "C:\\Users\\Administrator\\Desktop\\fin_res3"
detail_model = 'abstract.html'
index_model = 'Document.html'

my_dict = {
    "时间": "time",
    "标题": "title",
    "内容": "content",
    "摘要": "content",
    "正文": "main",
    "作者": "author",
    "PMID": "pmid",
    "PMCID": "pmcid",
    "期刊": "jou",
}

temp = Render(detail_model, index_model, my_dict, path)
temp.render()
