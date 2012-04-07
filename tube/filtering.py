# -*- coding: utf-8 -*-
'''tube filtering mixins'''

from re import compile
from inspect import getmro
from threading import local
from functools import reduce
from itertools import islice
from collections import deque
from operator import attrgetter, itemgetter, truth

from tube.compat import ifilter, ichain, imap, filterfalse


class ExtractMixin(local):

    '''collecting mixin'''

    @staticmethod
    def _attributes(names, _attrgetter=attrgetter):
        attrfind = _attrgetter(*names)
        def attributes__(iterable, get=attrfind): #@IgnorePep8
            for thing in iterable:
                try:
                    yield get(thing)
                except AttributeError:
                    pass
        return attributes__

    @staticmethod
    def _pluck(keys, _itemgetter=itemgetter):
        itemfind = _itemgetter(*keys)
        def pluck__(iterable, get=itemfind): #@IgnorePep8
            for thing in iterable:
                IndexErr_, KeyErr_, TypeErr_ = IndexError, KeyError, TypeError
                try:
                    yield get(thing)
                except (IndexErr_, KeyErr_, TypeErr_):
                    pass
        return pluck__

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
        def extract(truth, iterable):
            for member in ifilter(truth, members(truth, iterable)):
                yield member
        def members__(iterable):
            return ichain(imap(lambda x: extract(call, x), iterable))
        return members__

    @staticmethod
    def _mro(iterable, ichain_=ichain, imap_=imap, getmro_=getmro):
        return ichain_(imap_(getmro_, iterable))

    @staticmethod
    def _extract(pattern, flags=0, *things):
        search = compile(pattern, flags).search
        def find(x):
            results = search(x)
            if not results:
                return (), {}
            # extract any named results
            named = results.groupdict()
            # extract any positional arguments
            positions = tuple(i for i in results.groups() if i not in named)
            return positions, named
        def extract__(iterable):
            return ifilter(
                lambda x, y: truth(x and y), imap(find, iterable),
            )

    def attributes(self, *names):
        '''extract object attributes from inflow by their `*names`'''
        with self._flow():
            return self._iter(self._attributes(names))

    def pluck(self, *keys):
        '''extract object items from inflow by item `*keys`'''
        with self._flow():
            return self._iter(self._pluck(keys))

    def members(self):
        '''extract object members from inflow'''
        with self._flow():
            return self._xtend(
                self._members(self._truth, self._alt, self._wrap),
            )

    def mro(self):
        '''extract ancestors of things by method resolution order'''
        with self._flow():
            return self._xtend(self._mro)

    def extract(self, pattern, flags=0, *things):
        '''
        extract patterns from inflow strings
        
        @param pattern: search pattern 
        '''
        with self._flow():
            return self._xtend(self._extract(pattern, flags, things))


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
        def filter__(iterable):
            return f(call, iterable)
        return filter__

    @staticmethod
    def _find(truth, pattern, flags, things):
        if pattern is not None:
            call = compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = truth
        def find__(iterable):
            return next(ifilter(call, iterable))
        return find__
        
    @classmethod
    def _partition(cls, truth, pattern, flags, things, l=list):
        if pattern is not None:
            call = compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = truth
        def partition__(iterable):
            falsy, truey = cls._clone(iterable)
            return iter((
                l(ifilter(call, truey)), l(filterfalse(call, falsy)),
            ))
        return partition__

    @classmethod
    def _replace(pattern, new, count=0, flags=0):
        sub = compile(pattern, flags).sub
        def replace__(iterable):
            return imap(lambda x: sub(new, x, count), iterable)
        return replace__

    @staticmethod
    def _filterfalse(truth, pattern=None, flags=0, *things):
        if pattern is not None:
            call = compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = truth
        def filterfalse__(iterable):
            return filterfalse(call, iterable)
        return filterfalse__

    def filter(self, pattern=None, flags=0, *things):
        '''
        inflow for which current callable returns `True`
        
        @param pattern: search pattern expression (default: None)
        '''
        return self._xtend(self._filter(self._truth, pattern, flags, things))

    def find(self, pattern=None, flags=0, *things):
        '''first inflow thing for which current callable returns `True`'''
        with self._flow():
            return self._append(
                self._find(self._truth, pattern, flags, things)
            )
        
    def partition(self, pattern=None, flags=0, *things):
        '''
        split inflow into `True` and `False` things based on results
        of call
        '''
        with self._flow():
            return self._xtend(self._partition(
                self._truth, pattern, flags, things,
            ))

    def replace(self, pattern, new, count=0, flags=0):
        '''
        replace inflow strings matching pattern with replacement string
        
        @param pattern: search pattern 
        @param new: replacement string
        '''
        with self._flow():
            return self._xtend(self._replace(pattern, new, count, flags))

    def filterfalse(self, pattern=None, flags=0, *things):
        '''strip things from inflow'''
        return self._xtend(self._filterfalse(
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
        def difference__(iterable):
            return reduce_(test, iterable)
        return difference__
    
    @staticmethod
    def _first(iterable, n, islice_=islice, next_=next):
        def first__(iterable):
            return islice_(iterable, n) if n else next_(iterable)
        return first__

    @staticmethod
    def _disjointed(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).isdisjoint(y), iterable)

    @classmethod
    def _initial(cls, iterable, islice_=islice, len_=len, list_=list):
        i1, i2 = cls._clone(iterable)
        return islice_(i1, len_(list_(i2)) - 1)

    @staticmethod
    def _intersection(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).intersection(y), iterable)

    @classmethod
    def _last(cls, iterable, n, s=islice, d=deque, ln=len, l=list):
        def last__(iterable):
            i1, i2 = cls._clone(iterable)
            return s(i1, ln(l(i2)) - n, None) if n else d(i1, maxlen=1).pop()
        return last__

    @staticmethod
    def _nth(n, default, islice_=islice, next_=next):
        def nth__(iterable):
            return next_(islice_(iterable, n, None), default)
        return nth__

    @staticmethod
    def _subset(iterable, set_=set, reduce_=reduce):
        '''inflow that are subsets of inflow'''
        return reduce_(lambda x, y: set_(x).issubset(y), iterable)

    @staticmethod
    def _superset(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).issuperset(y), iterable)
    
    @staticmethod
    def _rest(iterable, _islice=islice):
        return _islice(iterable, 1, None)

    @staticmethod
    def _union(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).union(y), iterable)

    @staticmethod
    def _unique(key, set_=set):
        def unique__(iterable):
            seen = set_()
            seen_add_, key_ = seen.add, key
            for element in iterable:
                k = key_(element)
                if k not in seen:
                    seen_add_(k)
                    yield element
        return unique__
    
    def difference(self, symmetric=False):
        '''
        difference between inflow
        
        @param symmetric: use symmetric difference
        '''
        with self._flow():
            return self._xtend(self._difference(symmetric))

    def disjointed(self):
        '''disjoint between inflow'''
        with self._flow():
            return self._xtend(self._disjointed)

    def first(self, n=0):
        '''
        first `n` things of inflow or just the first thing

        @param n: number of things (default: 0)
        '''
        with self._flow():
            first = self._first
            return self._xtend(first(n)) if n else self._append(first())
            
    def initial(self):
        '''all inflow except the last thing'''
        with self._flow():
            return self._xtend(self._initial)

    def intersection(self):
        '''intersection between inflow'''
        with self._flow():
            return self._xtend(self._intersection)

    def last(self, n=0):
        '''
        last `n` things of inflow or just the last thing

        @param n: number of things (default: 0)
        '''
        with self._flow():
            last = self._last
            return self._xtend(last(n)) if n else self._append(last(n))

    def nth(self, n, default=None):
        '''
        `nth` inflow thing in inflow or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._flow():
            return self._append(self._nth(n, default))

    def rest(self):
        '''all inflow except the first thing'''
        with self._flow():
            return self._xtend(self._rest)

    def subset(self):
        '''inflow that are subsets of inflow'''
        with self._flow():
            return self._xtend(self._subset)

    def superset(self):
        '''inflow that are supersets of inflow'''
        with self._flow():
            return self._xtend(self._superset)

    def union(self):
        '''union between inflow'''
        with self._flow():
            return self._xtend(self._union)

    def unique(self):
        '''
        list unique inflow, preserving order and remember all inflow things
        ever seen
        '''
        with self._flow():
            return self._iter(self._unique(self._identity))
