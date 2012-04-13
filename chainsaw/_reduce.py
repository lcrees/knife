# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from inspect import getmro
from threading import local
from collections import deque
from fnmatch import translate
from random import choice, sample
from re import compile as rcompile
from functools import partial, reduce
from itertools import cycle, islice, tee, starmap
from operator import itemgetter, attrgetter, truth

from parse import compile as pcompile
from stuf.six import strings, items, values, keys

from chainsaw._compat import ifilter, ichain, imap, ifilterfalse, zip_longest


class _FilterMixin(local):

    '''filtering mixin'''

    @staticmethod
    def _attributes(names, _attrgetter=attrgetter):
        attrfind = _attrgetter(*names)
        def attributes(iterable, get=attrfind): #@IgnorePep8
            AttrErr_ = AttributeError
            for thing in iterable:
                try:
                    yield get(thing)
                except AttrErr_:
                    pass
        return attributes

    @staticmethod
    def _duality(true, f=ifilter, ff=ifilterfalse, l=list, t=tee):
        def duality(iterable): #@IgnorePep8
            truth_, false_ = t(iterable)
            return iter((l(f(true, truth_)), l(ff(true, false_))))
        return duality

    @staticmethod
    def _filter(true, false, ifilter_=ifilter, ifilterfalse_=ifilterfalse):
        if false:
            return lambda x: ifilterfalse_(true, x)
        return lambda x: ifilter_(true, x)

    @staticmethod
    def _mapping(call, key, value, k=keys, i=items, v=values, c=ichain):
        if key:
            return lambda x: imap(call, c(imap(k, x)))
        elif value:
            return lambda x: imap(call, c(imap(v, x)))
        return lambda x: starmap(call, c(imap(i, x)))

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

    @staticmethod
    def _pattern(pat, type, flag, t=translate, r=rcompile, p=pcompile):
        if type == 'glob':
            pat = t(pat)
            type = 'regex'
        return r(pat, flag).search if type == 'regex' else p(pat).search

    @staticmethod
    def _traverse(call, deep, anc, alt, wrap):
        mro = lambda i: ichain(imap(getmro, i))  # @UnusedVariable
        def members(true, iterable): #@IgnorePep8
            for k in ifilter(true, dir(iterable)):
                try:
                    v = getattr(iterable, k)
                except AttributeError:
                    pass
                else:
                    yield k, wrap(extract(true, v)) if alt(v) else k, v
        def extract(true, iterable): #@IgnorePep8
            for member in ifilter(truth, members(true, iterable)):
                yield member
        return lambda i: ichain(imap(lambda x: extract(call, x), i))


class _ReduceMixin(local):

    '''reduce mixin'''

    @classmethod
    def _flatten(cls, iterable, strings_=strings, isinstance_=isinstance):
        smash_ = cls._flatten
        for item in iterable:
            try:
                # don't recur over strings
                if isinstance_(item, strings_):
                    yield item
                else:
                    # do recur over other things
                    for j in smash_(item):
                        yield j
            except TypeError:
                # does not recur
                yield item

    @staticmethod
    def _merge(iterable, ichain_=ichain):
        return ichain_(iterable)

    @staticmethod
    def _reduce(call, initial, reverse, reduce_=reduce):
        if reverse:
            if initial is None:
                return lambda i: reduce_(lambda x, y: call(y, x), i)
            return lambda i: reduce_(lambda x, y: call(y, x), i, initial)
        if initial is None:
            return lambda x: reduce_(call, x)
        return lambda x: reduce_(call, x, initial)

    @staticmethod
    def _weave(b, i=iter, n=next, s=islice, c=cycle, p=partial, t=tee, l=list):
        work, measure = t(b)
        nexts = c(p(n, i(item)) for item in work)
        pending = len(l(measure))
        while pending:
            try:
                for nextz in nexts:
                    yield nextz()
            except StopIteration:
                pending -= 1
                nexts = c(s(nexts, pending))

    @staticmethod
    def _zip(iterable, zip_=zip_longest):
        return zip_(*iterable)


class _SliceMixin(local):

    '''slicing mixin'''

    @staticmethod
    def _at(n, default, islice_=islice, next_=next):
        return lambda x: next_(islice_(x, n, None), default)

    @staticmethod
    def _choice(iterable, choice_=choice, list_=list):
        return choice_(list_(iterable))

    @staticmethod
    def _dice(n, fill, zip_longest_=zip_longest, iter_=iter):
        return lambda x: zip_longest_(fillvalue=fill, *[iter_(x)] * n)

    @staticmethod
    def _first(n=0, islice_=islice, next_=next):
        return lambda x: islice_(x, n) if n else next_(x)

    @staticmethod
    def _initial(iterable, islice_=islice, len_=len, list_=list, t=tee):
        i1, i2 = t(iterable)
        return islice_(i1, len_(list_(i2)) - 1)

    @staticmethod
    def _last(n, s=islice, d=deque, ln=len, l=list, t=tee):
        def last(iterable):
            i1, i2 = t(iterable)
            return s(i1, ln(l(i2)) - n, None) if n else d(i1, maxlen=1).pop()
        return last

    @staticmethod
    def _rest(iterable, _islice=islice):
        return _islice(iterable, 1, None)

    @staticmethod
    def _sample(n, sample=sample, list_=list):
        return lambda x: sample(list_(x), n)

    @staticmethod
    def _slice(start, stop, step, _islice=islice):
        if stop and step:
            return lambda x: _islice(x, start, stop, step)
        elif stop:
            return lambda x: _islice(x, start, stop)
        return lambda x: _islice(x, start)
