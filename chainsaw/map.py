# -*- coding: utf-8 -*-
'''chainsaw mapping mixins'''

from threading import local


class RepeatMixin(local):

    '''repeating mixin'''

    def combinations(self, n):
        '''
        Find combinations of every `n` things from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.


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

    def permutations(self, n):
        '''
        Find permutations of every `n` things from an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: length of things to derive permutations from
        '''
        with self._chain():
            return self._many(self._permutations(n))

    def repeat(self, n=None, call=False):
        '''
        Repeat either an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or results of
        invoking active callable `n` times.

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

        :param merge: combinations global positional arguments with wildcard
          positional arguments from an iterable (*default:* :const:`False`)
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

        :param merge: combinations global positional and keyword arguments with
          positional and keyword arguments from an iterable into a single
          :class:`tuple` of wildcard positional and keyword arguments for the
          active callable (*default:* :const:`False`)
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
