# -*- coding: utf-8 -*-
'''chainsaw analyzing mixins'''

from threading import local


class CompareMixin(local):

    '''comparing mixin'''

    def all(self):
        '''
        Discover if the worker returns :const:`True` for **everything** within
        an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the iterable is empty).
        '''
        with self._chain():
            return self._one(self._all(self._test))

    def any(self):
        '''
        Discover if the worker returns :const:`True` for **anything** within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the iterable is empty).
        '''
        with self._chain():
            return self._one(self._any(self._test))

    def difference(self, symmetric=False):
        '''
        Find differences within a series of
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_.

        :param symmetric: use symmetric difference (*default:* :const:`False`)
        '''
        with self._chain():
            return self._many(self._difference(symmetric))

    def disjointed(self):
        '''
        Find disjoints within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._disjointed)

    def intersection(self):
        '''
        Find intersections within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._intersection)

    def subset(self):
        '''
        Find out if `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ are subsets
        other iterables.
        '''
        with self._chain():
            return self._one(self._subset)

    def superset(self):
        '''
        Find out if `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ are supersets of
        others iterables.
        '''
        with self._chain():
            return self._one(self._superset)

    def union(self):
        '''
        Find unions within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._union)

    def unique(self):
        '''
        Find unique things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._iter(self._unique(self._identity))


class MathMixin(local):

    '''mathing mixin'''

    def average(self):
        '''
        Find the average value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._iter(self._average)

    def count(self):
        '''
        Count how many times each thing occurs within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_. Result is a
        :class:`tuple` consisting of (*least common thing*, *most common
        thing*, *count of everything* consisting of a :class:`list` of
        :class:`tuple` pairs of (*thing*, *count*).
        '''
        with self._chain():
            return self._iter(self._count)

    def max(self):
        '''
        Find the maximum value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''
        with self._chain():
            return self._iter(self._max(self._identity))

    def median(self):
        '''
        Find the median value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._iter(self._median)

    def min(self):
        '''
        Find the minimum value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''
        with self._chain():
            return self._iter(self._min(self._identity))

    def minmax(self):
        '''
        Find the minimum and maximum values within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_. Result is a
        :class:`tuple` of (*minimum value*, *maximum value*).
        '''
        with self._chain():
            return self._iter(self._minmax)

    def range(self):
        '''
        Find the length of the smallest interval that can contain everything
        within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._iter(self._range)

    def sum(self, start=0, precision=False):
        '''
        Total up by adding `start` and everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ together.

        :param start: starting number (*default:* ``0``)

        :param precision: add floats with extended precision (*default:*
          :const:`False`)
        '''
        with self._chain():
            return self._iter(self._sum(start, precision))


class OrderMixin(local):

    '''ordering key'''

    def group(self):
        '''
        Group things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
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
        worker as the `key function
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
            return self._iter(self._sort(self._identity))
