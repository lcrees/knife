# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from threading import local

from stuf.six import u


class ReduceMixin(local):

    '''reduce mixin'''

    def concat(self):
        '''concatenate incoming together'''
        with self._chain():
            return self._many(self._concat)

    def flatten(self):
        '''flatten nested incoming'''
        with self._chain():
            return self._many(self._flatten)

    def join(self, sep=u(''), encoding='utf-8', errors='strict'):
        '''
        join incoming into one unicode string (regardless of type)

        @param sep: join separator (default: '')
        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._chain():
            return self._one(self._join(sep, encoding, errors))

    def reduce(self, initial=None, reverse=False):
        '''
        reduce incoming to one thing using current callable (from left
        side of incoming)

        @param initial: initial thing (default: None)
        @param reverse: reduce from right side of incoming things
        '''
        with self._chain():
            return self._one(self._reduce(self._call, initial, reverse))

    def weave(self):
        '''interleave incoming into one thing'''
        with self._chain():
            return self._many(self._roundrobin)

    def zip(self):
        '''
        smash incoming into one single thing, pairing things by iterable
        position
        '''
        with self._chain():
            return self._many(self._zip)


class SliceMixin(local):

    '''slicing mixin'''

    def first(self, n=0):
        '''
        first `n` things of incoming or just the first thing

        @param n: number of things (default: 0)
        '''
        with self._chain():
            first = self._first
            return self._many(first(n)) if n else self._one(first(n))

    def initial(self):
        '''all incoming except the last thing'''
        with self._chain():
            return self._many(self._initial)

    def last(self, n=0):
        '''
        last `n` things of incoming or just the last thing

        @param n: number of things (default: 0)
        '''
        with self._chain():
            last = self._last
            return self._many(last(n)) if n else self._one(last(n))

    def nth(self, n, default=None):
        '''
        `nth` incoming thing in incoming or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._chain():
            return self._one(self._nth(n, default))

    def rest(self):
        '''all incoming except the first thing'''
        with self._chain():
            return self._many(self._rest)

    def slice(self, start, stop=None, step=None):
        '''
        split incoming into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        with self._chain():
            return self._many(self._split(start, stop, step))

    def split(self, n, fill=None):
        '''
        split incoming into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        with self._chain():
            return self._many(self._split(n, fill))
