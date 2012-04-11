# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from threading import local


class MathMixin(local):

    '''math mixin'''

    def average(self):
        '''Average value within a series of things.'''
        with self._chain():
            return self._one(self._average)

    def max(self):
        '''
        Maximum value within a series of things using current callable as the
        key function.
        '''
        with self._chain():
            return self._one(self._max(self._identity))

    def median(self):
        '''Median value within a series of things.'''
        with self._chain():
            return self._one(self._median)

    def min(self):
        '''
        Minimum value within a series of things using the current callable as
        the key function.
        '''
        with self._chain():
            return self._one(self._min(self._identity))

    def minmax(self):
        '''Minimum and maximum values within a series of things.'''
        with self._chain():
            return self._many(self._minmax)

    def range(self):
        '''Statistical range within a series of things.'''
        with self._chain():
            return self._one(self._range)

    def sum(self, start=0, floats=False):
        '''
        Add the value of a series of things together.

        @param start: starting number (default: 0)
        @param floats: incoming are floats (default: False)
        '''
        with self._chain():
            return self._one(self._sum(start, floats))


class TruthMixin(local):

    '''truth mixin'''

    def all(self):
        '''Tell if everthing in a series of things is `True`.'''
        with self._chain():
            return self._one(self._all(self._test))

    def any(self):
        '''Tell if anything in a series of things is `True`'''
        with self._chain():
            return self._one(self._any(self._test))

    def frequency(self):
        '''Count of each thing in a series of things.'''
        with self._chain():
            return self._one(self._frequency)

    def quantify(self):
        '''
        Number of how many times current callable evaluates to `True` in a
        series of things.
        '''
        with self._chain():
            return self._one(self._quantify(self._test))


class OrderMixin(local):

    '''order mixin'''

    def choice(self):
        '''Select a random choice from a series of things.'''
        with self._chain():
            return self._one(self._choice)

    def groupby(self):
        '''
        Group things together using the current callable as the key function.
        '''
        with self._chain():
            return self._many(self._groupby(self._identity))

    def reverse(self):
        '''Reverse the order of a series of things.'''
        with self._chain():
            return self._many(self._reverse)

    def sort(self):
        '''
        Sort a series of things using the current callable as the key function.
        '''
        with self._chain():
            return self._many(self._sort(self._identity))

    def sample(self, n):
        '''
        Take a random sample drawn from a series of things.

        @param n: sample size
        '''
        with self._chain():
            return self._many(self._sample(n))

    def shuffle(self):
        '''Randomly reorder a series of things.'''
        with self._chain():
            return self._many(self._shuffle)
