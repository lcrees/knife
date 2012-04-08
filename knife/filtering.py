# -*- coding: utf-8 -*-
'''knife filtering mixins'''

from re import compile
from inspect import getmro
from threading import local
from functools import reduce
from itertools import islice
from collections import deque
from operator import attrgetter, itemgetter, truth

from knife.compat import ifilter, ichain, imap, ifilterfalse


class ExtractMixin(local):

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

    def attributes(self, *names):
        '''extract object attributes from incoming by their `*names`'''
        with self._flow():
            return self._iter(self._attributes(names))

    @staticmethod
    def _extract(pattern, flags=0, *things):
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

    def extract(self, pattern, flags=0, *things):
        '''
        extract patterns from incoming strings

        @param pattern: search pattern
        '''
        with self._flow():
            return self._many(self._extract(pattern, flags, things))

    @staticmethod
    def _members(call, alt, wrap, iterable, imap=imap, ifilter=ifilter):
        def members(truth, iterable):
            f, s, t, i = truth, alt, wrap, iterable
            d, w, g, e = dir, extract, getattr, AttributeError
            test = lambda x: x.startswith('__') or x.startswith('mro')
            for k in filterfalse(test, d(i)):
                try:
                    v = g(i, k)
                except e:
                    pass
                else:
                    yield k, t(w(f, v)) if s(v) else k, v
        def extract(truth, iterable): #@IgnorePep8
            for member in ifilter(truth, members(truth, iterable)):
                yield member
        def members_(iterable): #@IgnorePep8
            return ichain(imap(lambda x: extract(call, x), iterable))
        return members_

    def members(self):
        '''extract object members from incoming'''
        with self._flow():
            return self._many(
                self._members(self._truth, self._alt, self._wrap),
            )

    @staticmethod
    def _mro(iterable, ichain_=ichain, imap_=imap, getmro_=getmro):
        return ichain_(imap_(getmro_, iterable))

    def mro(self):
        '''extract ancestors of things by method resolution order'''
        with self._flow():
            return self._many(self._mro)

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

    def pluck(self, *keys):
        '''extract object items from incoming by item `*keys`'''
        with self._flow():
            return self._iter(self._pluck(keys))


class FilterMixin(local):

    '''filtering mixin'''

    @staticmethod
    def _filter(truth, pattern, flags, things, f=ifilter, c=compile):
        if pattern is not None:
            call = c(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = truth
        def filter(iterable): #@IgnorePep8
            return f(call, iterable)
        return filter

    def filter(self, pattern=None, flags=0, *things):
        '''
        incoming for which current callable returns `True`

        @param pattern: search pattern expression (default: None)
        '''
        return self._many(self._filter(self._truth, pattern, flags, things))

    @staticmethod
    def _find(truth, pattern, flags, things):
        if pattern is not None:
            call = compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = truth
        def find(iterable): #@IgnorePep8
            return next(ifilter(call, iterable))
        return find

    def find(self, pattern=None, flags=0, *things):
        '''first incoming thing for which current callable returns `True`'''
        with self._flow():
            return self._one(
                self._find(self._truth, pattern, flags, things)
            )

    @classmethod
    def _partition(cls, truth, pattern, flags, things, l=list):
        if pattern is not None:
            call = compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = truth
        def partition(iterable): #@IgnorePep8
            falsy, truey = cls._clone(iterable)
            return iter((
                l(ifilter(call, truey)), l(filterfalse(call, falsy)),
            ))
        return partition

    def partition(self, pattern=None, flags=0, *things):
        '''
        split incoming into `True` and `False` things based on results
        of call
        '''
        with self._flow():
            return self._many(self._partition(
                self._truth, pattern, flags, things,
            ))

    @staticmethod
    def _replace(pattern, new, count, flags, imap_=imap):
        sub = compile(pattern, flags).sub
        def replace(iterable): #@IgnorePep8
            return imap(lambda x: sub(new, x, count), iterable)
        return replace

    def replace(self, pattern, new, count=0, flags=0):
        '''
        replace incoming strings matching pattern with replacement string

        @param pattern: search pattern
        @param new: replacement string
        '''
        with self._flow():
            return self._many(self._replace(pattern, new, count, flags))

    @staticmethod
    def _filterfalse(truth, pattern, flags, things, ffalse_=ifilterfalse):
        if pattern is not None:
            call = compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = truth
        def filterfalse(iterable): #@IgnorePep8
            return ffalse_(call, iterable)
        return filterfalse

    def filterfalse(self, pattern=None, flags=0, *things):
        '''strip things from incoming'''
        return self._many(self._filterfalse(
            self._truth, pattern, flags, things,
        ))


class SliceMixin(local):

    '''slicing mixin'''

    @staticmethod
    def _difference(symmetric, reduce_=reduce, set_=set):
        if symmetric:
            test = lambda x, y: set_(x).symmetric_difference(y)
        else:
            test = lambda x, y: set_(x).difference(y)
        def difference(iterable): #@IgnorePep8
            return reduce_(test, iterable)
        return difference

    def difference(self, symmetric=False):
        '''
        difference between incoming

        @param symmetric: use symmetric difference
        '''
        with self._flow():
            return self._many(self._difference(symmetric))

    @staticmethod
    def _disjointed(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).isdisjoint(y), iterable)

    def disjointed(self):
        '''disjoint between incoming'''
        with self._flow():
            return self._many(self._disjointed)

    @staticmethod
    def _first(iterable, n, islice_=islice, next_=next):
        def first(iterable):
            return islice_(iterable, n) if n else next_(iterable)
        return first

    def first(self, n=0):
        '''
        first `n` things of incoming or just the first thing

        @param n: number of things (default: 0)
        '''
        with self._flow():
            first = self._first
            return self._many(first(n)) if n else self._one(first())

    @classmethod
    def _initial(cls, iterable, islice_=islice, len_=len, list_=list):
        i1, i2 = cls._clone(iterable)
        return islice_(i1, len_(list_(i2)) - 1)

    def initial(self):
        '''all incoming except the last thing'''
        with self._flow():
            return self._many(self._initial)

    @staticmethod
    def _intersection(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).intersection(y), iterable)

    def intersection(self):
        '''intersection between incoming'''
        with self._flow():
            return self._many(self._intersection)

    @classmethod
    def _last(cls, iterable, n, s=islice, d=deque, ln=len, l=list):
        def last(iterable):
            i1, i2 = cls._clone(iterable)
            return s(i1, ln(l(i2)) - n, None) if n else d(i1, maxlen=1).pop()
        return last

    def last(self, n=0):
        '''
        last `n` things of incoming or just the last thing

        @param n: number of things (default: 0)
        '''
        with self._flow():
            last = self._last
            return self._many(last(n)) if n else self._one(last(n))

    @staticmethod
    def _nth(n, default, islice_=islice, next_=next):
        def nth(iterable):
            return next_(islice_(iterable, n, None), default)
        return nth

    def nth(self, n, default=None):
        '''
        `nth` incoming thing in incoming or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._flow():
            return self._one(self._nth(n, default))

    @staticmethod
    def _rest(iterable, _islice=islice):
        return _islice(iterable, 1, None)

    def rest(self):
        '''all incoming except the first thing'''
        with self._flow():
            return self._many(self._rest)

    @staticmethod
    def _subset(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).issubset(y), iterable)

    def subset(self):
        '''incoming that are subsets of incoming'''
        with self._flow():
            return self._many(self._subset)

    @staticmethod
    def _superset(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).issuperset(y), iterable)

    def superset(self):
        '''incoming that are supersets of incoming'''
        with self._flow():
            return self._many(self._superset)

    @staticmethod
    def _union(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).union(y), iterable)

    def union(self):
        '''union between incoming'''
        with self._flow():
            return self._many(self._union)

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

    def unique(self):
        '''
        list unique incoming, preserving order and remember all incoming things
        ever seen
        '''
        with self._flow():
            return self._iter(self._unique(self._identity))
