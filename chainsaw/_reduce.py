# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from threading import local
from collections import deque
from functools import partial, reduce
from itertools import cycle, islice

from stuf.six import strings
from chainsaw._compat import imap, ichain, tounicode, zip_longest


class _ReduceMixin(local):

    '''reduce mixin'''

    @staticmethod
    def _concat(iterable, ichain_=ichain):
        return ichain_(iterable)

    @classmethod
    def _flatten(cls, iterable, strings_=strings, isinstance_=isinstance):
        smash_ = cls._flatten
        for item in iterable:
            try:
                # don't recur over strings
                if isinstance_(item, strings_):
                    yield item
                else:
                    # do recur over other things
                    for j in smash_(item):
                        yield j
            except TypeError:
                # does not recur
                yield item

    @staticmethod
    def _join(sep, encoding, errors, imap_=imap, tounicode_=tounicode):
        def join(iterable):
            return tounicode(
                sep.join(imap_(tounicode_, iterable)), encoding, errors,
            )
        return join

    @staticmethod
    def _reduce(call, initial, reverse, reduce_=reduce):
        if reverse:
            if initial is None:
                def reduceright(iterable):
                    return reduce_(lambda x, y: call(y, x), iterable)
                return reduceright
            else:
                def reduceright(iterable):
                    return reduce_(lambda x, y: call(y, x), iterable, initial)
                return reduceright
        if initial is None:
            def _reduce(iterable):
                return reduce_(call, iterable)
        else:
            def _reduce(iterable):
                return reduce_(call, iterable, initial)
        return _reduce

    @classmethod
    def _roundrobin(cls, itrble, i=iter, n=next, s=islice, c=cycle, p=partial):
        work, measure = cls._clone(itrble)
        nexts = c(p(n, i(item)) for item in work)
        pending = len(list(measure))
        while pending:
            try:
                for nextz in nexts:
                    yield nextz()
            except StopIteration:
                pending -= 1
                nexts = c(s(nexts, pending))

    @staticmethod
    def _zip(iterable, zip_=zip_longest):
        return zip_(*iterable)


class _SliceMixin(local):

    '''slicing mixin'''

    @staticmethod
    def _first(n=0, islice_=islice, next_=next):
        def first(iterable):
            return islice_(iterable, n) if n else next_(iterable)
        return first

    @classmethod
    def _initial(cls, iterable, islice_=islice, len_=len, list_=list):
        i1, i2 = cls._clone(iterable)
        return islice_(i1, len_(list_(i2)) - 1)

    @classmethod
    def _last(cls, n, s=islice, d=deque, ln=len, l=list):
        def last(iterable):
            i1, i2 = cls._clone(iterable)
            return s(i1, ln(l(i2)) - n, None) if n else d(i1, maxlen=1).pop()
        return last

    @staticmethod
    def _nth(n, default, islice_=islice, next_=next):
        def nth(iterable):
            return next_(islice_(iterable, n, None), default)
        return nth

    @staticmethod
    def _rest(iterable, _islice=islice):
        return _islice(iterable, 1, None)

    @staticmethod
    def _slice(start, stop, step, _islice=islice):
        if stop and step:
            def slice_(iterable):
                return _islice(iterable, start, stop, step)
        elif stop:
            def slice_(iterable):
                return _islice(iterable, start, stop)
        else:
            def slice_(iterable):
                return _islice(iterable, start)
        return slice_

    @staticmethod
    def _split(n, fill, zip_longest_=zip_longest, iter_=iter):
        def grouper(iterable):
            return zip_longest_(fillvalue=fill, *[iter_(iterable)] * n)
        return grouper
