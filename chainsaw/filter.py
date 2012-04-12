# -*- coding: utf-8 -*-
'''chainsaw filtering mixins'''

from threading import local


class CollectMixin(local):

    '''collecting mixin'''

#    def attributes(self, deep=False, ancestors=False, *names):
#        '''
#        Collect attributes from a series of objects by their attribute names.
#
#        :param deep: traverse deep inside an object (default: ``False``)
#
#        :param ancestors: traverse deep inside classes within method resolutio
#            order (default: ``False``)
#        '''
#        with self._chain():
#            return self._iter(self._attributes(names, deep, ancestors))

    def mapping(self, keys=False, values=False):
        '''
        Collect `keys` and `values` from an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ of
        `mappings <http://docs.python.org/glossary.html#term-mapping>`_.

        :param keys: gather keys only (*default:* :const:`False`)

        :param values: gather values only (*default:* :const:`False`)
        '''
        with self._chain():
            return self._many(self._mapping(self._call, keys, values))

    def items(self, *keys):
        '''
        Collect things from things (usually `sequences
        <http://docs.python.org/glossary.html#term-sequence>`_ or `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_) within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        by matching their `*keys`.

        :param `*keys`: item keys or indexes
        '''
        with self._chain():
            return self._iter(self._items(keys))


class FilterMixin(local):

    '''filtering mixin'''

    def filter(self, pattern=None, invert=False, flags=0):
        '''
        Collect anything within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ that
        passes a filter. Usually the first thing that the filter evaluates as
        :const:`True` is returned. If `reverse` is :const:`True`, things that
        the filter evaluates as :const:`False` are returned. The current
        callable is used as the filter unless regular expression `pattern`
        is supplied, in which case `pattern` is used as the filter.

        :param pattern: regular expression search pattern (*default:*
          :const:`None`)
        :param invert: return things for which filter is :const:`False` rather
          than :const:`True` (*default:* :const:`False`)
        :param flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
          ``0``)
        '''
        with self._chain():
            return self._many(
                self._filter(self._test, pattern, invert, flags)
            )

    def find(self, pattern=None, invert=False, flags=0):
        '''
        Collect the first thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ that
        passes a filter. Usually the first thing that the filter evaluates as
        :const:`True` is returned. If `reverse` is :const:`True`, the first
        thing that the filter evaluates as :const:`False` is returned.
        The current callable is used as the filter unless regular expression
        `pattern` is supplied, in which case `pattern` is used as the filter.

        :param pattern: regular expression search pattern (*default:*
          :const:`None`)
        :param invert: return things for which filter is :const:`False` rather
          than :const:`True` (*default:* :const:`False`)
        :param flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
          ``0``)
        '''
        with self._chain():
            return self._one(self._find(self._test, pattern, invert, flags))

    def replace(self, pattern, new, count=0, flags=0):
        '''
        Replace parts of string things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ with a
        new string thing if they match regular expression `pattern`.

        :param pattern: regular expression pattern

        :param new: replacement string

        :param count: maximum number of replacements to make within a string
          (*default:* ``0``)
        :param flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
          ``0``)
        '''
        with self._chain():
            return self._many(self._replace(pattern, new, count, flags))

    def difference(self, symmetric=False):
        '''
        Collect differences within a series of
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_.

        :param symmetric: use symmetric difference (*default:* :const:`False`)
        '''
        with self._chain():
            return self._many(self._difference(symmetric))

    def disjointed(self):
        '''
        Collect disjoints within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._disjointed)

    def intersection(self):
        '''
        Collect intersections within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._intersection)

    def partition(self, pattern=None, flags=0):
        '''
        Collect two `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ divided into
        :const:`True` and :const:`False` based on whether the current callable
        returns :const:`True` or :const:`False` for each thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        The current callable is used as the filter unless regular expression
        `pattern` is supplied, in which case `pattern` is used as the filter.

        :param pattern: regular expression search pattern (*default:*
          :const:`None`)
        :param flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
          ``0``)
        '''
        with self._chain():
            return self._many(self._partition(self._test, pattern, flags))

    def subset(self):
        '''
        Collect :const:`True` if an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ is a
        subset of another `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._subset)

    def superset(self):
        '''
        Collect :const:`True` if an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ is
        a superset of another `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._superset)

    def union(self):
        '''
        Collect the union of things within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._union)

    def unique(self):
        '''
        Collect unique things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._iter(self._unique(self._identity))
