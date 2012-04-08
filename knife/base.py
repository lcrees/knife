# -*- coding: utf-8 -*-
'''base knife mixins'''

from operator import truth
from threading import local
from collections import deque
from contextlib import contextmanager

from knife.compat import imap

SLOTS = [
    '_work', 'outgoing', '_util', 'incoming', '_call', '_alt', '_wrapper',
    '_args', '_buildup', '_flow', '_FLOWCFG', '_IN', '_WORK', '_HOLD', '_OUT',
    '_iterator', '_channel', '_sps', '_original', '_eval', '_baseline', '_kw',
    '_mode',
]


class KnifeMixin(local):

    '''knives mixin'''

    def __init__(self, incoming, outflow, **kw):
        '''
        init

        @param incoming: incoming
        @param outgoing: outgoing
        '''
        super(KnifeMixin, self).__init__()
        self.incoming = incoming
        self.outgoing = outflow
        # preferred channel
        self._channel = self._CHANGE
        # mode
        self._mode = self._SINGLE
        # condition
        self._eval = None
        ## flow defaults ######################################################
        # preferred flow
        self._flow = getattr(self, self._DEFAULT_CONTEXT)
        # default flow configuration
        self._FLOWCFG = {}
        # 1. default incoming pool
        self._IN = self._INVAR
        # 2. default work pool
        self._WORK = self._WORKVAR
        # 3. default holding pool
        self._HOLD = self._HOLDVAR
        # 4. default outgoing pool
        self._OUT = self._OUTVAR
        # clear outgoing pool before adding things to it?
        self._buildup = True
        ## snapshot defaults ##################################################
        self._original = self._baseline = None
        # maximum number of savepoints to keep at any one time (default: 5)
        maxlen = kw.pop('savepoints', 5)
        # create pool for snapshots
        self._sps = deque(maxlen=maxlen) if maxlen is not None else maxlen
        # take snapshot of original incoming
        if self._sps is not None:
            self.snapshot(original=True)
        ## callable defaults ##################################################
        # current callable
        self._call = None
        # current alternate callable
        self._alt = None
        # iterable outgoing wrapper
        self._wrapper = list
        # postition arguments
        self._args = ()
        # keyword arguments
        self._kw = {}

    ###########################################################################
    ## mode things ############################################################
    ###########################################################################

    _SINGLE = _DEFAULT_MODE = 'single'
    _MULTIPLE = 'multiple'

    def _single(self, call, _imap=imap):
        if self._mode == self._SINGLE:
            return self._append(call(self._iterable))
        elif self._mode == self._MULTIPLE:
            return self._xtend(imap(call, self._iterable))

    def _multi(self, call, _imap=imap):
        if self._mode == self._SINGLE:
            return self._xtend(call(self._iterable))
        elif self._mode == self._MULTIPLE:
            return self._xtend(imap(call, self._iterable))

    def single(self):
        self._mode = self._SINGLE
        return self

    def multiple(self):
        self._mode = self._MULTIPLE
        return self

    ###########################################################################
    ## channel things #########################################################
    ###########################################################################

    # change _channel
    _CHANGE = 'CHANGE'
    # query _channel
    _QUERY = 'QUERY'
    # condition _channel
    _COND = 'CONDITION'

    def change(self):
        '''switch to change channeling'''
        self._channel = self._CHANGE
        return self.clear().undo().unflow()

    def condition(self):
        '''switch to condition channeling'''
        self._channel = self._COND
        return self.baseline().flow(hard=True, savepoint=False)

    def query(self):
        '''switch to query channeling'''
        self._channel = self._QUERY
        return self.baseline().flow()

    ###########################################################################
    ## flow things ############################################################
    ###########################################################################

    # 1. incoming
    _INCFG = 'incoming'
    _INVAR = 'incoming'
    # 2. work things
    _WORKCFG = 'work'
    _WORKVAR = '_work'
    # 3. holding things
    _HOLDCFG = 'util'
    _HOLDVAR = '_util'
    # 4. outgoing
    _OUTCFG = 'outgoing'
    _OUTVAR = 'outgoing'

    def flow(self, **kw):
        '''switch flow'''
        # make snapshot
        if kw.pop('snapshot', True):
            self.snapshot()
        # keep flow-specific settings between flow swaps
        self._FLOWCFG = kw if kw.get('hard', False) else {}
        # set flow
        self._flow = kw.get('flow', getattr(self, self._DEFAULT_CONTEXT))
        # clear outgoing before extending them?
        self._buildup = kw.get('clearout', True)
        # 1. incoming
        self._IN = kw.get(self._INCFG, self._INVAR)
        # 2. work things
        self._WORK = kw.get(self._WORKCFG, self._WORKVAR)
        # 3. holding things
        self._HOLD = kw.get(self._HOLDCFG, self._HOLDVAR)
        # 4. outgoing
        self._OUT = kw.get(self._OUTCFG, self._OUTVAR)
        return self

    def _reflow(self):
        '''switch back to current flow'''
        return self.flow(keep=False, **self._FLOWCFG)

    def unflow(self):
        '''switch back to default flow'''
        return self.flow(keep=False)

    @contextmanager
    def _flow1(self, **kw):
        '''switch to one-step flow'''
        q = kw.pop(self._WORKCFG, self._INVAR)
        self.flow(work=q, util=q, flow=self._flow1, **kw)
        yield
        self._reflow()

    ###########################################################################
    ## balance things #########################################################
    ###########################################################################

    # automatically balance incoming with outgoing
    _DEFAULT_CONTEXT = _AUTO = '_autoflow'
    # manually balance incoming with outgoing
    _MANUAL = '_flow4'

    @classmethod
    def auto(cls):
        '''automatically balance incoming with outgoing'''
        cls._DEFAULT_CONTEXT = cls._AUTO
        return cls

    @classmethod
    def manual(cls):
        '''manually balance incoming with outgoing'''
        cls._DEFAULT_CONTEXT = cls._MANUAL
        return cls

    def balance(self, reverse=True):
        '''balance by shifting outgoing to incoming'''
        if reverse:
            # balance by shifting incoming to outgoing
            with self._autoflow(snapshot=False, keep=False):
                return self._multi(self._iterable)
        with self._autoflow(
            incoming=self._OUTVAR, outflow=self._INVAR, keep=False,
            snapshot=False,
        ):
            return self._multi(self._iterable)

    @property
    def balanced(self):
        '''if incoming and outgoing are in balance'''
        return self.countout() == self.__len__()

    ###########################################################################
    ## snapshot things ###################################################
    ###########################################################################

    def snapshot(self, baseline=False, original=False):
        '''
        Take snapshot of current incoming state.

        @param baseline: make this snapshot baseline version (default: False)
        @param original: make this snapshot original version (default: False)
        '''
        snapshot = self._clone(getattr(self, self._IN))[0]
        # make snapshot baseline snapshot
        if self._channel == self._CHANGE or baseline:
            self._baseline = snapshot
        # make snapshot original snapshot
        if original:
            self._original = snapshot
        # put snapshot at beginning of snapshot queue
        self._sps.appendleft(snapshot)
        return self

    def undo(self, snapshot=0, baseline=False, original=False):
        '''
        Revert incoming to previous incoming state.

        @param snapshot: snapshot to revert to e.g. 1, 2, 3, etc.
        @param baseline: return incoming to baseline version (default: False)
        @param original: return incoming to original version (default: False)
        '''
        # clear everything
        self.clear()
        if original:
            # clear savepoints
            self._clearsp()
            # clear baseline
            self._baseline = None
            # restore original incoming
            self.incoming = self._clone(self._original)[0]
        elif baseline:
            # clear savepoints
            self._clearsp()
            # restore baseline incoming
            self.incoming = self._clone(self._baseline)[0]
        # if specified, use specific snapshot
        elif snapshot:
            self._sps.rotate(snapshot)
            self.incoming = self._sps.popleft()
        # use most recent snapshot
        else:
            self.incoming = self._sps.popleft()
        return self

    ###########################################################################
    ## call things ############################################################
    ###########################################################################

    @property
    def _identity(self):
        '''substitute identity function if no current callable is set'''
        return self._call if self._call is not None else lambda x: x

    @property
    def _truth(self):
        '''substitute truth operator if no current callable is set'''
        return self._call if self._call is not None else truth

    def arguments(self, *args, **kw):
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
        self._alt = alt
        return self

    def untap(self):
        '''clear current callable'''
        # reset position arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset current callable
        self._call = None
        # reset alternative callable
        self._alt = None
        return self

    ###########################################################################
    ## incoming things ########################################################
    ###########################################################################

    def extend(self, things):
        '''
        put many things after the current incoming

        @param thing: some things
        '''
        with self._flow1():
            return self._multi(things)

    def extendleft(self, things):
        '''
        extend before incoming

        @param thing: some things
        '''
        with self._flow1():
            return self._xtendleft(things)

    def append(self, thing):
        '''
        append after current incoming

        @param thing: one thing
        '''
        with self._flow1():
            return self._single(thing)

    def appendleft(self, thing):
        '''
        append before current incoming

        @param thing: some thing
        '''
        with self._flow1():
            return self._appendleft(thing)

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __bool__(self):
        return (self._eval if self._eval is not None else self.__len__())

    @staticmethod
    def _repr(*args):
        '''knife representation'''
        return (
            '{0}.{1} ([IN: {2}({3}) => WORK: {4}({5}) => UTIL: {6}({7}) => '
            'OUT: {8}: ({9})]) <<{10}>>'
        ).format(*args)

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearsp(self):
        '''clear out savepoints'''
        self._sps.clear()
        return self

    def clear(self):
        '''clear out everything'''
        return self.untap().unwrap().clearout().clearin()._clearw()._clearh()
