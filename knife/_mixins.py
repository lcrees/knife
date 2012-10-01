# -*- coding: utf-8 -*-
'''specific knife mixins'''

from math import fsum
from copy import deepcopy
from threading import local
from functools import reduce
from inspect import getmro, isclass
from random import randrange, shuffle
from collections import deque, namedtuple
from operator import attrgetter, itemgetter, methodcaller, truediv
from itertools import (
    chain, combinations, groupby, islice, repeat, permutations, starmap, tee)

from stuf.utils import memoize
from stuf.deep import selfname, members
from stuf.six.moves import filterfalse, zip_longest  # @UnresolvedImport
from stuf.iterable import deferfunc, deferiter, count
from stuf.collects import OrderedDict, Counter, ChainMap
from stuf.six import filter, items, keys, map, isstring, values, next

Count = namedtuple('Count', 'least most overall')
GroupBy = namedtuple('Group', 'keys groups')
MinMax = namedtuple('MinMax', 'min max')
TrueFalse = namedtuple('TrueFalse', 'true false')
slicer = lambda x, y: next(islice(x, y, None))


class _CmpMixin(local):

    @memoize
    def _all(self):
        # invoke worker on each item to yield truth
        return self._append(all(map(self._test, self._iterable)))

    @memoize
    def _any(self):
        # invoke worker on each item to yield truth
        return self._append(any(map(self._test, self._iterable)))

    @memoize
    def _difference(self, symmetric):
        if symmetric:
            test = lambda x, y: set(x).symmetric_difference(y)
        else:
            test = lambda x, y: set(x).difference(y)
        return self._xtend(reduce(test, self._iterable))

    def _intersection(self):
        return self._xtend(
            reduce(lambda x, y: set(x).intersection(y), self._iterable)
        )

    def _union(self):
        return self._xtend(
            reduce(lambda x, y: set(x).union(y), self._iterable)
        )

    @memoize
    def _unique(self):
        def unique(key, iterable):
            seen = set()
            seenadd = seen.add
            try:
                while 1:
                    element = key(next(iterable))
                    if element not in seen:
                        yield element
                        seenadd(element)
            except StopIteration:
                pass
        return self._xtend(unique(self._identity, self._iterable))


class _MathMixin(local):

    def _average(self):
        i1, i2 = tee(self._iterable)
        return self._append(truediv(sum(i1, 0.0), count(i2)))

    def _count(self):
        cnt = Counter(self._iterable).most_common
        commonality = cnt()
        return self._append(Count(
            # least common
            commonality[:-2:-1][0][0],
            # most common (mode)
            cnt(1)[0][0],
            # overall commonality
            commonality,
        ))

    @memoize
    def _max(self):
        return self._append(max(self._iterable, key=self._identity))

    def _median(self):
        i1, i2 = tee(sorted(self._iterable))
        result = truediv(count(i1) - 1, 2)
        pint = int(result)
        if result % 2 == 0:
            return self._append(slicer(i2, pint))
        i3, i4 = tee(i2)
        return self._append(
            truediv(slicer(i3, pint) + slicer(i4, pint + 1), 2)
        )

    def _minmax(self):
        i1, i2 = tee(self._iterable)
        return self._append(MinMax(min(i1), max(i2)))

    def _range(self):
        i1, i2 = tee(sorted(self._iterable))
        return self._append(deque(i1, maxlen=1).pop() - next(i2))

    @memoize
    def _min(self):
        return self._append(min(self._iterable, key=self._identity))

    @memoize
    def _sum(self, start, floats):
        return self._append(
            fsum(self._iterable) if floats else sum(self._iterable, start)
        )


class _OrderMixin(local):

    @memoize
    def _group(self):
        def grouper(call, iterable):
            try:
                it = groupby(sorted(iterable, key=call), call)
                while 1:
                    k, v = next(it)
                    yield GroupBy(k, tuple(v))
            except StopIteration:
                pass
        return self._xtend(grouper(self._identity, self._iterable))

    def _reverse(self):
        return self._xtend(reversed(tuple(self._iterable)))

    def _shuffle(self):
        iterable = list(self._iterable)
        shuffle(iterable)
        return self._xtend(iterable)

    @memoize
    def _sort(self):
        return self._xtend(sorted(self._iterable, key=self._identity))


class _RepeatMixin(local):

    def _combinate(self, n):
        return self._xtend(combinations(self._iterable, n))

    def _copy(self):
        return self._xtend(map(deepcopy, self._iterable))

    def _permute(self, n):
        return self._xtend(permutations(self._iterable, n))

    @memoize
    def _repeat(self, n, use):
        call = self._identity
        if use:
            return self._xtend(starmap(call, repeat(tuple(self._iterable), n)))
        return self._xtend(repeat(tuple(self._iterable), n))


class _MapMixin(local):

    @memoize
    def _argmap(self, curr):
        call = self._identity
        if curr:
            def argmap(*args):
                return call(*(args + self._args))
            return self._xtend(starmap(argmap, self._iterable))
        return self._xtend(starmap(call, self._iterable))

    @memoize
    def _invoke(self, name):
        def invoke(thing, caller=methodcaller(name, *self._args, **self._kw)):
            read = caller(thing)
            return thing if read is None else read
        return self._xtend(map(invoke, self._iterable))

    @memoize
    def _kwargmap(self, curr):
        call = self._identity
        if curr:
            def kwargmap(*params):
                args, kwargs = params
                kwargs.update(self._kw)
                return call(*(args + self._args), **kwargs)
        else:
            kwargmap = lambda x, y: call(*x, **y)
        return self._xtend(starmap(kwargmap, self._iterable))

    @memoize
    def _map(self):
        return self._xtend(map(self._identity, self._iterable))

    @memoize
    def _mapping(self, key, value):
        if key:
            return self._xtend(map(
                self._identity, chain.from_iterable(map(keys, self._iterable))
            ))
        elif value:
            return self._xtend(map(self._identity, chain.from_iterable(
                map(values, self._iterable)
            )))
        call = (lambda x, y: (x, y)) if self._worker is None else self._worker
        return self._xtend(starmap(
            call, chain.from_iterable(map(items, self._iterable)))
        )


class _FilterMixin(local):

    @memoize
    def _attrs(self, names):
        def attrs(iterable, ):
            try:
                get = attrgetter(*names)
                nx = next
                while 1:
                    try:
                        yield get(nx(iterable))
                    except AttributeError:
                        pass
            except StopIteration:
                pass
        return self._xtend(attrs(self._iterable))

    @memoize
    def _duality(self):
        truth, false = tee(self._iterable)
        call = self._test
        return self._append(TrueFalse(
            tuple(filter(call, truth)), tuple(filterfalse(call, false))
        ))

    @memoize
    def _filter(self, false):
        return self._xtend(
            (filterfalse if false else filter)(self._worker, self._iterable)
        )

    @memoize
    def _items(self, keys):
        def itemz(iterable):
            try:
                get = itemgetter(*keys)
                nx = next
                while 1:
                    try:
                        yield get(nx(iterable))
                    except (IndexError, KeyError, TypeError):
                        pass
            except StopIteration:
                pass
        return self._xtend(itemz(self._iterable))

    @memoize
    def _traverse(self, invert):
        if self._worker is None:
            test = lambda x: not x[0].startswith('__')
        else:
            test = self._identity
        ifilter = filterfalse if invert else filter
        def members(iterable):  # @IgnorePep8
            mro = getmro(iterable)
            names = iter(dir(iterable))
            beenthere = set()
            adder = beenthere.add
            try:
                OD = OrderedDict
                vz = vars
                cn = chain
                ga = getattr
                ic = isclass
                nx = next
                while 1:
                    name = nx(names)
                    # yes, it's really supposed to be a tuple
                    for base in cn([iterable], mro):
                        var = vz(base)
                        if name in var:
                            obj = var[name]
                            break
                    else:
                        obj = ga(iterable, name)
                    if (name, obj) in beenthere:
                        continue
                    else:
                        adder((name, obj))
                    if ic(obj):
                        yield name, OD((k, v) for k, v in ifilter(
                            test, members(obj),
                        ))
                    else:
                        yield name, obj
            except StopIteration:
                pass
        def traverse(iterable):  # @IgnorePep8
            try:
                iterable = iter(iterable)
                OD = OrderedDict
                sn = selfname
                nx = next
                while 1:
                    iterator = nx(iterable)
                    chaining = ChainMap()
                    chaining['classname'] = sn(iterator)
                    cappend = chaining.maps.append
                    for k, v in ifilter(test, members(iterator)):
                        if isinstance(v, OD):
                            v['classname'] = k
                            cappend(v)
                        else:
                            chaining[k] = v
                    yield chaining
            except StopIteration:
                pass
        return self._xtend(traverse(self._iterable))

    def _mro(self):
        return self._xtend(chain.from_iterable(map(getmro, self._iterable)))

    def _members(self, invert):
        if self._worker is None:
            test = lambda x: not x[0].startswith('__')
        else:
            test = self._identity
        ifilter = filterfalse if invert else filter
        return self._xtend(ifilter(
            test, chain.from_iterable(map(members, self._iterable)),
        ))


class _ReduceMixin(local):

    def _flatten(self):
        def flatten(iterable):
            nx = next
            st = isstring
            next_ = iterable.__iter__()
            try:
                while 1:
                    item = nx(next_)
                    try:
                        # don't recur over strings
                        if st(item):
                            yield item
                        else:
                            # do recur over other things
                            for j in flatten(item):
                                yield j
                    except (AttributeError, TypeError):
                        # does not recur
                        yield item
            except StopIteration:
                pass
        return self._xtend(flatten(self._iterable))

    def _merge(self):
        return self._xtend(chain.from_iterable(self._iterable))

    @memoize
    def _reduce(self, initial, reverse):
        call = self._identity
        if reverse:
            if initial is None:
                return self._append(
                    reduce(lambda x, y: call(y, x), self._iterable)
                )
            return self._append(
                reduce(lambda x, y: call(y, x), self._iterable, initial)
            )
        if initial is None:
            return self._append(reduce(call, self._iterable))
        return self._append(reduce(call, self._iterable, initial))

    def _zip(self, zip_=zip_longest):
        return self._xtend(zip_(*self._iterable))


class _SliceMixin(local):

    @memoize
    def _at(self, n, default):
        return self._append(next(islice(self._iterable, n, None), default))

    @memoize
    def _choice(self):
        i1, i2 = tee(self._iterable)
        return self._append(islice(i1, randrange(0, count(i2)), None))

    @memoize
    def _dice(self, n, fill):
        return self._xtend(
            zip_longest(fillvalue=fill, *[self._iterable.__iter__()] * n)
        )

    @memoize
    def _first(self, n=0):
        return self._xtend(
            islice(self._iterable, n) if n else deferiter(self._iterable),
        )

    def _initial(self):
        i1, i2 = tee(self._iterable)
        return self._xtend(islice(i1, count(i2) - 1))

    @memoize
    def _last(self, n):
        if n:
            i1, i2 = tee(self._iterable)
            return self._xtend(islice(i1, count(i2) - n, None))
        return self._xtend(deferfunc(deque(self._iterable, maxlen=1).pop))

    def _rest(self, iz=islice):
        return self._xtend(iz(self._iterable, 1, None))

    @memoize
    def _sample(self, n):
        i1, i2 = tee(self._iterable)
        length = count(i1)
        return self._xtend(
            map(lambda x: slice(x, randrange(0, length)), tee(i2, n))
        )

    def _slice(self, start, stop, step):
        if stop and step:
            return self._xtend(islice(self._iterable, start, stop, step))
        elif stop:
            return self._xtend(islice(self._iterable, start, stop))
        return self._xtend(islice(self._iterable, start))
