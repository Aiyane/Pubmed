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
    1. 在data.py中将all_xing_file改成所有性状的文件路径, 里面的性状是一行一个
    2. 在data.py中将all_gene_file改成所有基因的路径, 里面的基因是一行一个
    3. 在data.py中将input_path改成你的nxml文件根目录, 注意看上面注释!!! 其子目录的格式要求
    4. 在data.py中将output_path改成你的输出路径, 提示: 最好是空目录
    5. 在data.py中将需要删除的pmid添加到need_del_pmid集合中去
    6. 改完以后点击运行 run.py 即可
"""
from nxml_paser import getRes
import os
from data import output_path, input_path
from functools import partial
from multiprocessing import Pool


# for (path, dirs, files_name) in os.walk(input_path):
#     for dir in dirs:
#         getRes(path, dir, output_path)

if __name__ == '__main__':
    pool = Pool()
    for (path, dirs, files_name) in os.walk(input_path):
        getRes = partial(getRes, path=path, goal=output_path)
        pool.map(getRes, dirs)
    pool.close()
    pool.join()
