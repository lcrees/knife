# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from threading import local


class FilterMixin(local):

    '''filtering mixin'''

    def attributes(self, *names):
        '''
        Collect `attribute
        <http://docs.python.org/glossary.html#term-attribute>`_ values from
        things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ that
        matches an attribute name value in `names`.

        :param names: attribute names
        '''
        with self._chain():
            return self._iter(self._attributes(names))

    def duality(self):  # @NoSelf
        '''
        Divide one iterable into two `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_, the first
        iterable being everything the active callable evaluates as
        :const:`True` and the second iterable being everythin the active
        callable evaluates as :const:`False`.
        '''
        with self._chain():
            return self._many(self._duality(self._test))

    def filter(self, invert=False):
        '''
        Collect each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ matched by the
        active callable.

        :param invert: return things for which the filter is :const:`False`
          rather than :const:`True` (*default:* :const:`False`)
        '''
        with self._chain():
            return self._many(self._filter(self._test, invert))

    def items(self, *keys):
        '''
        Collect values from things (usually `sequences
        <http://docs.python.org/glossary.html#term-sequence>`_ or `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_) within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        that match a key value in `keys`.

        :param keys: item keys (or indexes)
        '''
        with self._chain():
            return self._iter(self._items(keys))

    def mapping(self, keys=False, values=False):
        '''
        Collect items, keys, or values from things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ of `mappings
        <http://docs.python.org/glossary.html#term-mapping>`_.

        :param keys: collect keys only (*default:* :const:`False`)

        :param values: collect values only (*default:* :const:`False`)
        '''
        with self._chain():
            return self._many(self._mapping(self._identity, keys, values))

    def pattern(self, pattern, type='parse', flags=0):  # @NoSelf
        '''
        Compile a search pattern to use as the active callable.

        :param pattern: search pattern

        :param type: engine to compile pattern with. Valid options are
          ``'parse'``, ``'regex'``, or ``'glob'`` (default: ``'parse'``)

        :param flags: regular expression `flags
          <http://docs.python.org/library/re.html#re.DEBUG>`_ (*default:*
          ``0``)
        '''
        return self.tap(self._pattern(pattern, type, flags))

    def traverse(self, ancestors=False, invert=False):  # @NoSelf
        '''
        Collect nested values from each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ matched by the
        active callable.

        :param ancestors: collect things from parents of a thing based on
          `method resolution order (MRO)
          <http://docs.python.org/glossary.html#term-method-resolution-order>`_
          (default: :const:`False`)

        :param invert: return things active callable evaluates as
          :const:`False` rather than :const:`True` (*default:* :const:`False`)
        '''
        with self._chain():
            return self._many(self._traverse(
                self._test, self._alt, self._wrapper, ancestors, invert,
            ))


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
        <http://docs.python.org/glossary.html#term-iterable>`_ to one
        thing with active callable.

        :param initial: starting value (*default:*: :const:`None`)

        :param reverse: reduce from `the right side
          <http://www.zvon.org/other/haskell/Outputprelude/foldr_f.html>`_
          of an iterable (*default:* :const:`False`)
        '''
        with self._chain():
            return self._one(self._reduce(self._call, initial, reverse))

    def weave(self):
        '''
        Interleave every other thing from multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ into one
        iterable.
        '''
        with self._chain():
            return self._many(self._weave)

    def zip(self):
        '''
        Reduce multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ to one iterable
        by pairing every two things in a :class:`tuple` of
        (*thing1*, *thing2*).
        '''
        with self._chain():
            return self._many(self._zip)


class SliceMixin(local):

    '''slicing mixin'''

    def at(self, n, default=None):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off a thing
        found at `n` position within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or `default` if
        nothing is found at `n`.

        :param n: index of some thing

        :param default: default thing (*default:*: :const:`None`)
        '''
        with self._chain():
            return self._one(self._at(n, default))

    def choice(self):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off a thing
        at random from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._one(self._choice)

    def dice(self, n, fill=None):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ into multiple
        iterables of `n` things.

        :param n: number of things per split

        :param fill: value to pad out incomplete things (*default:*
          :const:`None`)
        '''
        with self._chain():
            return self._many(self._dice(n, fill))

    def first(self, n=0):
        '''
        Slice off either `n` things from the starting end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or the
        **first** thing within an iterable.

        :param n: number of things (*default:*: ``0``)
        '''
        with self._chain():
            first = self._first
            return self._many(first(n)) if n else self._one(first(n))

    def initial(self):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the very
        **last** thing.
        '''
        with self._chain():
            return self._many(self._initial)

    def last(self, n=0):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off either
        `n` things from the tail end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the
        **last** thing within an iterable.

        :param n: number of things (*default:*: ``0``)
        '''
        with self._chain():
            return self._many(self._last(n)) if n else self._one(self._last(n))

    def rest(self):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off
        everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the very
        **first** thing.
        '''
        with self._chain():
            return self._many(self._rest)

    def sample(self, n):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off a
        random sample of `n` things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: sample size
        '''
        with self._chain():
            return self._many(self._sample(n))

    def slice(self, start, stop=False, step=False):
        '''
        `Slice <http://docs.python.org/glossary.html#term-slice>`_ off things
        within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ from `start` to
        (optionally) `stop` in `step` steps.

        :param start: starting index of slice

        :param stop: stopping index of slice (*default:* :const:`False`)

        :param step: size of step in slice (*default:* :const:`False`)
        '''
        with self._chain():
            return self._many(self._slice(start, stop, step))
