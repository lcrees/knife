# -*- coding: utf-8 -*-
'''base chainsaw mixins'''

from itertools import tee
from threading import local
from collections import deque
from contextlib import contextmanager

from chainsaw._compat import imap

SLOTS = [
     '_IN', '_in', '_WORK', '_work', '_HOLD', '_hold', '_OUT', '_ss',
     '_out', '_buildup',  '_mode', '_CHAINCFG',  '_chain', '_truth',
     '_context', '_call', '_alt', '_wrapper', '_args', '_kw', '_original',
     '_baseline',
]


class ChainsawMixin(local):

    '''base chainsaw mixin'''

    def __init__(self, ins, out, **kw):
        '''
        init

        @param ins: incoming things
        @param out: outgoing things
        '''
        super(ChainsawMixin, self).__init__()
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
        # current callable
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
    ## things in chain ########################################################
    ###########################################################################

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
        return self._as_chain(
            keep=False, snap=False, **self._CHAINCFG
        )

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
    ## clearing things up #####################################################
    ###########################################################################

    def _clearsp(self):
        '''clear out snapshots'''
        self._ss.clear()
        return self
