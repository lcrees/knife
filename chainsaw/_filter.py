# -*- coding: utf-8 -*-
'''chainsaw filtering mixins'''

from re import compile
from inspect import getmro
from threading import local
from functools import reduce
from operator import attrgetter, itemgetter, truth

from chainsaw._compat import (
    ifilter, ichain, imap, ifilterfalse, ivalues, iitems, ikeys, istarmap)


class _CollectMixin(local):

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


class _FilterMixin(local):

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
