# -*- coding: utf-8 -*-
'''tube ordering mixins'''

from threading import local
from itertools import groupby
from random import choice, shuffle, sample

from tube.compat import zip_longest, imap


class BaseRandom(local):

    '''base random'''

    @staticmethod
    def _choice(iterable, choice_=choice, list_=list):
        return choice_(list_(iterable))

    @staticmethod
    def _sample(iterable, n, sample_=sample, list_=list):
        return sample_(list_(iterable), n)

    @staticmethod
    def _shuffle(iterable, list_=list, shuffle_=shuffle):
        iterable = list(iterable)
        shuffle(iterable)
        return iterable


class BaseRandomMixin(local):

    '''base random mixin'''

    def choice(self):
        '''random choice of/from inflow'''
        with self._flow():
            return self._append(self._choice(self._iterable))

    def sample(self, n):
        '''
        random sampling drawn from `n` inflow things

        @param n: number of inflow
        '''
        with self._flow():
            return self._xtend(self._sample(self._iterable, n))

    def shuffle(self):
        '''randomly order inflow'''
        with self._flow():
            return self._xtend(self._shuffle(self._iterable))


class RandomMixin(BaseRandom, BaseRandomMixin):

    '''random mixin'''


class BaseOrder(local):

    '''base order'''

    @staticmethod
    def _groupby(iterable, key, imap_=imap, list_=list, groupby_=groupby):
        return imap(lambda x: [x[0], list_(x[1])], groupby_(iterable, key))

    @staticmethod
    def _grouper(iterable, n, fill, zip_longest_=zip_longest, iter_=iter):
        return zip_longest_(fillvalue=fill, *[iter_(iterable)] * n)  

    @staticmethod
    def _reverse(iterable, list_=list, reversed_=reversed):
        return reversed_(list_(iterable))

    @staticmethod
    def _sort(iterable, key, sorted_=sorted):
        return sorted_(iterable, key=key)


class BaseOrderMixin(local):

    '''order mixin'''

    def groupby(self):
        '''
        group inflow, optionally using current call for key function
        '''
        with self._flow():
            return self._xtend(self._groupby(self._iterable, self._identity))

    def grouper(self, n, fill=None):
        '''
        split inflow into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        with self._flow():
            return self._xtend(self._grouper(self._iterable, n, fill)) 

    def reverse(self):
        '''reverse order of inflow'''
        with self._flow():
            return self._xtend(self._reversed(self._iterable))

    def sort(self):
        '''
        sort inflow, optionally using current call as key function
        '''
        with self._flow():
            return self._xtend(self._sort(self._iterable, self._identity))
        

class OrderMixin(BaseOrder, BaseOrderMixin):

    '''order mixin'''
