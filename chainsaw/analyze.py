# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from threading import local


class CompareMixin(local):

    '''compare mixin'''

    def all(self):
        '''
        :const:`True` if the active callable returns :const:`True` for
        **everything** within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the iterable is empty).
        '''
        with self._chain():
            return self._one(self._all(self._test))

    def any(self):
        '''
        :const:`True` if the active callable returns :const:`True` for
        **anything** within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if the
        iterable is empty).
        '''
        with self._chain():
            return self._one(self._any(self._test))

    def difference(self, symmetric=False):
        '''
        Differences within a series of
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_.

        :param symmetric: use symmetric difference (*default:* :const:`False`)
        '''
        with self._chain():
            return self._many(self._difference(symmetric))

    def disjointed(self):
        '''
        Disjoints within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._disjointed)

    def intersection(self):
        '''
        Intersections within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._intersection)

    def subset(self):
        '''
        :const:`True` if `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ are subsets
        each other.
        '''
        with self._chain():
            return self._one(self._subset)

    def superset(self):
        '''
        :const:`True` if an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ is a superset of
        another iterable.
        '''
        with self._chain():
            return self._one(self._superset)

    def union(self):
        '''
        Union of things within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._union)

    def unique(self):
        '''
        Unique things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._iter(self._unique(self._identity))


class NumberMixin(local):

    '''numbering mixin'''

    def average(self):
        '''
        Take average of things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._average)

    def count(self):
        '''
        Count the number of times each thing occurs within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_. Returns a
        :class:`tuple` consisting of (*least common thing*, *most common
        thing*, *count of everything* consisting of a :class:`list` of
        :class:`tuple` pairs of (*thing*, *count*).
        '''
        with self._chain():
            return self._one(self._count)

    def max(self):
        '''
        Take the maximum thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        active callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''
        with self._chain():
            return self._one(self._max(self._identity))

    def median(self):
        '''
        Take the median thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._iter(self._median)

    def min(self):
        '''
        Take the minimum thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        active callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''
        with self._chain():
            return self._one(self._min(self._identity))

    def minmax(self):
        '''
        Take the minimum and maximum things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_
        as a :class:`tuple` consisting of (*minimum value*, *maximum value*).
        '''
        with self._chain():
            return self._iter(self._minmax)

    def range(self):
        '''
        Take the length of the smallest interval that can contain each thing
        within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._iter(self._range)

    def sum(self, start=0, precision=False):
        '''
        Take the total from adding up `start` and each thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :param start: starting number (*default:* ``0``)

        :param precision: add floats with extended precision (*default:*
          :const:`False`)
        '''
        with self._chain():
            return self._one(self._sum(start, precision))


class OrderMixin(local):

    '''ordering key'''

    def group(self):
        '''
        Group things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using
        the active callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''
        with self._chain():
            return self._many(self._group(self._identity))

    def reverse(self):
        '''
        Reverse the order of things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._iter(self._reverse)

    def shuffle(self):
        '''
        Sort things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        active callable as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''
        with self._chain():
            return self._iter(self._shuffle)

    def sort(self):
        '''
        Randomly reorder things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._sort(self._identity))
