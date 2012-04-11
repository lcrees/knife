# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from threading import local


class MathMixin(local):

    '''math mixin'''

    def average(self):
        '''average value of incoming'''
        with self._chain():
            return self._one(self._average)

    def max(self):
        '''
        find maximum value among incoming using current callable as key
        function
        '''
        with self._chain():
            return self._one(self._max(self._identity))

    def median(self):
        '''median value of incoming'''
        with self._chain():
            return self._one(self._median)

    def min(self):
        '''
        find minimum value among incoming using current callable as key
        function
        '''
        with self._chain():
            return self._one(self._min(self._identity))

    def minmax(self):
        '''minimum and maximum values among incoming'''
        with self._chain():
            return self._many(self._minmax)

    def range(self):
        '''statistical range of incoming'''
        with self._chain():
            return self._one(self._range)

    def sum(self, start=0, floats=False):
        '''
        total incoming together

        @param start: starting number (default: 0)
        @param floats: incoming are floats (default: False)
        '''
        with self._chain():
            return self._one(self._sum(start, floats))


class TruthMixin(local):

    '''truth mixin'''

    def all(self):
        '''if `all` incoming are `True`'''
        with self._chain():
            return self._one(self._all(self._test))

    def any(self):
        '''if `any` incoming are `True`'''
        with self._chain():
            return self._one(self._any(self._test))

    def frequency(self):
        '''frequency of each incoming thing'''
        with self._chain():
            return self._one(self._frequency)

    def quantify(self):
        '''
        how many times current callable returns `True` for incoming
        '''
        with self._chain():
            return self._one(self._quantify(self._test))


class OrderMixin(local):

    '''order mixin'''

    def choice(self):
        '''random choice of/from incoming'''
        with self._chain():
            return self._one(self._choice)

    def groupby(self):
        '''
        group incoming, optionally using current call for key function
        '''
        with self._chain():
            return self._many(self._groupby(self._identity))

    def reverse(self):
        '''reverse order of incoming'''
        with self._chain():
            return self._many(self._reverse)

    def sort(self):
        '''
        sort incoming, optionally using current call as key function
        '''
        with self._chain():
            return self._many(self._sort(self._identity))

    def sample(self, n):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of incoming
        '''
        with self._chain():
            return self._many(self._sample(n))

    def shuffle(self):
        '''randomly order incoming'''
        with self._chain():
            return self._many(self._shuffle)
