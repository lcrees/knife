# -*- coding: utf-8 -*-
'''knife reducing mixins'''

from threading import local
from collections import deque
from functools import partial, reduce
from itertools import cycle, islice, groupby

from stuf.six import strings, u
from knife.compat import imap, ichain, tounicode, zip_longest


class ReduceMixin(local):

    '''reduce mixin'''

    @staticmethod
    def _concat(iterable, ichain_=ichain):
        return ichain_(iterable)

    @classmethod
    def _flatten(cls, iterable, strings_=strings, isinstance_=isinstance):
        smash_ = cls._flatten
        for item in iterable:
            try:
                # don't recur over strings
                if isinstance_(item, strings_):
                    yield item
                else:
                    # do recur over other things
                    for j in smash_(item):
                        yield j
            except TypeError:
                # does not recur
                yield item

    @staticmethod
    def _join(sep, encoding, errors, imap_=imap, tounicode_=tounicode):
        def join(iterable):
            return tounicode(
                sep.join(imap_(tounicode_, iterable)), encoding, errors,
            )
        return join

    @staticmethod
    def _reduce(call, initial, reverse, reduce_=reduce):
        if reverse:
            if initial is None:
                def reduceright(iterable):
                    return reduce_(lambda x, y: call(y, x), iterable)
                return reduceright
            else:
                def reduceright(iterable):
                    return reduce_(lambda x, y: call(y, x), iterable, initial)
                return reduceright
        if initial is None:
            def _reduce(iterable):
                return reduce_(call, iterable)
        else:
            def _reduce(iterable):
                return reduce_(call, iterable, initial)
        return _reduce

    @classmethod
    def _roundrobin(cls, itrble, i=iter, n=next, s=islice, c=cycle, p=partial):
        work, measure = cls._clone(itrble)
        nexts = c(p(n, i(item)) for item in work)
        pending = len(measure)
        while pending:
            try:
                for nextz in nexts:
                    yield nextz()
            except StopIteration:
                pending -= 1
                nexts = c(s(nexts, pending))

    @staticmethod
    def _zip(iterable, zip_=zip_longest):
        return zip_(*iterable)

    def concat(self):
        '''concatenate incoming together'''
        with self._flow():
            return self._multi(self._concat)

    def flatten(self):
        '''flatten nested incoming'''
        with self._flow():
            return self._multi(self._flatten)

    def join(self, sep=u(''), encoding='utf-8', errors='strict'):
        '''
        join incoming into one unicode string (regardless of type)

        @param sep: join separator (default: '')
        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._flow():
            return self._single(self._join(sep, encoding, errors))

    def reduce(self, initial=None, reverse=False):
        '''
        reduce incoming to one thing using current callable (from left
        side of incoming)

        @param initial: initial thing (default: None)
        @param reverse: reduce from right side of incoming things
        '''
        with self._flow():
            return self._single(self._reduce(self._call, initial, reverse))

    def roundrobin(self):
        '''interleave incoming into one thing'''
        with self._flow():
            return self._multi(self._roundrobin)

    def zip(self):
        '''
        smash incoming into one single thing, pairing things by iterable
        position
        '''
        with self._flow():
            return self._multi(self._zip)


class SliceMixin(local):

    '''slicing mixin'''

    @staticmethod
    def _first(n, islice_=islice, next_=next):
        def first(iterable):
            return islice_(iterable, n) if n else next_(iterable)
        return first

    @staticmethod
    def _groupby(key, imap_=imap, tuple_=tuple, groupby_=groupby):
        def grouper(x):
            return (x[0], tuple_(x[1]))
        def groupby__(iterable): #@IgnorePep8
            return imap_(grouper, groupby_(iterable, key))
        return groupby__

    @classmethod
    def _initial(cls, iterable, islice_=islice, len_=len, list_=list):
        i1, i2 = cls._clone(iterable)
        return islice_(i1, len_(list_(i2)) - 1)

    @classmethod
    def _last(cls, n, s=islice, d=deque, ln=len, l=list):
        def last(iterable):
            i1, i2 = cls._clone(iterable)
            return s(i1, ln(l(i2)) - n, None) if n else d(i1, maxlen=1).pop()
        return last

    @staticmethod
    def _nth(n, default, islice_=islice, next_=next):
        def nth(iterable):
            return next_(islice_(iterable, n, None), default)
        return nth

    @staticmethod
    def _rest(iterable, _islice=islice):
        return _islice(iterable, 1, None)

    def first(self, n=0):
        '''
        first `n` things of incoming or just the first thing

        @param n: number of things (default: 0)
        '''
        with self._flow():
            first = self._first
            return self._multi(first(n)) if n else self._single(first())

    def groupby(self):
        '''
        group incoming, optionally using current call for key function
        '''
        with self._flow():
            return self._multi(self._groupby(self._identity))

    def initial(self):
        '''all incoming except the last thing'''
        with self._flow():
            return self._multi(self._initial)

    def last(self, n=0):
        '''
        last `n` things of incoming or just the last thing

        @param n: number of things (default: 0)
        '''
        with self._flow():
            last = self._last
            return self._multi(last(n)) if n else self._single(last(n))

    def nth(self, n, default=None):
        '''
        `nth` incoming thing in incoming or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._flow():
            return self._single(self._nth(n, default))

    def rest(self):
        '''all incoming except the first thing'''
        with self._flow():
            return self._multi(self._rest)

    @staticmethod
    def _split(n, fill, zip_longest_=zip_longest, iter_=iter):
        def grouper(iterable):
            return zip_longest_(fillvalue=fill, *[iter_(iterable)] * n)
        return grouper

    def split(self, n, fill=None):
        '''
        split incoming into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        with self._flow():
            return self._multi(self._split(n, fill))
