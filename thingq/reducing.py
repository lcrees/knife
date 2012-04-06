# -*- coding: utf-8 -*-
'''thingq reducing mixins'''

from math import fsum
from threading import local
from functools import partial, reduce
from operator import contains, truediv
from itertools import cycle, tee, islice

from stuf.six import strings, u
from thingq.support import Counter, imap, zip, ichain, tounicode


class MathMixin(local):

    '''math mixin'''

    def average(self):
        '''average value of incoming things'''
        def average(iterable):
            i1, i2 = tee(iterable)
            return truediv(sum(i1, 0.0), len(list(i2)))
        with self._context():
            return self._append(average(self._iterable))

    def fsum(self):
        '''add incoming things together (if floats)'''
        with self._context():
            return self._append(fsum(self._iterable))

    def max(self):
        '''
        find maximum value among incoming things using current callable as key
        function
        '''
        with self._context():
            return self._append(max(self._iterable, key=self._call))

    def median(self):
        '''median value of incoming things'''
        def median(iterable):
            i = list(sorted(iterable))
            e = truediv(len(i) - 1, 2)
            p = int(e)
            return i[p] if e % 2 == 0 else truediv(i[p] + i[p + 1], 2)
        with self._context():
            return self._append(median(self._iterable))

    def min(self):
        '''
        find minimum value among incoming things using current callable as key
        function
        '''
        with self._context():
            return self._append(min(self._iterable, key=self._call))

    def minmax(self):
        '''minimum and maximum values among incoming things'''
        with self._context():
            i1, i2 = tee(self._iterable)
            return self._xtend(iter([min(i1), max(i2)]))

    def statrange(self):
        '''statistical range of incoming things'''
        with self._context():
            iterz = list(sorted(self._iterable))
            return self._append(iterz[-1] - iterz[0])

    def sum(self, start=0):
        '''
        total incoming things together

        @param start: starting number (default: 0)
        '''
        with self._context():
            return self._append(sum(self._iterable, start))


class TruthMixin(local):

    '''truth mixin'''

    def all(self):
        '''if `all` incoming things are `True`'''
        with self._context():
            return self._append(all(imap(self._call, self._iterable)))

    def any(self):
        '''if `any` incoming things are `True`'''
        with self._context():
            return self._append(any(imap(self._call, self._iterable)))

    def common(self):
        '''mode value of incoming things'''
        with self._context():
            return self._append(
                Counter(self._iterable).most_common(1)[0][0]
            )

    def contains(self, thing):
        '''
        if `thing` is found in incoming things

        @param thing: some thing
        '''
        with self._context():
            return self._append(contains(self._iterable, thing))

    def frequency(self):
        '''frequency of each incoming thing'''
        with self._context():
            return self._append(Counter(self._iterable).most_common())

    def quantify(self):
        '''
        how many times current callable returns `True` for incoming things
        '''
        with self._context():
            return self._append(sum(imap(self._call, self._iterable)))

    def uncommon(self):
        '''least common incoming thing'''
        with self._context():
            return self._append(
                Counter(self._iterable).most_common()[:-2:-1][0][0]
            )


class ReduceMixin(local):

    '''reduce mixin'''

    def concat(self):
        '''concatenate all incoming things together'''
        with self._context():
            return self._xtend(ichain(self._iterable))

    def flatten(self):
        '''flatten deeply nested incoming things'''
        def smash(iterable):
            smash_, strings_, isinst_ = smash, strings, isinstance
            for item in iterable:
                try:
                    # don't recur over strings
                    if isinst_(item, strings_):
                        yield item
                    else:
                        # do recur over other things
                        for j in smash_(item):
                            yield j
                except TypeError:
                    # does not recur
                    yield item
        with self._context():
            return self._xtend(smash(self._iterable))

    def join(self, sep=u(''), encoding='utf-8', errors='strict'):
        '''
        join incoming things into one unicode string (regardless of type)

        @param sep: join separator (default: '')
        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._context():
            return self._append(tounicode(sep.join(imap(
                tounicode, self._iterable,
            )), encoding, errors))

    def pairwise(self):
        '''every two incoming things as a `tuple`'''
        with self._context():
            i1, i2 = tee(self._iterable)
            next(i2, None)
            return self._xtend(zip(i1, i2))

    def reduce(self, initial=None):
        '''
        reduce incoming things to one thing using current callable (from left
        side of incoming things)

        @param initial: initial thing (default: None)
        '''
        with self._context():
            if initial is None:
                return self._append(reduce(self._call, self._iterable))
            return self._append(reduce(self._call, self._iterable, initial))

    def reduce_right(self, initial=None):
        '''
        reduce incoming things to one thing from right side of incoming things
        using current callable

        @param initial: initial thing (default: None)
        '''
        call = self._call
        with self._context():
            if initial is None:
                return self._append(reduce(
                    lambda x, y: call(y, x), self._iterable,
                ))
            return self._append(reduce(
                 lambda x, y: call(y, x), self._iterable, initial,
            ))

    def roundrobin(self):
        '''interleave incoming things into one thing'''
        def roundrobin(iterable):
            islice_, next_, cycle_ = islice, next, cycle
            nexts_ = cycle_(partial(next_, iter(i)) for i in iterable)
            pending = len(tee(iterable, 1))
            while pending:
                try:
                    for nextz in nexts_:
                        yield nextz()
                except StopIteration:
                    pending -= 1
                    nexts_ = cycle_(islice_(nexts_, pending))
        with self._context():
            return self._xtend(roundrobin(self._iterable))

    def zip(self):
        '''
        smash incoming things into one single thing, pairing things by iterable
        position
        '''
        with self._context():
            return self._xtend(zip(*self._iterable))
