# coding: utf-8
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
import os


def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content


# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s\%s' % (filepath, allDir))
        child = child.replace("\\", "\\\\")
        try:
            allDir = allDir.replace('.pdf', '')
            txt = readPDF(open(child, 'rb'))
            with open("C:\\Users\\Administrator\\Desktop\\txt1\\"+allDir+".txt", "w", encoding='utf-8') as f:
                f.write(txt)
        except:
            with open("C:\\Users\\Administrator\\Desktop\\notTran.txt", 'a')as f1:
                f1.write(allDir+"\n")

eachFile("C:\\Users\\Administrator\\Desktop\\goal")
