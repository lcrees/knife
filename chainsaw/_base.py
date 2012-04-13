# -*- coding: utf-8 -*-
'''base chainsaw mixins'''

from itertools import tee
from operator import truth
from threading import local
from collections import deque
from contextlib import contextmanager

from chainsaw._compat import imap

SLOTS = [
     '_IN', '_in', '_WORK', '_work', '_HOLD', '_hold', '_OUT', '_out',
     '_buildup',  '_mode', '_CHAINCFG',  '_chain', '_truth', '_ss',
     '_context', '_call', '_alt', '_wrapper', '_args', '_kw', '_original',
     '_baseline',
]


class _ChainsawMixin(local):

    '''base chainsaw mixin'''

    _REPR = '{0}.{1} ([IN: {2}({3}) => WORK: {4}({5}) => UTIL: {6}({7}) => ' \
        'OUT: {8}: ({9})]) <<mode: {10}/context: {11}>>'

    def __init__(self, ins, out, **kw):
        '''
        init

        @param ins: incoming things
        @param out: outgoing things
        '''
        super(_ChainsawMixin, self).__init__()
        # incoming things
        self._in = ins
        # outgoing things
        self._out = out
        # default context
        self._context = self._DEFAULT_CONTEXT
        # default mode
        self._mode = self._DEFAULT_MODE
        # no truth value to override default `__bool__` response
        self._truth = None
        ## chain defaults #####################################################
        self._chain = getattr(self, self._DEFAULT_CHAIN)
        # 1. default chain in
        self._IN = self._INVAR
        # 2. default work link
        self._WORK = self._WORKVAR
        # 3. default holding link
        self._HOLD = self._HOLDVAR
        # 4. default chainout
        self._OUT = self._OUTVAR
        # default chain configuration
        self._CHAINCFG = {}
        # clear things out of out link before adding other things to it?
        self._buildup = True
        ## snapshot defaults ##################################################
        # original and baseline snapshots
        self._original = self._baseline = None
        # maximum number of snapshots to keep (default: 5)
        maxlen = kw.pop('snapshots', 5)
        # snapshot stack
        self._ss = deque(maxlen=maxlen) if maxlen is not None else maxlen
        # take snapshot of original incoming things
        if self._ss is not None:
            self.snapshot(original=True)
        ## callable defaults ##################################################
        # active callable
        self._call = None
        # position arguments
        self._args = ()
        # keyword arguments
        self._kw = {}
        # current alternate callable
        self._alt = None
        # default output class
        self._wrapper = list

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    # chainsaw all incoming things as one thing
    _ONE = _DEFAULT_MODE = 'TREAT AS ONE'
    # chainsaw each incoming thing as one of many individual things
    _MANY = 'TREAT AS MANY'

    def _one(self, call, _imap=imap):
        # append incoming things to out if chainsawing them as one thing
        if self._mode == self._ONE:
            return self._append(call(self._iterable))
        # map incoming things and extend out if chainsawing many things
        elif self._mode == self._MANY:
            return self._xtend(imap(call, self._iterable))

    def _many(self, call, _imap=imap):
        # extend out with incoming things if chainsawing them as one thing
        if self._mode == self._ONE:
            return self._xtend(call(self._iterable))
        # map incoming things and extend out if chainsawing many things
        elif self._mode == self._MANY:
            return self._xtend(imap(call, self._iterable))

    def _iter(self, call, iter_=iter):
        '''extend work link with `things` wrapped in iterator'''
        # extend out with incoming things if chainsawing them as one thing
        if self._mode == self._ONE:
            return self._xtend(iter_(call(self._iterable)))
        # map incoming things and extend out if chainsawing many things
        elif self._mode == self._MANY:
            return self._xtend(imap(lambda x: iter_(call(x)), self._iterable))

    ###########################################################################
    ## things in context ######################################################
    ###########################################################################

    # modify incoming things from input to output in one series of operations
    _EDIT = _DEFAULT_CONTEXT = 'EDIT'
    # reset incoming things back to a baseline snapshot after each query
    _QUERY = 'QUERY'
    # reset incoming things back to a baseline snapshot after using results of
    # operations on incoming to determine which of two paths to follow
    _TRUTH = 'CONDITION'

    ###########################################################################
    ## things in chain ########################################################
    ###########################################################################

    # automatically balance ins with out
    _DEFAULT_CHAIN = _AUTO = '_auto'
    # manually balance ins with out
    _MANUAL = '_man4'
    # 1. link for incoming things which is chained to =>
    _INCFG = 'chainin'
    _INVAR = '_in'
    # 2. link for working on incoming things which is chained to =>
    _WORKCFG = 'work'
    _WORKVAR = '_work'
    # 3. link temporarily holding chainsawed things which is chained to =>
    _HOLDCFG = 'hold'
    _HOLDVAR = '_hold'
    # 4. link where outgoing things can be removed from chain
    _OUTCFG = 'chainout'
    _OUTVAR = '_out'

    def _as_chain(self, **kw):
        '''switch chains'''
        # retain chain-specific settings between chain switching
        self._CHAINCFG = kw if kw.get('hard', False) else {}
        # take snapshot
        if kw.get('snap', True):
            self.snapshot()
        # set current chain
        self._chain = kw.get('chain', getattr(self, self._DEFAULT_CHAIN))
        # if clear outgoing things before adding more things
        self._buildup = kw.get('keep', True)
        # 1. assign "ins" link
        self._IN = kw.get(self._INCFG, self._INVAR)
        # 2. assign "work" link
        self._WORK = kw.get(self._WORKCFG, self._WORKVAR)
        # 3. assign "holding" link
        self._HOLD = kw.get(self._HOLDCFG, self._HOLDVAR)
        # 4. assign "out" link
        self._OUT = kw.get(self._OUTCFG, self._OUTVAR)
        return self

    def _rechain(self):
        '''switch to currently selected chain'''
        return self._as_chain(keep=False, snap=False, **self._CHAINCFG)

    def _unchain(self):
        '''switch to default chain'''
        return self._as_chain(keep=False, snap=False)

    @contextmanager
    def _man1(self, **kw):
        '''switch to one-link chain'''
        q = kw.pop(self._WORKCFG, self._INVAR)
        self._as_chain(work=q, hold=q, chain=self._man1, **kw)
        yield
        self._rechain()

    @staticmethod
    def _clone(iterable, n=2, tee_=tee):
        '''
        clone an iterable

        @param n: number of clones
        '''
        return tee_(iterable, n)

    ###########################################################################
    ## things called ##########################################################
    ###########################################################################

    @property
    def _identity(self):
        '''
        Substitute generic identity function for active callable if no current
        callable is assigned.
        '''
        return self._call if self._call is not None else lambda x: x

    @property
    def _test(self):
        '''
        Substitute truth operator function for active callable is no current
        callable is assigned.
        '''
        return self._call if self._call is not None else truth

    ###########################################################################
    ## clearing things up #####################################################
    ###########################################################################

    def _clearsp(self):
        '''clear out snapshots'''
        self._ss.clear()
        return self
