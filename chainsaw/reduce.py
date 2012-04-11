# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from threading import local

from stuf.six import u


class ReduceMixin(local):

    '''reduce mixin'''

    def concat(self):
        '''Merge many iterables into one iterables.'''
        with self._chain():
            return self._many(self._concat)

    def flatten(self):
        '''
        Reduce an iterable of nested things to an iterable of unnested
        things.
        '''
        with self._chain():
            return self._many(self._flatten)

    def join(self, separator=u(''), encoding='utf-8', errors='strict'):
        '''
        Combine an iterable into one :class:`unicode` (:class:`str` on Python
        3) regardless of type.

        :param separator: string to join at (*default:*: ``''``)

        :param encoding: Unicode encoding for things (*default:*: ``'utf-8'``)

        :param errors: error handling when encoding things (*default:*:
          ``'strict'``)
        '''
        with self._chain():
            return self._one(self._join(separator, encoding, errors))

    def reduce(self, initial=None, reverse=False):
        '''
        Reduce an iterable down to one thing using the current callable. If
        ``reverse`` is set to ``True``, reduction comes from the right side of
        the iterable. Otherwise, reduction comes from the left side of the
        iterable.

        :param initial: starting value (*default:*: ``None``)

        :param reverse: reduce from right side of iterable (*default:*:
          ``False``)
        '''
        with self._chain():
            return self._one(self._reduce(self._call, initial, reverse))

    def weave(self):
        '''Interleave multiple iterables into one iterable.'''
        with self._chain():
            return self._many(self._roundrobin)

    def zip(self):
        '''
        Reduce a iterables down to one thing, pairing each things by
        their position within the iterable.
        '''
        with self._chain():
            return self._many(self._zip)


class SliceMixin(local):

    '''slicing mixin'''

    def first(self, n=0):
        '''
        Return either `n` things from the start of an iterable or just the
        first thing in the iterable.

        :param n: number of things (*default:*: ``0``)
        '''
        with self._chain():
            first = self._first
            return self._many(first(n)) if n else self._one(first(n))

    def initial(self):
        '''Return everything in an iterable except the very **last** thing.'''
        with self._chain():
            return self._many(self._initial)

    def last(self, n=0):
        '''
        Return either `n` things from the end of an iterable or just the
        **last** thing.

        :param n: number of things (*default:*: ``0``)
        '''
        with self._chain():
            last = self._last
            return self._many(last(n)) if n else self._one(last(n))

    def at(self, n, default=None):
        '''
        Return thing at `n` index within an iterable or `default` if nothing is
        found at `n` index.

        :param n: index of some thing

        :param default: default thing (*default:*: ``None``)
        '''
        with self._chain():
            return self._one(self._nth(n, default))

    def rest(self):
        '''Return everything in an iterable except the very **first** thing.'''
        with self._chain():
            return self._many(self._rest)

    def slice(self, start, stop=False, step=False):
        '''
        Slice an iterable down to a certain size.

        :param start: starting index of slice

        :param stop: stopping index of slice (*default:* ``False``)

        :param step: size of step in slice (*default:* ``False``)
        '''
        with self._chain():
            return self._many(self._slice(start, stop, step))

    def split(self, n, fill=None):
        '''
        Split an iterable into multiple iterables of length `n` while using
        `fill` value to pad out any incomplete iterables.

        :param n: number of things per split (*default:*  ``0``)

        :param fill: value to pad out incomplete iterables with (*default*:
          ``None``)
        '''
        with self._chain():
            return self._many(self._split(n, fill))
