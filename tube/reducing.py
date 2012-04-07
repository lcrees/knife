# -*- coding: utf-8 -*-
'''tube reducing mixins'''

from math import fsum
from threading import local
from itertools import cycle, islice
from functools import partial, reduce
from operator import contains, truediv

from stuf.six import strings, u
from tube.compat import Counter, imap, zip, ichain, tounicode


class BaseMath(local):

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

    @staticmethod
    def _min(iterable, key, min_=min):
        return min_(iterable, key=key)

    @classmethod
    def _minmax(cls, iterable, iter_=iter, min_=min, max_=max):
        i1, i2 = cls._clone(iterable)
        return iter_((min_(i1), max_(i2)))

    @classmethod
    def _max(iterable, key, max_=max):
        return max_(iterable, key=key)

    @staticmethod
    def _sum(iterable, start, floats, sum_=sum, fsum_=fsum):
        return sum_(iterable, start) if not floats else fsum_(iterable)

    @staticmethod
    def _statrange(iterable, list_=list, sorted_=sorted):
        i1 = list_(sorted_(iterable))
        return i1[-1] - i1[0]


class BaseMathMixin(local):

    '''math mixin'''

    def average(self):
        '''average value of inflow'''
        with self._flow():
            return self._append(self._average(self._iterable))

    def max(self):
        '''
        find maximum value among inflow using current callable as key
        function
        '''
        with self._flow():
            return self._append(self._max(self._iterable, self._identity))

    def median(self):
        '''median value of inflow'''
        with self._flow():
            return self._append(self._median(self._iterable))

    def min(self):
        '''
        find minimum value among inflow using current callable as key
        function
        '''
        with self._flow():
            return self._append(self._min(self._iterable, self._identity))

    def minmax(self):
        '''minimum and maximum values among inflow'''
        with self._flow():
            return self._xtend(self._minmax(self._iterable))

    def statrange(self):
        '''statistical range of inflow'''
        with self._flow():
            return self._append(self._statrange(self._iterable))

    def sum(self, start=0, floats=False):
        '''
        total inflow together

        @param start: starting number (default: 0)
        @param floats: inflow are floats (default: False)
        '''
        with self._flow():
            return self._append(self._sum(self._iterable, start, floats))


class MathMixin(BaseMath, BaseMathMixin):

    '''math mixin'''


class BaseReduce(local):

    '''base reduce'''

    @staticmethod
    def _concat(iterable, ichain_=ichain):
        return ichain_(iterable)

    @classmethod
    def _flatten(cls, iterable, strings_=strings, isinstance_=isinstance):
        smash_, strings_, isinst_ = cls._flatten, strings_, isinstance_
        for item in iterable:
            try:
                # don't recur over strings
                if isinst_(item, strings_):
                    yield item
                else:
                    # do recur over other things
                    for j in smash_(item):
                        yield j
            except TypeError:
                # does not recur
                yield item

    @staticmethod
    def _join(iterable, sep, encoding, errors, imap=imap, tounicode=tounicode):
        return tounicode(sep.join(imap(tounicode, iterable)), encoding, errors)

    @classmethod
    def _pairwise(cls, iterable, next_=next, zip_=zip):
        i1, i2 = cls._clone(iterable)
        next_(i2, None)
        return zip_(i1, i2)

    @staticmethod
    def _reduce(call, iterable, initial, reduce_=reduce):
        if initial is None:
            return reduce_(call, iterable)
        return reduce_(call, iterable, initial)

    @staticmethod
    def _reduceright(call, iterable, initial, reduce_=reduce):
        if initial is None:
            return reduce_(lambda x, y: call(y, x), iterable)
        return reduce_(lambda x, y: call(y, x), iterable, initial)

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


class BaseReduceMixin(local):

    '''base reduce mixin'''

    def concat(self):
        '''concatenate inflow together'''
        with self._flow():
            return self._xtend(self._concat(self._iterable))

    def flatten(self):
        '''flatten nested inflow'''
        with self._flow():
            return self._xtend(self._flatten(self._iterable))

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
            return self._xtend(self._pairwise(self._iterable))

    def reduce(self, initial=None):
        '''
        reduce inflow to one thing using current callable (from left
        side of inflow)

        @param initial: initial thing (default: None)
        '''
        with self._flow():
            return self._append(
                self._reduce(self._call, self._iterable, initial),
            )

    def reduceright(self, initial=None):
        '''
        reduce inflow to one thing from right side of inflow
        using current callable

        @param initial: initial thing (default: None)
        '''
        with self._flow():
            return self._append(
                self._reduceright(self._call, self._iterable, initial)
            )

    def roundrobin(self):
        '''interleave inflow into one thing'''
        with self._flow():
            return self._xtend(self._roundrobin(self._iterable))

    def zip(self):
        '''
        smash inflow into one single thing, pairing things by iterable
        position
        '''
        with self._flow():
            return self._xtend(self._zip(self._iterable))


class ReduceMixin(BaseReduce, BaseReduceMixin):

    '''reduce mixin'''


class BaseTruth(local):

    '''truth mixin'''

    @staticmethod
    def _all(truth, iterable, all_=all, imap_=imap):
        return all_(imap_(truth, iterable))
    
    @staticmethod
    def _any(truth, iterable, any_=any, imap_=imap):
        return any_(imap_(truth, iterable))
    
    @staticmethod
    def _common(iterable, counter=Counter):
        return counter(iterable).most_common(1)[0][0]
    
    @staticmethod
    def _contains(iterable, thing, contains_=contains):
        return contains(iterable, thing)

    @staticmethod
    def _frequency(iterable, counter=Counter):
        return Counter(iterable).most_common()
    
    @staticmethod
    def _quantify(call, iterable, imap_=imap, sum_=sum):
        return sum_(imap_(call, iterable))

    @staticmethod
    def uncommon(iterable, counter=Counter):
        return counter(iterable).most_common()[:-2:-1][0][0]


class BaseTruthMixin(local):

    '''truth mixin'''

    def all(self):
        '''if `all` inflow are `True`'''
        with self._flow():
            return self._append(self._all(self._truth, self._iterable))

    def any(self):
        '''if `any` inflow are `True`'''
        with self._flow():
            return self._append(self._any(self._truth, self._iterable))

    def common(self):
        '''mode value of inflow'''
        with self._flow():
            return self._append(self._common(self._iterable))

    def contains(self, thing):
        '''
        if `thing` is found in inflow

        @param thing: some thing
        '''
        with self._flow():
            return self._append(self._contains(self._iterable, thing))

    def frequency(self):
        '''frequency of each inflow thing'''
        with self._flow():
            return self._append(self._frequency(self._iterable))

    def quantify(self):
        '''
        how many times current callable returns `True` for inflow
        '''
        with self._flow():
            return self._append(self._quantify(self._call, self._iterable))

    def uncommon(self):
        '''least common inflow thing'''
        with self._flow():
            return self._append(self._uncommon(self._iterable))


class TruthMixin(BaseTruth, BaseTruthMixin):

    '''truth mixin'''
