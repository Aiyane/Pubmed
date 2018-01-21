# coding: utf-8
import requests
import re
from multiprocessing import Pool
global line


def getHTMLText(start_url):#进入最开始页面的函数
    try:

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Referer": start_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }

        r = requests.get(start_url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print(r.status_code)
        return r.text
    except:
        return "获取失败1"

def prasePage(html):#匹配url的函数
    try:
        plt = re.match(r'[\s\S]*href\=\"(\S*)\"\>PDF', html)
        print(plt.group(1))
        return plt.group(1)
    except:
        print("提取失败")
        with open("C:\\Users\\Administrator\\Desktop\\cuowu4.txt", 'a')as f1:
            f1.write(line)

def download(URL):#这个不用管，之前写的一个下载函数
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding": "gzip",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Referer": "http://www.example.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
        }
        r = requests.get(URL,heasers=headers,timeout=3)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        print("写入失败")

def callbackfunc(blocknum,blocksize,totalsize):#显示下载进度的函数
    percent = 100.0*blocknum*blocksize/totalsize
    if percent > 100:
        percent = 100
    print("%.2f%%"% percent)

def main(line):
    url = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
    start_url = url+line
    start_url = start_url.replace("\n", "")
    print(start_url)
    try:
        html = getHTMLText(start_url)
        URL = 'https://www.ncbi.nlm.nih.gov' + str(prasePage(html))
        print(URL)
        lastStr = URL.rsplit('/', 1)[1]


        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding": "gzip",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Referer": URL,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
        }
        r = requests.get(URL, headers=headers, timeout=3, stream=True)

        with open("D:\\goal\\gg\\"+line+".pdf", "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
    except:
        print("获取失败")
        with open("C:\\Users\\Administrator\\Desktop\\cuowu4.txt", 'a')as f1:
            f1.write(line)


def getPMC():
    with open("C:\\Users\\Administrator\\Desktop\\pmcid.txt", "r", encoding="utf8") as fin:
        for words in fin.readlines():
            yield words.split()[-1].strip()

if __name__ == '__main__':
    need_words = tuple(word for word in getPMC())
    pool = Pool()
    pool.map(main, need_words)
    pool.close()
    pool.join()
