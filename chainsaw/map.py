# -*- coding: utf-8 -*-
'''chainsaw mapping mixins'''

from threading import local


class RepeatMixin(local):

    '''repetition mixin'''

    def combinations(self, n):
        '''
        Each possible combinations for every number of things within a series
        of things.

        :param n: number of things to derive combinations from
        '''
        with self._chain():
            return self._many(self._combinations(n))

    def copy(self):
        '''Duplicate each thing in a series of things'''
        with self._chain():
            return self._many(self._copy)

    def product(self, n=1):
        '''
        Results of nested for each loops repeated a certain number of times.

        :param n: number of loops to repeat (*default*: ``1``)
        '''
        with self._chain():
            return self._many(self._product(n))

    def permutations(self, n):
        '''
        Each possible permutation for every number of things within a series of
        things.

        :param n: number of things to derive permutations from
        '''
        with self._chain():
            return self._many(self._permutations(n))

    def repeat(self, n=None, call=False):
        '''
        Repeat a series of things or the results of the current callable.

        :param n: number of times to repeat (*default*: ``None``)

        :param call: repeat result of current callable (*default*: ``False``)
        '''
        with self._chain():
            return self._many(self._repeat(n, call, self._identity))


class MapMixin(local):

    '''mapping mixin'''

    def invoke(self, name):
        '''
        Invoke method `name` on each thing within a series of things with the
        current positio nnd keyword arguments but return the thing as the
        result if the method returns ``None``.

        :param name: method name
        '''
        with self._chain():
            return self._many(
                self._invoke(name, (self._args, self._kw))
            )

    def map(self, args=False, kwargs=False, current=False):
        '''
        Invoke current callable on each thing in an iterable. Pass
        results of iterable as `*args` to current callable if `args` flag is
        set. Pass results of iterable to current callable as a :class:`tuple`
        of `*args` and `**kwargs` if `kwargs` flag is set.

        :param args: map each thing as a :class:`tuple` of Python `*args` for
          the current callable (*default*: ``False``)
        :param kwargs: map each thing as a :class:`tuple` of Python `*args` and
          `**kwargs` for the current callable (*default*: ``False``)
        :param current: map each thing as a :class"`tuple` of Python `*args`
          and `**kwargs` and any assigned positional and/or keyword arguments
          for the current callable (*default*: ``False``)
        '''
        args = kwargs if kwargs else args
        with self._chain():
            return self._many(self._map(
                self._call, args, kwargs, current, self._args, self._kw,
            ))
