# -*- coding: utf-8 -*-
'''chainsaw mapping mixins'''

from threading import local


class RepeatMixin(local):

    '''repetition mixin'''

    def combinations(self, n):
        '''
        Find every possible combination of each `n` things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: length of things to derive combinations from
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

    def loops(self, n=1):
        '''
        Repeat results of nested `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ `n` times.

        :param n: number of loops to repeat (*default:* ``1``)
        '''
        with self._chain():
            return self._many(self._product(n))

    def permutations(self, n):
        '''
        Find every possible permutation of each `n` things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: length of things to derive permutations from
        '''
        with self._chain():
            return self._many(self._permutations(n))

    def repeat(self, n=None, call=False):
        '''
        Repeat either an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or the results
        of invoking the active callable `n` times.

        :param n: number of times to repeat (*default:* :const:`None`)

        :param call: repeat result of active callable (*default:*
          :const:`False`)
        '''
        with self._chain():
            return self._many(self._repeat(n, call, self._identity))


class MapMixin(local):

    '''mapping mixin'''

    def argmap(self, merge=False):  # @NoSelf
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ as wildcard
        `positional arguments
        <http://docs.python.org/glossary.html#term-positional-argument>`_ to
        the active callable.

        :param merge: combine global `positional
          <http://docs.python.org/glossary.html#term-positional-argument>`_
          arguments with wildcard `positional
          <http://docs.python.org/glossary.html#term-positional-argument>`_
          arguments from an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ (*default:*
          :const:`False`)
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
        collect the original thing instead of the value returned by calling the
        method if the return value of the method call is :const:`None`.

        :param name: method name
        '''
        with self._chain():
            return self._many(self._invoke(name, (self._args, self._kw)))

    def kwargmap(self, merge=False):  # @NoSelf
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ as a
        :class:`tuple` of wildcard `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword arguments
        <http://docs.python.org/glossary.html#term-keyword-argument>`_ to the
        active callable.

        :param merge: combine global `positional
          <http://docs.python.org/glossary.html#term-positional-argument>`_ and
          `keyword
          <http://docs.python.org/glossary.html#term-keyword-argument>`_
          arguments with `positional
          <http://docs.python.org/glossary.html#term-positional-argument>`_ and
          `keyword
          <http://docs.python.org/glossary.html#term-keyword-argument>`_
          arguments from an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ into a single
          tuple of wildcard `positional
          <http://docs.python.org/glossary.html#term-positional-argument>`_ and
          `keyword arguments
          <http://docs.python.org/glossary.html#term-keyword-argument>`_ for
          the active callable (*default:* :const:`False`)
        '''
        with self._chain():
            return self._many(self._kwargmap(
                self._call, merge, self._args, self._kw,
            ))

    def map(self):
        '''
        Feed each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ to the active
        callable.
        '''
        with self._chain():
            return self._many(self._map(self._call))
