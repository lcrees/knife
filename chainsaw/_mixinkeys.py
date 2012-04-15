# -*- coding: utf-8 -*-
'''reference keys'''

from appspace.keys import AppspaceKey


class KCompare(AppspaceKey):

    '''comparing key'''

    def all():  # @NoSelf
        '''
        Discover if the worker returns :const:`True` for **everything** within
        an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the iterable is empty).
        
        :rtype: :class:`bool`
        '''

    def any():  # @NoSelf
        '''
        Discover if the worker returns :const:`True` for **anything** within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ (or if
        the iterable is empty).
        
        :rtype: :class:`bool`
        '''

    def difference(symmetric=False):  # @NoSelf
        '''
        Find differences within a series of
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_.

        :keyword boolean symmetric: use symmetric difference
        :rtype: :class:`set`
        '''

    def disjoint():  # @NoSelf
        '''
        Find disjoints within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        
        :rtype: :class:`set`
        '''

    def intersect():  # @NoSelf
        '''
        Find intersections within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :rtype: :class:`set`
        '''

    def subset():  # @NoSelf
        '''
        Discover if `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ are subsets
        other iterables.
        
        :rtype: :class:`bool`
        '''

    def superset():  # @NoSelf
        '''
        Discover if `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ are supersets of
        others iterables.
        
        :rtype: :class:`bool`
        '''

    def union():  # @NoSelf
        '''
        Find unions within a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_.
        
        :rtype: :class:`set`
        '''

    def unique():  # @NoSelf
        '''
        Find unique things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        
        :rtype: :class:`set`
        '''


class KMath(AppspaceKey):

    '''mathing key'''

    def average():  # @NoSelf
        '''
        Find average value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        
        :rtype: number
        '''

    def count():  # @NoSelf
        '''
        Count how many times each thing occurs within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        
        :returns: :class:`tuple` consisting of (*least common thing*, *most common
          thing*, *count of everything* consisting of a :class:`list` of
          :class:`tuple` pairs of (*thing*, *count*).
        
        :rtype: :class:`tuple`
        '''

    def max():  # @NoSelf
        '''
        Find maximum value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        
        :rtype: number
        '''

    def median():  # @NoSelf
        '''
        Find median value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        
        :rtype: number
        '''

    def min():  # @NoSelf
        '''
        Find minimum value within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        
        :rtype: number
        '''

    def minmax():  # @NoSelf
        '''
        Find minimum and maximum values within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        
        :returns: :class:`tuple` of (*minimum value*, *maximum value*).
        :rtype: :class:`tuple`
        '''

    def range():  # @NoSelf
        '''
        Find length of the smallest interval that can contain everything
        within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        
        :rtype: number
        '''

    def sum(start=0, precision=False):  # @NoSelf
        '''
        Find total value by adding `start` and everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ together.

        :keyword start: starting number
        :type start: integer or float

        :keyword boolean precision: add floats with extended precision
        
        :rtype: number
        '''


class KOrder(AppspaceKey):

    '''ordering mixin'''

    def group():  # @NoSelf
        '''
        Group things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def reverse():  # @NoSelf
        '''
        Reverse the order of things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def sort():  # @NoSelf
        '''
        Sort things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ using the
        worker as the `key function
        <http://docs.python.org/glossary.html#term-key-function>`_.
        '''

    def shuffle():  # @NoSelf
        '''
        Randomly reorder things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''


class KRepeat(AppspaceKey):

    '''repeating key'''

    def combinations(n):  # @NoSelf
        '''
        Find combinations of every `n` things withing an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :argument integer n: length of things to combine from
        '''

    def copy():  # @NoSelf
        '''
        Duplicate each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def permutations(n):  # @NoSelf
        '''
        Find permutations of every `n` things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :argument integer n: length of things to permutate from
        '''

    def repeat(n=None, call=False):  # @NoSelf
        '''
        Repeat either an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or invoke
        worker `n` times.

        :keyword integer n: number of times to repeat

        :keyword boolean call: repeat results of invoking worker
        '''


class KMap(AppspaceKey):

    '''mapping key'''

    def argmap(merge=False):  # @NoSelf
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ to
        the worker as `wildcard
        <http://docs.python.org/reference/compound_stmts.html#function>`_
        `positional arguments
        <http://docs.python.org/glossary.html#term-positional-argument>`_ .

        :keyword boolean merge: merge global positional arguments with positional
          arguments from an iterable
        '''

    def invoke(name):  # @NoSelf
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

    def kwargmap(merge=False):  # @NoSelf
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

        :keyword boolean merge: merge global positional or keyword arguments with
          positional and keyword arguments from an iterable into a single
          :class:`tuple` of wildcard positional and keyword arguments like
          (*iterable_args* + *global_args*, *global_kwargs* +
          *iterable_kwargs*)
        '''

    def map():  # @NoSelf
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ to the worker.
        '''


class KFilter(AppspaceKey):

    '''filtering key'''

    def attributes(*names):  # @NoSelf
        '''
        Collect `attribute
        <http://docs.python.org/glossary.html#term-attribute>`_ values from
        things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ that matches an
        attribute name value in `names`.

        :argument string names: attribute names
        '''

    def duality():  # @NoSelf
        '''
        Divide one `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ into two
        iterables, the first being everything the worker evaluates as
        :const:`True` and the second being everything the worker evaluates as
        :const:`False`.
        '''

    def filter(invert=False):  # @NoSelf
        '''
        Collect each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ matched by the
        worker.

        :keyword boolean invert: collect things the worker evaluates as :const:`False`
          instead of :const:`True`
        '''

    def items(*keys):  # @NoSelf
        '''
        Collect values from things (usually `sequences
        <http://docs.python.org/glossary.html#term-sequence>`_ or `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_) within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        that match a key value in `keys`.

        :argument string keys: item keys (or indexes)
        '''

    def mapping(keys=False, values=False):  # @NoSelf
        '''
        Collect items, keys, or values from things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ of `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_.

        :keyword boolean keys: collect keys only

        :keyword boolean values: collect values only
        '''

    def traverse(ancestors=False, invert=False):  # @NoSelf
        '''
        Collect nested values from each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ matched by the worker.

        :keyword boolean ancestors: collect things from parents of things based on
          `method resolution order (MRO)
          <http://docs.python.org/glossary.html#term-method-resolution-order>`_

        :keyword boolean invert: select things that the worker evaluates as
          :const:`False` rather than :const:`True`
        '''


class KReduce(AppspaceKey):

    '''reducing key'''

    def flatten():  # @NoSelf
        '''
        Flatten nested things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def merge():  # @NoSelf
        '''
        Combine multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ into one
        iterable.
        '''

    def reduce(initial=None, reverse=False):  # @NoSelf
        '''
        Reduce an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ down to one
        thing using the worker.

        :keyword initial: starting value

        :keyword boolean reverse: reduce from `the right side
          <http://www.zvon.org/other/haskell/Outputprelude/foldr_f.html>`_
          of an iterable
        '''

    def weave():  # @NoSelf
        '''
        Interleave things found at the same position across multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ while reducing
        multiple iterables to one.
        '''

    def zip():  # @NoSelf
        '''
        Reduce multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ to one iterable
        by pairing every two things as a :class:`tuple` of (*thing1*,
        *thing2*).
        '''


class KSlice(AppspaceKey):

    '''slicing key'''

    def at(n):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off thing
        found at `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ index `n`.

        :argument integer n: index of some thing

        :keyword default: default thing returned if nothing is found at `n`
        '''

    def choice():  # @NoSelf
        '''
        `Randomly slice <http://docs.python.org/glossary.html#term-slice>`_ off
        one thing from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''

    def dice(n, fill=None):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ one
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ into
        multiple iterables of `n` things.

        :argument integer n: number of things per slice

        :keyword fill: value to pad out incomplete things
        '''

    def first(n=0):  # @NoSelf
        '''
        Slice off `n` things from the starting end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the
        **first** thing.

        :keyword integer n: number of things
        '''

    def initial():  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the
        **last** thing.
        '''

    def last(n=0):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off either
        `n` things from the tail end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the
        **last** thing.

        :keyword integer n: number of things
        '''

    def rest():  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the
        **first** thing.
        '''

    def sample(n):  # @NoSelf
        '''
        Randomly `slice <http://docs.python.org/glossary.html#term-slice>`_ off
        `n` things from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :argument integer n: size of sample
        '''

    def slice(start, stop=False, step=False):  # @NoSelf
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off things
        from `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :argument integer start: starting index of slice

        :keyword integer stop: stopping index of slice

        :keyword integer step: size of step in slice
        '''
