# -*- coding: utf-8 -*-
'''tube filtering mixins'''

import re
from inspect import getmro
from threading import local
from functools import reduce
from collections import deque
from itertools import tee, islice
from operator import attrgetter, itemgetter, truth

from tube.compat import ifilter, ichain, imap, filterfalse


class ExtractMixin(local):

    '''collecting mixin'''

    def attributes(self, *names):
        '''extract object attributes from inflow by their `*names`'''
        def pick(names, iterable):
            attrfind = attrgetter(*names)
            for thing in iterable:
                try:
                    yield attrfind(thing)
                except AttributeError:
                    pass
        with self._flow():
            return self._xtend(pick(names, self._iterable))

    def items(self, *keys):
        '''extract object items from inflow by item `*keys`'''
        def pluck(keys, iterable, _itemgetter=itemgetter):
            itemfind = _itemgetter(*keys)
            IndexErr_, KeyErr_, TypeErr_ = IndexError, KeyError, TypeError
            for thing in iterable:
                try:
                    yield itemfind(thing)
                except (IndexErr_, KeyErr_, TypeErr_):
                    pass
        with self._flow():
            return self._xtend(pluck(keys, self._iterable))

    def members(self):
        '''extract object members from inflow'''
        call_, alt_, wrap_ = self._call, self._alt, self._wrapper
        def members(truth, iterable): #@IgnorePep8
            f, s, t, i = truth, alt_, wrap_, iterable
            d, w, g, e = dir, extract, getattr, AttributeError
            test = lambda x: x.startswith('__') or x.startswith('mro')
            for k in filterfalse(test, d(i)):
                try:
                    v = g(i, k)
                except e:
                    pass
                else:
                    yield k, t(w(f, v)) if s(v) else k, v
        def extract(truth, iterable, ifilter_=ifilter, members_=members):
            for member in ifilter_(truth, members_(truth, iterable)):
                yield member
        with self._flow():
            return self._xtend(ichain(imap(
                lambda x: extract(call_, x), self._iterable,
            )))

    def mro(self):
        '''extract ancestors of things by method resolution order'''
        with self._flow():
            return self._xtend(ichain(getmro(i) for i in self._iterable))

    def extract(self, pattern, flags=0, *things):
        '''
        extract patterns from inflow strings
        
        @param pattern: search pattern 
        '''
        search = re.compile(pattern, flags).search
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


class FilterMixin(local):

    '''filter mixin'''

    def filter(self, pattern=None, flags=0, *things):
        '''
        inflow for which current callable returns `True`
        
        @param pattern: search pattern expression (default: None)
        '''
        if pattern is not None:
            call = re.compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = self._call if self._call is not None else truth
        with self._flow():
            return self._xtend(ifilter(call, self._iterable))

    def find(self):
        '''first inflow thing for which current callable returns `True`'''
        with self._flow():
            return self._append(
                next(ifilter(self._call, self._iterable))
            )
        
    def partition(self):
        '''
        split inflow into `True` and `False` things based on results
        of call
        '''
        list_, call_ = list, self._call
        with self._flow():
            falsy, truey = tee(self._iterable)
            return self._xtend(iter([
                list_(filterfalse(call_, falsy)), list_(ifilter(call_, truey)),
            ]))

    def replace(self, pattern, new, count=0, flags=0):
        '''
        replace inflow strings matching pattern with replacement string
        
        @param pattern: search pattern 
        @param new: replacement string
        '''
        sub = re.compile(pattern, flags).sub
        with self._flow():
            return self._xtend(imap(
                lambda x: sub(new, x, count), self._iterable,
            ))

    def filterfalse(self, pattern=None, flags=0, *things):
        '''strip things from inflow'''
        if pattern is not None:
            call = re.compile(pattern, flags).search
        elif things:
            call = lambda y: y in things
        else:
            call = self._call if self._call is not None else truth
        with self._flow():
            return self._xtend(filterfalse(call, self._iterable))


class SetMixin(local):

    '''set and uniqueness mixin'''

    def difference(self, symmetric=False):
        '''
        difference between inflow
        
        @param symmetric: use symmetric difference
        '''
        with self._flow():
            test = (
                lambda x, y: set(x).difference(y) if symmetric else
                lambda x, y: set(x).symmetric_difference(y)
            )
            return self._xtend(reduce(test, self._iterable))

    def disjointed(self):
        '''disjoint between inflow'''
        with self._flow():
            return self._append(reduce(
                lambda x, y: set(x).isdisjoint(y), self._iterable,
            ))

    def intersection(self):
        '''intersection between inflow'''
        with self._flow():
            return self._xtend(reduce(
                lambda x, y: set(x).intersection(y), self._iterable,
            ))

    def subset(self):
        '''inflow that are subsets of inflow'''
        with self._flow():
            return self._append(reduce(
                lambda x, y: set(x).issubset(y), self._iterable,
            ))

    def superset(self):
        '''inflow that are supersets of inflow'''
        with self._flow():
            return self._append(reduce(
                lambda x, y: set(x).issubset(y), self._iterable
            ))

    def union(self):
        '''union between inflow'''
        with self._flow():
            return self._xtend(
                reduce(lambda x, y: set(x).union(y), self._iterable)
            )

    def unique(self):
        '''
        list unique inflow, preserving order and remember all inflow
        things ever seen
        '''
        def unique(iterable, key=None):
            seen = set()
            seen_add_, key_ = seen.add, key
            for element in iterable:
                k = key_(element)
                if k not in seen:
                    seen_add_(k)
                    yield element
        with self._flow():
            return self._iter(unique(self._iterable, self._call))


class SliceMixin(local):

    '''slicing mixin'''

    def first(self, n=0):
        '''
        first `n` things of inflow or just the first thing

        @param n: number of things (default: 0)
        '''
        with self._flow():
            if n:
                return self._xtend(islice(self._iterable, n))
            return self._append(next(self._iterable))

    def last(self, n=0):
        '''
        last `n` things of inflow or just the last thing

        @param n: number of things (default: 0)
        '''
        with self._flow():
            i1, i2 = tee(self._iterable)
            if n:
                return self._xtend(islice(i1, len(list(i2)) - n, None))
            return self._append(deque(i1, maxlen=1).pop())

    def nth(self, n, default=None):
        '''
        `nth` inflow thing in inflow or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._flow():
            return self._append(
                next(islice(self._iterable, n, None), default)
            )

    def head(self):
        '''all inflow except the last thing'''
        with self._flow():
            i1, i2 = tee(self._iterable)
            return self._xtend(islice(i1, len(list(i2)) - 1))

    def rest(self):
        '''all inflow except the first thing'''
        with self._flow():
            return self._xtend(islice(self._iterable, 1, None))
