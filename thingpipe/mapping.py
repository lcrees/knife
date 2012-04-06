# -*- coding: utf-8 -*-
'''thingpipe mapping mixins'''

from time import sleep
from copy import deepcopy
from threading import local
from operator import methodcaller
from itertools import starmap, repeat, product, combinations, permutations

from stuf.six import keys, values, items
from thingpipe.compat import imap, ichain, xrange


class RepeatMixin(local):

    '''repetition mixin'''

    def combinations(self, n):
        '''
        repeat every combination for `n` of incoming things

        @param n: number of repetitions
        '''
        with self._context():
            return self._xtend(combinations(self._iterable, n))

    def copy(self):
        '''copy each incoming thing'''
        with self._context():
            return self._xtend(imap(deepcopy, self._iterable))

    def product(self, n=1):
        '''
        nested for each loops repeated `n` times

        @param n: number of repetitions (default: 1)
        '''
        with self._context():
            return self._xtend(product(*self._iterable, repeat=n))

    def permutations(self, n):
        '''
        repeat every permutation for every `n` of incoming things

        @param n: length of thing to permutate
        '''
        with self._context():
            return self._xtend(permutations(self._iterable, n))

    def range(self, start, stop=0, step=1):
        '''
        put sequence of numbers in incoming things

        @param start: number to start with
        @param stop: number to stop with (default: 0)
        @param step: number of steps to advance per iteration (default: 1)
        '''
        with self._context():
            return self._xtend(
                xrange(start, stop, step) if stop else xrange(start)
            )

    def repeat(self, n):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._context():
            return self._xtend(repeat(tuple(self._iterable), n))

    def times(self, n=None):
        '''
        repeat call with incoming things `n` times

        @param n: repeat call n times on incoming things (default: None)
        '''
        with self._context():
            if n is None:
                return self._xtend(starmap(
                    self._call, repeat(list(self._iterable)),
                ))
            return self._xtend(starmap(
                self._call, repeat(list(self._iterable), n),
            ))


class MapMixin(local):

    '''mapping mixin'''

    def each(self, wait=0):
        '''
        invoke call with passed arguments, keywords in incoming things

        @param wait: time in seconds (default: 0)
        '''
        call = self._call
        if wait:
            def delay_each(x, y, wait=0, caller=None):
                sleep(wait)
                return caller(*x, **y)
            de = delay_each
            call_ = lambda x, y: de(x, y, wait, call)
        else:

            call_ = lambda x, y: call(*x, **y)
        with self._context():
            return self._xtend(starmap(call_, self._iterable))

    def invoke(self, name, wait=0):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        @param wait: time in seconds (default: 0)
        '''
        caller = methodcaller(name, *self._args, **self._kw)
        def invoke(thing):
            results = caller(thing)
            return thing if results is None else results
        if wait:
            def invoke(x, wait=0):
                sleep(wait)
                results = caller(x)
                return x if results is None else results
        with self._context():
            return self._xtend(imap(invoke, self._iterable))

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        with self._context():
            return self._xtend(starmap(
                self._call, ichain(imap(items, self._iterable))
            ))

    def keys(self):
        '''invoke call on each mapping to get keys'''
        with self._context():
            return self._xtend(starmap(
                self._call, ichain(imap(keys, self._iterable))
            ))

    def map(self, wait=0):
        '''
        invoke call on each incoming thing
        
        @param wait: time in seconds (default: 0)
        '''
        call_ = self._call
        if wait:
            def delay_map(x, wait=None, caller=None):
                sleep(wait)
                return caller(x)
            call = self._call
            call_ = lambda x: delay_map(x, wait, call)
        with self._context():
            return self._xtend(imap(call_, self._iterable))

    def starmap(self):
        '''invoke call on each sequence of incoming things'''
        with self._context():
            return self._xtend(starmap(self._call, self._iterable))

    def values(self):
        '''invoke call on each mapping to get values'''
        with self._context():
            return self._xtend(starmap(
                self._call, ichain(imap(values, self._iterable))
            ))
