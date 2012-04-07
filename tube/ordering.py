# -*- coding: utf-8 -*-
'''tube ordering mixins'''

from threading import local
from itertools import groupby
from random import choice, shuffle, sample

from tube.compat import zip_longest, imap


class RandomMixin(local):

    '''base random'''

    @staticmethod
    def _choice(iterable, choice_=choice, list_=list):
        return choice_(list_(iterable))

    @staticmethod
    def _sample(n, sample_=sample, list_=list):
        def sample__(iterable):
            return sample_(list_(iterable), n)
        return sample__

    @staticmethod
    def _shuffle(iterable, list_=list, shuffle_=shuffle):
        iterable = list(iterable)
        shuffle(iterable)
        return iterable

    def choice(self):
        '''random choice of/from inflow'''
        with self._flow():
            return self._append(self._choice)

    def sample(self, n):
        '''
        random sampling drawn from `n` inflow things

        @param n: number of inflow
        '''
        with self._flow():
            return self._xtend(self._sample(n))

    def shuffle(self):
        '''randomly order inflow'''
        with self._flow():
            return self._xtend(self._shuffle)


class OrderMixin(local):

    '''order mixin'''

    @staticmethod
    def _groupby(key, imap_=imap, tuple_=tuple, groupby_=groupby):
        def grouper(x):
            return (x[0], tuple_(x[1]))
        def groupby__(iterable): #@IgnorePep8
            return imap(grouper, groupby_(iterable, key))
        return groupby__

    @staticmethod
    def _grouper(n, fill, zip_longest_=zip_longest, iter_=iter):
        def grouper__(iterable):
            return zip_longest_(fillvalue=fill, *[iter_(iterable)] * n)
        return grouper__

    @staticmethod
    def _reverse(iterable, list_=list, reversed_=reversed):
        return reversed_(list_(iterable))

    @staticmethod
    def _sort(key, sorted_=sorted):
        def sort__(iterable):
            return sorted_(iterable, key=key)
        return sort__

    def groupby(self):
        '''
        group inflow, optionally using current call for key function
        '''
        with self._flow():
            return self._xtend(self._groupby(self._identity))

    def grouper(self, n, fill=None):
        '''
        split inflow into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        with self._flow():
            return self._xtend(self._grouper(n, fill))

    def reverse(self):
        '''reverse order of inflow'''
        with self._flow():
            return self._xtend(self._reversed)

    def sort(self):
        '''
        sort inflow, optionally using current call as key function
        '''
        with self._flow():
            return self._xtend(self._sort(self._identity))
