# -*- coding: utf-8 -*-
'''chainsaw reducing mixins'''

from math import fsum
from random import shuffle
from threading import local
from operator import truediv
from itertools import groupby, tee

from chainsaw._compat import Counter, imap


class _CompareMixin(local):

    '''comparing mixin'''

    @staticmethod
    def _all(truth, all_=all, imap_=imap):
        return lambda x: all_(imap_(truth, x))

    @staticmethod
    def _any(truth, any_=any, imap_=imap):
        return lambda x: any_(imap_(truth, x))

    @staticmethod
    def _difference(symmetric, reduce_=reduce, set_=set):
        if symmetric:
            test = lambda x, y: set_(x).symmetric_difference(y)
        else:
            test = lambda x, y: set_(x).difference(y)
        return lambda x: reduce_(test, x)

    @staticmethod
    def _disjointed(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).isdisjoint(y), iterable)

    @staticmethod
    def _intersection(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).intersection(y), iterable)

    @staticmethod
    def _subset(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).issubset(y), iterable)

    @staticmethod
    def _superset(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).issuperset(y), iterable)

    @staticmethod
    def _union(iterable, set_=set, reduce_=reduce):
        return reduce_(lambda x, y: set_(x).union(y), iterable)

    @staticmethod
    def _unique(key, set_=set):
        def unique(iterable):
            seen = set_()
            seenadd, key_ = seen.add, key
            for element in iterable:
                k = key_(element)
                if k not in seen:
                    seenadd(k)
                    yield element
        return unique


class _NumberMixin(local):

    '''number mixin'''

    @staticmethod
    def _average(iterable, s=sum, t=truediv, n=len, tee_=tee):
        i1, i2 = tee_(iterable)
        return t(s(i1, 0.0), n(list(i2)))

    @staticmethod
    def _count(iterable, counter=Counter):
        count = counter(iterable)
        commonality = count.most_common()
        return (
            # least common
            commonality[:-2:-1][0][0],
            # most common (mode)
            count.most_common(1)[0][0],
            # overall commonality
            commonality,
        )

    @staticmethod
    def _max(key, imax_=max):
        return lambda x: imax_(x, key=key)

    @staticmethod
    def _median(iterable, s=sorted, l=list, d=truediv, int=int, len=len):
        i = l(s(iterable))
        e = d(len(i) - 1, 2)
        p = int(e)
        return i[p] if e % 2 == 0 else truediv(i[p] + i[p + 1], 2)

    @staticmethod
    def _minmax(iterable, iter_=iter, imin=min, imax=max, tee_=tee):
        i1, i2 = tee_(iterable)
        return iter_((imin(i1), imax(i2)))

    @staticmethod
    def _range(iterable, list_=list, sorted_=sorted):
        i1 = list_(sorted_(iterable))
        return i1[-1] - i1[0]

    @staticmethod
    def _min(key, imin_=min):
        return lambda x: imin_(x, key=key)

    @staticmethod
    def _sum(start, floats, isum=sum, fsum_=fsum):
        return lambda x: (fsum_ if floats else lambda x: isum(x, start))(x)


class _OrderMixin(local):

    '''order mixin'''

    @staticmethod
    def _group(key, imap_=imap, tuple_=tuple, groupby_=groupby):
        grouper = lambda x: (x[0], tuple_(x[1]))
        return lambda x: imap_(grouper, groupby_(x, key))

    @staticmethod
    def _reverse(iterable, list_=list, reversed_=reversed):
        return reversed_(list_(iterable))

    @staticmethod
    def _shuffle(iterable, list_=list, shuffle_=shuffle):
        iterable = list_(iterable)
        shuffle_(iterable)
        return iterable

    @staticmethod
    def _sort(key, sorted_=sorted):
        return lambda x: sorted_(x, key=key)
