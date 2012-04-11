# -*- coding: utf-8 -*-
'''chainsaw filtering mixins'''

from threading import local


class CollectMixin(local):

    '''collecting mixin'''

    def attributes(self, *names):
        '''extract object attributes from incoming by their `*names`'''
        with self._chain():
            return self._iter(self._attributes(names))

    def extract(self, pattern, flags=0):
        '''
        extract patterns from incoming strings

        @param pattern: search pattern
        '''
        with self._chain():
            return self._many(self._extract(pattern, flags))

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        with self._chain():
            return self._many(self._items(self._call))

    def keys(self):
        '''invoke call on each mapping to get keys'''
        with self._chain():
            return self._many(self._keys(self._call))

    def members(self):
        '''extract object members from incoming'''
        with self._chain():
            return self._many(
                self._members(self._test, self._alt, self._wrapper),
            )

    def mro(self):
        '''extract ancestors of things by method resolution order'''
        with self._chain():
            return self._many(self._mro)

    def pluck(self, *keys):
        '''extract object items from incoming by item `*keys`'''
        with self._chain():
            return self._iter(self._pluck(keys))

    def values(self):
        '''invoke call on each mapping to get values'''
        with self._chain():
            return self._many(self._values(self._call))


class FilterMixin(local):

    '''filtering mixin'''

    def filter(self, pattern=None, reverse=False, flags=0):
        '''
        incoming for which current callable returns `True`

        @param pattern: search pattern expression (default: None)
        @param reverse: reduce from right side (default: False)
        '''
        with self._chain():
            return self._many(
                self._filter(self._test, pattern, reverse, flags)
            )

    def find(self, pattern=None, reverse=False, flags=0):
        '''first incoming thing for which current callable returns `True`'''
        with self._chain():
            return self._one(self._find(self._test, pattern, reverse, flags))

    def replace(self, pattern, new, count=0, flags=0):
        '''
        replace incoming strings matching pattern with replacement string

        @param pattern: search pattern
        @param new: replacement string
        '''
        with self._chain():
            return self._many(self._replace(pattern, new, count, flags))

    def difference(self, symmetric=False):
        '''
        difference between incoming

        @param symmetric: use symmetric difference
        '''
        with self._chain():
            return self._many(self._difference(symmetric))

    def disjointed(self):
        '''disjoint between incoming'''
        with self._chain():
            return self._one(self._disjointed)

    def intersection(self):
        '''intersection between incoming'''
        with self._chain():
            return self._many(self._intersection)

    def partition(self, pattern=None, flags=0):
        '''
        split incoming into `True` and `False` things based on results
        of call
        '''
        with self._chain():
            return self._many(self._divide(self._test, pattern, flags))

    def subset(self):
        '''incoming that are subsets of incoming'''
        with self._chain():
            return self._one(self._subset)

    def superset(self):
        '''incoming that are supersets of incoming'''
        with self._chain():
            return self._one(self._superset)

    def union(self):
        '''union between incoming'''
        with self._chain():
            return self._many(self._union)

    def unique(self):
        '''
        list unique incoming, preserving order and remember all incoming things
        ever seen
        '''
        with self._chain():
            return self._iter(self._unique(self._identity))
