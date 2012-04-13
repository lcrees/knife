# -*- coding: utf-8 -*-
'''chainsaw filtering mixins'''

from re import compile
from inspect import getmro
from threading import local
from functools import reduce
from operator import itemgetter, attrgetter, truth

from chainsaw._compat import (
    ifilter, ichain, imap, ifilterfalse, ivalues, iitems, ikeys, istarmap)


class _FilterMixin(local):

    '''filtering mixin'''

    @staticmethod
    def _attributes(names, deep, ancestors, call, alt, wrap, imap_=imap, ifilter_=ifilter, getmro_=getmro, _attrgetter=attrgetter): 
        attrfind = _attrgetter(*names)
        def attributes(iterable, get=attrfind): #@IgnorePep8
            for thing in iterable:
                try:
                    yield get(thing)
                except AttributeError:
                    pass
        return attributes
        def _mro(iterable, ichain_=ichain, imap_=imap):
            return ichain_(imap_(getmro_, iterable))
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

    @staticmethod
    def _mapping(call, key, value, k=ikeys, i=iitems, v=ivalues):
        if key:
            def keys(iterable, ichain=ichain, imap=imap):
                return imap(call, ichain(imap(k, iterable)))
            return keys
        elif value:
            def values(iterable, ichain=ichain, imap=imap):
                return imap(call, ichain(imap(v, iterable)))
            return values
        else:
            def items(iterable, ichain=ichain, imap=imap, istarmap=istarmap):
                return istarmap(call, ichain(imap(i, iterable)))
            return items

    @staticmethod
    def _items(keys, _itemgetter=itemgetter):
        itemfind = _itemgetter(*keys)
        def items(iterable, get=itemfind): #@IgnorePep8
            IndexErr_, KeyErr_, TypeErr_ = IndexError, KeyError, TypeError
            for thing in iterable:
                try:
                    yield get(thing)
                except (IndexErr_, KeyErr_, TypeErr_):
                    pass
        return items

    @classmethod
    def _partition(cls, true, pat, flag, f=ifilter, ff=ifilterfalse, l=list):
        if pat is not None:
            call = compile(pat, flag).search
        else:
            call = true
        def partition(iterable): #@IgnorePep8
            falsy, truey = cls._clone(iterable)
            return iter((l(f(call, truey)), l(ff(call, falsy))))
        return partition
