# -*- coding: utf-8 -*-
'''knife filtering mixins'''

from re import compile
from inspect import getmro
from threading import local
from functools import reduce
from operator import attrgetter, itemgetter, truth

from knife.compat import (
    ifilter, ichain, imap, ifilterfalse, ivalues, iitems, ikeys, istarmap)


class CollectMixin(local):

    '''collecting mixin'''

    @staticmethod
    def _attributes(names, _attrgetter=attrgetter):
        attrfind = _attrgetter(*names)
        def attributes(iterable, get=attrfind): #@IgnorePep8
            for thing in iterable:
                try:
                    yield get(thing)
                except AttributeError:
                    pass
        return attributes

    @staticmethod
    def _extract(pattern, flags=0):
        search = compile(pattern, flags).search
        def find(x): #@IgnorePep8
            results = search(x)
            if not results:
                return (), {}
            # extract any named results
            named = results.groupdict()
            # extract any positional arguments
            positions = tuple(i for i in results.groups() if i not in named)
            return positions, named
        def extract_(iterable): #@IgnorePep8
            return ifilter(
                lambda x, y: truth(x and y), imap(find, iterable),
            )
        return extract_

    @staticmethod
    def _items(call, m=imap, c=ichain, i=iitems, s=istarmap):
        def items(iterable):
            return s(call, c(m(i, iterable)))
        return items

    @staticmethod
    def _keys(call, m=imap, c=ichain, k=ikeys, s=istarmap):
        def keys(iterable):
            return s(call, c(m(k, iterable)))
        return keys

    @staticmethod
    def _members(call, alt, wrap, imap_=imap, ifilter_=ifilter):
        def members(truth_, iterable):
            f, s, t, i = truth_, alt, wrap, iterable
            d, w, g, e = dir, extract, getattr, AttributeError
            test = lambda x: x.startswith('__') or x.startswith('mro')
            for k in ifilterfalse(test, d(i)):
                try:
                    v = g(i, k)
                except e:
                    pass
                else:
                    yield k, t(w(f, v)) if s(v) else k, v
        def extract(truth_, iterable): #@IgnorePep8
            for member in ifilter_(truth, members(truth_, iterable)):
                yield member
        def members_(iterable): #@IgnorePep8
            return ichain(imap_(lambda x: extract(call, x), iterable))
        return members_

    @staticmethod
    def _mro(iterable, ichain_=ichain, imap_=imap, getmro_=getmro):
        return ichain_(imap_(getmro_, iterable))

    @staticmethod
    def _pluck(keys, _itemgetter=itemgetter):
        itemfind = _itemgetter(*keys)
        def pluck(iterable, get=itemfind): #@IgnorePep8
            for thing in iterable:
                IndexErr_, KeyErr_, TypeErr_ = IndexError, KeyError, TypeError
                try:
                    yield get(thing)
                except (IndexErr_, KeyErr_, TypeErr_):
                    pass
        return pluck

    @staticmethod
    def _values(call, m=imap, c=ichain, v=ivalues, s=istarmap):
        def values(iterable):
            return s(call, c(m(v, iterable)))
        return values

    def attributes(self, *names):
        '''extract object attributes from incoming by their `*names`'''
        with self._flow():
            return self._iter(self._attributes(names))

    def extract(self, pattern, flags=0):
        '''
        extract patterns from incoming strings

        @param pattern: search pattern
        '''
        with self._flow():
            return self._many(self._extract(pattern, flags))

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        with self._flow():
            return self._many(self._items(self._call))

    def keys(self):
        '''invoke call on each mapping to get keys'''
        with self._flow():
            return self._many(self._keys(self._call))

    def members(self):
        '''extract object members from incoming'''
        with self._flow():
            return self._many(
                self._members(self._test, self._alt, self._wrapper),
            )

    def mro(self):
        '''extract ancestors of things by method resolution order'''
        with self._flow():
            return self._many(self._mro)

    def pluck(self, *keys):
        '''extract object items from incoming by item `*keys`'''
        with self._flow():
            return self._iter(self._pluck(keys))

    def values(self):
        '''invoke call on each mapping to get values'''
        with self._flow():
            return self._many(self._values(self._call))


class FilterMixin(local):

    '''filtering mixin'''

    @classmethod
    def _filter(cls, true, pat, false, flag, f=ifilter, ff=ifilterfalse):
        if pat is not None:
            call = compile(pat, flag).search
        else:
            call = true
        if false:
            def falsefilter(iterable):
                return ff(call, iterable)
            return falsefilter
        else:
            def truefilter(iterable):
                return f(call, iterable)
            return truefilter

    @classmethod
    def _find(cls, true, pat, false, flag, f=ifilter, ff=ifilterfalse):
        if pat is not None:
            call = compile(pat, flag).search
        else:
            call = true
        if false:
            def falsefind(iterable): #@IgnorePep8
                return next(ff(call, iterable))
            return falsefind
        else:
            def truefind(iterable):
                return next(f(call, iterable))
            return truefind

    @staticmethod
    def _replace(pattern, new, count, flags, imap_=imap):
        sub = compile(pattern, flags).sub
        def replace(iterable): #@IgnorePep8
            return imap_(lambda x: sub(new, x, count), iterable)
        return replace

    @staticmethod
    def _difference(symmetric, reduce_=reduce, set_=set):
        if symmetric:
            test = lambda x, y: set_(x).symmetric_difference(y)
        else:
            test = lambda x, y: set_(x).difference(y)
        def difference(iterable): #@IgnorePep8
            return reduce_(test, iterable)
        return difference

    @staticmethod
    def _disjointed(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).isdisjoint(y), iterable)

    @staticmethod
    def _intersection(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).intersection(y), iterable)

    @classmethod
    def _divide(cls, true, pat, flag, f=ifilter, ff=ifilterfalse, l=list):
        if pat is not None:
            call = compile(pat, flag).search
        else:
            call = true
        def partition(iterable): #@IgnorePep8
            falsy, truey = cls._clone(iterable)
            return iter((l(f(call, truey)), l(ff(call, falsy))))
        return partition

    @staticmethod
    def _subset(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).issubset(y), iterable)

    @staticmethod
    def _superset(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).issuperset(y), iterable)

    @staticmethod
    def _union(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).union(y), iterable)

    @staticmethod
    def _unique(key, set_=set):
        def unique(iterable):
            seen = set_()
            seenadd, key_ = seen.add, key
            for element in iterable:
                k = key_(element)
                if k not in seen:
                    seenadd(k)
                    yield element
        return unique

    def filter(self, pattern=None, reverse=False, flags=0):
        '''
        incoming for which current callable returns `True`

        @param pattern: search pattern expression (default: None)
        @param reverse: reduce from right side (default: False)
        '''
        with self._flow():
            return self._many(
                self._filter(self._test, pattern, reverse, flags)
            )

    def find(self, pattern=None, reverse=False, flags=0):
        '''first incoming thing for which current callable returns `True`'''
        with self._flow():
            return self._one(self._find(self._test, pattern, reverse, flags))

    def replace(self, pattern, new, count=0, flags=0):
        '''
        replace incoming strings matching pattern with replacement string

        @param pattern: search pattern
        @param new: replacement string
        '''
        with self._flow():
            return self._many(self._replace(pattern, new, count, flags))

    def difference(self, symmetric=False):
        '''
        difference between incoming

        @param symmetric: use symmetric difference
        '''
        with self._flow():
            return self._many(self._difference(symmetric))

    def disjointed(self):
        '''disjoint between incoming'''
        with self._flow():
            return self._one(self._disjointed)

    def intersection(self):
        '''intersection between incoming'''
        with self._flow():
            return self._many(self._intersection)

    def partition(self, pattern=None, flags=0):
        '''
        split incoming into `True` and `False` things based on results
        of call
        '''
        with self._flow():
            return self._many(self._divide(self._test, pattern, flags))

    def subset(self):
        '''incoming that are subsets of incoming'''
        with self._flow():
            return self._one(self._subset)

    def superset(self):
        '''incoming that are supersets of incoming'''
        with self._flow():
            return self._one(self._superset)

    def union(self):
        '''union between incoming'''
        with self._flow():
            return self._many(self._union)

    def unique(self):
        '''
        list unique incoming, preserving order and remember all incoming things
        ever seen
        '''
        with self._flow():
            return self._iter(self._unique(self._identity))
