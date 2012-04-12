# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from threading import local

from stuf.six import u


class ReduceMixin(local):

    '''reduce mixin'''

    def concat(self):
        '''
        Collect one
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        created by merge multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ together.
        '''
        with self._chain():
            return self._many(self._concat)

    def flatten(self):
        '''
        Collect the result of reducing an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ of nested things
        to an `iterable <http://docs.python.org/glossary.html#term-iterable>`_
        of unnested things because `flat is better than nested
        <http://www.python.org/dev/peps/pep-0020/>`_.
        '''
        with self._chain():
            return self._many(self._flatten)

    def join(self, separator=u(''), encoding='utf-8', errors='strict'):
        '''
        Collect the result of combining an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ of multiple
        things into one :class:`unicode` (:class:`str` on Python 3) decoded
        thing.

        :param separator: string to join at (*default:*: ``''``)

        :param encoding: Unicode encoding for things (*default:*: ``'utf-8'``)

        :param errors: error handling when encoding things (*default:*:
          ``'strict'``)
        '''
        with self._chain():
            return self._one(self._join(separator, encoding, errors))

    def reduce(self, initial=None, reverse=False):
        '''
        Collect the result of reducing an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ down to one
        thing using the current callable. If ``reverse`` is set to
        :const:`True`, reduction `comes from the right side
        <http://www.zvon.org/other/haskell/Outputprelude/foldr_f.html>`_ of an
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        Otherwise, reduction comes from the left side of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param initial: starting value (*default:*: :const:`None`)

        :param reverse: reduce from right side of an `iterable
          <http://docs.python.org/glossary.html#term-iterable>`_ (*default:*:
          :const:`False`)
        '''
        with self._chain():
            return self._one(self._reduce(self._call, initial, reverse))

    def weave(self):
        '''
        Collect the result of interleaving multiple `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ into one
        `iterable <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._roundrobin)

    def zip(self):
        '''
        Collect the result of reducing a series of `iterables
        <http://docs.python.org/glossary.html#term-iterable>`_ to one `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ where every two
        things are paired in a :class:`tuple` of (*thing1*, *thing2*) based on
        where they were found within the original `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.
        '''
        with self._chain():
            return self._many(self._zip)


class SliceMixin(local):

    '''slicing mixin'''

    def first(self, n=0):
        '''
        Collect either `n` things from the starting end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the
        **first** thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: number of things (*default:*: ``0``)
        '''
        with self._chain():
            first = self._first
            return self._many(first(n)) if n else self._one(first(n))

    def initial(self):
        '''
        Collect everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the very
        **last** thing.
        '''
        with self._chain():
            return self._many(self._initial)

    def last(self, n=0):
        '''
        Collect either `n` things from the trailing end of an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or just the
        **last** thing within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param n: number of things (*default:*: ``0``)
        '''
        with self._chain():
            last = self._last
            return self._many(last(n)) if n else self._one(last(n))

    def at(self, n, default=None):
        '''
        Collect thing found at `n` position within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ or `default` if
        nothing is found at `n`.

        :param n: index of some thing

        :param default: default thing (*default:*: :const:`None`)
        '''
        with self._chain():
            return self._one(self._nth(n, default))

    def rest(self):
        '''
        Collect everything within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ except the very
        **first** thing.
        '''
        with self._chain():
            return self._many(self._rest)

    def slice(self, start, stop=False, step=False):
        '''
        Collect a `slice <http://docs.python.org/glossary.html#term-slice>`_ of
        things within an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_.

        :param start: starting index of slice

        :param stop: stopping index of slice
          (*default:* :const:`False`)
        :param step: size of step in slice
          (*default:* :const:`False`)
        '''
        with self._chain():
            return self._many(self._slice(start, stop, step))

    def split(self, n, fill=None):
        '''
        Split an `iterable
        <http://docs.python.org/glossary.html#term-iterable>`_ into multiple
        `iterables <http://docs.python.org/glossary.html#term-iterable>`_ of
        `n` things while using `fill` to pad out results that fall short of
        `n`.

        :param n: number of things per split
        :param fill: value to pad out incomplete things (*default:*
          :const:`None`)
        '''
        with self._chain():
            return self._many(self._split(n, fill))
