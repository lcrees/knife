# -*- coding: utf-8 -*-
'''tube ordering mixins'''

from threading import local
from itertools import groupby
from random import choice, shuffle, sample

from tube.compat import zip_longest, imap


class RandomMixin(local):

    '''random mixin'''

    def choice(self):
        '''random choice of/from inflow'''
        with self._flow():
            return self._append(choice(list(self._iterable)))

    def sample(self, n):
        '''
        random sampling drawn from `n` inflow

        @param n: number of inflow
        '''
        with self._flow():
            return self._xtend(sample(list(self._iterable), n))

    def shuffle(self):
        '''randomly order inflow'''
        with self._flow():
            iterable = list(self._iterable)
            shuffle(iterable)
            return self._xtend(iterable)


class OrderMixin(local):

    '''order mixin'''

    def groupby(self):
        '''
        group inflow, optionally using current call for key function
        '''
        call_, list_ = self._call, list
        with self._flow():
            return self._xtend(imap(
                lambda x: [x[0], list_(x[1])], groupby(self._iterable, call_)
            ))

    def grouper(self, n, fill=None):
        '''
        split inflow into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        with self._flow():
            return self._xtend(
                zip_longest(fillvalue=fill, *[iter(self._iterable)] * n)
            )  

    def reverse(self):
        '''reverse order of inflow'''
        with self._flow():
            return self._xtend(reversed(list(self._iterable)))

    def sort(self):
        '''
        sort inflow, optionally using current call as key function
        '''
        call_ = self._call
        with self._flow():
            return self._xtend(sorted(self._iterable, key=call_))
