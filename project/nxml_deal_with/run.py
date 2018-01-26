# coding: utf-8
"""
此模块处理nxml格式的全文, 使用前将所有的nxml文件按照性状放入各个子文件夹, 例如

 xing
    |_高产_Branching
    |   |
    |   |_20661290.nxml
    |   |
    |   |_23977368.nxml
    |
    |_高产_Fertility
    |   |
    |   |_12033818.nxml
    |
    |_抗病虫_Aphis glycines
    |   |
    |   |_16222805.nxml
    |   |
    |   |_18190926.nxml
    |   |
    |   |_18419900.nxml
    |
    ...

其中, xing文件夹为根目录, 它的子目录的命名规范为 "大类性状_具体性状" ,在子目录下的nxml文件并没有命名格式的要求
最后输出为序列化的.txt文件, 其目录结构例如

  res
    |_高产_Branching.txt
    |
    |_高产_Fertility.txt
    |
    |_抗病虫_Aphis glycines
    |
    ...

运行说明:
    1. 将all_xing_file改成所有性状的文件路径, 里面的性状是一行一个
    2. 将all_gene_file改成所有基因的路径, 里面的基因是一行一个
    3. 将input_path改成你的nxml文件根目录, 注意看上面注释!!! 其子目录的格式要求
    4. 将output_path改成你的输出路径, 提示: 最好是空目录
    5. 将需要删除的pmid添加到need_del_pmid集合中去
    6. 改完以后点击运行即可
"""
from nxml_paser import getRes
import os

all_xing_file = "C:\\Users\\Administrator\\Desktop\\全部性状.txt"
all_gene_file = "C:\\Users\\Administrator\\Desktop\\基因处理\\geneprimary.set.txt"
input_path = "D:\\我的文档\\xing"
output_path = "D:\\我的文档\\res"
need_del_pmid = {'10947181', '29305230', '29287393', '27794206', '26601587', '18096944', '29293767', '29290449',
                 '28562076', '28938771', '28709434', '28496985', '28373120', '27822738', '27746355', '27718430'}

for (path, dirs, files_name) in os.walk(input_path):
    for dir in dirs:
        getRes(path, dir, output_path)
