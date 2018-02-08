# coding: utf-8


class _Missing(object):

    def __repr__(self):
        return 'no value'

    def __reduce__(self):
        return '_missing'

_missing = _Missing()


class TypeConversionDict(dict):
    """
    提供一个get方法, 于普通字典不同的是该get方法可以转换类型
    """
    def get(self, key, default=None, type=None):
        try:
            value = self[key]
            if type is not None:
                value = type(value)
        except (KeyError, ValueError):
            value = default
        return value


class MultiDict(TypeConversionDict):
    """
    构成一个复合字典, key与一般字典一样, value是一个list
    """
    KeyError = None

    def __init__(self, mapping=None):
        if isinstance(mapping, MultiDict):
            # 是MutiDict就复制一份
            dict.__init__(self, ((k, l[:]) for k, l in mapping.iterlists()))
        elif isinstance(mapping, dict):
            tmp = {}
            for key, value in mapping.items():
                if isinstance(value, (tuple, list)):
                    value = list(value)
                else:
                    value = [value]
                tmp[key] = value
            dict.__init__(self, tmp)
        else:
            # 类似于[("key", "value"), ("key2", "value2")]这种
            tmp = {}
            for key, value in mapping or ():
                # setdefault查找键, 键不存在时设默认值
                tmp.setdefault(key, []).append(value)
            dict.__init__(self, tmp)

    def __getstate__(self):
        """{[("key1", [1,2,3]), ("key2", [4,5])]}
        存储pickle的关键信息
        """
        return dict(self.lists())

    def __setstate__(self, state):
        """pickle解压
        在__getstate__中存的字典在实例化
        """
        dict.clear(self)
        dict.update(self, state)

    def __iter__(self):
        # 迭代就是迭代键
        return self.keys()

    def __setitem__(self, key, value):
        """通过 A["key"] = value 来设值, 直接设成list"""
        dict.__setitem__(self, key, [value])

    def getlist(self, key, type=None):
        """通过key获取value的list, 但是可以转换元素类型"""
        try:
            rv = dict.__getitem__(self, key)
        except KeyError:
            return []
        if type is None:
            return list(rv)
        result = []
        for item in rv:
            try:
                result.append(type(item))
            except ValueError:
                pass
        return result

    def setlist(self, key, new_list):
        """
        >>> d = MultiDict()
        >>> d.setlist('foo', ['1', '2'])
        >>> d['foo']
        '1'
        >>> d.getlist('foo')
        """
        dict.__setitem__(self, key, list(new_list))

    def setdefault(self, k, default=None):
        if k not in self:
            self[k] = default
        else:
            default = self[k]
        return default

    def setlistdefault(self, key, default_list=None):
        """
        >>> d = MultiDict({"foo": 1})
        >>> d.setlistdefault("foo").extend([2, 3])
        >>> d.getlist("foo")
        [1, 2, 3]
        """
        if key not in self:
            default_list = list(default_list or ())
            dict.__setitem__(self, key, default_list)
        else:
            default_list = dict.__getitem__(self, key)
        return default_list

    def items(self, multi=False):
        """
        { "key1": [1, 2, 3], "key2": [4, 5] }
        如果multi是False
            返回 [("key1", 1), ("key2", 4)]
        如果multi是True
            返回 [("key1", 1), ("key1", 2), ("key1", 3), ("key2", 4), ("key2", 5)]
        """
        return list(self.iteritems(multi))

    def values(self):
        return [self[key] for key in self.keys()]

    def iterlistvalues(self):
        """
        {"key1": (1, 2, 3), "key2": (4, 5)}
        返回 [1,2,3], [4,5]
        """
        for values in dict.values(self):
            yield list(values)

    def listvalues(self):
        """
        >>> d = MultiDict({"foo": [1, 2, 3]})
        >>> zip(d.keys(), d.listvalues()) == d.lists()
        True
        {"key1": (1, 2, 3), "key2": (4, 5)}
        返回 [[1,2,3], [4,5]]
        """
        return list(self.iterlistvalues())

    def lists(self):
        """[("key1", [1,2,3]), ("key2", [4,5])]"""
        return list(self.iterlists())

    def add(self, key, value):
        dict.setdefault(self, key, []).append(value)

    def iterlists(self):
        """
        {"key1": (1, 2, 3), "key2": (4, 5)}
        返回 ("key1", [1,2,3]), ("key2", [4,5])
        """
        for key, values in dict.items(self):
            yield key, list(values)

    def iteritems(self, multi=False):
        """
        { "key1": [1, 2, 3], "key2": [4, 5] }
        如果multi是False
            返回 ("key1", 1), ("key2", 4)
        如果multi是True
            返回 ("key1", 1), ("key1", 2), ("key1", 3), ("key2", 4), ("key2", 5)
        """
        for key, values in dict.items(self):
            if multi:
                for value in values:
                    yield key, value
            else:
                yield key, values[0]

    def copy(self):
        return self.__class__(self)

    def to_dict(self, flat=True):
        """
        { "key1": [1, 2, 3], "key2": [4, 5] }
        返回 { "key1": 1, "key2": 4 }
        """
        if flat:
            return dict(self.iteritems())
        return dict(self.lists())

    def update(self, other_dict):
        # 支持上传MutiDict
        for key, value in iter_multi_items(other_dict):
            MultiDict.add(self, key, value)

    def pop(self, key, default=_missing):
        """返回list的第一个元素"""
        try:
            return dict.pop(self, key)[0]
        except KeyError as e:
            if default is not _missing:
                return default
            raise self.KeyError(str(e))

    def popitem(self):
        """Pop value"""
        try:
            item = dict.popitem(self)
            return item[0], item[1][0]
        except KeyError as e:
            raise self.KeyError(str(e))

    def poplist(self, key):
        """返回list"""
        return dict.pop(self, key, [])

    def popitemlist(self):
        try:
            return dict.popitem(self)
        except KeyError as e:
            raise self.KeyError(str(e))

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.items(multi=True))


def iter_multi_items(mapping):
    """{ "key1": [1, 2, 3], "key2": [4, 5] }
    返回("key1", 1), ("key", 2), ("key", 3), ("key2", 4), ("key2", 5)
    """
    if isinstance(mapping, MultiDict):
        for item in mapping.iteritems(multi=True):
            yield item
    elif isinstance(mapping, dict):
        for key, value in mapping.iteritems():
            if isinstance(value, (tuple, list)):
                for value in value:
                    yield key, value
            else:
                yield key, value
    else:
        for item in mapping:
            yield item


def is_immutable(self):
    raise TypeError('%r objects are immutable' % self.__class__.__name__)


class ImmutableDictMixin(object):
    """不可变的字典"""
    def __reduce_ex__(self, protocol):
        return type(self), (dict(self),)

    def setdefault(self, key, default=None):
        is_immutable(self)

    def update(self, *args, **kwargs):
        is_immutable(self)

    def pop(self, key, default=None):
        is_immutable(self)

    def popitem(self):
        is_immutable(self)

    def __setitem__(self, key, value):
        is_immutable(self)

    def __delitem__(self, key):
        is_immutable(self)

    def clear(self):
        is_immutable(self)


class ImmutableMultiDictMixin(ImmutableDictMixin):
    """不可变属性
    """

    def __reduce_ex__(self, protocol):
        return type(self), (self.items(multi=True),)

    def add(self, key, value):
        is_immutable(self)

    def popitemlist(self):
        is_immutable(self)

    def poplist(self, key):
        is_immutable(self)

    def setlist(self, key, new_list):
        is_immutable(self)

    def setlistdefault(self, key, default_list=None):
        is_immutable(self)


class ImmutableMultiDict(ImmutableMultiDictMixin, MultiDict):
    """混合不可变字典
    """

    def copy(self):
        """浅拷贝, 标准库中对它不可用
        """
        return MultiDict(self)

    def __copy__(self):
        return self


class ImmutableListMixin(object):
    """不可变列表
    """

    def __reduce_ex__(self, protocol):
        return type(self), (list(self),)

    def __delitem__(self, key):
        is_immutable(self)

    def __delslice__(self, i, j):
        is_immutable(self)

    def __iadd__(self, other):
        is_immutable(self)
    __imul__ = __iadd__

    def __setitem__(self, key, value):
        is_immutable(self)

    def __setslice__(self, i, j, value):
        is_immutable(self)

    def append(self, item):
        is_immutable(self)
    remove = append

    def extend(self, iterable):
        is_immutable(self)

    def insert(self, pos, value):
        is_immutable(self)

    def pop(self, index=-1):
        is_immutable(self)

    def reverse(self):
        is_immutable(self)

    def sort(self, cmp=None, key=None, reverse=None):
        is_immutable(self)


def _proxy_repr(cls):
    def proxy_repr(self):
        return '%s(%s)' % (self.__class__.__name__, cls.__repr__(self))
    return proxy_repr


class ImmutableList(ImmutableListMixin, list):
    """不可变列表
    """

    __repr__ = _proxy_repr(list)


class ImmutableTypeConversionDict(ImmutableDictMixin, TypeConversionDict):
    """不可变支持get且转类型的字典
    """

    def copy(self):
        return TypeConversionDict(self)

    def __copy__(self):
        return self