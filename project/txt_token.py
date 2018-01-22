# coding: utf-8
from types import GeneratorType
import re
__all__ = [
    'AllDoc', 'BlockToken', 'TimeToken', 'TitleToken', 'AuthorToken',
    'Content', 'IdToken'
]


def tokenizer_line(lines):
    index = 0
    info = False
    begin = False
    tem = ''
    title = False
    author = False

    for line in lines:
        if line != '\n':
            index += 1
        if not begin and line.split(".", 1)[0].isdigit():
            begin = True
            time = re.split(r",|\.|;|:", line)[2]
            yield TimeToken(time)
        elif not title and index == 2:
            title = True
            yield TitleToken(line.strip())
        elif not author and index == 3:
            author = True
            yield AuthorToken(line.strip())
        elif line.startswith("Author information"):
            info = True
        elif info:
            if line == '\n':
                info = False
                yield AuthorMessageToken(tem.strip())
                tem = ''
            else:
                tem = tem + line
        elif line.startswith("PMID:"):
            ID = line.split(":")[1].strip()
            begin = False
            yield IdToken(ID)
        elif line.startswith("PMCID") or line.startswith("DOI"):
            continue
        elif line != '\n':
            yield Content(line.strip())


def _tokenizer(root=None):
    with open(
            "C:\\Users\\Administrator\\Desktop\\处理后的摘要\\高产_yield.txt",
            "r",
            encoding="utf8") as f:
        buffer = []
        for line in f.readlines():
            buffer.append(line)
            if line.startswith("PMID"):
                yield BlockToken(buffer)
                buffer.clear()


class BaseToken(object):
    def __init__(self, token, func):
        self._kid = tuple(
            children for children in func(token) if children is not None)

    @property
    def children(self):
        if isinstance(self._kid, GeneratorType):
            self.kid = tuple(self._kid)
        return self.kid


class AllDoc(BaseToken):
    def __init__(self):
        self._kid = tuple(line for line in _tokenizer(root=self))


class BlockToken(BaseToken):
    def __init__(self, lines):
        self._kid = tuple(line for line in tokenizer_line(lines))


class TimeToken(BaseToken):
    def __init__(self, content):
        self.content = content


class TitleToken(BaseToken):
    def __init__(self, title):
        self.content = title


class AuthorToken(BaseToken):
    def __init__(self, message):
        self.content = message


class Content(BaseToken):
    def __init__(self, content):
        self.content = content


class IdToken(BaseToken):
    def __init__(self, ID):
        self.content = ID


class AuthorMessageToken(BaseToken):
    def __init__(self, message):
        self.content = message


# _token_type = [AllDoc, BlockToken, TimeToken, TitleToken, AuthorToken, Content, IdToken]
# AST = AllDoc()
# print(AST)
