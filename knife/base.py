# -*- coding: utf-8 -*-
'''base knife mixins'''

from operator import truth
from threading import local
from collections import deque
from contextlib import contextmanager

from stuf.utils import OrderedDict
from stuf.core import stuf, frozenstuf, orderedstuf

from knife.compat import tounicode, tobytes, imap

SLOTS = [
     '_IN', '_inflow', '_WORK', '_work', '_HOLD', '_hold', '_OUT', '_outflow',
     '_buildup',  '_mode', '_FLOWCFG',  '_flow', '_truth', '_context',
     '_call', '_alt', '_wrapper', '_args', '_kw', '_iterator', '_sps',
     '_original', '_baseline',
]


class KnifeMixin(local):

    '''knives mixin'''

    def __init__(self, inflow, outflow, **kw):
        '''
        init

        @param inflow: incoming things
        @param outflow: outgoing things
        '''
        super(KnifeMixin, self).__init__()
        # incoming things
        self._inflow = inflow
        # outgoing things
        self._outflow = outflow
        # default context
        self._context = self._DEFAULT_CONTEXT
        # default mode
        self._mode = self._DEFAULT_MODE
        # no truth value to override default `__bool__` response
        self._truth = None
        ## flow defaults ######################################################
        self._flow = getattr(self, self._DEFAULT_FLOW)
        # 1. default inflow stage
        self._IN = self._INVAR
        # 2. default work stage
        self._WORK = self._WORKVAR
        # 3. default holding stage
        self._HOLD = self._HOLDVAR
        # 4. default outflow stage
        self._OUT = self._OUTVAR
        # default flow configuration
        self._FLOWCFG = {}
        # clear things out of outflow stage before adding other things to it?
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

    # process all incoming things as one thing
    _ONE = _DEFAULT_MODE = 'TREAT AS ONE'
    # process each incoming thing as one of many individual things
    _MANY = 'TREAT AS MANY'

    def _one(self, call, _imap=imap):
        # append incoming things to outflow if processing them as one thing
        if self._mode == self._ONE:
            return self._append(call(self._iterable))
        # map incoming things and extend outflow if processed as many things
        elif self._mode == self._MANY:
            return self._xtend(imap(call, self._iterable))

    def _many(self, call, _imap=imap):
        # extend outflow with incoming things if procesing them as one thing
        if self._mode == self._ONE:
            return self._xtend(call(self._iterable))
        # map incoming things and extend outflow if processed as many things
        elif self._mode == self._MANY:
            return self._xtend(imap(call, self._iterable))

    def _iter(self, call, iter_=iter):
        '''extend work stage with `things` wrapped in iterator'''
        # extend outflow with incoming things if procesing them as one thing
        if self._mode == self._ONE:
            return self._xtend(iter_(call(self._iterable)))
        # map incoming things and extend outflow if processed as many things
        elif self._mode == self._MANY:
            return self._xtend(imap(lambda x: iter_(call(x)), self._iterable))

    def as_one(self):
        '''Switch to processing incoming things as one individual thing.'''
        self._mode = self._ONE
        return self

    def as_many(self):
        '''
        Switch to processing each incoming thing as one individual thing among
        many individual things.
        '''
        self._mode = self._MANY
        return self

    ###########################################################################
    ## things in context ######################################################
    ###########################################################################

    # modify incoming things from input to output in one series of operations
    _EDIT = _DEFAULT_CONTEXT = 'EDIT KNIFE'
    # reset incoming things back to a baseline snapshot after each query
    _QUERY = 'QUERY KNIFE'
    # reset incoming things back to a baseline snapshot after using results of
    # operations on incoming to determine which of two paths to follow
    _TRUTH = 'CONDITION KNIFE'

    def as_edit(self):
        '''
        Switch to editing context where incoming things can be extracted and
        transformed in sequence of operations from their initial placement in
        the inflow to their final extraction from the outflow.
        '''
        self._context = self._EDIT
        self._truth = None
        return self.clear().undo(baseline=True)._unflow()

    def as_truth(self):
        '''
        Switch to evaluation context where incoming things can be extracted and
        transformed so that the results of processing them can be used to
        determine which of two potential paths should be executed. After
        they're evaluated, the inflow state is automatically returned to a
        previously taken baseline snapshot of the incoming things so further
        opportunities to extract and transform them aren't lost.
        '''
        self._context = self._TRUTH
        return self.snapshot(baseline=True)._as_flow(hard=True, snap=False)

    def as_view(self):
        '''
        Switch to query context where incoming things can be extracted and
        transformed so that the results of processing them can be queried.
        After they're queried, the inflow state is automatically returned to a
        previously taken baseline snapshot of the incoming things so further
        opportunities to extract and transform them aren't lost.
        '''
        self._context = self._QUERY
        self._truth = None
        return self.snapshot(baseline=True)._as_flow()

    ###########################################################################
    ## things in flow #########################################################
    ###########################################################################

    # automatically shift_in inflow with outflow
    _DEFAULT_FLOW = _AUTO = '_autoflow'
    # manually shift_in inflow with outflow
    _MANUAL = '_flow4'
    # 1. stage for incoming things which flows to =>
    _INCFG = 'inflow'
    _INVAR = '_inflow'
    # 2. stage for working on incoming things which flows to =>
    _WORKCFG = 'work'
    _WORKVAR = '_work'
    # 3. stage to temporarily hold processed incoming things which flows to =>
    _HOLDCFG = 'hold'
    _HOLDVAR = '_hold'
    # 4. stage where outgoing things can be removed from pipeline
    _OUTCFG = '_outflow'
    _OUTVAR = '_outflow'

    def _as_flow(self, **kw):
        '''switch between flows'''
        # retain flow-specific settings between flow switches
        self._FLOWCFG = kw if kw.get('hard', False) else {}
        # take snapshot
        if kw.get('snapshot', True):
            self.snapshot()
        # set current flow
        self._flow = kw.get('flow', getattr(self, self._DEFAULT_FLOW))
        # if outflow should be cleared before adding more things to it
        self._buildup = kw.get('keep', True)
        # 1. assign inflow stage
        self._IN = kw.get(self._INCFG, self._INVAR)
        # 2. assign work stage
        self._WORK = kw.get(self._WORKCFG, self._WORKVAR)
        # 3. assign holding stage
        self._HOLD = kw.get(self._HOLDCFG, self._HOLDVAR)
        # 4. assign outflow stage
        self._OUT = kw.get(self._OUTCFG, self._OUTVAR)
        return self

    def _reflow(self):
        '''switch to currently selected flow'''
        return self._as_flow(keep=False, **self._FLOWCFG)

    def _unflow(self):
        '''switch to default flow'''
        return self._as_flow(keep=False)

    @contextmanager
    def _manual1(self, **kw):
        '''switch to one-stage flow'''
        q = kw.pop(self._WORKCFG, self._INVAR)
        self._as_flow(work=q, hold=q, flow=self._manual1, **kw)
        yield
        self._reflow()

    @classmethod
    def as_auto(cls):
        '''Context where inflow is automatically rebalanced outflow.'''
        cls._DEFAULT_FLOW = cls._AUTO
        return cls

    @classmethod
    def as_manual(cls):
        '''
        Context where inflow must be explicitly and manually rebalanced
        outflow.
        '''
        cls._DEFAULT_CONTEXT = cls._MANUAL
        return cls

    def shift_in(self):
        '''Copy outgoing things back to inflow.'''
        with self._autoflow(
            inflow=self._OUTVAR, outflow=self._INVAR, keep=False, snap=False,
        ):
            return self._xtend(self._iterable)

    def shift_out(self):
        '''
        Manually copy incoming things to outflow as outgoing things.
        '''
        with self._autoflow(snap=False, keep=False):
            return self._xtend(self._iterable)

    def reup(self):
        '''put incoming in incoming as one incoming thing'''
        with self._manual2(keep=False):
            return self._xtend(list(self._iterable))

    @property
    def balanced(self):
        '''Determine if inflow and outflow are in balance'''
        return self.count_out() == self.__len__()

    ###########################################################################
    ## snapshot of things #####################################################
    ###########################################################################

    def snapshot(self, baseline=False, original=False):
        '''
        Take a snapshot of incoming things currently in inflow.

        @param baseline: make snapshot baseline version (default: False)
        @param original: make snapshot original version (default: False)
        '''
        # take snapshot
        snapshot = self._clone(getattr(self, self._IN))[0]
        # make this snapshot the baseline snapshot
        if self._context == self._EDIT or baseline:
            self._baseline = snapshot
        # make this snapshot the original snapshot
        if original:
            self._original = snapshot
        # place snapshot at beginning of snapshot stack
        self._sps.appendleft(snapshot)
        return self

    def undo(self, snapshot=0, baseline=False, original=False):
        '''
        Revert incoming things to a previous version within inflow.

        @param snapshot: snapshot to revert to e.g. 1, 2, 3, etc. (default: 0)
        @param baseline: return inflow to baseline version (default: False)
        @param original: return inflow to original version (default: False)
        '''
        # clear everything
        self.clear()
        if original:
            # clear snapshots
            self._clearsp()
            # clear baseline
            self._baseline = None
            # restore original version of incoming things
            self._inflow = self._clone(self._original)[0]
        elif baseline:
            # clear snapshots
            self._clearsp()
            # restore baseline version of incoming things
            self._inflow = self._clone(self._baseline)[0]
        # if specified, use a specific snapshot
        elif snapshot:
            self._sps.rotate(snapshot)
            self._inflow = self._sps.popleft()
        # by default revert to most recent snapshot
        else:
            self._inflow = self._sps.popleft()
        return self

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
        inflow.

        @param things: wannabe incoming things
        '''
        with self._manual1():
            return self._xtend(things)

    def extendfront(self, things):
        '''
        Place many `things` before any incoming `things` already in current
        inflow.

        @param thing: wannabe incoming things
        '''
        with self._manual1():
            return self._xtendfront(things)

    def append(self, thing):
        '''
        Place one `thing` after any incoming `things` already in current
        inflow.

        @param thing: one wannabe incoming thing
        '''
        with self._manual1():
            return self._append(thing)

    def appendfront(self, thing):
        '''
        Place one `thing` before any incoming `things` already in current
        inflow.

        @param thing: one wannabe incoming thing
        '''
        with self._manual1():
            return self._appendfront(thing)

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __bool__(self):
        '''Return results build while in truth context or length of inflow.'''
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


class OutflowMixin(local):

    '''knifing output mixin'''

    def which(self, call=None, alt=None):
        '''
        choose current callable based on results of operations in CONDITION
        mode

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
        self._unflow()
        value = self.preview()
        # clear every last thing
        self.clear()._clearsp()
        return value

    def results(self):
        '''Return outgoing things and clear outflow.'''
        self._unflow()
        value = self.preview()
        # clear outflow
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
        wrapper for outflow

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
