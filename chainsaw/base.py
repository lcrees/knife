# -*- coding: utf-8 -*-
'''base chainsaw mixins'''

from itertools import tee
from operator import truth
from threading import local
from collections import deque
from contextlib import contextmanager

from stuf.utils import OrderedDict
from stuf.core import stuf, frozenstuf, orderedstuf

from chainsaw.compat import tounicode, tobytes, imap

SLOTS = [
     '_IN', '_ins', '_WORK', '_work', '_HOLD', '_hold', '_OUT', '_sps',
     '_outs', '_buildup',  '_mode', '_CHAINCFG',  '_chain', '_truth',
     '_context', '_call', '_alt', '_wrapper', '_args', '_kw', '_iterator',
     '_original', '_baseline',
]


class ChainsawMixin(local):

    '''base chainsaw mixin'''

    def __init__(self, ins, outs, **kw):
        '''
        init

        @param ins: incoming things
        @param outs: outgoing things
        '''
        super(ChainsawMixin, self).__init__()
        # incoming things
        self._ins = ins
        # outgoing things
        self._outs = outs
        # default context
        self._context = self._DEFAULT_CONTEXT
        # default mode
        self._mode = self._DEFAULT_MODE
        # no truth value to override default `__bool__` response
        self._truth = None
        ## chain defaults #####################################################
        self._chain = getattr(self, self._DEFAULT_CHAIN)
        # 1. default ins link
        self._IN = self._INVAR
        # 2. default work link
        self._WORK = self._WORKVAR
        # 3. default holding link
        self._HOLD = self._HOLDVAR
        # 4. default outs link
        self._OUT = self._OUTVAR
        # default chain configuration
        self._CHAINCFG = {}
        # clear things out of outs link before adding other things to it?
        self._buildup = True
        ## snapshot defaults ##################################################
        # original and baseline snapshots
        self._original = self._baseline = None
        # maximum number of snapshots to keep (default: 5)
        maxlen = kw.pop('snapshots', 5)
        # snapshot stack
        self._sps = deque(maxlen=maxlen) if maxlen is not None else maxlen
        # take snapshot of original incoming things
        if self._sps is not None:
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

    # chainsaw all incoming things as one thing
    _ONE = _DEFAULT_MODE = 'TREAT AS ONE'
    # chainsaw each incoming thing as one of many individual things
    _MANY = 'TREAT AS MANY'

    def _one(self, call, _imap=imap):
        # append incoming things to outs if chainsawing them as one thing
        if self._mode == self._ONE:
            return self._append(call(self._iterable))
        # map incoming things and extend outs if chainsawing many things
        elif self._mode == self._MANY:
            return self._xtend(imap(call, self._iterable))

    def _many(self, call, _imap=imap):
        # extend outs with incoming things if chainsawing them as one thing
        if self._mode == self._ONE:
            return self._xtend(call(self._iterable))
        # map incoming things and extend outs if chainsawing many things
        elif self._mode == self._MANY:
            return self._xtend(imap(call, self._iterable))

    def _iter(self, call, iter_=iter):
        '''extend work link with `things` wrapped in iterator'''
        # extend outs with incoming things if chainsawing them as one thing
        if self._mode == self._ONE:
            return self._xtend(iter_(call(self._iterable)))
        # map incoming things and extend outs if chainsawing many things
        elif self._mode == self._MANY:
            return self._xtend(imap(lambda x: iter_(call(x)), self._iterable))

    def as_one(self):
        '''Switch to chainsawing incoming things as one individual thing.'''
        self._mode = self._ONE
        return self

    def as_many(self):
        '''
        Switch to chainsawing each incoming thing as one individual thing among
        many individual things.
        '''
        self._mode = self._MANY
        return self

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

    def as_edit(self):
        '''
        Switch to editing context where incoming things can be extracted and
        transformed in sequence of operations from their initial placement in
        the ins to their final extraction from the outs.
        '''
        self._context = self._EDIT
        self._truth = None
        return self.clear().undo(baseline=True)._unchain()

    def as_truth(self):
        '''
        Switch to evaluation context where incoming things can be extracted and
        transformed so that the results of chainsawing them can be used to
        determine which of two potential paths should be executed. After
        they're evaluated, the ins state is automatically returned to a
        previously taken baseline snapshot of the incoming things so further
        opportunities to extract and transform them aren't lost.
        '''
        self._context = self._TRUTH
        return self.snapshot(baseline=True)._as_chain(hard=True, snap=False)

    def as_view(self):
        '''
        Switch to query context where incoming things can be extracted and
        transformed so that the results of chainsawing them can be queried.
        After they're queried, the ins state is automatically returned to a
        previously taken baseline snapshot of the incoming things so further
        opportunities to extract and transform them aren't lost.
        '''
        self._context = self._QUERY
        self._truth = None
        return self.snapshot(baseline=True)._as_chain()

    ###########################################################################
    ## things in chain ########################################################
    ###########################################################################

    # automatically balance ins with outs
    _DEFAULT_CHAIN = _AUTO = '_auto'
    # manually balance ins with outs
    _MANUAL = '_man4'
    # 1. link for incoming things which is chained to =>
    _INCFG = 'ins'
    _INVAR = '_ins'
    # 2. link for working on incoming things which is chained to =>
    _WORKCFG = 'work'
    _WORKVAR = '_work'
    # 3. link temporarily holding chainsawed things which is chained to =>
    _HOLDCFG = 'hold'
    _HOLDVAR = '_hold'
    # 4. link where outgoing things can be removed from chain
    _OUTCFG = 'outs'
    _OUTVAR = '_outs'

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
        # 4. assign "outs" link
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

    @classmethod
    def as_auto(cls):
        '''Context where ins is automatically rebalanced outs.'''
        cls._DEFAULT_CHAIN = cls._AUTO
        return cls

    @classmethod
    def as_manual(cls):
        '''Context where ins must be manually rebalanced with outs.'''
        cls._DEFAULT_CHAIN = cls._MANUAL
        return cls

    def shift_in(self):
        '''Manually copy outgoing things to ins.'''
        with self._auto(
            ins=self._OUTVAR, outs=self._INVAR, snap=False,
        ):
            return self._xtend(self._iterable)

    def shift_out(self):
        '''Manually copy incoming things to outs.'''
        with self._auto(snap=False):
            return self._xtend(self._iterable)

    @property
    def balanced(self):
        '''Determine if ins and outs are in balance'''
        return self.count_out() == self.__len__()

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
        Substitute generic identity function for current callable if no current
        callable is assigned.
        '''
        return self._call if self._call is not None else lambda x: x

    @property
    def _test(self):
        '''
        Substitute truth operator function for current callable is no current
        callable is assigned.
        '''
        return self._call if self._call is not None else truth

    def arguments(self, *args, **kw):
        '''
        Assign arguments to be used by the current or alternative callable.
        '''
        # position arguments
        self._args = args
        # keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call, alt=None, factory=False):
        '''
        Assign current callable and/or alternative callable.

        @param call: callable to assign
        @param alt: alternative callable to assign (default: None)
        @param factor: whether `call` is a callable factory (default: False)
        '''
        # reset stored position arguments
        self._args = ()
        # reset stored keyword arguments
        self._kw = {}
        # if callable is a factory for building current callable, configure
        if factory:
            def factory_(*args, **kw):
                return call(*args, **kw)
            self._call = factory_
        # or just assign current callable
        else:
            self._call = call
        # set any alternative callable
        self._alt = alt
        return self

    def untap(self):
        '''
        Clear current callable, alternative callable, and stored arguments.
        '''
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
    ## things coming in #######################################################
    ###########################################################################

    def extend(self, things):
        '''
        Place many `things` after any incoming `things` already in current
        ins.

        @param things: wannabe incoming things
        '''
        with self._man1():
            return self._xtend(things)

    def extendfront(self, things):
        '''
        Place many `things` before any incoming `things` already in current
        ins.

        @param thing: wannabe incoming things
        '''
        with self._man1():
            return self._xtendfront(things)

    def append(self, thing):
        '''
        Place one `thing` after any incoming `things` already in current
        ins.

        @param thing: one wannabe incoming thing
        '''
        with self._man1():
            return self._append(thing)

    def appendfront(self, thing):
        '''
        Place one `thing` before any incoming `things` already in current
        ins.

        @param thing: one wannabe incoming thing
        '''
        with self._man1():
            return self._appendfront(thing)

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __bool__(self):
        '''Return results build while in truth context or length of ins.'''
        return (self._truth if self._truth is not None else self.__len__())

    @staticmethod
    def _repr(*args):
        '''object representation'''
        return (
            '{0}.{1} ([IN: {2}({3}) => WORK: {4}({5}) => UTIL: {6}({7}) => '
            'OUT: {8}: ({9})]) <<mode: {10}/context: {11}>>'
        ).format(*args)

    ###########################################################################
    ## clearing things up #####################################################
    ###########################################################################

    def _clearsp(self):
        '''clear out snapshots'''
        self._sps.clear()
        return self

    def clear(self):
        '''Clear out everything.'''
        self._truth = None
        return self.untap().unwrap().clear_out().clear_in()._clearw()._clearh()


class OutchainMixin(local):

    '''knifing output mixin'''

    def which(self, call=None, alt=None):
        '''
        choose current callable based on results of CONDITION mode

        @param call: external callable to use if condition is `True`
        @param alt: external callable  to use if condition if `False`
        '''
        if self.__bool__():
            # use external call or current callable
            self._call = call if call is not None else self._call
        else:
            # use external callable or current alternative callable
            self._call = alt if alt is not None else self._alt
        # return to edit mode
        return self.as_edit()

    def end(self):
        '''Return outgoing things and clear out everything.'''
        self._unchain()
        value = self.preview()
        # clear every last thing
        self.clear()._clearsp()
        return value

    def results(self):
        '''Return outgoing things and clear outs.'''
        self._unchain()
        value = self.preview()
        # clear outs
        self.clear_out()
        # restore baseline if in query context
        if self._context == self._QUERY:
            self.undo(baseline=True)
        return value

    ###########################################################################
    ## wrapping things ########################################################
    ###########################################################################

    def wrap(self, wrapper):
        '''
        wrapper for outs

        @param wrapper: an iterator class
        '''
        self._wrapper = wrapper
        return self

    ###########################################################################
    ## string wrapping things #################################################
    ###########################################################################

    def as_ascii(self, errors='strict'):
        '''
        encode each incoming thing as ascii string (regardless of type)

        @param errors: error handling (default: 'strict')
        '''
        return self.wrap(lambda x: tobytes(x, 'ascii', errors))

    def as_bytes(self, encoding='utf-8', errors='strict'):
        '''
        encode each incoming thing as byte string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        return self.wrap(lambda x: tobytes(x, encoding, errors))

    def as_unicode(self, encoding='utf-8', errors='strict'):
        '''
        decode each incoming thing as unicode string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        return self.wrap(lambda x: tounicode(x, encoding, errors))

    ###########################################################################
    ## sequence wrapping things ###############################################
    ###########################################################################

    def as_list(self):
        '''clear current wrapper'''
        return self.wrap(list)

    unwrap = as_list

    def as_deque(self):
        '''set wrapper to `deque`'''
        return self.wrap(deque)

    def as_tuple(self):
        '''set wrapper to `tuple`'''
        return self.wrap(tuple)

    ###########################################################################
    ## map wrapping things ####################################################
    ###########################################################################

    def as_dict(self):
        '''set wrapper to `dict`'''
        return self.wrap(dict)

    def as_ordereddict(self):
        '''set wrapper to `OrderedDict`'''
        return self.wrap(OrderedDict)

    ###########################################################################
    ## stuf wrapping things ###################################################
    ###########################################################################

    def as_frozenstuf(self):
        '''set wrapper to `frozenstuf`'''
        return self.wrap(frozenstuf)

    def as_orderedstuf(self):
        '''set wrapper to `orderedstuf`'''
        return self.wrap(orderedstuf)

    def as_stuf(self):
        '''set wrapper to `stuf`'''
        return self.wrap(stuf)

    ###########################################################################
    ## set wrapping things ####################################################
    ###########################################################################

    def as_frozenset(self):
        '''set wrapper to `frozenset`'''
        return self.wrap(frozenset)

    def as_set(self):
        '''set wrapper to `set`'''
        return self.wrap(set)
