# -*- coding: utf-8 -*-
'''chainsaw mapping mixins'''

from threading import local


class RepeatMixin(local):

    '''repetition mixin'''

    def combinations(self, n):
        '''
        Collect every possible combination of every `n` things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.


        :param n: number of things to derive combinations from
        '''
        with self._chain():
            return self._many(self._combinations(n))

    def copy(self):
        '''
        Collect duplicates of each thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._copy)

    def product(self, n=1):
        '''
        Collect results of nested `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ repeated `n`
        times.

        :param n: number of loops to repeat (*default:* ``1``)
        '''
        with self._chain():
            return self._many(self._product(n))

    def permutations(self, n):
        '''
        Collect every possible permutation of every `n` things within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: number of things to derive permutations from
        '''
        with self._chain():
            return self._many(self._permutations(n))

    def repeat(self, n=None, call=False):
        '''
        Collect the results of repeating an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or results
        of invoking the current callable `n` times.

        :param n: number of times to repeat (*default:* :const:`None`)

        :param call: repeat result of current callable (*default:*
          :const:`False`)
        '''
        with self._chain():
            return self._many(self._repeat(n, call, self._identity))


class MapMixin(local):

    '''mapping mixin'''

    def invoke(self, name):
        '''
        Invoke method `name` on each thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_ with
        the currently assigned `positional
        <http://docs.python.org/glossary.html#term-positional-argument>`_ and
        `keyword arguments
        <http://docs.python.org/glossary.html#term-keyword-argument>`_ and
        collect the results but
        collect the original thing instead of the value returned after calling
        the method the return value is :const:`None`.

        :param name: method name
        '''
        with self._chain():
            return self._many(
                self._invoke(name, (self._args, self._kw))
            )

    def map(self, args=False, kwargs=False, current=False):
        '''
        Invoke the current callable on each thing within an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.

        :param args: pass each thing within an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ as `*args
          <http://docs.python.org/glossary.html#term-positional-argument>`_ to
          the current callable (*default:* :const:`False`)
        :param kwargs: pass each thing within an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ to the current
          callable as a :class:`tuple` of `*args
          <http://docs.python.org/glossary.html#term-positional-argument>`_ and
          `**kwargs
          <http://docs.python.org/glossary.html#term-keyword-argument>`_
          (*default:* :const:`False`)
        :param current: pass each thing within an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ as a
          :class:`tuple` of `*args
          <http://docs.python.org/glossary.html#term-positional-argument>`_ and
          `**kwargs
          <http://docs.python.org/glossary.html#term-keyword-argument>`_
          combined with any assigned `positional
          <http://docs.python.org/glossary.html#term-positional-argument>`_ or
          `keyword arguments
          <http://docs.python.org/glossary.html#term-keyword-argument>`_ for
          the current callable (*default:* :const:`False`)
        '''
        args = kwargs if kwargs else args
        with self._chain():
            return self._many(self._map(
                self._call, args, kwargs, current, self._args, self._kw,
            ))
