# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

from threading import local
from collections import deque
from itertools import tee, repeat
from contextlib import contextmanager

from stuf.utils import OrderedDict
from stuf.core import stuf, frozenstuf, orderedstuf

from twoq.support import n2u, n2b

SLOTS = [
    '_work', 'outgoing', '_util', 'incoming', '_call', '_alt', '_wrapper',
    '_args', '_kw', '_clearout', '_context', '_CONFIG', '_INQ', '_WORKQ',
    '_UTILQ', '_OUTQ', '_iterator', 'current_mode', '_snapshots',
]


class ThingsMixin(local):

    '''things management mixin'''

    # 1. incoming things
    _INCFG = 'inq'
    _INVAR = 'incoming'
    # 2. utility things
    _UTILCFG = 'utilq'
    _UTILVAR = '_util'
    # 3. work things
    _WORKCFG = 'workq'
    _WORKVAR = '_work'
    # 4. outgoing things
    _OUTCFG = 'outq'
    _OUTVAR = 'outgoing'
    # read/write mode marker
    _RW = 'read/write'
    # read-only mode marker
    _RO = 'read-only'

    def __init__(self, incoming, outgoing, **kw):
        '''
        init

        @param incoming: incoming things
        @param outgoing: outgoing things
        '''
        super(ThingsMixin, self).__init__()
        # snapshots
        self._snapshots = deque(maxlen=kw.pop('snapshots', 5))
        # incoming things
        self.incoming = incoming
        # outgoing things
        self.outgoing = outgoing
        # current callable
        self._call = lambda x: x
        # current alt callable
        self._alt = lambda x: x
        # clear wrapper
        self._wrapper = list
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # mode
        self.current_mode = self._RW
        # set defaults
        self.unswap()

    @property
    def balanced(self):
        '''if queues are balanced'''
        return self.outcount() == self.__len__()

    @staticmethod
    def _repr(*args):
        return (
            '<{0}.{1}<<{2}>>([IN: {3}({4}) => WORK: {5}({6}) => UTIL: {7}({8})'
            ' => OUT: {9}: ({10})]) at {11}>'
        ).format(*args)

    def clear(self):
        '''clear every thing'''
        self.detap().unwrap().dealt()
        return self.outclear().inclear()._wclear()._uclear()

    ###########################################################################
    ## context rotation #######################################################
    ###########################################################################

    @contextmanager
    def ctx1(self, **kw):
        '''swap to one-armed context'''
        self.snapshot()
        q = kw.pop(self._WORKCFG, self._INVAR)
        self.swap(workq=q, utilq=q, context=self.ctx1, **kw)
        yield
        # return to global context
        self.reswap()

    def swap(self, hard=False, **kw):
        '''swap contexts'''
        self._context = kw.get('context', getattr(self, self._default_context))
        # clear out outgoing things before extending them?
        self._clearout = kw.get('clearout', True)
        # keep context-specific settings between context swaps
        self._CONFIG = kw if kw.get('hard', False) else {}
        # 1. incoming things
        self._INQ = kw.get(self._INCFG, self._INVAR)
        # 2. work things
        self._WORKQ = kw.get(self._WORKCFG, self._WORKVAR)
        # 3. utility things
        self._UTILQ = kw.get(self._UTILCFG, self._UTILVAR)
        # 4. outgoing things
        self._OUTQ = kw.get(self._OUTCFG, self._OUTVAR)
        return self

    def unswap(self):
        '''swap context to default context'''
        return self.swap()

    def reswap(self):
        '''swap contexts to current preferred context'''
        return self.swap(**self._CONFIG)

    ###########################################################################
    ## mode ###################################################################
    ###########################################################################

    def rw(self):
        '''switch to read/write mode'''
        self.current_mode = self._RW
        return self._uclear().unswap()

    ###########################################################################
    ## snapshots ##############################################################
    ###########################################################################

    def undo(self):
        '''revert to last snapshot'''
        self.clear()
        self.incoming = self._snapshots.pop()
        self.snapshot()
        return self

    def revert(self, snapshot=0):
        '''revert to specific snapshot'''
        self.clear()
        self.incoming = self._snapshots[snapshot]
        self.snapshot()
        return self

    ###########################################################################
    ## current callable management ############################################
    ###########################################################################

    def args(self, *args, **kw):
        '''arguments for current callable'''
        # set positional arguments
        self._args = args
        # set keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call):
        '''
        set current callable

        @param call: a callabler
        '''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # set current callable
        self._call = call
        return self

    def alt(self, call):
        '''
        set alternative current callable

        @param call: an alternative callable
        '''
        self._alt = call
        return self

    def detap(self):
        '''clear current callable'''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset current callable (default is identity)
        self._call = lambda x: x
        return self

    def dealt(self):
        '''clear current alternative callable'''
        self._alt = lambda x: x
        return self

    def factory(self, call):
        '''
        build current callable from factory

        @param call: a callable
        '''
        def wrap(*args, **kw):
            return call(*args, **kw)
        return self.tap(wrap)

    defactory = detap

    ###########################################################################
    ## things rotation ########################################################
    ###########################################################################

    def outshift(self):
        '''shift incoming things to outgoing things'''
        with self.autoctx():
            return self._xtend(self._iterable)

    outsync = outshift

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        with self.ctx2():
            return self._append(list(self._iterable))

    def shift(self):
        '''shift outgoing things to incoming things'''
        with self.autoctx(inq=self._OUTVAR, outq=self._INVAR):
            return self._xtend(self._iterable)

    sync = shift

    ###########################################################################
    ## things appending #######################################################
    ###########################################################################

    def append(self, thing):
        '''
        append thing to right side of incoming things

        @param thing: some thing
        '''
        with self.ctx1():
            return self._append(thing)

    def prepend(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        with self.ctx1():
            return self._appendleft(thing)

    appendleft = prepend

    ###########################################################################
    ## things extension #######################################################
    ###########################################################################

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        with self.ctx1():
            return self._xtend(things)

    def prextend(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        with self.ctx1():
            return self._xtendleft(things)

    extendleft = prextend

    def outextend(self, things):
        '''
        extend right side of outgoing things with `things`

        @param thing: some things
        '''
        with self.ctx1(workq=self._OUTVAR):
            return self._xtend(things)

    ###########################################################################
    ## iteration runners ######################################################
    ###########################################################################

    @classmethod
    def breakcount(cls, call, length, exception=StopIteration):
        '''
        rotate through iterator until it reaches its original length

        @param iterable: an iterable to exhaust
        '''
        for i in repeat(None, length):  # @UnusedVariable
            try:
                yield call()
            except exception:
                pass

    @staticmethod
    def iterexcept(call, exception):
        '''
        call a function repeatedly until an exception is raised

        Converts a call-until-exception interface to an iterator interface.
        Like `iter(call, sentinel)` but uses an exception instead of a sentinel
        to end the loop.

        Raymond Hettinger, Python Cookbook recipe # 577155
        '''
        try:
            while 1:
                yield call()
        except exception:
            pass


class ResultMixin(local):

    '''result things mixin'''

    def wrap(self, wrapper):
        '''
        wrapper for outgoing things

        @param wrapper: an iterator
        '''
        self._wrapper = wrapper
        return self

    def unwrap(self):
        '''clear current wrapper'''
        return self.list()

    def dict(self):
        '''set wrapper to `d    ict`'''
        self._wrap = dict
        return self

    def ordered_dict(self):
        '''set wrapper to `OrderedDict`'''
        self._wrap = OrderedDict

    def list(self):
        '''set wrapper to `list`'''
        self._wrap = list
        return self

    def unicode(self, encoding='utf-8'):
        '''set wrapper to `unicode` with given `encoding`'''
        self._wrap = lambda x: n2u(x, encoding)
        return self

    def bytes(self, encoding='ISO-8859-1'):
        '''set wrapper to `bytes` with given `encoding`'''
        self._wrap = lambda x: n2b(x, encoding)
        return self

    def tuple(self):
        '''set wrapper to `tuple`'''
        self._wrap = tuple
        return self

    def set(self):
        '''set wrapper to `set`'''
        self._wrap = set
        return self

    def frozenset(self):
        '''set wrapper to `frozenset`'''
        self._wrap = frozenset
        return self

    def deque(self):
        '''set wrapper to `deque`'''
        self._wrap = deque
        return self

    def stuf(self):
        '''set wrapper to `stuf`'''
        self._wrap = stuf
        return self

    def frozenstuf(self):
        '''set wrapper to `frozenstuf`'''
        self._wrap = frozenstuf
        return self

    def orderedstuf(self):
        '''set wrapper to `orderedstuf`'''
        self._wrap = orderedstuf
        return self

    def first(self):
        '''first incoming thing'''
        with self._context():
            return self._append(next(self._iterable))

    def last(self):
        '''last incoming thing'''
        with self._context():
            i1, _ = tee(self._iterable)
            return self._append(deque(i1, maxlen=1).pop())

    def peek(self):
        '''results from read-only context'''
        self.ro()
        out = self._wrapper(self._util)
        results = out[0] if len(out) == 1 else out
        self.rw()
        return results

    def results(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self.__iter__()
