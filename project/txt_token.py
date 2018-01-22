# coding: utf-8
from types import GeneratorType
import re
__all__ = ['AllDoc', 'BlockToken', 'TimeToken', 'TitleToken', 'AuthorToken', 'Content', 'IdToken']


def tokenizer_line(lines):
    index = 0
    Next = False
    for line in lines:
        index += 1
        if Next:
            line = re.split(r'[\.\;]+', line)
            Next = False
            index -= 1
            yield TimeToken(line[1])
        elif line.split(".")[0].isdigit():
            line = re.split(r'[\.\;]+', line)
            try:
                yield TimeToken(line[2])
            except IndexError:
                Next = True
        elif line.find("PMID") != -1:
            line = line.split()
            for num in line:
                if num.isdigit():
                    yield IdToken(num)
                    break
            index = 0
            break
        elif index == 2:
            yield TitleToken(line)
        elif index == 3:
            if line.startswith("[") and line.endswith("]"):
                index -= 1
                continue
            yield AuthorToken(line)
        elif line.startswith("Author information"):
            continue
        else:
            yield Content(line)


def _tokenizer(lines, root=None):
    buffer = []
    for line in lines:
        if line == "\n":
            continue
        if line.split(".")[0].isdigit() and buffer:
            yield BlockToken(buffer)
            buffer.clear()
        buffer.append(line)
    if buffer:
        yield BlockToken(buffer)
        buffer.clear()


class BaseToken(object):
    def __init__(self, token, func):
        self._children = tuple(children for children in func(token) if children is not None)

    @property
    def children(self):
        if isinstance(self._children, GeneratorType):
            self._children = tuple(self._children)
        return self._children


class AllDoc(BaseToken):
    def __init__(self, lines):
        self._children = tuple(_tokenizer(lines, root=self))


class BlockToken(BaseToken):
    def __init__(self, lines):
        self._children = tuple(tokenizer_line(lines))


class TimeToken(BaseToken):
    def __init__(self, content):
        self.time = content


class TitleToken(BaseToken):
    def __init__(self, title):
        self.title = title


class AuthorToken(BaseToken):
    def __init__(self, message):
        self.author = message


class Content(BaseToken):
    def __init__(self, content):
        self.content = content


class IdToken(BaseToken):
    def __init__(self, ID):
        self.id = ID

# _token_type = [AllDoc, BlockToken, TimeToken, TitleToken, AuthorToken, Content, IdToken]
# with open("C:\\Users\\Administrator\\Desktop\\summary.txt", "r", encoding="utf8") as fin:
#     AST = AllDoc(fin)
#
# print(AST)
