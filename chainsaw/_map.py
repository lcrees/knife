# -*- coding: utf-8 -*-
'''chainsaw mapping mixins'''

from copy import deepcopy
from threading import local
from operator import methodcaller
from itertools import starmap, repeat, combinations, permutations

from chainsaw._compat import imap


class _RepeatMixin(local):

    '''repetition mixin'''

    @staticmethod
    def _combinations(n, combinations_=combinations):
        return lambda x: combinations_(x, n)

    @staticmethod
    def _copy(iterable, deepcopy_=deepcopy, imap_=imap):
        return imap_(deepcopy_, iterable)

    @staticmethod
    def _permutations(n, permutations_=permutations):
        return lambda x: permutations_(x, n)

    @staticmethod
    def _repeat(n, usecall, call, r=repeat, tuple_=tuple, l=list, s=starmap):
        if usecall:
            return lambda x: s(call, r(l(x), n))
        return lambda x: r(tuple_(x), n)


class _MapMixin(local):

    '''mapping mixin'''

    @staticmethod
    def _argmap(call, curr, arg, kw, starmap_=starmap):
        if curr:
            def argmap(*args):
                return call(*(args + arg))
        else:
            argmap = call
        return lambda x: starmap_(argmap, x)

    @staticmethod
    def _invoke(name, args, mc_=methodcaller, imap_=imap):
        caller = mc_(name, *args[0], **args[1])
        def invoke(thing): #@IgnorePep8
            results = caller(thing)
            return thing if results is None else results
        return lambda x: imap_(invoke, x)

    @staticmethod
    def _kwargmap(call, curr, arg, kw, starmap_=starmap):
        if curr:
            def kwargmap(*arguments):
                args, kwargs = arguments
                kwargs.update(kw)
                return call(*(args + arg), **kwargs)
        else:
            kwargmap = lambda x, y: call(*x, **y)
        return lambda x: starmap_(kwargmap, x)

    @staticmethod
    def _map(call, imap_=imap):
        return lambda x: imap_(call, x)
