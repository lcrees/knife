# -*- coding: utf-8 -*-
'''knife mapping mixins'''

from time import sleep
from copy import deepcopy
from threading import local
from operator import methodcaller

from knife.compat import (
    imap, ichain, irange, istarmap, irepeat, iproduct, icombinations, ikeys,
    ipermutations, ivalues, iitems)


class RepeatMixin(local):

    '''repetition mixin'''

    @staticmethod
    def _combinations(n, combinations_=icombinations):
        def combinations(iterable):
            return combinations_(iterable, n)
        return combinations

    def combinations(self, n):
        '''
        repeat every combination for `n` of incoming

        @param n: number of repetitions
        '''
        with self._flow():
            return self._many(self._combinations(n))

    @staticmethod
    def _copy(iterable, deepcopy_=deepcopy, imap_=imap):
        return imap_(deepcopy_, iterable)

    def copy(self):
        '''copy each incoming thing'''
        with self._flow():
            return self._many(self._copy)

    @staticmethod
    def _product(n=1, product_=iproduct):
        def product(iterable):
            return product_(*iterable, repeat=n)
        return product

    def product(self, n=1):
        '''
        nested for each loops repeated `n` times

        @param n: number of repetitions (default: 1)
        '''
        with self._flow():
            return self._many(self._product(n))

    @staticmethod
    def _permutations(n, permutations_=ipermutations):
        def permutations(iterable):
            return permutations_(iterable, n)
        return permutations

    def permutations(self, n):
        '''
        repeat every permutation for every `n` of incoming

        @param n: length of thing to permutate
        '''
        with self._flow():
            return self._many(self._permutations(n))

    def range(self, start, stop=0, step=1):
        '''
        put sequence of numbers in incoming

        @param start: number to start with
        @param stop: number to stop with (default: 0)
        @param step: number of steps to advance per iteration (default: 1)
        '''
        with self._flow():
            return self._many(
                irange(start, stop, step) if stop else irange(start)
            )

    @staticmethod
    def _repeat(n, repeat_=irepeat, tuple_=tuple):
        def repeat(iterable):
            return repeat_(tuple_(iterable), n)
        return repeat

    def repeat(self, n):
        '''
        repeat incoming `n` times

        @param n: number of times to repeat
        '''
        with self._flow():
            return self._many(self._repeat(n))

    @staticmethod
    def _times(call, n=None, r=irepeat, l=list, s=istarmap):
        def times(iterable):
            return (
                s(call, r(l(iterable))) if n is None
                else s(call, r(l(iterable), n))
            )
        return times

    def times(self, n=None):
        '''
        repeat call with incoming `n` times

        @param n: repeat call n times on incoming (default: None)
        '''
        with self._flow():
            return self._many(self._times(self._call, n))


class MapMixin(local):

    '''mapping mixin'''

    @staticmethod
    def _each(call, wait, starmap_=istarmap, sleep_=sleep):
        if wait:
            def delay_each(x, y, wait=wait, caller=call):
                sleep_(wait)
                return caller(*x, **y)
            call_ = delay_each
        else:
            call_ = lambda x, y: call(*x, **y)
        def each(iterable): #@IgnorePep8
            return starmap_(call_, iterable)
        return each

    def each(self, wait=0):
        '''
        invoke call with passed arguments, keywords in incoming

        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._many(self._each(self._call, wait))

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
        def invoke_(iterable): #@IgnorePep8
            return m(invoke, iterable)
        return invoke_

    def invoke(self, name, wait=0):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._many(
                self._invoke(name, (self._args, self._kw), wait)
            )

    @staticmethod
    def _items(call, m=imap, c=ichain, i=iitems, s=istarmap):
        def items(iterable):
            return s(call, c(m(i, iterable)))
        return items

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        with self._flow():
            return self._many(self._items(self._call))

    @staticmethod
    def _keys(call, m=imap, c=ichain, k=ikeys, s=istarmap):
        def keys(iterable):
            return s(call, c(m(k, iterable)))
        return keys

    def keys(self):
        '''invoke call on each mapping to get keys'''
        with self._flow():
            return self._many(self._keys(self._call))

    @staticmethod
    def _map(call, wait, sleep_=sleep, imap_=imap):
        if wait:
            def call_(x, wait=wait, caller=call):
                sleep_(wait)
                return caller(x)
        else:
            call_ = call
        def map(iterable): #@IgnorePep8
            return imap_(call_, iterable)
        return map

    def map(self, wait=0):
        '''
        invoke call on each incoming thing

        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._many(self._map(self._call, wait))

    @staticmethod
    def _starmap(call, wait=0, sleep_=sleep, starmap_=istarmap):
        if wait:
            def call_(x, wait=wait, caller=call):
                sleep_(wait)
                return caller(x)
        else:
            call_ = call
        def starmap(iterable): #@IgnorePep8
            return starmap_(call_, iterable)
        return starmap

    def starmap(self, wait=0):
        '''
        invoke call on each sequence of incoming

        @param wait: time in seconds (default: 0)
        '''
        with self._flow():
            return self._many(self._starmap(self._call, wait))

    @staticmethod
    def _values(call, m=imap, c=ichain, v=ivalues, s=istarmap):
        def values(iterable):
            return s(call, c(m(v, iterable)))
        return values

    def values(self):
        '''invoke call on each mapping to get values'''
        with self._flow():
            return self._many(self._values(self._call))
