# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

from threading import local
from collections import deque
from contextlib import contextmanager

from stuf.utils import OrderedDict
from stuf.core import stuf, frozenstuf, orderedstuf

SLOTS = [
    '_work', 'outgoing', '_util', 'incoming', '_call', '_alt', '_wrapper',
    '_args', '_kw', '_clearout', '_context', '_CONFIG', '_INQ', '_WORKQ',
    '_UTILQ', '_OUTQ', '_iterator', 'current_mode', '_savepoints', '_start',
]


class ThingsMixin(local):

    '''things management mixin'''

    def __init__(self, incoming, outgoing, **kw):
        '''
        init

        @param incoming: incoming things
        @param outgoing: outgoing things
        '''
        super(ThingsMixin, self).__init__()
        # incoming things
        self.incoming = incoming
        # outgoing things
        self.outgoing = outgoing
        # preferred mode
        self.current_mode = self._RW
        #######################################################################
        ## context defaults ###################################################
        #######################################################################
        # preferred context
        self._context = getattr(self, self._DEFAULT_CONTEXT)
        # default context settings
        self._CONFIG = {}
        # 1. default incoming things
        self._INQ = self._INVAR
        # 2. default work things
        self._WORKQ = self._WORKVAR
        # 3. default utility things
        self._UTILQ = self._UTILVAR
        # 4. default outgoing things
        self._OUTQ = self._OUTVAR
        # clear outgoing things before extending/appending to them?
        self._clearout = True
        #######################################################################
        ## snapshotting defaults ##############################################
        #######################################################################
        # number of savepoints to keep (default: 5)
        maxlen = kw.pop('savepoints', 5)
        # create stack for savepoint things
        self._savepoints = deque(maxlen=maxlen) if maxlen is not None else None
        # savepoint of original incoming things
        if self._savepoints is not None:
            self._original()
        #######################################################################
        ## callable defaults ##################################################
        #######################################################################
        # current callable (default: identity)
        self._call = lambda x: x
        # current alternate callable (default: identity)
        self._alt = lambda x: x
        # iterable export wrapper (default: `list`)
        self._wrapper = list
        # postition arguments (default: `tuple`)
        self._args = ()
        # keyword arguments (default: `dict`)
        self._kw = {}

    ###########################################################################
    ## mode things ############################################################
    ###########################################################################

    # read/write mode
    _RW = 'read/write'
    # read-only mode
    _RO = 'read-only'

    def rw(self):
        '''switch to read/write mode'''
        self.current_mode = self._RW
        return self._clearu().unswap()

    ###########################################################################
    ## context things #EE######################################################
    ###########################################################################

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

    def swap(self, **kw):
        '''swap context'''
        # savepoint
        savepoint = kw.pop('savepoint', True)
        if savepoint:
            self._savepoint()
        # keep context-specific settings between context swaps
        self._CONFIG = kw if kw.get('hard', False) else {}
        # set context
        self._context = kw.get('context', getattr(self, self._DEFAULT_CONTEXT))
        # clear out outgoing things before extending them?
        self._clearout = kw.get('clearout', True)
        # 1. incoming things
        self._INQ = kw.get(self._INCFG, self._INVAR)
        # 2. work things
        self._WORKQ = kw.get(self._WORKCFG, self._WORKVAR)
        # 3. utility things
        self._UTILQ = kw.get(self._UTILCFG, self._UTILVAR)
        # 4. outgoing things
        self._OUTQ = kw.get(self._OUTCFG, self._OUTVAR)
        return self

    def reswap(self):
        '''swap for preferred context'''
        return self.swap(savepoint=False, **self._CONFIG)

    def unswap(self):
        '''swap for current default context'''
        return self.swap(savepoint=False)

    @contextmanager
    def ctx1(self, **kw):
        '''swap for one-armed context'''
        q = kw.pop(self._WORKCFG, self._INVAR)
        self.swap(workq=q, utilq=q, context=self.ctx1, **kw)
        yield
        self.reswap()

    ###########################################################################
    ## savepoint for things ##################################################
    ###########################################################################

    def _original(self):
        '''preserve original incoming things'''
        self._savepoint()
        # preserve from savepoint stack
        self._start = self._savepoints.pop()
        return self

    def undo(self, index=0, everything=False):
        '''
        revert to previous savepoint

        @param index: index of savepoint (default: 0)
        @param everything: undo everything and return things to original state
        '''
        if everything:
            self.clear()._clearsp()
            self.incoming = self._start
            self._original()
            return self
        self.clear()
        if not index:
            self.incoming = self._savepoints.pop()
        else:
            self.incoming = deque(reversed(self._savepoints))[index]
        return self._savepoint()

    ###########################################################################
    ## rotate things ##########################################################
    ###########################################################################

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        with self.ctx2(savepoint=False):
            return self._append(list(self._iterable))

    def sync(self):
        '''shift outgoing things to incoming things'''
        with self.autoctx(inq=self._OUTVAR, outq=self._INVAR, savepoint=False):
            return self._xtend(self._iterable)

    def syncout(self):
        '''shift incoming things to outgoing things'''
        with self.autoctx(savepoint=False):
            return self._xtend(self._iterable)

    ###########################################################################
    ## extend incoming things #################################################
    ###########################################################################

    def extend(self, things):
        '''
        extend after incoming things

        @param thing: some things
        '''
        with self.ctx1():
            return self._xtend(things)

    def extendleft(self, things):
        '''
        extend before incoming things

        @param thing: some things
        '''
        with self.ctx1():
            return self._xtendleft(things)

    def outextend(self, things):
        '''
        extend right side of outgoing things

        @param thing: some things
        '''
        with self.ctx1(workq=self._OUTVAR):
            return self._xtend(things)

    ###########################################################################
    ## append incoming things #################################################
    ###########################################################################

    def append(self, thing):
        '''
        append after incoming things

        @param thing: some thing
        '''
        with self.ctx1():
            return self._append(thing)

    def prepend(self, thing):
        '''
        append before incoming things

        @param thing: some thing
        '''
        with self.ctx1():
            return self._appendleft(thing)

    ###########################################################################
    ## call things ############################################################
    ###########################################################################

    def args(self, *args, **kw):
        '''set arguments for current or alternative callable'''
        # set position arguments
        self._args = args
        # set keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call, alt=None, factory=False):
        '''
        set current callable

        @param call: a callable
        @param alt: an alternative callable (default: None)
        @param factor: call is a factory? (default: False)
        '''
        # reset postition arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # set factory for building current callable
        if factory:
            def factory(*args, **kw):
                return call(*args, **kw)
            self._call = factory
        else:
            # set current callable
            self._call = call
        # set alternative callable
        self._alt = alt if alt is not None else lambda x: x
        return self

    def untap(self):
        '''clear current callable'''
        # reset postition arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset current callable (default is identity)
        self._call = lambda x: x
        # reset alternative callable
        self._alt = lambda x: x
        return self

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    @staticmethod
    def _repr(*args):
        '''queue representation'''
        return (
            '<{0}.{1}<<{2}>>([IN: {3}({4}) => WORK: {5}({6}) => UTIL: {7}({8})'
            ' => OUT: {9}: ({10})]) at {11}>'
        ).format(*args)

    @property
    def balanced(self):
        '''queues are balanced?'''
        return self.countout() == self.__len__()

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearsp(self):
        '''clear savepoints'''
        self._savepoints.clear()
        return self

    def clear(self):
        '''clear anything'''
        return self.untap().unwrap().clearout().clearin()._clearw()._clearu()


class ResultsMixin(local):

    '''result of things mixin'''

    ###########################################################################
    ## outgoing things export #################################################
    ###########################################################################

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

    ###########################################################################
    ## wrap outgoing things ###################################################
    ###########################################################################

    def wrap(self, wrapper):
        '''
        wrapper for outgoing things

        @param wrapper: an iterator class
        '''
        self._wrapper = wrapper
        return self

    def tuple_wrap(self):
        '''set wrapper to `tuple`'''
        return self.wrap(tuple)

    def set_wrap(self):
        '''set wrapper to `set`'''
        return self.wrap(set)

    def deque_wrap(self):
        '''set wrapper to `deque`'''
        return self.wrap(deque)

    def dict_wrap(self):
        '''set wrapper to `dict`'''
        return self.wrap(dict)

    def frozenset_wrap(self):
        '''set wrapper to `frozenset`'''
        return self.wrap(frozenset)

    def frozenstuf_wrap(self):
        '''set wrapper to `frozenstuf`'''
        return self.wrap(frozenstuf)

    def ordereddict_wrap(self):
        '''set wrapper to `OrderedDict`'''
        return self.wrap(OrderedDict)

    def orderedstuf_wrap(self):
        '''set wrapper to `orderedstuf`'''
        return self.wrap(orderedstuf)

    def stuf_wrap(self):
        '''set wrapper to `stuf`'''
        return self.wrap(stuf)

    def list_wrap(self):
        '''clear current wrapper'''
        return self.wrap(list)

    unwrap = list_wrap
