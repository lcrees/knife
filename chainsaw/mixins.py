# -*- coding: utf-8 -*-
'''chainsaw mixins'''

from threading import local


class CompareMixin(local):

    '''comparing mixin'''

    def all(self):
        '''
        Discover if the worker returns :const:`True` for **everything** within
        an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the iterable is empty).

        :rtype: :class:`bool`
        '''
        with self._chain():
            return self._one(self._all(self._test))

    def any(self):
        '''
        Discover if the worker returns :const:`True` for **anything** within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the iterable is empty).

        :rtype: :class:`bool`
        '''
        with self._chain():
            return self._one(self._any(self._test))

    def difference(self, symmetric=False):
        '''
        Find differences within a series of
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_.

        :keyword boolean symmetric: use symmetric difference
        :rtype: :class:`set`
        '''
        with self._chain():
            return self._many(self._difference(symmetric))

    def disjointed(self):
        '''
        Find disjoints within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :rtype: :class:`set`
        '''
        with self._chain():
            return self._one(self._disjointed)

    def intersection(self):
        '''
        Find intersections within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :rtype: :class:`set`
        '''
        with self._chain():
            return self._many(self._intersection)

    def subset(self):
        '''
        Discover if `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ are subsets
        other iterables.

        :rtype: :class:`bool`
        '''
        with self._chain():
            return self._one(self._subset)

    def superset(self):
        '''
        Discover if `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ are supersets of
        others iterables.

        :rtype: :class:`bool`
        '''
        with self._chain():
            return self._one(self._superset)

    def union(self):
        '''
        Find unions within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :rtype: :class:`set`
        '''
        with self._chain():
            return self._many(self._union)

    def unique(self):
        '''
        Find unique things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :rtype: :class:`set`
        '''
        with self._chain():
            return self._iter(self._unique(self._identity))


class MathMixin(local):

    '''mathing mixin'''

    def average(self):
        '''
        Find average value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :rtype: number
        '''
        with self._chain():
            return self._iter(self._average)

    def count(self):
        '''
        Count how many times each thing occurs within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :returns: :class:`tuple` consisting of (*least common thing*,
          *most common thing*, *count of everything* consisting of a
          :class:`list` of :class:`tuple` pairs of (*thing*, *count*).

        :rtype: :class:`tuple`
        '''
        with self._chain():
            return self._iter(self._count)

    def max(self):
        '''
        Find maximum value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.

        :rtype: number
        '''
        with self._chain():
            return self._iter(self._max(self._identity))

    def median(self):
        '''
        Find median value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :rtype: number
        '''
        with self._chain():
            return self._iter(self._median)

    def min(self):
        '''
        Find minimum value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.

        :rtype: number
        '''
        with self._chain():
            return self._iter(self._min(self._identity))

    def minmax(self):
        '''
        Find minimum and maximum values within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :returns: :class:`tuple` of (*minimum value*, *maximum value*).
        :rtype: :class:`tuple`
        '''
        with self._chain():
            return self._iter(self._minmax)

    def range(self):
        '''
        Find length of the smallest interval that can contain everything
        within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :rtype: number
        '''
        with self._chain():
            return self._iter(self._range)

    def sum(self, start=0, precision=False):
        '''
        Find total value by adding `start` and everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ together.

        :keyword start: starting number
        :type start: integer or float

        :keyword boolean precision: add floats with extended precision

        :rtype: number
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


class RepeatMixin(local):

    '''repeating mixin'''

    def combinations(self, n):
        '''
        Find combinations of every `n` things withing an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :argument integer n: length of things to combine from
        '''
        with self._chain():
            return self._many(self._combinations(n))

    def copy(self):
        '''
        Duplicate each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._copy)

    def permutations(self, n):
        '''
        Find permutations of every `n` things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :argument integer n: length of things to permutate from
        '''
        with self._chain():
            return self._many(self._permutations(n))

    def repeat(self, n=None, call=False):
        '''
        Repeat either an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or invoke
        worker `n` times.

        :keyword integer n: number of times to repeat

        :keyword boolean call: repeat results of invoking worker
        '''
        with self._chain():
            return self._many(self._repeat(n, call, self._identity))


class MapMixin(local):

    '''mapping mixin'''

    def argmap(self, merge=False):  # @NoSelf
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ to
        the worker as `wildcard
        <http://docs.python.org/reference/compound_stmts.html#function>`_
        `positional arguments
        <http://docs.python.org/glossary.html#term-positional-argument>`_ .

        :keyword boolean merge: merge global positional arguments with
          positional arguments derived from an iterable
        '''
        with self._chain():
            return self._many(self._argmap(
                self._call, merge, self._args, self._kw,
            ))

    def invoke(self, name):
        '''
        Call method `name` from each thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ with
        the global `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword arguments
        <http://docs.python.org/glossary.html#term-keyword-argument>`_ but
        take the original thing if the return value of the method call is
        :const:`None`.

        :argument string name: method name
        '''
        with self._chain():
            return self._many(self._invoke(name, (self._args, self._kw)))

    def kwargmap(self, merge=False):  # @NoSelf
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ as a
        :class:`tuple` of `wildcard
        <http://docs.python.org/reference/compound_stmts.html#function>`_
        `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword arguments
        <http://docs.python.org/glossary.html#term-keyword-argument>`_ to the
        worker.

        :keyword boolean merge: merge global positional or keyword arguments
          with positional and keyword arguments derived from an iterable into
          a single :class:`tuple` of wildcard positional and keyword arguments
          like (*iterable_args* + *global_args*, *global_kwargs* +
          *iterable_kwargs*)
        '''
        with self._chain():
            return self._many(self._kwargmap(
                self._call, merge, self._args, self._kw,
            ))

    def map(self):
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ to the worker.
        '''
        with self._chain():
            return self._many(self._map(self._call))


class FilterMixin(local):

    '''filtering mixin'''

    def attributes(self, *names):
        '''
        Collect `attribute
        <http://docs.python.org/glossary.html#term-attribute>`_ values from
        things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ that matches an
        attribute name value found in `names`.

        :argument string names: attribute names
        '''
        with self._chain():
            return self._iter(self._attributes(names))

    def duality(self):
        '''
        Divide one `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ into two
        iterables, the first being everything the worker evaluates as
        :const:`True` and the second being everything the worker evaluates as
        :const:`False`.
        '''
        with self._chain():
            return self._iter(self._duality(self._test))

    def filter(self, invert=False):
        '''
        Collect each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ matched by the
        worker.

        :keyword boolean invert: collect things the worker evaluates as
          :const:`False` instead of :const:`True`
        '''
        with self._chain():
            return self._many(self._filter(self._test, invert))

    def items(self, *keys):
        '''
        Collect values from things (usually `sequences
        <http://docs.python.org/glossary.html#term-sequence>`_ or `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_) within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        that match a key value found in `keys`.

        :argument string keys: item keys (or indexes)
        '''
        with self._chain():
            return self._iter(self._items(keys))

    def mapping(self, keys=False, values=False):
        '''
        Collect items, keys, or values from things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ of `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_.

        :keyword boolean keys: collect keys only

        :keyword boolean values: collect values only
        '''
        with self._chain():
            return self._many(self._mapping(self._identity, keys, values))

    def traverse(self, invert=False):
        '''
        Collect nested values from each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ matched by the
        worker.

        :keyword boolean ancestors: collect things from parents of things based
          on `method resolution order (MRO)
          <http://docs.python.org/glossary.html#term-method-resolution-order>`_

        :keyword boolean invert: select things that the worker evaluates as
          :const:`False` rather than :const:`True`
        '''
        with self._chain():
            if self._call is None:
                test = lambda x: not x[0].startswith('__')
            else:
                test = self._call
            return self._many(self._traverse(test, invert))


class ReduceMixin(local):

    '''reducing mixin'''

    def flatten(self):
        '''
        Flatten nested things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._flatten)

    def merge(self):
        '''
        Combine multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ into one
        iterable.
        '''
        with self._chain():
            return self._many(self._merge)

    def reduce(self, initial=None, reverse=False):
        '''
        Reduce an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ down to one
        thing using the worker.

        :keyword initial: starting value

        :keyword boolean reverse: reduce from `the right side
          <http://www.zvon.org/other/haskell/Outputprelude/foldr_f.html>`_
          of an iterable
        '''
        with self._chain():
            return self._one(self._reduce(self._call, initial, reverse))

    def weave(self):
        '''
        Interleave things found at the same position across multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ while reducing
        multiple iterables to one.
        '''
        with self._chain():
            return self._many(self._weave)

    def zip(self):
        '''
        Reduce multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ to one iterable
        by pairing every two things as a :class:`tuple` of (*thing1*,
        *thing2*).
        '''
        with self._chain():
            return self._many(self._zip)


class SliceMixin(local):

    '''slicing mixin'''

    def at(self, n, default=None):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off thing
        found at `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ index `n`.

        :argument integer n: index of some thing

        :keyword default: default thing returned if nothing is found at `n`
        '''
        with self._chain():
            return self._one(self._at(n, default))

    def choice(self):
        '''
        `Randomly slice <http://docs.python.org/glossary.html#term-slice>`_ off
        one thing from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._iter(self._choice)

    def dice(self, n, fill=None):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ one
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ into
        multiple iterables of `n` things.

        :argument integer n: number of things per slice

        :keyword fill: value to pad out incomplete things
        '''
        with self._chain():
            return self._many(self._dice(n, fill))

    def first(self, n=0):
        '''
        Slice off `n` things from the starting end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the
        **first** thing.

        :keyword integer n: number of things
        '''
        with self._chain():
            return self._iter(self._first(n))

    def initial(self):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the
        **last** thing.
        '''
        with self._chain():
            return self._many(self._initial)

    def last(self, n=0):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off either
        `n` things from the tail end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the
        **last** thing.

        :keyword integer n: number of things
        '''
        with self._chain():
            return self._iter(self._last(n))

    def rest(self):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the
        **first** thing.
        '''
        with self._chain():
            return self._many(self._rest)

    def sample(self, n):
        '''
        Randomly `slice <http://docs.python.org/glossary.html#term-slice>`_ off
        `n` things from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :argument integer n: size of sample
        '''
        with self._chain():
            return self._iter(self._sample(n))

    def slice(self, start, stop=False, step=False):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off things
        from `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :argument integer start: starting index of slice

        :keyword integer stop: stopping index of slice

        :keyword integer step: size of step in slice
        '''
        with self._chain():
            return self._many(self._slice(start, stop, step))
