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


class BaseExtract(local):

    '''collecting mixin'''

    @staticmethod
    def _attributes(iterable, names, _attrgetter=attrgetter):
        attrfind = _attrgetter(*names)
        for thing in iterable:
            try:
                yield attrfind(thing)
            except AttributeError:
                pass

    @staticmethod
    def _pluck(iterable, keys, _itemgetter=itemgetter):
        itemfind = _itemgetter(*keys)
        IndexErr_, KeyErr_, TypeErr_ = IndexError, KeyError, TypeError
        for thing in iterable:
            try:
                yield itemfind(thing)
            except (IndexErr_, KeyErr_, TypeErr_):
                pass

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
        return ichain(imap(lambda x: extract(call, x), iterable))

    @staticmethod
    def _mro(iterable, ichain_=ichain, imap_=imap, getmro_=getmro):
        return ichain_(imap_(getmro_, iterable))

    def _extract(self, pattern, flags=0, *things):
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
        with self._flow():
            return self._xtend(ifilter(
                lambda x, y: truth(x and y), imap(find, self._iterable),
            ))
            

class BaseExtractMixin(local):

    '''collecting mixin'''

    def attributes(self, *names):
        '''extract object attributes from inflow by their `*names`'''
        with self._flow():
            return self._iter(self._attributes(self._iterable, names))

    def pluck(self, *keys):
        '''extract object items from inflow by item `*keys`'''
        with self._flow():
            return self._iter(self._pluck(self._iterable, keys))

    def members(self):
        '''extract object members from inflow'''
        with self._flow():
            return self._xtend(self._truth, self._iterable)

    def mro(self):
        '''extract ancestors of things by method resolution order'''
        with self._flow():
            return self._xtend(self._iterable)

    def extract(self, pattern, flags=0, *things):
        '''
        extract patterns from inflow strings
        
        @param pattern: search pattern 
        '''
        with self._flow():
            return self._xtend(self._extract(self._iterable, pattern))
            

class ExtractMixin(BaseExtract, BaseExtractMixin):

    '''collecting mixin'''


class BaseFilter(local):

    '''base set'''

    @staticmethod
    def _filter(truth, iterable, pattern, flags, things, f=ifilter, c=compile):
        if pattern is not None:
            call = c(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = truth
        return f(call, iterable)

    @staticmethod
    def _find(truth, iterable, pattern, flags, things):
        if pattern is not None:
            call = compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = truth
        return next(ifilter(call, iterable))
        
    @classmethod
    def _partition(cls, truth, iterable, pattern, flags, things, l=list):
        if pattern is not None:
            call = compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = truth
        falsy, truey = cls._clone(iterable)
        return iter((
            l(ifilter(call, truey)), l(filterfalse(call, falsy)),
        ))

    @classmethod
    def _replace(iterable, pattern, new, count=0, flags=0):
        sub = compile(pattern, flags).sub
        return imap(lambda x: sub(new, x, count), iterable)

    def _filterfalse(self, pattern=None, flags=0, *things):
        '''strip things from inflow'''
        if pattern is not None:
            call = compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = self._call if self._call is not None else truth
        with self._flow():
            return self._xtend(filterfalse(call, self._iterable))


class BaseFilterMixin(local):

    '''base set'''

    def filter(self, pattern=None, flags=0, *things):
        '''
        inflow for which current callable returns `True`
        
        @param pattern: search pattern expression (default: None)
        '''
        return self._xtend(self._filter(
            self._truth, self._iterable, pattern, flags, things,
        ))

    def find(self, pattern=None, flags=0, *things):
        '''first inflow thing for which current callable returns `True`'''
        with self._flow():
            return self._append(self._find(
                self._truth, self._iterable, pattern, flags, things,
            ))
        
    def partition(self, pattern=None, flags=0, *things):
        '''
        split inflow into `True` and `False` things based on results
        of call
        '''
        with self._flow():
            return self._xtend(self._partition(
                self._truth, self._iterable, pattern, flags, things,
            ))

    def replace(self, pattern, new, count=0, flags=0):
        '''
        replace inflow strings matching pattern with replacement string
        
        @param pattern: search pattern 
        @param new: replacement string
        '''
        with self._flow():
            return self._xtend(self._partition(
                self._iterable, pattern, new, count, flags,
            ))

    def filterfalse(self, pattern=None, flags=0, *things):
        '''strip things from inflow'''
        return self._xtend(self._filterfalse(
            self._truth, self._iterable, pattern, flags, things,
        ))
        
class FilterMixin(BaseFilter, BaseFilterMixin):

    '''base filtering mixin'''


class BaseSlice(local):

    '''slicing mixin'''
    
    @staticmethod
    def _difference(iterable, symmetric, reduce_=reduce, set_=set):
        test = (
            lambda x, y: set_(x).difference(y) if symmetric else
            lambda x, y: set_(x).symmetric_difference(y)
        )
        return reduce_(test, iterable)

    @staticmethod
    def _disjointed(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).isdisjoint(y), iterable)

    @staticmethod
    def _intersection(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).intersection(y), iterable)

    @staticmethod
    def _subset(iterable, set_=set, reduce_=reduce):
        '''inflow that are subsets of inflow'''
        return reduce_(lambda x, y: set_(x).issubset(y), iterable)

    @staticmethod
    def _superset(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).issuperset(y), iterable)

    @staticmethod
    def _union(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).union(y), iterable)

    @staticmethod
    def _unique(iterable, key, set_=set):
        seen = set_()
        seen_add_, key_ = seen.add, key
        for element in iterable:
            k = key_(element)
            if k not in seen:
                seen_add_(k)
                yield element


    @staticmethod
    def _first(iterable, n, islice_=islice, next_=next):
        return islice_(iterable, n) if n else next_(iterable)

    @classmethod
    def _last(cls, iterable, n, s=islice, d=deque, ln=len, l=list):
        i1, i2 = cls._clone(iterable)
        return s(i1, ln(l(i2)) - n, None) if n else d(i1, maxlen=1).pop()

    @staticmethod
    def _nth(iterable, n, default, islice_=islice, next_=next):
        return next_(islice_(iterable, n, None), default)

    @classmethod
    def _initial(cls, iterable, islice_=islice, len_=len, list_=list):
        i1, i2 = cls._clone(iterable)
        return islice_(i1, len_(list_(i2)) - 1)

    @staticmethod
    def _rest(iterable, _islice=islice):
        return _islice(iterable, 1, None)


class BaseSliceMixin(local):

    '''slicing mixin'''

    def first(self, n=0):
        '''
        first `n` things of inflow or just the first thing

        @param n: number of things (default: 0)
        '''
        with self._flow():
            return (
                self._xtend(self._first(self._iterable, n)) if n
                else self._append(self._first(self._iterable))
            )

    def last(self, n=0):
        '''
        last `n` things of inflow or just the last thing

        @param n: number of things (default: 0)
        '''
        with self._flow():
            return (
                self._xtend(self._last(self._iterable, n)) if n
                else self._append(self._last(self._iterable))
            )

    def nth(self, n, default=None):
        '''
        `nth` inflow thing in inflow or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._flow():
            return self._append(self._nth(self._iterable, n, default))

    def initial(self):
        '''all inflow except the last thing'''
        with self._flow():
            return self._xtend(self._initial(self._iterable))

    def rest(self):
        '''all inflow except the first thing'''
        with self._flow():
            return self._xtend(self._rest(self._iterable))
        
    def difference(self, symmetric=False):
        '''
        difference between inflow
        
        @param symmetric: use symmetric difference
        '''
        with self._flow():
            return self._xtend(self._difference(self._iterable, symmetric))

    def disjointed(self):
        '''disjoint between inflow'''
        with self._flow():
            return self._xtend(self._disjointed(self._iterable))

    def intersection(self):
        '''intersection between inflow'''
        with self._flow():
            return self._xtend(self._intersection(self._iterable))

    def subset(self):
        '''inflow that are subsets of inflow'''
        with self._flow():
            return self._xtend(self._subset(self._iterable))

    def superset(self):
        '''inflow that are supersets of inflow'''
        with self._flow():
            return self._xtend(self._superset(self._iterable))

    def union(self):
        '''union between inflow'''
        with self._flow():
            return self._xtend(self._union(self._iterable))

    def unique(self):
        '''
        list unique inflow, preserving order and remember all inflow things
        ever seen
        '''
        with self._flow():
            return self._iter(self._unique(self._iterable, self._call))


class SliceMixin(BaseSlice, BaseSliceMixin):

    '''slicing mixin'''
