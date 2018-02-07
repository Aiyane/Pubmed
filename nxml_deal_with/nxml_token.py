# coding: utf-8
from types import GeneratorType


def _tokenizer(lines, root=None):
    fence = False
    pmc_close = True
    pmid_close = True
    jou_close = True
    time_close = True
    title_close = True
    author_close = True
    zai_close = True
    is_zai = True
    buffer = []
    for line in lines:
        if fence:
            if line.startswith('</abstract>'):
                yield ZaiToken(buffer)
                buffer.clear()
                fence = False
                is_zai = True
                continue
            elif line.startswith('</article-id>'):
                yield IDToken(buffer)
                buffer.clear()
                fence = False
                continue
            elif line.startswith('</journal-title>'):
                yield JouToken(buffer)
                buffer.clear()
                fence = False
                continue
            elif line.startswith('</article-title>'):
                yield TitleToken(buffer)
                buffer.clear()
                fence = False
                continue
            elif line.startswith('</date>'):
                yield TimeToken(buffer)
                buffer.clear()
                fence = False
                continue
            elif line.startswith('</contrib-group>'):
                yield AuthorToken(buffer)
                buffer.clear()
                fence = False
                continue
            elif is_zai and line.startswith('</p>'):
                yield ContentToken(buffer)
                buffer.clear()
                fence = False
                continue
            buffer.append(line)

        elif zai_close and line.startswith('<abstract>'):
            zai_close = False
            buffer.append("内容:")
            fence = True
            is_zai = False
        elif pmc_close and line.startswith('<article-id pub-id-type="pmc">'):
            buffer.append("PMCID:")
            pmc_close = False
            fence = True
        elif pmid_close and line.startswith('<article-id pub-id-type="pmid">'):
            buffer.append("PMID:")
            pmid_close = False
            fence = True
        elif jou_close and line.startswith('<journal-title>'):
            buffer.append("期刊:")
            jou_close = False
            fence = True
        elif title_close and line.startswith('<article-title>'):
            title_close = False
            buffer.append("标题:")
            fence = True
        elif time_close and line.startswith('<date date-type="accepted">'):
            time_close = False
            buffer.append("时间:")
            fence = True
        elif author_close and line.startswith('<contrib-group>'):
            author_close = False
            buffer.append("作者:")
            fence = True
        elif line.startswith('<p>'):
            fence = True


class AllDoc(object):
    def __init__(self, lines):
        self._kid = tuple(line for line in _tokenizer(lines, root=self))

    @property
    def kid(self):
        if isinstance(self._kid, GeneratorType):
            self._kid = tuple(self._kid)
        return self._kid
        

class IDToken(object):
    def __init__(self, lines):
        self.content = ' '.join(lines)
       

class JouToken(object):
    def __init__(self, lines):
        self.content = ' '.join(lines)
        
    
class TitleToken(object):
    def __init__(self, lines):
        self.content = ' '.join(lines)
    

class TimeToken(object):
    def __init__(self, lines):
        self.content = ' '.join(lines)
        
        
class AuthorToken(object):
    def __init__(self, lines):
        self.content = ' '.join(lines)
        

class ContentToken(object):
    def __init__(self, lines):
        content = ' '.join(lines)
        content = content.split(".")
        self.content = content


class ZaiToken(object):
    def __init__(self, lines):
        self.content = ' '.join(lines)

# if __name__ == '__main__':
#     import re, os
#     all_file = os.listdir("C:\\Users\\Administrator\\Desktop\\nxml全文")
#     for file in all_file:
#         zai = False
#         with open("C:\\Users\\Administrator\\Desktop\\nxml全文\\"+file, "r", encoding="utf8") as fin:
#             lines = re.split(r'(?s)(<.*?>)', fin.read())
#             AST = AllDoc(lines)
#         with open("C:\\Users\\Administrator\\Desktop\\nxml_res\\"+file, "w", encoding="utf8") as f:
#             for token in AST.kid:
#                 if isinstance(token, ZaiToken):
#                     f.write(token.content)
#                     zai = True
#         if not zai:
#             print(file)
