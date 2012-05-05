# -*- coding: utf-8 -*-
'''specific knife mixins'''

from math import fsum
from copy import deepcopy
from threading import local
from inspect import isclass, getmro
from functools import reduce, partial
from random import shuffle, randrange
from collections import deque, namedtuple
from operator import methodcaller, itemgetter, attrgetter, truediv
from itertools import (
    groupby, islice, tee, starmap, repeat, combinations, permutations, chain)

from stuf.utils import selfname, deferiter, deferfunc
from stuf.six import (
    OrderedDict, strings, items, values, keys, filter, map)

from knife._compat import (
    Counter, ChainMap, filterfalse, zip_longest, count, memoize)

Count = namedtuple('Count', 'least most overall')
MinMax = namedtuple('MinMax', 'min max')
TrueFalse = namedtuple('TrueFalse', 'true false')
GroupBy = namedtuple('Group', 'keys groups')


def slice(x, y, nx=next, iz=islice):
    return nx(iz(x, y, None))


class _CmpMixin(local):

    '''comparing mixin'''

    @staticmethod
    @memoize
    def _all(call, a=all, m=map):
        # invoke worker on each item to yield truth
        return lambda x: a(m(call, x))

    @staticmethod
    @memoize
    def _any(call, a=any, m=map):
        # invoke worker on each item to yield truth
        return lambda x: a(m(call, x))

    @staticmethod
    @memoize
    def _difference(symmetric, rz=reduce, se=set, pt=partial):
        if symmetric:
            test = lambda x, y: se(x).symmetric_difference(y)
        else:
            test = lambda x, y: se(x).difference(y)
        return pt(rz, test)

    @staticmethod
    def _intersection(iterable, se=set, rz=reduce):
        return rz(lambda x, y: se(x).intersection(y), iterable)

    @staticmethod
    def _union(iterable, se=set, rz=reduce):
        return rz(lambda x, y: se(x).union(y), iterable)

    @staticmethod
    @memoize
    def _unique(call, se=set, nx=next, S=StopIteration):
        def unique(iterable):
            seen = se()
            seenadd = seen.add
            key = call
            try:
                while 1:
                    element = key(nx(iterable))
                    if element not in seen:
                        yield element
                        seenadd(element)
            except S:
                pass
        return unique


class _MathMixin(local):

    '''number mixin'''

    @staticmethod
    def _average(iterable, su=sum, td=truediv, cnt=count, t=tee):
        i1, i2 = t(iterable)
        yield td(su(i1, 0.0), cnt(i2))

    @staticmethod
    def _count(iterable, R=Counter, T=Count):
        cnt = R(iterable).most_common
        commonality = cnt()
        yield T(
            # least common
            commonality[:-2:-1][0][0],
            # most common (mode)
            cnt(1)[0][0],
            # overall commonality
            commonality,
        )

    @staticmethod
    @memoize
    def _max(call, mx=max):
        def imax(iterable):
            yield mx(iterable, key=call)
        return imax

    @staticmethod
    def _median(
        iterable, t=tee, sd=sorted, td=truediv, int=int, cnt=count, z=slice,
    ):
        i1, i2 = t(sd(iterable))
        result = td(cnt(i1) - 1, 2)
        pint = int(result)
        if result % 2 == 0:
            yield z(i2, pint)
        else:
            i3, i4 = t(i2)
            yield td(z(i3, pint) + z(i4, pint + 1), 2)

    @staticmethod
    def _minmax(iterable, mn=min, mx=max, t=tee, MM=MinMax):
        i1, i2 = t(iterable)
        yield MM(mn(i1), mx(i2))

    @staticmethod
    def _range(iterable, d=deque, sd=sorted, nx=next, t=tee):
        i1, i2 = t(sd(iterable))
        yield d(i1, maxlen=1).pop() - nx(i2)

    @staticmethod
    @memoize
    def _min(call, mn=min):
        def imin(iterable):
            yield mn(iterable, key=call)
        return imin

    @staticmethod
    @memoize
    def _sum(start, floats, su=sum, fs=fsum):
        def isum(iterable): #@IgnorePep8
            yield (fs if floats else lambda x: su(x, start))(iterable)
        return isum


class _OrderMixin(local):

    '''order mixin'''

    @staticmethod
    @memoize
    def _group(
        call, g=groupby, sd=sorted, G=GroupBy, u=tuple, nx=next,
        S=StopIteration,
    ):
        def grouper(iterable):
            try:
                it = g(sd(iterable, key=call), call)
                while 1:
                    k, v = nx(it)
                    yield G(k, u(v))
            except S:
                pass
        return grouper

    @staticmethod
    def _reverse(iterable, rv=reversed, u=tuple, nx=next, S=StopIteration):
        try:
            rev = rv(u(iterable))
            while 1:
                yield nx(rev)
        except S:
            pass

    @staticmethod
    def _shuffle(iterable, l=list, sf=shuffle):
        iterable = l(iterable)
        sf(iterable)
        yield iterable

    @staticmethod
    @memoize
    def _sort(call, sd=sorted):
        def isort(iterable):
            yield sd(iterable, key=call)
        return isort


class _RepeatMixin(local):

    '''repetition mixin'''

    @staticmethod
    def _combinations(n, cb=combinations):
        return lambda x: cb(x, n)

    @staticmethod
    def _copy(iterable, dc=deepcopy, m=map):
        return m(dc, iterable)

    @staticmethod
    def _permutations(n, pm=permutations):
        return lambda x: pm(x, n)

    @staticmethod
    @memoize
    def _repeat(n, use, call, rt=repeat, u=tuple, sm=starmap):
        if use:
            return lambda x: sm(call, rt(u(x), n))
        return lambda x: rt(u(x), n)


class _MapMixin(local):

    '''mapping mixin'''

    @staticmethod
    @memoize
    def _argmap(call, curr, arg, sm=starmap, pt=partial):
        if curr:
            def argmap(*args):
                return call(*(args + arg))
            return pt(sm, argmap)
        return pt(sm, call)

    @staticmethod
    @memoize
    def _invoke(name, args, mc=methodcaller, m=map, pt=partial):
        def invoke(thing, caller=mc(name, *args[0], **args[1])):
            read = caller(thing)
            return thing if read is None else read
        return pt(m, invoke)

    @staticmethod
    @memoize
    def _kwargmap(call, curr, arg, kw, sm=starmap, pt=partial):
        if curr:
            def kwargmap(*params):
                args, kwargs = params
                kwargs.update(kw)
                return call(*(args + arg), **kwargs)
        else:
            kwargmap = lambda x, y: call(*x, **y)
        return pt(sm, kwargmap)

    @staticmethod
    @memoize
    def _map(call, m=map, pt=partial):
        return pt(m, call)

    @staticmethod
    @memoize
    def _mapping(
        call, key, value, ky=keys, it=items, vl=values, sm=starmap, m=map,
        ci=chain.from_iterable,
    ):
        if key:
            return lambda x: m(call, ci(m(ky, x)))
        elif value:
            return lambda x: m(call, ci(m(vl, x)))
        return lambda x: sm(call, ci(m(it, x)))


class _FilterMixin(local):

    '''filtering mixin'''

    @staticmethod
    @memoize
    def _attributes(
        names, ag=attrgetter, nx=next, A=AttributeError, S=StopIteration,
    ):
        def attrs(iterable, get=ag(*names)):
            try:
                while 1:
                    try:
                        yield get(nx(iterable))
                    except A:
                        pass
            except S:
                pass
        return attrs

    @staticmethod
    @memoize
    def _duality(call, f=filter, ff=filterfalse, u=tuple, t=tee, TF=TrueFalse):
        def duality(iterable): #@IgnorePep8
            truth, false = t(iterable)
            yield TF(u(f(call, truth)), u(ff(call, false)))
        return duality

    @staticmethod
    @memoize
    def _filter(call, false, f=filter, ff=filterfalse, pt=partial):
        return pt(ff if false else f, call)

    @staticmethod
    @memoize
    def _items(
        key, ig=itemgetter, I=IndexError, K=KeyError, T=TypeError, nx=next,
        S=StopIteration,
    ):
        def itemz(iterable, get=ig(*key)):
            try:
                while 1:
                    try:
                        yield get(nx(iterable))
                    except (I, K, T):
                        pass
            except S:
                pass
        return itemz

    @staticmethod
    @memoize
    def _traverse(
        call, invert, O=OrderedDict, cn=chain, vz=vars, ff=filterfalse,
        f=filter, ic=isclass, ga=getattr, se=set, gm=getmro, d=dir, nx=next,
        CM=ChainMap, ii=isinstance, sn=selfname, S=StopIteration,
    ):
        ifilter = ff if invert else f
        def members(iterable, beenthere=None): #@IgnorePep8
            isclass_ = ic
            getattr_ = ga
            o_ = O
            members_ = members
            ifilter_ = ifilter
            varz_ = vz
            test_ = call
            mro = gm(iterable)
            names = d(iterable).__iter__()
            if beenthere is None:
                beenthere = se()
            adder_ = beenthere.add
            try:
                while 1:
                    name = nx(names)
                    # yes, it's really supposed to be a tuple
                    for base in cn([iterable], mro):
                        var = varz_(base)
                        if name in var:
                            obj = var[name]
                            break
                    else:
                        obj = getattr_(iterable, name)
                    if obj in beenthere:
                        continue
                    else:
                        adder_(obj)
                    if isclass_(obj):
                        yield name, o_((k, v) for k, v in ifilter_(
                            test_, members_(obj, beenthere),
                        ))
                    else:
                        yield name, obj
            except S:
                pass
        def traverse(iterable): #@IgnorePep8
            isinstance_ = ii
            selfname_ = sn
            members_ = members
            o_ = O
            cm_ = CM
            ifilter_ = ifilter
            test_ = call
            try:
                while 1:
                    iterator = nx(iterable)
                    chaining = cm_()
                    chaining['classname'] = selfname_(iterator)
                    cappend = chaining.maps.append
                    for k, v in ifilter_(test_, members_(iterator)):
                        if isinstance_(v, o_):
                            v['classname'] = k
                            cappend(v)
                        else:
                            chaining[k] = v
                    yield chaining
            except S:
                pass
        return traverse


class _ReduceMixin(local):

    '''reduce mixin'''

    @classmethod
    def _flatten(
        cls, iterable, st=strings, ii=isinstance, nx=next, S=StopIteration,
        A=AttributeError, T=TypeError,
    ):
        smash_ = cls._flatten
        next_ = iterable.__iter__()
        try:
            while 1:
                item = nx(next_)
                try:
                    # don't recur over strings
                    if ii(item, st):
                        yield item
                    else:
                        # do recur over other things
                        for j in smash_(item):
                            yield j
                except (A, T):
                    # does not recur
                    yield item
        except S:
            pass

    @staticmethod
    def _merge(iterable, ci=chain.from_iterable):
        return ci(iterable)

    @staticmethod
    @memoize
    def _reduce(call, initial, reverse, rz=reduce):
        if reverse:
            if initial is None:
                return lambda i: rz(lambda x, y: call(y, x), i)
            return lambda i: rz(lambda x, y: call(y, x), i, initial)
        if initial is None:
            return lambda x: rz(call, x)
        return lambda x: rz(call, x, initial)

    @staticmethod
    def _zip(iterable, zip_=zip_longest):
        return zip_(*iterable)


class _SliceMixin(local):

    '''slicing mixin'''

    @staticmethod
    @memoize
    def _at(n, default, iz=islice, nx=next):
        return lambda x: nx(iz(x, n, None), default)

    @staticmethod
    @memoize
    def _choice(t=tee, iz=islice, rr=randrange, cnt=count, nx=next):
        def choice(iterable):
            i1, i2 = t(iterable)
            yield nx(iz(i1, rr(0, cnt(i2)), None))
        return choice

    @staticmethod
    @memoize
    def _dice(n, fill, zl=zip_longest):
        return lambda x: zl(fillvalue=fill, *[x.__iter__()] * n)

    @staticmethod
    @memoize
    def _first(n=0, iz=islice, df=deferiter):
        return (lambda x: iz(x, n)) if n else (lambda x: df(x))

    @staticmethod
    def _initial(iterable, iz=islice, t=tee, cnt=count):
        i1, i2 = t(iterable)
        return iz(i1, cnt(i2) - 1)

    @staticmethod
    @memoize
    def _last(n, iz=islice, d=deque, t=tee, df=deferfunc, cnt=count):
        if n:
            def last(iterable):
                i1, i2 = t(iterable)
                return iz(i1, cnt(i2) - n, None)
            return last
        return lambda x: df(d(x, maxlen=1).pop)

    @staticmethod
    def _rest(iterable, iz=islice):
        return iz(iterable, 1, None)

    @staticmethod
    @memoize
    def _sample(n, t=tee, z=slice, rr=randrange, m=map, cnt=count):
        def sample(iterable):
            i1, i2 = t(iterable)
            length = cnt(i1)
            return m(lambda x: z(x, rr(0, length)), t(i2, n))
        return sample

    @staticmethod
    def _slice(start, stop, step, iz=islice):
        if stop and step:
            return lambda x: iz(x, start, stop, step)
        elif stop:
            return lambda x: iz(x, start, stop)
        return lambda x: iz(x, start)
