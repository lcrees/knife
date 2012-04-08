# -*- coding: utf-8 -*-
'''knife reducing mixins'''

from math import fsum
from threading import local
from operator import truediv
from random import choice, shuffle, sample

from knife.compat import Counter, imap, iall, iany, imax, imin, isum


class StatsMixin(local):

    '''math mixin'''

    @classmethod
    def _average(cls, iterable, s=sum, t=truediv, n=len):
        i1, i2 = cls._clone(iterable)
        return t(s(i1, 0.0), n(list(i2)))

    @classmethod
    def _max(key, imax_=imax):
        def max_(iterable):
            return imax_(iterable, key=key)
        return max_

    @staticmethod
    def _median(iterable, s=sorted, l=list, d=truediv, i=int, n=len):
        i = l(s(iterable))
        e = d(n(i) - 1, 2)
        p = i(e)
        return i[p] if e % 2 == 0 else truediv(i[p] + i[p + 1], 2)

    @classmethod
    def _minmax(cls, iterable, iter_=iter, min=imin, max=imax):
        i1, i2 = cls._clone(iterable)
        return iter_((min(i1), max(i2)))

    @staticmethod
    def _range(iterable, list_=list, sorted_=sorted):
        i1 = list_(sorted_(iterable))
        return i1[-1] - i1[0]

    @classmethod
    def _min(key, imin_=imin):
        def min_(iterable):
            return imin_(iterable, key=key)
        return min_

    @staticmethod
    def _sum(start, floats, sum=isum, fsum_=fsum):
        summer = lambda x: sum(x, start) if not floats else fsum_
        def sum_(iterable): #@IgnorePep8
            return summer(iterable)
        return sum_

    def average(self):
        '''average value of incoming'''
        with self._flow():
            return self._single(self._average)

    def max(self):
        '''
        find maximum value among incoming using current callable as key
        function
        '''
        with self._flow():
            return self._single(self._max(self._identity))

    def median(self):
        '''median value of incoming'''
        with self._flow():
            return self._single(self._median)

    def min(self):
        '''
        find minimum value among incoming using current callable as key
        function
        '''
        with self._flow():
            return self._single(self._min(self._identity))

    def minmax(self):
        '''minimum and maximum values among incoming'''
        with self._flow():
            return self._multi(self._minmax)

    def range(self):
        '''statistical range of incoming'''
        with self._flow():
            return self._single(self._range)

    def sum(self, start=0, floats=False):
        '''
        total incoming together

        @param start: starting number (default: 0)
        @param floats: incoming are floats (default: False)
        '''
        with self._flow():
            return self._single(self._sum(start, floats))


class TruthMixin(local):

    '''truth mixin'''

    @staticmethod
    def _all(truth, all_=iall, imap_=imap):
        def all(iterable):
            return all_(imap_(truth, iterable))
        return all

    @staticmethod
    def _any(truth, any_=iany, imap_=imap):
        def any(iterable):
            return any_(imap_(truth, iterable))
        return any

    @staticmethod
    def _frequency(iterable, counter=Counter):
        count = counter(iterable)
        commonality = count.most_common()
        return (
            # least common
            commonality[:-2:-1][0][0],
            # most common (mode)
            count.most_common(1)[0][0],
            # overall commonality
            commonality,
        )

    @staticmethod
    def _quantify(call, imap_=imap, sum=isum):
        def quantify(iterable):
            return sum(imap_(call, iterable))
        return quantify

    def all(self):
        '''if `all` incoming are `True`'''
        with self._flow():
            return self._single(self._all(self._truth))

    def any(self):
        '''if `any` incoming are `True`'''
        with self._flow():
            return self._single(self._any(self._truth))

    def frequency(self):
        '''frequency of each incoming thing'''
        with self._flow():
            return self._single(self._frequency)

    def quantify(self):
        '''
        how many times current callable returns `True` for incoming
        '''
        with self._flow():
            return self._single(self._quantify(self._truth))


class OrderMixin(local):

    '''order mixin'''

    @staticmethod
    def _reverse(iterable, list_=list, reversed_=reversed):
        return reversed_(list_(iterable))

    @staticmethod
    def _sort(key, sorted_=sorted):
        def sort(iterable):
            return sorted_(iterable, key=key)
        return sort

    @staticmethod
    def _choice(iterable, choice_=choice, list_=list):
        return choice_(list_(iterable))

    @staticmethod
    def _sample(n, _sample=sample, list_=list):
        def sample_(iterable):
            return _sample(list_(iterable), n)
        return sample_

    @staticmethod
    def _shuffle(iterable, list_=list, shuffle_=shuffle):
        iterable = list_(iterable)
        shuffle_(iterable)
        return iterable

    def choice(self):
        '''random choice of/from incoming'''
        with self._flow():
            return self._single(self._choice)

    def reverse(self):
        '''reverse order of incoming'''
        with self._flow():
            return self._multi(self._reversed)

    def sort(self):
        '''
        sort incoming, optionally using current call as key function
        '''
        with self._flow():
            return self._multi(self._sort(self._identity))

    def sample(self, n):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of incoming
        '''
        with self._flow():
            return self._multi(self._sample(n))

    def shuffle(self):
        '''randomly order incoming'''
        with self._flow():
            return self._multi(self._shuffle)
