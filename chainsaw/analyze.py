# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from threading import local


class MathMixin(local):

    '''math mixin'''

    def average(self):
        '''
        Collect average thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._average)

    def max(self):
        '''
        Collect maximum thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        current callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''
        with self._chain():
            return self._one(self._max(self._identity))

    def median(self):
        '''
        Collect median thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._median)

    def min(self):
        '''
        Collect minimum thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        current callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''
        with self._chain():
            return self._one(self._min(self._identity))

    def minmax(self):
        '''
        Collect minimum and maximum things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_
        as a :class:`tuple` consisting of (*minimum value*, *maximum value*).
        '''
        with self._chain():
            return self._many(self._minmax)

    def range(self):
        '''
        Collect length of the smallest interval that can contain each thing
        within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._range)

    def sum(self, start=0, floats=False):
        '''
        Collect total from adding up `start` and each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param start: starting number (*default:* ``0``)

        :param floats: add floats with extended precision (*default:*
          :const:`False`)
        '''
        with self._chain():
            return self._one(self._sum(start, floats))


class TruthMixin(local):

    '''truth mixin'''

    def all(self):
        '''
        Collect :const:`True` if the current callable returns :const:`True` for
        **everything** within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        is empty).
        '''
        with self._chain():
            return self._one(self._all(self._test))

    def any(self):
        '''
        Collect :const:`True` if the current callable returns :const:`True` for
        **anything** within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        is empty).
        '''
        with self._chain():
            return self._one(self._any(self._test))

    def frequency(self):
        '''
        Collect the number of times each thing occurs within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_. Returns a
        :class:`tuple` consisting of (*least common thing*, *most common
        thing*, *count of everything* consisting of a :class:`list` of
        :class:`tuple` pairs of (*thing*, *count*).
        '''
        with self._chain():
            return self._one(self._frequency)

    def quantify(self):
        '''
        Collect the number of times the current callable returns :const:`True`
        for *anything* within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._quantify(self._test))


class OrderMixin(local):

    '''order mixin'''

    def choice(self):
        '''
        Collect a randomly selected thing from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._choice)

    def groupby(self):
        '''
        Collect things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ grouped using
        the current callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''
        with self._chain():
            return self._many(self._groupby(self._identity))

    def reverse(self):
        '''
        Collect the current order of things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._reverse)

    def sort(self):
        '''
        Collect things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ sorted using the
        current callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''
        with self._chain():
            return self._many(self._sort(self._identity))

    def sample(self, n):
        '''
        Collect a randomly sample of `n` size from things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: size of sample
        '''
        with self._chain():
            return self._many(self._sample(n))

    def shuffle(self):
        '''
        Collect things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ that have been
        randomly rearranged from their previous order.
        '''
        with self._chain():
            return self._many(self._shuffle)
