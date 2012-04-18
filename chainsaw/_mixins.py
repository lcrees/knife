# -*- coding: utf-8 -*-
'''chainsaw _mixins'''

from math import fsum
from copy import deepcopy
from threading import local
from collections import deque
from inspect import isclass, getmro
from functools import partial, reduce
from random import choice, sample, shuffle
from operator import methodcaller, itemgetter, attrgetter, truediv
from itertools import (
    groupby, cycle, islice, tee, starmap, repeat, combinations, permutations)


from stuf.six import strings, items, values, keys, filter, map
from stuf.utils import OrderedDict, selfname, deferiter, deferfunc

from chainsaw._compat import (
    Counter, ChainMap, ichain, ifilterfalse, zip_longest)


class _CompareMixin(local):

    '''comparing mixin'''

    @staticmethod
    def _all(truth, all_=all, imap_=map):
        return lambda x: all_(imap_(truth, x))

    @staticmethod
    def _any(truth, any_=any, imap_=map):
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


class _MathMixin(local):

    '''number mixin'''

    @staticmethod
    def _average(iterable, s=sum, t=truediv, n=len, e=tee, l=list):
        i1, i2 = e(iterable)
        yield t(s(i1, 0.0), n(l(i2)))

    @staticmethod
    def _count(iterable, counter=Counter):
        count = counter(iterable)
        commonality = count.most_common()
        yield (
            # least common
            commonality[:-2:-1][0][0],
            # most common (mode)
            count.most_common(1)[0][0],
            # overall commonality
            commonality,
        )

    @staticmethod
    def _max(key, imax_=max):
        def imax(iterable):
            yield imax_(iterable, key=key)
        return imax

    @staticmethod
    def _median(iterable, s=sorted, l=list, d=truediv, int=int, len=len):
        i = l(s(iterable))
        e = d(len(i) - 1, 2)
        p = int(e)
        yield i[p] if e % 2 == 0 else truediv(i[p] + i[p + 1], 2)

    @staticmethod
    def _minmax(iterable, imin=min, imax=max, tee_=tee):
        i1, i2 = tee_(iterable)
        yield imin(i1), imax(i2)

    @staticmethod
    def _range(iterable, list_=list, sorted_=sorted):
        i1 = list_(sorted_(iterable))
        yield i1[-1] - i1[0]

    @staticmethod
    def _min(key, imin_=min):
        def imin(iterable):
            yield imin_(iterable, key=key)
        return imin

    @staticmethod
    def _sum(start, floats, isum_=sum, fsum_=fsum):
        summer = fsum_ if floats else lambda x: isum_(x, start)
        def isum(iterable): #@IgnorePep8
            yield summer(iterable)
        return isum


class _OrderMixin(local):

    '''order mixin'''

    @staticmethod
    def _group(key, imap_=map, tuple_=tuple, groupby_=groupby):
        grouper = lambda x: (x[0], tuple_(x[1]))
        return lambda x: imap_(grouper, groupby_(x, key))

    @staticmethod
    def _reverse(iterable, list_=list, reversed_=reversed):
        yield list_(reversed_(list_(iterable)))

    @staticmethod
    def _shuffle(iterable, list_=list, shuffle_=shuffle):
        iterable = list_(iterable)
        shuffle_(iterable)
        yield iterable

    @staticmethod
    def _sort(key, sorted_=sorted):
        def isort(iterable):
            yield sorted_(iterable, key=key)
        return isort


class _RepeatMixin(local):

    '''repetition mixin'''

    @staticmethod
    def _combinations(n, combinations_=combinations):
        return lambda x: combinations_(x, n)

    @staticmethod
    def _copy(iterable, deepcopy_=deepcopy, imap_=map):
        return imap_(deepcopy_, iterable)

    @staticmethod
    def _permutations(n, permutations_=permutations):
        return lambda x: permutations_(x, n)

    @staticmethod
    def _repeat(n, usecall, call, r=repeat, tuple_=tuple, l=list, s=starmap):
        if usecall:
            return lambda x: s(call, r(l(x), n))
        return lambda x: r(tuple_(x), n)


class _MapMixin(local):

    '''mapping mixin'''

    @staticmethod
    def _argmap(call, curr, arg, kw, starmap_=starmap):
        if curr:
            def argmap(*args):
                return call(*(args + arg))
        else:
            argmap = call
        return lambda x: starmap_(argmap, x)

    @staticmethod
    def _invoke(name, args, mc_=methodcaller, imap_=map):
        caller = mc_(name, *args[0], **args[1])
        def invoke(thing): #@IgnorePep8
            read = caller(thing)
            return thing if read is None else read
        return lambda x: imap_(invoke, x)

    @staticmethod
    def _kwargmap(call, curr, arg, kw, starmap_=starmap):
        if curr:
            def kwargmap(*params):
                args, kwargs = params
                kwargs.update(kw)
                return call(*(args + arg), **kwargs)
        else:
            kwargmap = lambda x, y: call(*x, **y)
        return lambda x: starmap_(kwargmap, x)


class _FilterMixin(local):

    '''filtering mixin'''

    @staticmethod
    def _attributes(names, _attrgetter=attrgetter):
        attrfind = _attrgetter(*names)
        def attributes(iterable, get=attrfind): #@IgnorePep8
            AttrErr_ = AttributeError
            for thing in iterable:
                try:
                    yield get(thing)
                except AttrErr_:
                    pass
        return attributes

    @staticmethod
    def _duality(true, f=filter, ff=ifilterfalse, l=list, t=tee):
        def duality(iterable): #@IgnorePep8
            truth_, false_ = t(iterable)
            yield l(f(true, truth_)), l(ff(true, false_))
        return duality

    @staticmethod
    def _filter(true, false, ifilter_=filter, ifilterfalse_=ifilterfalse):
        if false:
            return lambda x: ifilterfalse_(true, x)
        return lambda x: ifilter_(true, x)

    @staticmethod
    def _mapping(call, key, value, k=keys, i=items, v=values, c=ichain):
        if key:
            return lambda x: map(call, c(map(k, x)))
        elif value:
            return lambda x: map(call, c(map(v, x)))
        return lambda x: starmap(call, c(map(i, x)))

    @staticmethod
    def _items(keys, _itemgetter=itemgetter):
        itemfind = _itemgetter(*keys)
        def items(iterable, get=itemfind): #@IgnorePep8
            IndexErr_, KeyErr_, TypeErr_ = IndexError, KeyError, TypeError
            for thing in iterable:
                try:
                    yield get(thing)
                except (IndexErr_, KeyErr_, TypeErr_):
                    pass
        return items

    @staticmethod
    def _traverse(test, invert):
        if invert:
            ifilter = ifilterfalse
        else:
            ifilter = filter
        def members(iterable, beenthere=None): #@IgnorePep8
            mro = getmro(iterable)
            names = dir(iterable)
            if beenthere is None:
                beenthere = set()
            adder = beenthere.add
            isclass_ = isclass
            getattr_ = getattr
            dict_ = OrderedDict
            members_ = members
            for name in names:
                # yes, it's really supposed to be a tuple
                for base in (iterable,) + mro:
                    var = vars(base)
                    if name in var:
                        obj = var[name]
                        break
                else:
                    obj = getattr_(iterable, name)
                if obj in beenthere:
                    continue
                else:
                    adder(obj)
                if isclass_(obj):
                    this = dict_()
                    for k, v in ifilter(test, members_(obj, beenthere)):
                        this[k] = v
                    yield name, this
                else:
                    yield name, obj
        def traverse(iterable): #@IgnorePep8
            isinstance_ = isinstance
            selfname_ = selfname
            members_ = members
            odict = OrderedDict
            cm = ChainMap
            for iterator in iterable:
                chaining = cm()
                chaining['classname'] = selfname_(iterator)
                cappend = chaining.maps.append
                for k, v in ifilter(test, members_(iterator)):
                    if isinstance_(v, odict):
                        v['classname'] = k
                        cappend(v)
                    else:
                        chaining[k] = v
                yield chaining
        return traverse


class _ReduceMixin(local):

    '''reduce mixin'''

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
    def _reduce(call, initial, reverse, reduce_=reduce):
        if reverse:
            if initial is None:
                return lambda i: reduce_(lambda x, y: call(y, x), i)
            return lambda i: reduce_(lambda x, y: call(y, x), i, initial)
        if initial is None:
            return lambda x: reduce_(call, x)
        return lambda x: reduce_(call, x, initial)

    @staticmethod
    def _weave(b, i=iter, n=next, s=islice, c=cycle, p=partial, t=tee, l=list):
        work, measure = t(b)
        nexts = c(p(n, i(item)) for item in work)
        pending = len(l(measure))
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
    def _at(n, default, islice_=islice, next_=next):
        return lambda x: next_(islice_(x, n, None), default)

    @staticmethod
    def _choice(iterable, choice_=choice, list_=list):
        yield choice_(list_(iterable))

    @staticmethod
    def _dice(n, fill, zip_longest_=zip_longest, iter_=iter):
        return lambda x: zip_longest_(fillvalue=fill, *[iter_(x)] * n)

    @staticmethod
    def _first(n=0, islice_=islice, next_=deferiter):
        return lambda x: islice_(x, n) if n else next_(x)

    @staticmethod
    def _initial(iterable, islice_=islice, len_=len, list_=list, t=tee):
        i1, i2 = t(iterable)
        return islice_(i1, len_(list_(i2)) - 1)

    @staticmethod
    def _last(n, s=islice, d=deque, ln=len, l=list, t=tee, f=deferfunc):
        if n:
            def last(iterable):
                i1, i2 = t(iterable)
                return s(i1, ln(l(i2)) - n, None)
            return last
        return lambda x: f(d(x, maxlen=1).pop)

    @staticmethod
    def _rest(iterable, _islice=islice):
        return _islice(iterable, 1, None)

    @staticmethod
    def _sample(n, sample_=sample, list_=list):
        def sample(iterable):
            yield sample_(list_(iterable), n)
        return sample

    @staticmethod
    def _slice(start, stop, step, _islice=islice):
        if stop and step:
            return lambda x: _islice(x, start, stop, step)
        elif stop:
            return lambda x: _islice(x, start, stop)
        return lambda x: _islice(x, start)
