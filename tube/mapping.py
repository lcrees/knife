# -*- coding: utf-8 -*-
'''tube mapping mixins'''

from time import sleep
from copy import deepcopy
from threading import local
from operator import methodcaller
from itertools import starmap, repeat, product, combinations, permutations

from stuf.six import keys, values, items
from tube.compat import imap, ichain, xrange


class RepeatMixin(local):

    '''repetition mixin'''

    @staticmethod
    def _combinations(n, combinations_=combinations):
        def combinations__(iterable):
            return combinations_(iterable, n)
        return combinations__

    @staticmethod
    def _copy(iterable, deepcopy_=deepcopy, imap_=imap):
        return imap_(deepcopy_, iterable)

    @staticmethod
    def _product(n=1, product_=product):
        def product__(iterable):
            return product_(*iterable, repeat=n)
        return product__

    @staticmethod
    def _permutations(n, permutations_=permutations):
        def permutations__(iterable):
            return permutations_(iterable, n)
        return permutations__

    @staticmethod
    def _repeat(n, repeat_=repeat, tuple_=tuple):
        def repeat__(iterable):
            return repeat_(tuple_(iterable), n)
        return repeat__

    @staticmethod
    def _times(call, n=None, r=repeat, l=list, s=starmap):
        def times__(iterable):
            return (
                s(call, r(l(iterable))) if n is None
                else s(call, r(l(iterable), n))
            )
        return times__

    def combinations(self, n):
        '''
        repeat every combination for `n` of inflow

        @param n: number of repetitions
        '''
        with self._flow():
            return self._xtend(self._combinations(n))

    def copy(self):
        '''copy each inflow thing'''
        with self._flow():
            return self._xtend(self._copy)

    def product(self, n=1):
        '''
        nested for each loops repeated `n` times

        @param n: number of repetitions (default: 1)
        '''
        with self._flow():
            return self._xtend(self._product(n))

    def permutations(self, n):
        '''
        repeat every permutation for every `n` of inflow

        @param n: length of thing to permutate
        '''
        with self._flow():
            return self._xtend(self._permutations(n))

    def range(self, start, stop=0, step=1):
        '''
        put sequence of numbers in inflow

        @param start: number to start with
        @param stop: number to stop with (default: 0)
        @param step: number of steps to advance per iteration (default: 1)
        '''
        with self._flow():
            return self._xtend(
                xrange(start, stop, step) if stop else xrange(start)
            )

    def repeat(self, n):
        '''
        repeat inflow `n` times

        @param n: number of times to repeat
        '''
        with self._flow():
            return self._xtend(self._repeat(n))

    def times(self, n=None):
        '''
        repeat call with inflow `n` times

        @param n: repeat call n times on inflow (default: None)
        '''
        with self._flow():
            return self._xtend(self._times(self._call, n))


class MapMixin(local):

    '''mapping mixin'''

    @staticmethod
    def _each(call, wait, starmap_=starmap, sleep_=sleep):
        if wait:
            def delay_each(x, y, wait=wait, caller=call):
                sleep_(wait)
                return caller(*x, **y)
            call_ = delay_each
        else:
            call_ = lambda x, y: call(*x, **y)
        def each__(iterable):
            return starmap_(call_, iterable)
        return each__

    @staticmethod
    def _invoke(name, args, wait, mc=methodcaller, sleep=sleep, m=imap):
        caller = mc(name, *args[0], **args[1])
        if wait:
            def invoke(x, wait=0):
                sleep(wait)
                results = caller(x)
                return x if results is None else results
        else:
            def invoke(thing):
                results = caller(thing)
                return thing if results is None else results
        def invoke__(iterable):
            return m(invoke, iterable)
        return invoke__

    @staticmethod
    def _items(call, m=imap, c=ichain, i=items, s=starmap):
        def items__(iterable):
            return s(call, c(m(i, iterable)))
        return items__

    @staticmethod
    def _keys(call, m=imap, c=ichain, k=keys, s=starmap):
        def keys__(iterable):
            return s(call, c(m(k, iterable)))
        return keys__

    @staticmethod
    def _map(call, wait, sleep_=sleep, imap_=imap):
        if wait:
            def call_(x, wait=wait, caller=call):
                sleep_(wait)
                return caller(x)
        else:
            call_ = call
        def map__(iterable):
            return imap_(call_, iterable)
        return map__

    @staticmethod
    def _starmap(call, wait=0, sleep_=sleep, starmap_=starmap):
        if wait:
            def call_(x, wait=wait, caller=call):
                sleep_(wait)
                return caller(x)
        else:
            call_ = call
        def starmap__(iterable):
            return starmap_(call_, iterable)
        return starmap__

    @staticmethod
    def _values(call, m=imap, c=ichain, v=values, s=starmap):
        def values__(iterable):
            return s(call, c(m(v, iterable)))
        return values__

    def each(self, wait=0):
        '''
        invoke call with passed arguments, keywords in inflow

        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._xtend(self._each(self._call, wait))

    def invoke(self, name, wait=0):
        '''
        invoke method `name` on each inflow thing with passed arguments,
        keywords but return inflow thing instead if method returns `None`

        @param name: name of method
        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._xtend(
                self._invoke(name, (self._args, self._kw), wait)
            )

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        with self._flow():
            return self._xtend(self._items(self._call))

    def keys(self):
        '''invoke call on each mapping to get keys'''
        with self._flow():
            return self._xtend(self._keys(self._call))

    def map(self, wait=0):
        '''
        invoke call on each inflow thing
        
        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._xtend(self._map(self._call, wait))

    def starmap(self, wait=0):
        '''
        invoke call on each sequence of inflow
        
        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._xtend(self._starmap(self._call, wait))

    def values(self):
        '''invoke call on each mapping to get values'''
        with self._flow():
            return self._xtend(self._values(self._call))
