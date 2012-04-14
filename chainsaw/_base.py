# -*- coding: utf-8 -*-
'''base chainsaw mixins'''

from operator import truth
from threading import local
from collections import deque
from fnmatch import translate
from re import compile as rcompile
from contextlib import contextmanager

from parse import compile as pcompile

from chainsaw._compat import imap

SLOTS = [
     '_IN', '_in', '_WORK', '_work', '_HOLD', '_hold', '_OUT', '_out',
     '_nokeep',  '_mode', '_CHAINCFG',  '_chain', '_ss', '_context', '_call',
     '_wrapper', '_args', '_kw', '_original', '_baseline',
]


class _ChainsawMixin(local):

    '''base chainsaw mixin'''

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
        self._nokeep = True
        ## snapshot defaults ##################################################
        # original and baseline snapshots
        self._original = self._baseline = None
        # maximum number of snapshots to keep (default: 5)
        maxlen = kw.pop('snapshots', 5)
        # snapshot stack
        self._ss = deque(maxlen=maxlen) if maxlen is not None else maxlen
        ## callable defaults ##################################################
        # worker
        self._call = None
        # position arguments
        self._args = ()
        # keyword arguments
        self._kw = {}
        # default output class
        self._wrapper = list

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    def _iter(self, call, iter_=iter):
        '''extend work link with `things` wrapped in iterator'''
        # extend out with incoming things if chainsawing them as one thing
        if self._mode == self._ONE:
            return self._xtend(iter_(call(self._iterable)))
        # map incoming things and extend out if chainsawing many things
        elif self._mode == self._MANY:
            return self._xtend(imap(lambda x: iter_(call(x)), self._iterable))

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

    def _as_chain(self, **kw):
        '''switch chains'''
        # retain chain-specific settings between chain switching
        self._CHAINCFG = kw if kw.get('hard', False) else {}
        # set current chain
        self._chain = kw.get('chain', getattr(self, self._DEFAULT_CHAIN))
        # take snapshot
        if kw.get('snap', True):
            self.snapshot()
        # clear outgoing things before adding more things?
        self._nokeep = kw.get('keep', True)
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

    ###########################################################################
    ## things called ##########################################################
    ###########################################################################

    @property
    def _identity(self):
        '''
        Substitute generic identity function for worker if no other
        function is assigned.
        '''
        return self._call if self._call is not None else lambda x: x

    @property
    def _test(self, truth_=truth):
        '''
        Substitute truth operator function for worker if no other
        function assigned.
        '''
        return self._call if self._call is not None else truth_

    @staticmethod
    def _pattern(pat, type, flag, t=translate, r=rcompile, p=pcompile):
        if type == 'glob':
            pat = t(pat)
            type = 'regex'
        return r(pat, flag).search if type == 'regex' else p(pat).search

    ###########################################################################
    ## clearing things up #####################################################
    ###########################################################################

    def _clearsp(self):
        '''clear out snapshots'''
        self._ss.clear()
        return self
