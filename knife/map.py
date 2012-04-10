# -*- coding: utf-8 -*-
'''knife mapping mixins'''

from copy import deepcopy
from threading import local
from operator import methodcaller

from knife.compat import (
    imap, istarmap, irepeat, iproduct, icombinations, ipermutations)


class RepeatMixin(local):

    '''repetition mixin'''

    @staticmethod
    def _combinations(n, combinations_=icombinations):
        def combinations(iterable):
            return combinations_(iterable, n)
        return combinations

    @staticmethod
    def _copy(iterable, deepcopy_=deepcopy, imap_=imap):
        return imap_(deepcopy_, iterable)

    @staticmethod
    def _product(n=1, product_=iproduct):
        def product(iterable):
            return product_(*iterable, repeat=n)
        return product

    @staticmethod
    def _permutations(n, permutations_=ipermutations):
        def permutations(iterable):
            return permutations_(iterable, n)
        return permutations

    @staticmethod
    def _repeat(n, repeat_=irepeat, tuple_=tuple):
        def repeat(iterable):
            return repeat_(tuple_(iterable), n)
        return repeat

    @staticmethod
    def _times(call, n=None, r=irepeat, l=list, s=istarmap):
        def times(iterable):
            return (
                s(call, r(l(iterable))) if n is None
                else s(call, r(l(iterable), n))
            )
        return times

    def combinations(self, n):
        '''
        repeat every combination for `n` of incoming

        @param n: number of repetitions
        '''
        with self._flow():
            return self._many(self._combinations(n))

    def copy(self):
        '''copy each incoming thing'''
        with self._flow():
            return self._many(self._copy)

    def product(self, n=1):
        '''
        nested for each loops repeated `n` times

        @param n: number of repetitions (default: 1)
        '''
        with self._flow():
            return self._many(self._product(n))

    def permutations(self, n):
        '''
        repeat every permutation for every `n` of incoming

        @param n: length of thing to permutate
        '''
        with self._flow():
            return self._many(self._permutations(n))

    def repeat(self, n):
        '''
        repeat incoming `n` times

        @param n: number of times to repeat
        '''
        with self._flow():
            return self._many(self._repeat(n))

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
    def _invoke(name, args, mc_=methodcaller, imap_=imap):
        caller = mc_(name, *args[0], **args[1])
        def invoke(thing): #@IgnorePep8
            results = caller(thing)
            return thing if results is None else results
        def invoke_(iterable): #@IgnorePep8
            return imap_(invoke, iterable)
        return invoke_

    @staticmethod
    def _map(call, args, kwargs, imap_=imap, starmap_=istarmap):
        if kwargs:
            call_ = lambda x, y: call(*x, **y)
        else:
            call_ = call
        if args:
            def starmap(iterable): #@IgnorePep8
                return starmap_(call_, iterable)
            return starmap
        else:
            def map(iterable): #@IgnorePep8
                return imap_(call_, iterable)
            return map

    def invoke(self, name):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        '''
        with self._flow():
            return self._many(
                self._invoke(name, (self._args, self._kw))
            )

    def map(self, args=False, kwargs=False):
        '''
        invoke call on each incoming thing

        @param args: map each incoming thing as python *args for call
        @param kwargs: map each incoming thing as python **kwargs for call
        '''
        args = kwargs if kwargs else args
        with self._flow():
            return self._many(self._map(self._call, args, kwargs))
