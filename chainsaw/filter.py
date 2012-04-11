# -*- coding: utf-8 -*-
'''chainsaw filtering mixins'''

from threading import local


class CollectMixin(local):

    '''collecting mixin'''

    def attributes(self, deep=False, ancestors=False, *names):
        '''
        Collect attributes from a series of objects by their attribute names.

        @param deep: traverse deep inside an object (default: `False`)
        @param ancestors: traverse deep inside classes within method resolution
            order (default: `False`)
        @param *keys: item keys
        '''
        with self._chain():
            return self._iter(self._attributes(names, deep, ancestors))

    def mapping(self, keys=False, values=False):
        '''
        Collect keys and values from a series of mappings.

        @param keys: gather keys only (default: `False`)
        @param values: gather values only (default: `False`)
        '''
        with self._chain():
            return self._many(self._items(self._call, keys, values))

    def items(self, *keys):
        '''
        Collect object items from a series of things matching their keys.

        @param *keys: item keys
        '''
        with self._chain():
            return self._iter(self._pluck(keys))


class FilterMixin(local):

    '''filtering mixin'''

    def filter(self, pattern=None, reverse=False, flags=0):
        '''
        Things within a series of things that pass a filter. By default things
        that evaluate to `True` pass the filter but if the `reverse` flag is
        set to `True` than things that evaluate to `False` pass the filter
        while things that evaluate to False do not. If a `pattern` is supplied
        the filter will be a regular expression. Otherwise the current callable
        will be used.

        @param pattern: regular expression search pattern (default: `None`)
        @param reverse: return things for which filter is `False` rather than
            `True` (default: `False`)
        @param flags: regular expression flags (default: 0)
        '''
        with self._chain():
            return self._many(
                self._filter(self._test, pattern, reverse, flags)
            )

    def find(self, pattern=None, reverse=False, flags=0):
        '''
        The first in a series of things that pass a filter. By default things
        that evaluate to `True` pass the filter but if the `reverse` flag is
        set to `True` than things that evaluate to `False` pass the filter
        while things that evaluate to False do not. If a `pattern` is supplied
        the filter will be a regular expression. Otherwise the current callable
        will be used.

        @param pattern: regular expression search pattern (default: `None`)
        @param reverse: return things for which filter is `False` rather than
            `True` (default: `False`)
        @param flags: regular expression flags (default: 0)
        '''
        with self._chain():
            return self._one(self._find(self._test, pattern, reverse, flags))

    def replace(self, pattern, new, count=0, flags=0):
        '''
        Replace segments within a series of strings with a new string segment
        if they match a pattern.

        @param pattern: regular expression search pattern
        @param new: replacement string
        @param count: number of replacements to make in a string (default: 0)
        @param flags: regular expression flags (default: 0)
        '''
        with self._chain():
            return self._many(self._replace(pattern, new, count, flags))

    def difference(self, symmetric=False):
        '''
        The difference between a series of things.

        @param symmetric: use symmetric difference (default: `False`)
        '''
        with self._chain():
            return self._many(self._difference(symmetric))

    def disjointed(self):
        '''The disjoint between a series of things.'''
        with self._chain():
            return self._one(self._disjointed)

    def intersection(self):
        '''The intersection between a series of things.'''
        with self._chain():
            return self._many(self._intersection)

    def partition(self, pattern=None, flags=0):
        '''
        Divide a series of things into `True` and `False` things based on the
        results returned by the current callable.

        @param pattern: regular expression search pattern (default: `None`)
        @param flags: regular expression flags (default: 0)
        '''
        with self._chain():
            return self._many(self._divide(self._test, pattern, flags))

    def subset(self):
        '''
        Tell if a series of things is a subset of other series of things.
        '''
        with self._chain():
            return self._one(self._subset)

    def superset(self):
        '''
        Tell if a series of things is a superset of another series of things.
        '''
        with self._chain():
            return self._one(self._superset)

    def union(self):
        '''The union between two series of things.'''
        with self._chain():
            return self._many(self._union)

    def unique(self):
        '''
        Get unique things within a series of things while preserving order and
        remember everything ever encountered.
        '''
        with self._chain():
            return self._iter(self._unique(self._identity))
