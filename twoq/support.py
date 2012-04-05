# -*- coding: utf-8 -*-
'''twoq support'''

from itertools import chain
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # @UnusedImport

from stuf import six
# pylint: disable-msg=f0401,w0611
from stuf.six.moves import (
    map, filterfalse, filter, zip, zip_longest, xrange)  # @UnresolvedImport @UnusedImport @IgnorePep8
# pylint: enable-msg=f0401

__all__ = ['port']
items = six.items
ichain = chain.from_iterable
range = xrange
imap = map
ifilter = filter


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


isstring = port.isstring
isunicode = port.isunicode

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


if six.PY3:

    def n2b(n, encoding='ISO-8859-1'):
        '''
        the given native string as a byte string in the given encoding
        '''
        # In Python 3, the native string type is unicode
        return n.encode(encoding)

    def n2u(n, encoding='ISO-8859-1'):
        '''
        the given native string as a unicode string with the given encoding
        '''
        # In Python 3, the native string type is unicode
        return n

    def ton(n, encoding='ISO-8859-1'):
        '''
        the given string as a native string in the given encoding
        '''
        # In Python 3, the native string type is unicode
        if isinstance(n, bytes):
            return n.decode(encoding)
        return n
else:
    import re

    def n2b(n, encoding='ISO-8859-1'):
        '''the given native string as a byte string in the given encoding'''
        # In Python 2, the native string type is bytes. Assume it's already
        # in the given encoding, which for ISO-8859-1 is almost always what
        # was intended.
        return n

    def n2u(n, encoding='ISO-8859-1'):
        '''
        the given native string as a unicode string with the given encoding
        '''
        # In Python 2, the native string type is bytes.
        # First, check for the special encoding 'escape'. The test suite uses
        # this
        # to signal that it wants to pass a string with embedded \unnnn
        # escapes, but without having to prefix it with u'' for Python 2, but
        # no prefix for Python 3.
        if encoding == 'escape':
            return unicode(re.sub(
                r'\\u([0-9a-zA-Z]{4})',
               lambda m: unichr(int(m.group(1), 16)),
               n.decode('ISO-8859-1')
            ))
        # assume it's already in the given encoding, which for ISO-8859-1 is
        # almost always what was intended.
        return n.decode(encoding)

    def ton(n, encoding='ISO-8859-1'):
        '''return the given string as a native string in the given encoding'''
        # in Python 2, the native string type is bytes.
        if isinstance(n, unicode):
            return n.encode(encoding)
        return n
