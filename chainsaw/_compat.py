# -*- coding: utf-8 -*-
'''chainsaw support'''

from itertools import chain
from collections import Iterable
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # @UnusedImport

from stuf import six
# pylint: disable-msg=f0401,w0611
from stuf.six.moves import (
    map, filterfalse, filter, zip, zip_longest)  # @UnresolvedImport @UnusedImport @IgnorePep8
# pylint: enable-msg=f0401

ichain = chain.from_iterable
ifilter = filter
ifilterfalse = filterfalse
imap = map
izip = zip
items = six.items


class port(object):

    '''python 2/3 helper'''

    # is python 3?
    PY3 = six.PY3
    # types
    BINARY = six.binaries
    CLASS = six.classes
    INTEGER = six.integers
    MAXSIZE = six.MAXSIZE
    STRING = six.strings
    UNICODE = six.texts
    # classes
    BytesIO = six.BytesIO
    StringIO = six.StringIO
    # character data
    b = staticmethod(six.b)
    int2byte = staticmethod(six.int2byte)
    u = staticmethod(six.u)
    # dictionary
    items = staticmethod(six.items)
    keys = staticmethod(six.keys)
    values = staticmethod(six.values)
    # iterables
    iterator = staticmethod(six.advance_iterator)
    # classes
    metaclass = staticmethod(six.with_metaclass)
    # methods
    code = staticmethod(six.function_code)
    defaults = staticmethod(six.function_defaults)
    method_function = staticmethod(six.method_function)
    method_self = staticmethod(six.method_self)
    unbound = staticmethod(six.get_unbound_function)
    # exception
    reraise = staticmethod(six.reraise)

    @classmethod
    def isbinary(cls, value):
        '''is binary?'''
        return isinstance(value, cls.BINARY)

    @classmethod
    def isclass(cls, value):
        '''is class?'''
        return isinstance(value, cls.CLASS)

    @classmethod
    def iscall(cls, value):
        '''is callable?'''
        return six.callable(value)

    @classmethod
    def isgtemax(cls, value):
        '''greater than max size?'''
        return value > cls.MAXSIZE

    @classmethod
    def isinteger(cls, value):
        '''is integer?'''
        return isinstance(value, cls.INTEGER)

    @classmethod
    def isltemax(cls, value):
        '''less than max size?'''
        return value < cls.MAXSIZE

    @classmethod
    def isstring(cls, value):
        '''is string'''
        return isinstance(value, cls.STRING)

    @classmethod
    def isunicode(cls, value):
        '''is text?'''
        return isinstance(value, cls.UNICODE)

    @staticmethod
    def printf(*args, **kw):
        '''print output'''
        return six.printf(*args, **kw)


isbinary = port.isbinary
isstring = port.isstring
isunicode = port.isunicode
texts = six.texts


def deferfunc(func):
    yield func()


def deferiter(iterz):
    yield next(iterz)


def iterthing(iterator, wrap, noniter):
    yield wrap(iterator(wrap(noniter)))


def makeiter(wrap, thing):
    if not isstring(thing) and isinstance(thing, Iterable):
        return thing
    return wrap(thing)


def tounicode(thing, encoding='utf-8', errors='strict'):
    return (
        thing.decode(encoding, errors) if isbinary(thing) else
        texts(texts(thing).encode(encoding, errors), encoding, errors)
    )


def tobytes(thing, encoding='utf-8', errors='strict'):
    return (
        texts(thing).encode(encoding, errors) if not isbinary(thing) else thing
    )


import sys
if not sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from collections import Counter  # @UnresolvedImport
else:
    import heapq
    from operator import itemgetter

    class Counter(dict):

        '''dict subclass for counting hashable items'''

        def __init__(self, iterable=None, **kw):
            '''
            If given, count elements from an input iterable. Or, initialize
            count from another mapping of elements to their counts.
            '''
            super(Counter, self).__init__()
            self.update(iterable, **kw)

        def most_common(self, n=None):
            '''
            list the n most common elements and their counts from the most
            common to the least

            If n is None, then list all element counts.
            '''
            # Emulate Bag.sortedByCount from Smalltalk
            if n is None:
                return sorted(items(self), key=itemgetter(1), reverse=True)
            return heapq.nlargest(n, self.iteritems(), key=itemgetter(1))

        # Override dict methods where necessary

        def update(self, iterable=None, **kw):
            '''like dict.update() but add counts instead of replacing them'''
            if iterable is not None:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
