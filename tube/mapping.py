# -*- coding: utf-8 -*-
'''tube mapping mixins'''

from time import sleep
from copy import deepcopy
from threading import local
from operator import methodcaller
from itertools import starmap, repeat, product, combinations, permutations

from stuf.six import keys, values, items
from tube.compat import imap, ichain, xrange


class BaseRepeat(local):

    '''base repetition'''

    @staticmethod
    def _combinations(iterable, n, combinations_=combinations):
        return combinations_(iterable, n)

    @staticmethod
    def _copy(iterable, deepcopy_=deepcopy, imap_=imap):
        return imap_(deepcopy_, iterable)

    @staticmethod
    def _product(iterable, n=1, product_=product):
        return product_(*iterable, repeat=n)

    @staticmethod
    def _permutations(iterable, n, permutations_=permutations):
        return permutations_(iterable, n)

    @staticmethod
    def _repeat(iterable, n, repeat_=repeat, tuple_=tuple):
        return repeat_(tuple_(iterable), n)

    @staticmethod
    def _times(call, iterable, n=None, r=repeat, l=list, s=starmap):
        return (
            s(call, r(l(iterable))) if n is None
            else s(call, r(l(iterable), n))
        )


class BaseRepeatMixin(local):

    '''repetition mixin'''

    def combinations(self, n):
        '''
        repeat every combination for `n` of inflow

        @param n: number of repetitions
        '''
        with self._flow():
            return self._xtend(self._combinations(self._iterable, n))

    def copy(self):
        '''copy each inflow thing'''
        with self._flow():
            return self._xtend(self._copy(self._iterable))

    def product(self, n=1):
        '''
        nested for each loops repeated `n` times

        @param n: number of repetitions (default: 1)
        '''
        with self._flow():
            return self._xtend(self._product(self._iterable, n))

    def permutations(self, n):
        '''
        repeat every permutation for every `n` of inflow

        @param n: length of thing to permutate
        '''
        with self._flow():
            return self._xtend(self._permutations(self._iterable, n))

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
            return self._xtend(self._repeat(self._iterable, n))

    def times(self, n=None):
        '''
        repeat call with inflow `n` times

        @param n: repeat call n times on inflow (default: None)
        '''
        with self._flow():
            return self._xtend(self._times(self._call, self._iterable, n))


class RepeatMixin(BaseRepeat, BaseRepeatMixin):

    '''repetition mixin'''


class BaseMap(local):

    '''mapping mixin'''

    @staticmethod
    def _each(call, iterable, wait, starmap_=starmap, sleep_=sleep):
        if wait:
            def delay_each(x, y, wait=wait, caller=call):
                sleep_(wait)
                return caller(*x, **y)
            call_ = delay_each
        else:
            call_ = lambda x, y: call(*x, **y)
        return starmap_(call_, iterable)

    @staticmethod
    def _invoke(name, iterable, args, wait=0, mc=methodcaller, sleep=sleep):
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
        return imap(invoke, iterable)

    @staticmethod
    def _items(call, iterable, m=imap, c=ichain, i=items, s=starmap):
        return s(call, c(m(i, iterable)))

    @staticmethod
    def _keys(call, iterable, m=imap, c=ichain, k=keys, s=starmap):
        return s(call, c(m(k, iterable)))

    @staticmethod
    def _map(call, iterable, wait=0, sleep_=sleep, imap_=imap):
        if wait:
            def call_(x, wait=wait, caller=call):
                sleep_(wait)
                return caller(x)
        else:
            call_ = call
        return imap_(call_, iterable)

    @staticmethod
    def _starmap(call, iterable, wait=0, sleep_=sleep, starmap_=starmap):
        if wait:
            def call_(x, wait=wait, caller=call):
                sleep_(wait)
                return caller(x)
        else:
            call_ = call
        return starmap_(call_, iterable)

    @staticmethod
    def _values(call, iterable, m=imap, c=ichain, v=values, s=starmap):
        return s(call, c(m(v, iterable)))


class BaseMapMixin(local):

    '''mapping mixin'''

    def each(self, wait=0):
        '''
        invoke call with passed arguments, keywords in inflow

        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._xtend(self._each(self._call, self._iterable, wait))

    def invoke(self, name, wait=0):
        '''
        invoke method `name` on each inflow thing with passed arguments,
        keywords but return inflow thing instead if method returns `None`

        @param name: name of method
        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._xtend(self._invoke(
                name, self._iterable, (self._args, self._kw), wait, 
            ))

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        with self._flow():
            return self._xtend(self._items(self._call, self._iterable))

    def keys(self):
        '''invoke call on each mapping to get keys'''
        with self._flow():
            return self._xtend(self._keys(self._call, self._iterable))

    def map(self, wait=0):
        '''
        invoke call on each inflow thing
        
        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._xtend(self._map(self._call, self._iterable, wait))

    def starmap(self, wait=0):
        '''
        invoke call on each sequence of inflow
        
        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._xtend(self._starmap(self._call, self._iterable, wait))

    def values(self):
        '''invoke call on each mapping to get values'''
        with self._flow():
            return self._xtend(self._values(self._call, self._iterable))


class MapMixin(BaseMap, BaseMapMixin):

    '''mapping mixin'''
