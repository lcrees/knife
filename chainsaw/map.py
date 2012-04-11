# -*- coding: utf-8 -*-
'''chainsaw mapping mixins'''

from threading import local


class RepeatMixin(local):

    '''repetition mixin'''

    def combinations(self, n):
        '''
        repeat every combination for `n` of incoming

        @param n: number of repetitions
        '''
        with self._chain():
            return self._many(self._combinations(n))

    def copy(self):
        '''copy each incoming thing'''
        with self._chain():
            return self._many(self._copy)

    def product(self, n=1):
        '''
        nested for each loops repeated `n` times

        @param n: number of repetitions (default: 1)
        '''
        with self._chain():
            return self._many(self._product(n))

    def permutations(self, n):
        '''
        repeat every permutation for every `n` of incoming

        @param n: length of thing to permutate
        '''
        with self._chain():
            return self._many(self._permutations(n))

    def repeat(self, n):
        '''
        repeat incoming `n` times

        @param n: number of times to repeat
        '''
        with self._chain():
            return self._many(self._repeat(n))

    def times(self, n=None):
        '''
        repeat call with incoming `n` times

        @param n: repeat call n times on incoming (default: None)
        '''
        with self._chain():
            return self._many(self._times(self._call, n))


class MapMixin(local):

    '''mapping mixin'''

    def invoke(self, name):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        '''
        with self._chain():
            return self._many(
                self._invoke(name, (self._args, self._kw))
            )

    def map(self, args=False, kwargs=False):
        '''
        invoke call on each incoming thing

        @param args: map each incoming thing as python *args for call
        @param kwargs: map each incoming thing as python **kwargs for call
        '''
        args = kwargs if kwargs else args
        with self._chain():
            return self._many(self._map(self._call, args, kwargs))
