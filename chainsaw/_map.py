# -*- coding: utf-8 -*-
'''chainsaw mapping mixins'''

from copy import deepcopy
from threading import local
from functools import partial
from operator import methodcaller

from chainsaw._compat import (
    imap, istarmap, irepeat, iproduct, icombinations, ipermutations)


class _RepeatMixin(local):

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
    def _repeat(n, usecall, call, r=irepeat, tuple_=tuple, l=list, s=istarmap):
        if usecall:
            if n is None:
                return lambda x: s(call, r(l(x)))
            return lambda x: s(call, r(l(x), n))
        else:
            def repeat(iterable):
                return r(tuple_(iterable), n)
            return repeat


class _MapMixin(local):

    '''mapping mixin'''

    @staticmethod
    def _invoke(name, args, mc_=methodcaller, imap_=imap):
        caller = mc_(name, *args[0], **args[1])
        def invoke_(iterable): #@IgnorePep8
            def invoke(thing): #@IgnorePep8
                results = caller(thing)
                return thing if results is None else results
            return imap_(invoke, iterable)
        return invoke_

    @staticmethod
    def _map(call, args, kwargs, curr, arg, kw, imap_=imap, starmap_=istarmap):
        if kwargs:
            call_ = lambda x, y: call(*x, **y)
        elif curr:
            call = partial(lambda x, y: call(*x, **y), arg, kw)
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
