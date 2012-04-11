# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from threading import local

from stuf.six import u


class ReduceMixin(local):

    '''reduce mixin'''

    def concat(self):
        '''Concatenate a series of things into one series of things.'''
        with self._chain():
            return self._many(self._concat)

    def flatten(self):
        '''Flatten a series of nested things into a flat series of things.'''
        with self._chain():
            return self._many(self._flatten)

    def join(self, separator=u(''), encoding='utf-8', errors='strict'):
        '''
        Combine a series of stringish things join into one unicode string
        (regardless of the original string type).

        @param separator: string to join at (default: '')
        @param encoding: encoding for stringish things (default: 'utf-8')
        @param errors: error handling when encoding stringish things
            (default: 'strict')
        '''
        with self._chain():
            return self._one(self._join(separator, encoding, errors))

    def reduce(self, initial=None, reverse=False):
        '''
        Reduce a series of things down to one thing using the current callable.
        If `reverse` flag is set, reduction will come from the right side of
        the series. Otherwise, reduction will come from the left side of the
        series.

        @param initial: initial thing (default: `None`)
        @param reverse: reduce from right side of things (default: `False`)
        '''
        with self._chain():
            return self._one(self._reduce(self._call, initial, reverse))

    def weave(self):
        '''Interleave a series of things into one thing.'''
        with self._chain():
            return self._many(self._roundrobin)

    def zip(self):
        '''
        Reduce of a series of things down to one thing, pairing each things by
        their position in the series.
        '''
        with self._chain():
            return self._many(self._zip)


class SliceMixin(local):

    '''slicing mixin'''

    def first(self, n=0):
        '''
        Return either the specified number of things from the beginning of a
        series of things or just the first thing.

        @param n: number of things (default: 0)
        '''
        with self._chain():
            first = self._first
            return self._many(first(n)) if n else self._one(first(n))

    def initial(self):
        '''
        Return everything within a series of things except the very last thing
        within the series of things.
        '''
        with self._chain():
            return self._many(self._initial)

    def last(self, n=0):
        '''
        Return either the specified number of things from the end of a series
        of things or just the last thing.

        @param n: number of things (default: 0)
        '''
        with self._chain():
            last = self._last
            return self._many(last(n)) if n else self._one(last(n))

    def index(self, n, default=None):
        '''
        Return each thing at a specified index in a series of incoming things
        or the passed default thing.

        @param n: index of thing
        @param default: default thing (default: `None`)
        '''
        with self._chain():
            return self._one(self._nth(n, default))

    def rest(self):
        '''
        Return everything within a series of things except the very first thing
        within the series of things.
        '''
        with self._chain():
            return self._many(self._rest)

    def slice(self, start, stop=False, step=False):
        '''
        Slice a series of things down to a certain size.

        @param start: starting point of slice
        @param stop: stopping point of slice (default: `False`)
        @param step: size of step in slice (default: `False`)
        '''
        with self._chain():
            return self._many(self._slice(start, stop, step))

    def split(self, n, fill=None):
        '''
        Split a series of things into series of things of a specified length
        using `fill` argument to pad out incomplete series.

        @param n: number of things per split
        @param fill: value to pad out incomplete things (default: `None`)
        '''
        with self._chain():
            return self._many(self._split(n, fill))
