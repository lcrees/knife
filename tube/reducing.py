# -*- coding: utf-8 -*-
'''tube reducing mixins'''

from math import fsum
from threading import local
from itertools import cycle, islice
from functools import partial, reduce
from operator import contains, truediv

from stuf.six import strings, u
from tube.compat import Counter, imap, zip, ichain, tounicode


class MathMixin(local):

    '''math mixin'''

    @classmethod
    def _average(cls, iterable, s=sum, t=truediv, n=len):
        i1, i2 = cls._clone(iterable)
        return t(s(i1, 0.0), n(list(i2)))

    @staticmethod
    def _median(iterable, s=sorted, l=list, d=truediv, i=int, n=len):
        i = l(s(iterable))
        e = d(n(i) - 1, 2)
        p = i(e)
        return i[p] if e % 2 == 0 else truediv(i[p] + i[p + 1], 2)

    @classmethod
    def _min(iterable, key, min_=min):
        def min__(iterable):
            return min_(iterable, key=key)
        return min__

    @classmethod
    def _minmax(cls, iterable, iter_=iter, min_=min, max_=max):
        i1, i2 = cls._clone(iterable)
        return iter_((min_(i1), max_(i2)))

    @classmethod
    def _max(iterable, key, max_=max):
        def max__(iterable):
            return max_(iterable, key=key)
        return max__

    @staticmethod
    def _sum(iterable, start, floats, sum_=sum, fsum_=fsum):
        summer = lambda x: sum_(x, start) if not floats else fsum_(iterable)
        def sum__(iterable):
            return summer(iterable)
        return sum__

    @staticmethod
    def _statrange(iterable, list_=list, sorted_=sorted):
        i1 = list_(sorted_(iterable))
        return i1[-1] - i1[0]

    def average(self):
        '''average value of inflow'''
        with self._flow():
            return self._append(self._average)

    def max(self):
        '''
        find maximum value among inflow using current callable as key
        function
        '''
        with self._flow():
            return self._append(self._max(self._identity))

    def median(self):
        '''median value of inflow'''
        with self._flow():
            return self._append(self._median)

    def min(self):
        '''
        find minimum value among inflow using current callable as key
        function
        '''
        with self._flow():
            return self._append(self._min(self._identity))

    def minmax(self):
        '''minimum and maximum values among inflow'''
        with self._flow():
            return self._xtend(self._minmax)

    def statrange(self):
        '''statistical range of inflow'''
        with self._flow():
            return self._append(self._statrange)

    def sum(self, start=0, floats=False):
        '''
        total inflow together

        @param start: starting number (default: 0)
        @param floats: inflow are floats (default: False)
        '''
        with self._flow():
            return self._append(self._sum(start, floats))


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
        def join__(iterable):
            return tounicode(
                sep.join(imap_(tounicode_, iterable)), encoding, errors,
            )
        return join__

    @classmethod
    def _pairwise(cls, iterable, next_=next, zip_=zip):
        i1, i2 = cls._clone(iterable)
        next_(i2, None)
        return zip_(i1, i2)

    @staticmethod
    def _reduce(call, initial, reduce_=reduce):
        if initial is None:
            def reduce__(iterable):
                return reduce_(call, iterable)
        else:
            def reduce__(iterable):
                return reduce_(call, iterable, initial)
        return reduce__

    @staticmethod
    def _reduceright(call, initial, reduce_=reduce):
        if initial is None:
            def reduceright__(iterable):
                return reduce_(lambda x, y: call(y, x), iterable)
            return reduceright__
        else:
            def reduceright__(iterable):
                return reduce_(lambda x, y: call(y, x), iterable, initial)
        return reduceright__

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
    def _zip(iterable, zip_=zip):
        return zip_(*iterable)

    def concat(self):
        '''concatenate inflow together'''
        with self._flow():
            return self._xtend(self._concat)

    def flatten(self):
        '''flatten nested inflow'''
        with self._flow():
            return self._xtend(self._flatten)

    def join(self, sep=u(''), encoding='utf-8', errors='strict'):
        '''
        join inflow into one unicode string (regardless of type)

        @param sep: join separator (default: '')
        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._flow():
            return self._append(self._join(sep, encoding, errors))

    def pairwise(self):
        '''every two inflow as a `tuple`'''
        with self._flow():
            return self._xtend(self._pairwise)

    def reduce(self, initial=None):
        '''
        reduce inflow to one thing using current callable (from left
        side of inflow)

        @param initial: initial thing (default: None)
        '''
        with self._flow():
            return self._append(self._reduce(self._call, initial))

    def reduceright(self, initial=None):
        '''
        reduce inflow to one thing from right side of inflow
        using current callable

        @param initial: initial thing (default: None)
        '''
        with self._flow():
            return self._append(self._reduceright(self._call, initial))

    def roundrobin(self):
        '''interleave inflow into one thing'''
        with self._flow():
            return self._xtend(self._roundrobin)

    def zip(self):
        '''
        smash inflow into one single thing, pairing things by iterable
        position
        '''
        with self._flow():
            return self._xtend(self._zip)


class TruthMixin(local):

    '''truth mixin'''
    
    @staticmethod
    def _all(truth, all_=all, imap_=imap):
        def all__(iterable):
            return all_(imap_(truth, iterable))
        return all__
    
    @staticmethod
    def _any(truth, any_=any, imap_=imap):
        def any__(iterable):
            return any_(imap_(truth, iterable))
        return any__
    
    @staticmethod
    def _common(iterable, counter=Counter):
        return counter(iterable).most_common(1)[0][0]
    
    @staticmethod
    def _contains(thing, contains_=contains):
        def contains__(iterable):
            return contains_(iterable, thing)
        return contains__

    @staticmethod
    def _frequency(iterable, counter=Counter):
        return Counter(iterable).most_common()
    
    @staticmethod
    def _quantify(call, imap_=imap, sum_=sum):
        def quantify__(iterable):
            return sum_(imap_(call, iterable))
        return quantify__
    
    @staticmethod
    def _uncommon(iterable, counter=Counter):
        return counter(iterable).most_common()[:-2:-1][0][0]

    def all(self):
        '''if `all` inflow are `True`'''
        with self._flow():
            return self._append(self._all(self._truth))

    def any(self):
        '''if `any` inflow are `True`'''
        with self._flow():
            return self._append(self._any(self._truth))

    def common(self):
        '''mode value of inflow'''
        with self._flow():
            return self._append(self._common)

    def contains(self, thing):
        '''
        if `thing` is found in inflow

        @param thing: some thing
        '''
        with self._flow():
            return self._append(self._contains(thing))

    def frequency(self):
        '''frequency of each inflow thing'''
        with self._flow():
            return self._append(self._frequency)

    def quantify(self):
        '''
        how many times current callable returns `True` for inflow
        '''
        with self._flow():
            return self._append(self._quantify(self._truth))

    def uncommon(self):
        '''least common inflow thing'''
        with self._flow():
            return self._append(self._uncommon)
