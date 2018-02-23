## 这里是详细的说明及例子

工具地址在[这里](https://github.com/qq2310091880/Pubmed/tree/master/pubmed "Pubmud工具")

```py
from pubmed import OneFilePubmud, MultiFilePubmud
```

<!-- more -->

原生Pubmed的Abstract摘要文件的路径

```py
init_path = "C:/Users/Administrator/Desktop/摘要/高产_100-seed weight.txt"
```
很多Pubmed摘要文件的文件夹路径

```py
path = "C:/Users/Administrator/Desktop/摘要"
```

以下是例子, text_root和root就是可操作的对象了

```py
text_root = OneFilePubmud(init_path)
root = MultiFilePubmud(path)
```

试试查看text_root的路径信息

```py
path = text_root.path  # 路径
file_name = text_root.file_name  # 文件名
no_dot_file_name = text_root.no_dot_file_name  # 无后缀文件名
```
这些信息在root中可没有, 因为root是包含很多文件的, 不过在root中, 每篇文章都有自己的路径键值

```py
path1 = root["28828506"].path
file_name1 = root["28828506"].file_name
no_dot_file_name1 = root["28828506"].no_dot_file_name
```
如果你的文件名不是标准的.txt文件, 可能上面的调用就会出错, 比如他们也许没有后缀文件名属性


### 接下来的操作绝大部分text_root和root都适用, 有例外会特别说明

下面是为了得到一篇文章的全部属性

```py
all_elements = text_root["28828506"]
```

下面是得到一篇文章的特定属性

```py
time = text_root["28828506"]["时间"]
```
也可以用这个函数

```py
text_root.get_value("28828506", "时间")  # 这个函数只能支持'主键'加'属性'参数调用
text_root.get_element("28828506", "时间")  # 这个函数则更加强大!
```

当然get_element函数不止这么简单, 例如下面是得到两篇文章的'时间'和'PMID'属性

```py
text_root.get_element(["28828506", "28363587"], ["时间", "PMID"])
```
get_element函数可以接收两个list或set或tuple, 或者参数只是简单的字符串也OK

下面是得到两篇文章的时间属性, 不过要将主键PMID号一同返回, 即得到 '{PMID}: {时间}'这样的格式

```py
text_root.get_element(["28828506", "28363587"], ["时间"], True)
```
这个功能可能在某些情况会有用¬_¬


下面是yield出某几篇文章的'时间','PMID'属性

```py
text_root.yield_element(["28828506", "28363587"], ["时间", "PMID"])
```
yield_element与get_element用法基本一致, 只是yield_element函数是一个生成器

顺便一提, get_element函数内部也是调用的yield_element函数


下面是得到所有文章的'时间'属性

```py
text_root.get_all('时间')
```
得到所有文章的'时间'和'PMID'属性

```py
text_root.get_all(['时间', 'PMID'])
```
同样有一个yield所有文章的属性的生成器函数

```py
text_root.yield_all('时间')
text_root.yield_all(['时间', 'PMID'])
```

### 基础的Article类(文章类)

```py
from pubmed import Article
```

Article类是一篇文章的基础类, 它相当于一个特殊的字典, 一般不会对这个类进行直接操作

不过你可能会自己想构造一个Article类, 也许你通过字典构造会简单点

```py
article = {"PMID": "12345", "时间": "2018 5 5", "作者": "aiyane", "摘要": "这是摘要内容"}
article = Article(article)
```
或者你通过上面的类来得到它

```py
article1 = text_root["28828506"]
```

你可以增加属性

```py
article.add("PMCID", "12345")
article.update({"住址": "xxx", "信息": "xxxx"})
```

你可以得到属性

```py
article.get("PMID")
```
这个类的操作是基于wrappers.py文件的MultiDict类, 它是MultiDict的子类, 也就具备MultiDict的全部方法

方法很多就不具体写了, 每一个方法在wrappers.py上都有输入输出的注释, 可以自己查看.


你可以将新增的文章加入到我们上面的OneFilePubmud, MultiFilePubmud的实例中

```py
text_root.save_article(article)
```
这个函数会自动将'PMID'当作主键, 如果没有PMID, 则将'PMCID'当作主键, 如果都没有则添加失败

顺便一说, 如果PMID在里面已经存在了, 会直接覆盖之前的文章, 不过会抛出一个警告

当然你会想自己定义一个主键, 下面函数支持你自己定义主键添加文章

```py
text_root.add_article("001", article)
```

### 辅助函数

```py
from pubmed import deal_line
```

你也许并不想得Pubmed文章的什么信息, 你只是想要将Pubmed下载的文章里那麻烦的断行合并

并且每一块的信息你都想标注它具体是什么信息, 那么这个辅助函数将会帮到你

```py
text = []
for line in deal_line(init_path):  # init_path是文件的路径
    text.append(line)
print(''.join(text))
```

deal_line是一个生成器, 它会一行行解析你的文件, 并且标注这一行的信息再一行行返回给你

以下是返回的一行的例子

  时间: 2018 7 18

  作者: Aiyane

  摘要: xxxxxxxxx

  PMID: 12345

另外每一篇文章的分界点它会返回一个空的'\n'来区分


听起来不错, 不过你可能很讨厌它给你标注行头信息, 你就想得到单纯的没有断行的文本

那下面的辅助函数就是为了这而存在的

```py
from pubmed import init_txt
text = []
for line in init_txt(init_path):  # init_path是文件路径
    text.append(line)
print(''.join(text))
```
现在你会发现断行已经不存在了, 而且已经没有了令你讨厌的标注信息, 就是单纯的PubMed摘要信息!!

也许你想要制作一个html页面来展示一篇文章

```py
from pubmed import make_summary, make_file
html = make_summary(article)
```
make_summary这个函数接收两个参数, 第一个是Article类的实例, 第二个是你写的页面模板, 如果你没有写第二个参数

默认是pubmed/templite/summary.model, 返会的就是html的具体内容

```py
make_file(html, path)  # 这里path是某个文件路径
```
make_file函数就是接收内容和文件路径来创建这个文件, 相当于以下
```py
with open(path, "w", encoding="utf8") as f:
	f.write(html)
```
如果是你自己的创建的Article类的实例article, 很可能这个实例没有路径的属性, 你可以通过以下函数添加路径属性

```py
from pubmed import add_path_info_to_article
add_path_info_to_article(path, article)  # 这里的path是路径, article是Article类实例
```
这样你的article会有path(路径), file_name(文件名), no_dot_file_name(无后缀文件名)三个属性

### 其他~~正在建设~~(已完成)的功能

也许你想要将你的文章变成可展示的页面, 你可以在页面上浏览...比如摘要之类的, 最好将全部文章列一张表格

魔法出现了, 你只需要调用这个函数

```py
text_root.make_pages(make_html=True)
```
上面的函数会为你的text_root(也就是OneFilePubmud或MultiFilePubmud对象的实例)创建页面

在你的当前目录下, 会出现一个index.html, 也会多出一个HTML文件夹, 试试打开你的index.html

你需要查看具体信息的时候可以点击里面的'摘要'链接, 它指向HTML中的文件, 你会看到你想要的.


当然这一部分还有很多可以扩展的功能, 比如我并不希望生成庞大数量的HTML文件, 而是创建本例服务器

~~这样我们访问某个url时才会生成某个页面, 听上去很好, 我接下来准备将它实现~~(已实现)

当需要创建本地服务器是还是调用

```py
text_root.make_pages()
```

即可, 默认make_html参数为False, 即不生成html, 而是创建服务器, 打开http://127.0.0.1:8080/ 那么你就可以看到主页列表了.

这里的服务器端, 用的是我写另一个小玩具["Jay"](https://github.com/qq2310091880/Jay "Jay").