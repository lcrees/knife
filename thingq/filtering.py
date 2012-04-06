# -*- coding: utf-8 -*-
'''thingq filtering mixins'''

import re
from inspect import getmro
from threading import local
from functools import reduce
from collections import deque
from json import dumps, loads
from itertools import tee, islice
from htmlentitydefs import name2codepoint
from xml.sax.saxutils import escape, unescape
from operator import attrgetter, itemgetter, truth

from thingq.support import (
    ifilter, ichain, imap, filterfalse, tounicode, tobytes)


class CollectMixin(local):

    '''collecting mixin'''

    def members(self):
        '''extract object members from incoming things'''
        call_, alt_, wrap_ = self._call, self._alt, self._wrapper
        def members(truth, iterable): #@IgnorePep8
            f, s, t, i = truth, alt_, wrap_, iterable
            d, w, g, e = dir, extract, getattr, AttributeError
            test = lambda x: x.startswith('__') or x.startswith('mro')
            for k in filterfalse(test, d(i)):
                try:
                    v = g(i, k)
                except e:
                    pass
                else:
                    if s(v):
                        yield k, t(w(f, v))
                    else:
                        yield k, v
        def extract(truth, iterable, ifilter_=ifilter, members_=members):
            for member in ifilter_(truth, members_(truth, iterable)):
                yield member
        with self._context():
            return self._xtend(ichain(imap(
                lambda x: extract(call_, x), self._iterable,
            )))

    def mro(self):
        '''extract ancestors of things by method resolution order'''
        with self._context():
            return self._xtend(ichain(getmro(i) for i in self._iterable))

    def pick(self, *names):
        '''collect object attributes from incoming things by their `*names`'''
        def pick(names, iterable):
            '''
            collect attributes of things in iterable
    
            @param names: sequence of names
            @param iterable: an iterable
            '''
            attrfind = attrgetter(*names)
            for thing in iterable:
                try:
                    yield attrfind(thing)
                except AttributeError:
                    pass
        with self._context():
            return self._xtend(pick(names, self._iterable))

    def pluck(self, *keys):
        '''collect object items from incoming things by item `*keys`'''
        def pluck(keys, iterable, _itemgetter=itemgetter):
            '''
            collect values of things in iterable
    
            @param keys: sequence of keys
            @param iterable: an iterable
            '''
            itemfind = _itemgetter(*keys)
            IndexErr_, KeyErr_, TypeErr_ = IndexError, KeyError, TypeError
            for thing in iterable:
                try:
                    yield itemfind(thing)
                except (IndexErr_, KeyErr_, TypeErr_):
                    pass
        with self._context():
            return self._xtend(pluck(keys, self._iterable))


class SetMixin(local):

    '''set and uniqueness mixin'''

    def difference(self):
        '''difference between incoming things'''
        with self._context():
            return self._xtend(reduce(
                lambda x, y: set(x).difference(y), self._iterable,
            ))

    def symmetric_difference(self):
        '''symmetric difference between incoming things'''
        with self._context():
            return self._xtend(reduce(
                lambda x, y: set(x).symmetric_difference(y), self._iterable,
            ))

    def disjointed(self):
        '''disjoint between incoming things'''
        with self._context():
            return self._append(reduce(
                lambda x, y: set(x).isdisjoint(y), self._iterable,
            ))

    def intersection(self):
        '''intersection between incoming things'''
        with self._context():
            return self._xtend(reduce(
                lambda x, y: set(x).intersection(y), self._iterable,
            ))

    def subset(self):
        '''incoming things that are subsets of incoming things'''
        with self._context():
            return self._append(reduce(
                lambda x, y: set(x).issubset(y), self._iterable,
            ))

    def superset(self):
        '''incoming things that are supersets of incoming things'''
        with self._context():
            return self._append(reduce(
                lambda x, y: set(x).issubset(y), self._iterable
            ))

    def union(self):
        '''union between incoming things'''
        with self._context():
            return self._xtend(
                reduce(lambda x, y: set(x).union(y), self._iterable)
            )

    def unique(self):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen
        '''
        def unique(iterable, key=None):
            seen = set()
            seen_add_, key_ = seen.add, key
            for element in iterable:
                k = key_(element)
                if k not in seen:
                    seen_add_(k)
                    yield element
        with self._context():
            return self._iter(unique(self._iterable, self._call))


class SliceMixin(local):

    '''slicing mixin'''

    def first(self):
        '''first incoming thing'''
        with self._context():
            return self._append(next(self._iterable))

    def last(self):
        '''last incoming thing'''
        with self._context():
            i1, _ = tee(self._iterable)
            return self._append(deque(i1, maxlen=1).pop())

    def nth(self, n, default=None):
        '''
        `nth` incoming thing or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._context():
            return self._append(
                next(islice(self._iterable, n, None), default)
            )

    def initial(self):
        '''all incoming things except the last thing'''
        with self._context():
            i1, i2 = tee(self._iterable)
            return self._xtend(islice(i1, len(list(i2)) - 1))

    def partition(self):
        '''
        split incoming things into `True` and `False` things based on results
        of call
        '''
        list_, call_ = list, self._call
        with self._context():
            falsy, truey = tee(self._iterable)
            return self._xtend(iter([
                list_(filterfalse(call_, falsy)), list_(ifilter(call_, truey)),
            ]))

    def rest(self):
        '''all incoming things except the first thing'''
        with self._context():
            return self._xtend(islice(self._iterable, 1, None))

    def snatch(self, n):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        with self._context():
            i1, i2 = tee(self._iterable)
            return self._xtend(islice(i1, len(list(i2)) - n, None))

    def take(self, n):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._context():
            return self._xtend(islice(self._iterable, n))


class FilterMixin(local):

    '''filters mixin'''

    def compact(self):
        '''strip "untrue" things from incoming things'''
        with self._context():
            return self._iter(ifilter(truth, self._iterable))

    def filter(self):
        '''incoming things for which call is `True`'''
        with self._context():
            return self._xtend(ifilter(self._call, self._iterable))

    def find(self):
        '''first incoming thing for which call is `True`'''
        with self._context():
            return self._append(
                next(ifilter(self._call, self._iterable))
            )

    def reject(self):
        '''incoming things for which call is `False`'''
        with self._context():
            return self._xtend(filterfalse(self._call, self._iterable))

    def without(self, *things):
        '''strip things from incoming things'''
        with self._context():
            return self._xtend(
                filterfalse(lambda y: y in things, self._iterable)
            )
    
    def ascii(self, errors='strict'):
        '''
        encode each incoming thing as ascii string (regardless of type)

        @param errors: error handling (default: 'strict')
        '''
        with self._context():
            return self._xtend(imap(
                lambda x: tobytes(x, 'ascii', errors), self._iterable,
            ))
    
    def bytes(self, encoding='utf-8', errors='strict'):
        '''
        encode each incoming thing as byte string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._context():
            return self._xtend(imap(
                lambda x: tobytes(x, encoding, errors), self._iterable,
            ))

    def unicode(self, encoding='utf-8', errors='strict'):
        '''
        decode each incoming thing as unicode string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        with self._context():
            return self._xtend(imap(
                lambda x: tounicode(x, encoding, errors), self._iterable,
            ))
    
    def match(self, pattern, flags=0):
        '''
        look for pattern among incoming strings
        
        @param pattern: search pattern 
        '''
        search = re.compile(pattern, flags)
        def find(x):
            return True if search.search(x) else False
        with self._context():
            return self._xtend(imap(find, self._iterable))
        
    def extract(self, pattern, flags=0):
        '''
        look for pattern among incoming strings
        
        @param pattern: search pattern 
        '''
        search = re.compile(pattern, flags)
        def find(x):
            results = search.search(x)
            if not results:
                return None, None
            # extract any named results
            named = results.groupdict()
            # extract any positional arguments
            positions = tuple(i for i in search.groups() if i not in named)
            return positions, named
        with self._context():
            return self._xtend(ifilter(
                lambda x, y: x is not None and y is not None,  
                imap(find, self._iterable),
            ))

    def sub(self, pattern, repl, flags=0, count=0):
        '''
        replace strings matching pattern with replacement
        
        @param pattern: search pattern 
        @param repl: replacement string
        '''
        search = re.compile(pattern, flags)
        def find(x):
            return search.sub(repl, x, count)
        with self._context():
            return self._xtend(imap(find, self._iterable))

    def htmlescape(self):
        '''escape HTML (&, <, >, ", and ')'''
        with self._context():
            return self._xtend(imap(
                lambda x: escape(x, {'"':"&quot;", "'":'&#39;'}),
                self._iterable,
            ))

    def htmlunescape(self):
        '''
        unescape HTML
        
        from -> John J. Lee 
        http://groups.google.com/group/comp.lang.python/msg/ce3fc3330cbbac0a
        '''
        def unescape_charref(ref): 
            name = ref[2:-1] 
            base = 10 
            if name.startswith("x"): 
                name = name[1:] 
                base = 16 
            return unichr(int(name, base)) 
        def replace_entities(match): 
            ent = match.group() 
            if ent[1] == "#": 
                return unescape_charref(ent) 
            repl = name2codepoint.get(ent[1:-1]) 
            if repl is not None: 
                repl = unichr(repl) 
            else: 
                repl = ent 
            return repl 
        def unescape(data): 
            return re.sub(r"&#?[A-Za-z0-9]+?;", replace_entities, data) 
        with self._context():
            return self._xtend(imap(unescape, self._iterable)) 

    def jsunescape(self):
        '''javascript/json unescape each incoming things'''
        with self._context():
            return self._xtend(imap(loads, self._iterable))

    def jsescape(self):
        '''javascript/json unescape each incoming things'''
        with self._context():
            return self._xtend(imap(dumps, self._iterable))

    def xmlunescape(self):
        '''xml unexcape each incoming things'''
        with self._context():
            return self._xtend(imap(unescape, self._iterable))

    def xmlescape(self):
        '''xml excape each incoming things'''
        with self._context():
            return self._xtend(imap(escape, self._iterable))
