# -*- coding: utf-8 -*-
'''tube reducing mixins'''

from math import fsum
from threading import local
from itertools import cycle, islice
from functools import partial, reduce
from operator import contains, truediv

from stuf.six import strings, u
from tube.compat import (
    Counter, imap, izip, ichain, tounicode, iall, iany, imax, imin, isum,
    icontains)


class MathMixin(local):

    '''math mixin'''

    @classmethod
    def _average(cls, iterable, s=sum, t=truediv, n=len):
        i1, i2 = cls._clone(iterable)
        return t(s(i1, 0.0), n(list(i2)))

    def average(self):
        '''average value of inflow'''
        with self._flow():
            return self._one(self._average)

    @classmethod
    def _max(key, max=imax):
        def max(iterable):
            return max(iterable, key=key)
        return max

    def max(self):
        '''
        find maximum value among inflow using current callable as key
        function
        '''
        with self._flow():
            return self._one(self._max(self._identity))

    @staticmethod
    def _median(iterable, s=sorted, l=list, d=truediv, i=int, n=len):
        i = l(s(iterable))
        e = d(n(i) - 1, 2)
        p = i(e)
        return i[p] if e % 2 == 0 else truediv(i[p] + i[p + 1], 2)

    def median(self):
        '''median value of inflow'''
        with self._flow():
            return self._one(self._median)

    @classmethod
    def _min(key, min=imin):
        def min(iterable):
            return min(iterable, key=key)
        return min

    def min(self):
        '''
        find minimum value among inflow using current callable as key
        function
        '''
        with self._flow():
            return self._one(self._min(self._identity))

    @classmethod
    def _minmax(cls, iterable, iter_=iter, min=imin, max=imax):
        i1, i2 = cls._clone(iterable)
        return iter_((min(i1), max(i2)))

    def minmax(self):
        '''minimum and maximum values among inflow'''
        with self._flow():
            return self._many(self._minmax)

    @staticmethod
    def _statrange(iterable, list_=list, sorted_=sorted):
        i1 = list_(sorted_(iterable))
        return i1[-1] - i1[0]

    def statrange(self):
        '''statistical range of inflow'''
        with self._flow():
            return self._one(self._statrange)

    @staticmethod
    def _sum(start, floats, sum=isum, fsum_=fsum):
        summer = lambda x: sum(x, start) if not floats else fsum_
        def sum_(iterable): #@IgnorePep8
            return summer(iterable)
        return sum_

    def sum(self, start=0, floats=False):
        '''
        total inflow together

        @param start: starting number (default: 0)
        @param floats: inflow are floats (default: False)
        '''
        with self._flow():
            return self._one(self._sum(start, floats))


class ReduceMixin(local):

    '''reduce mixin'''

    @staticmethod
    def _concat(iterable, ichain_=ichain):
        return ichain_(iterable)

    def concat(self):
        '''concatenate inflow together'''
        with self._flow():
            return self._many(self._concat)

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

    def flatten(self):
        '''flatten nested inflow'''
        with self._flow():
            return self._many(self._flatten)

    @staticmethod
    def _join(sep, encoding, errors, imap_=imap, tounicode_=tounicode):
        def join(iterable):
            return tounicode(
                sep.join(imap_(tounicode_, iterable)), encoding, errors,
            )
        return join

    def join(self, sep=u(''), encoding='utf-8', errors='strict'):
        '''
        join inflow into one unicode string (regardless of type)

        @param sep: join separator (default: '')
        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._flow():
            return self._one(self._join(sep, encoding, errors))

    @classmethod
    def _pairwise(cls, iterable, next_=next, zip_=izip):
        i1, i2 = cls._clone(iterable)
        next_(i2, None)
        return zip_(i1, i2)

    def pairwise(self):
        '''every two inflow as a `tuple`'''
        with self._flow():
            return self._many(self._pairwise)

    @staticmethod
    def _reduce(call, initial, reduce_=reduce):
        if initial is None:
            def reduce(iterable):
                return reduce_(call, iterable)
        else:
            def reduce(iterable):
                return reduce_(call, iterable, initial)
        return reduce

    def reduce(self, initial=None):
        '''
        reduce inflow to one thing using current callable (from left
        side of inflow)

        @param initial: initial thing (default: None)
        '''
        with self._flow():
            return self._one(self._reduce(self._call, initial))

    @staticmethod
    def _reduceright(call, initial, reduce_=reduce):
        if initial is None:
            def reduceright(iterable):
                return reduce_(lambda x, y: call(y, x), iterable)
            return reduceright
        else:
            def reduceright(iterable):
                return reduce_(lambda x, y: call(y, x), iterable, initial)
        return reduceright

    def reduceright(self, initial=None):
        '''
        reduce inflow to one thing from right side of inflow
        using current callable

        @param initial: initial thing (default: None)
        '''
        with self._flow():
            return self._one(self._reduceright(self._call, initial))

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

    def roundrobin(self):
        '''interleave inflow into one thing'''
        with self._flow():
            return self._many(self._roundrobin)

    @staticmethod
    def _zip(iterable, zip_=izip):
        return zip_(*iterable)

    def zip(self):
        '''
        smash inflow into one single thing, pairing things by iterable
        position
        '''
        with self._flow():
            return self._many(self._zip)


class TruthMixin(local):

    '''truth mixin'''

    @staticmethod
    def _all(truth, all_=iall, imap_=imap):
        def all(iterable):
            return all_(imap_(truth, iterable))
        return all

    def all(self):
        '''if `all` inflow are `True`'''
        with self._flow():
            return self._one(self._all(self._truth))

    @staticmethod
    def _any(truth, any_=iany, imap_=imap):
        def any(iterable):
            return any_(imap_(truth, iterable))
        return any

    def any(self):
        '''if `any` inflow are `True`'''
        with self._flow():
            return self._one(self._any(self._truth))

    @staticmethod
    def _common(iterable, counter=Counter):
        return counter(iterable).most_common(1)[0][0]

    def common(self):
        '''mode value of inflow'''
        with self._flow():
            return self._one(self._common)

    @staticmethod
    def _contains(thing, contains_=icontains):
        def contains(iterable):
            return contains_(iterable, thing)
        return contains

    def contains(self, thing):
        '''
        if `thing` is found in inflow

        @param thing: some thing
        '''
        with self._flow():
            return self._one(self._contains(thing))

    @staticmethod
    def _frequency(iterable, counter=Counter):
        return counter(iterable).most_common()

    def frequency(self):
        '''frequency of each inflow thing'''
        with self._flow():
            return self._one(self._frequency)

    @staticmethod
    def _quantify(call, map=imap, sum=isum):
        def quantify(iterable):
            return sum(map(call, iterable))
        return quantify

    def quantify(self):
        '''
        how many times current callable returns `True` for inflow
        '''
        with self._flow():
            return self._one(self._quantify(self._truth))

    @staticmethod
    def _uncommon(iterable, counter=Counter):
        return counter(iterable).most_common()[:-2:-1][0][0]

    def uncommon(self):
        '''least common inflow thing'''
        with self._flow():
            return self._one(self._uncommon)
