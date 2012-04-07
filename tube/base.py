# -*- coding: utf-8 -*-
'''base mixins'''

from operator import truth
from threading import local
from collections import deque
from contextlib import contextmanager

SLOTS = [
    '_work', 'outflow', '_util', 'inflow', '_call', '_alt', '_wrapper', '_kw',
    '_args', '_buildup', '_flow', '_CTXCFG', '_IN', '_WORK', '_UTIL', '_OUT',
    '_iterator', 'channel', '_sps', '_original', '_condition', '_baseline',
]


class TubeMixin(local):

    '''tubing mixin'''

    def __init__(self, inflow, outflow, **kw):
        '''
        init

        @param inflow: inflow
        @param outflow: outflow
        '''
        super(TubeMixin, self).__init__()
        self.auto(kw.pop('manual', False))
        self.inflow = inflow
        self.outflow = outflow
        # preferred channel
        self.channel = self._CHANGE
        # condition
        self._condition = None
        #######################################################################
        ## flow defaults ######################################################
        #######################################################################
        # preferred flow
        self._flow = getattr(self, self._DEFAULT_CONTEXT)
        # default flow configuration
        self._CTXCFG = {}
        # 1. default inflow
        self._IN = self._INVAR
        # 2. default work things
        self._WORK = self._WORKVAR
        # 3. default utility things
        self._UTIL = self._UTILVAR
        # 4. default outflow
        self._OUT = self._OUTVAR
        # clear outflow before extending/appending to them?
        self._buildup = True
        #######################################################################
        ## savepoint defaults #################################################
        #######################################################################
        self._original = self._baseline = None
        # number of savepoints to retain (default: 5)
        maxlen = kw.pop('savepoints', 5)
        # create stack for savepoint things
        self._sps = deque(maxlen=maxlen) if maxlen is not None else None
        # savepoint of original inflow
        if self._sps is not None:
            self.rebase(True)
        #######################################################################
        ## callable defaults ##################################################
        #######################################################################
        # current callable (default: `None`)
        self._call = None
        # current alternate callable (default: `None`)
        self._alt = None
        # iterable outflow wrapper (default: `list`)
        self._wrapper = list
        # postition arguments (default: `tuple`)
        self._args = ()
        # keyword arguments (default: `dict`)
        self._kw = {}

    ###########################################################################
    ## channel things #########################################################
    ###########################################################################

    # change channel
    _CHANGE = 'CHANGE'
    # query channel
    _QUERY = 'QUERY'
    # condition channel
    _COND = 'CONDITION'

    def change(self):
        '''flow to change channeling'''
        self.channel = self._CHANGE
        return self.self.clear().undo(rebase=True).unflow()

    def condition(self):
        '''switch to condition channeling'''
        self.channel = self._COND
        return self.baseline().flow(hard=True, savepoint=False)

    def query(self):
        '''switch to query channeling'''
        self.channel = self._QUERY
        return self.baseline().flow()

    ###########################################################################
    ## flow things #EE######################################################
    ###########################################################################

    # 1. inflow
    _INCFG = 'inflow'
    _INVAR = 'inflow'
    # 2. utility things
    _UTILCFG = 'util'
    _UTILVAR = '_util'
    # 3. work things
    _WORKCFG = 'work'
    _WORKVAR = '_work'
    # 4. outflow
    _OUTCFG = 'outflow'
    _OUTVAR = 'outflow'

    def flow(self, **kw):
        '''flow flow'''
        # savepoint
        savepoint = kw.pop('savepoint', True)
        if savepoint:
            self._savepoint()
        # keep flow-specific settings between flow swaps
        self._CTXCFG = kw if kw.get('hard', False) else {}
        # set flow
        self._flow = kw.get('flow', getattr(self, self._DEFAULT_CONTEXT))
        # clear outflow before extending them?
        self._buildup = kw.get('clearout', True)
        # 1. inflow
        self._IN = kw.get(self._INCFG, self._INVAR)
        # 2. work things
        self._WORK = kw.get(self._WORKCFG, self._WORKVAR)
        # 3. utility things
        self._UTIL = kw.get(self._UTILCFG, self._UTILVAR)
        # 4. outflow
        self._OUT = kw.get(self._OUTCFG, self._OUTVAR)
        return self

    def reflow(self):
        '''flow to current flow'''
        return self.flow(keep=False, **self._CTXCFG)

    def unflow(self):
        '''flow to default flow'''
        return self.flow(keep=False)

    @contextmanager
    def flow1(self, **kw):
        '''flow to one-armed flow'''
        q = kw.pop(self._WORKCFG, self._INVAR)
        self.flow(work=q, util=q, flow=self.flow1, **kw)
        yield
        self.reflow()

    ###########################################################################
    ## savepoint for things ##################################################
    ###########################################################################

    def _savepoint(self):
        '''take savepoint of inflow'''
        self._sps.append(self._clone(getattr(self, self._IN)))
        return self

    def baseline(self, original):
        '''preserve a rebase for inflow'''
        self._savepoint()
        self._baseline = self._sps[-1]
        return self

    def rebase(self, original=False):
        '''preserve a rebase for inflow'''
        self._savepoint()
        self._baseline = self._sps.pop()
        if original:
            self._original = self._baseline
        return self

    def undo(self, index=0, original=False, baseline=False):
        '''
        revert to previous savepoint

        @param index: index of savepoint (default: 0)
        @param everything: undo everything and return things to original state
        '''
        if original:
            # clear everything plus savepoints
            self.clear()._clearsp()
            # restore original inflow
            self.inflow = self._original
            return self
        elif baseline:
            # clear everything plus savepoints
            self.clear()._clearsp()
            # restore original inflow
            self.inflow = self._baseline
            return self
        self.clear()
        # use most recent savepoint by default
        if not index:
            self.inflow = self._sps.pop()
        # if specified, use savepoint at specific index
        else:
            self.inflow = deque(reversed(self._sps))[index]
        return self._savepoint()

    ###########################################################################
    ## balance things #########################################################
    ###########################################################################

    # automatic balance
    _AUTO = 'autoflow'
    # manual balance
    _MANUAL = 'ctx4'

    @classmethod
    def auto(cls):
        '''automatically balance inflow with outflow'''
        cls._DEFAULT_CONTEXT = cls._AUTO
        return cls

    @classmethod
    def manual(cls, manual=False):
        '''manually balance inflow with outflow'''
        cls._DEFAULT_CONTEXT = cls._MANUAL
        return cls

    def balance(self):
        '''shift outflow to inflow'''
        with self.autoflow(
            inflow=self._OUTVAR, outflow=self._INVAR, keep=False
        ):
            return self._xtend(self._iterable)

    def balanceout(self):
        '''shift inflow to outflow'''
        with self.autoflow(keep=False):
            return self._xtend(self._iterable)

    @property
    def balanced(self):
        '''whether inflow and outflow are in balance'''
        return self.countout() == self.__len__()

    ###########################################################################
    ## extend inflow #################################################
    ###########################################################################

    def extend(self, things):
        '''
        extend after inflow

        @param thing: some things
        '''
        with self.flow1():
            return self._xtend(things)

    def prextend(self, things):
        '''
        extend before inflow

        @param thing: some things
        '''
        with self.flow1():
            return self._xtendleft(things)

    ###########################################################################
    ## append inflow #################################################
    ###########################################################################

    def append(self, thing):
        '''
        append after inflow

        @param thing: some thing
        '''
        with self.flow1():
            return self._append(thing)

    def prepend(self, thing):
        '''
        append before inflow

        @param thing: some thing
        '''
        with self.flow1():
            return self._appendleft(thing)

    ###########################################################################
    ## call things ############################################################
    ###########################################################################

    @property
    def _truth(self):
        return self._call if self._call is not None else truth

    @property
    def _identity(self):
        return self._call if self._call is not None else lambda x: x

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

    def when(self, call=None, alt=None):
        if self:
            self._call = call if call is not None else self._call
        else:
            self._call = alt if alt is not None else self._alt
        return self

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __bool__(self):
        return (
            self._condition if self._condition is not None else self.__len__()
        )

    @staticmethod
    def _repr(*args):
        '''tube representation'''
        return (
            '<{0}.{1} <<{2}>> ([IN: {3}({4}) => WORK: {5}({6}) => UTIL: {7}'
            '({8}) => OUT: {9}: ({10})])>'
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
        return self.untap().unwrap().clearout().clearin()._clearw()._clearu()
