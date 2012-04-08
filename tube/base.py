# -*- coding: utf-8 -*-
'''base mixins'''

import re
from json import loads
from operator import truth
from threading import local
from collections import deque
from contextlib import contextmanager
from htmlentitydefs import name2codepoint
from json.encoder import encode_basestring
from xml.sax.saxutils import escape, unescape

from stuf.utils import OrderedDict
from stuf.core import stuf, frozenstuf, orderedstuf

from tube.compat import tounicode, tobytes, imap

SLOTS = [
    '_work', 'outflow', '_util', 'inflow', '_call', '_alt', '_wrapper', '_kw',
    '_args', '_buildup', '_flow', '_FLOWCFG', '_IN', '_WORK', '_HOLD', '_OUT',
    '_iterator', '_channel', '_sps', '_original', '_eval', '_baseline',
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
        self.inflow = inflow
        self.outflow = outflow
        # preferred _channel
        self._channel = self._CHANGE
        # condition
        self._eval = None
        #######################################################################
        ## flow defaults ######################################################
        #######################################################################
        # preferred flow
        self._flow = getattr(self, self._DEFAULT_CONTEXT)
        # default flow configuration
        self._FLOWCFG = {}
        # 1. default inflow pool
        self._IN = self._INVAR
        # 2. default work pool
        self._WORK = self._WORKVAR
        # 3. default holding pool
        self._HOLD = self._HOLDVAR
        # 4. default outflow pool
        self._OUT = self._OUTVAR
        # clear outflow pool before adding things to it?
        self._buildup = True
        #######################################################################
        ## snapshot defaults ##################################################
        #######################################################################
        self._original = self._baseline = None
        # maximum number of savepoints to keep at any one time (default: 5)
        maxlen = kw.pop('savepoints', 5)
        # create pool for snapshots
        self._sps = deque(maxlen=maxlen) if maxlen is not None else None
        # take snapshot of original inflow
        if self._sps is not None:
            self.snapshot(original=True)
        #######################################################################
        ## callable defaults ##################################################
        #######################################################################
        # current callable
        self._call = None
        # current alternate callable
        self._alt = None
        # iterable outflow wrapper
        self._wrapper = list
        # postition arguments
        self._args = ()
        # keyword arguments
        self._kw = {}

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

    def _one(self, call, _imap=imap):
        if self._ONE:
            return self._append(call(self._iterable))
        elif self._MANY:
            return self._xtend(imap(call, self._iterable))

    def _many(self, call, _imap=imap):
        if self._ONE:
            return self._xtend(call(self._iterable))
        elif self._MANY:
            return self._xtend(imap(call, self._iterable))

    ###########################################################################
    ## flow things ############################################################
    ###########################################################################

    # 1. inflow
    _INCFG = 'inflow'
    _INVAR = 'inflow'
    # 2. work things
    _WORKCFG = 'work'
    _WORKVAR = '_work'
    # 3. holding things
    _HOLDCFG = 'util'
    _HOLDVAR = '_util'
    # 4. outflow
    _OUTCFG = 'outflow'
    _OUTVAR = 'outflow'

    def flow(self, **kw):
        '''switch flow'''
        # make snapshot
        if kw.pop('snapshot', True):
            self.snapshot()
        # keep flow-specific settings between flow swaps
        self._FLOWCFG = kw if kw.get('hard', False) else {}
        # set flow
        self._flow = kw.get('flow', getattr(self, self._DEFAULT_CONTEXT))
        # clear outflow before extending them?
        self._buildup = kw.get('clearout', True)
        # 1. inflow
        self._IN = kw.get(self._INCFG, self._INVAR)
        # 2. work things
        self._WORK = kw.get(self._WORKCFG, self._WORKVAR)
        # 3. holding things
        self._HOLD = kw.get(self._HOLDCFG, self._HOLDVAR)
        # 4. outflow
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
    ## snapshot things ###################################################
    ###########################################################################

    def snapshot(self, baseline=False, original=False):
        '''
        Take snapshot of current inflow state.

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
        Revert inflow to previous inflow state.

        @param snapshot: snapshot to revert to e.g. 1, 2, 3, etc.
        @param baseline: return inflow to baseline version (default: False)
        @param original: return inflow to original version (default: False)
        '''
        # clear everything
        self.clear()
        if original:
            # clear savepoints
            self._clearsp()
            # clear baseline
            self._baseline = None
            # restore original inflow
            self.inflow = self._clone(self._original)[0]
        elif baseline:
            # clear savepoints
            self._clearsp()
            # restore baseline inflow
            self.inflow = self._clone(self._baseline)[0]
        # if specified, use specific snapshot
        elif snapshot:
            self._sps.rotate(snapshot)
            self.inflow = self._sps.popleft()
        # use most recent snapshot
        else:
            self.inflow = self._sps.popleft()
        return self

    ###########################################################################
    ## balance things #########################################################
    ###########################################################################

    # automatically balance inflow with outflow
    _DEFAULT_CONTEXT = _AUTO = '_autoflow'
    # manually balance inflow with outflow
    _MANUAL = 'ctx4'

    @classmethod
    def auto(cls):
        '''automatically balance inflow with outflow'''
        cls._DEFAULT_CONTEXT = cls._AUTO
        return cls

    @classmethod
    def manual(cls):
        '''manually balance inflow with outflow'''
        cls._DEFAULT_CONTEXT = cls._MANUAL
        return cls

    def balance(self):
        '''balance by shifting outflow to inflow'''
        with self._autoflow(
            inflow=self._OUTVAR, outflow=self._INVAR, keep=False
        ):
            return self._many(self._iterable)

    def rebalance(self):
        '''balance by shifting inflow to outflow'''
        with self._autoflow(keep=False):
            return self._many(self._iterable)

    @property
    def balanced(self):
        '''if inflow and outflow are in balance'''
        return self.countout() == self.__len__()

    ###########################################################################
    ## inflow things ##########################################################
    ###########################################################################

    def extend(self, things):
        '''
        put many things after the current inflow

        @param thing: some things
        '''
        with self._flow1():
            return self._many(things)

    def extendleft(self, things):
        '''
        extend before inflow

        @param thing: some things
        '''
        with self._flow1():
            return self._xtendleft(things)

    def append(self, thing):
        '''
        append after current inflow

        @param thing: one thing
        '''
        with self._flow1():
            return self._one(thing)

    def appendleft(self, thing):
        '''
        append before current inflow

        @param thing: some thing
        '''
        with self._flow1():
            return self._appendleft(thing)

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
            self._eval if self._eval is not None else self.__len__()
        )

    @staticmethod
    def _repr(*args):
        '''tube representation'''
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
        return self.untap().unwrap().clearout().clearin()._clearw()._clearu()


class OutflowMixin(local):

    '''tube output mixin'''

    def _html(self):
        return self.wrap(lambda x: escape(x, {'"': "&quot;", "'": '&#39;'}))

    def _js(self):
        return self.wrap(encode_basestring)

    def _unhtml(self):
        '''
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
            return unichr(repl) if repl is not None else ent

        def unescape(data):
            return re.sub(r'&#?[A-Za-z0-9]+?;', replace_entities, data)
        return self.wrap(unescape)

    @staticmethod
    def _unjs(self):
        return self.wraps(loads)

    @staticmethod
    def _unxml(self):
        return unescape

    @staticmethod
    def _xml(self):
        return escape

    def asciiout(self, errors='strict'):
        '''
        encode each inflow thing as ascii string (regardless of type)

        @param errors: error handling (default: 'strict')
        '''
        return self.wrap(lambda x: tobytes(x, 'ascii', errors))

    def bytesout(self, encoding='utf-8', errors='strict'):
        '''
        encode each inflow thing as byte string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        return self.wrap(lambda x: tobytes(x, encoding, errors))

    def dequeout(self):
        '''set wrapper to `deque`'''
        return self.wrap(deque)

    def dictout(self):
        '''set wrapper to `dict`'''
        return self.wrap(dict)

    def escapeout(self, format='html'):
        '''escape inflow'''
        return self.wrap(getattr(self, format))

    def fsetout(self):
        '''set wrapper to `frozenset`'''
        return self.wrap(frozenset)

    def fstufout(self):
        '''set wrapper to `frozenstuf`'''
        return self.wrap(frozenstuf)

    def listout(self):
        '''clear current wrapper'''
        return self.wrap(list)

    unwrap = listout

    def odictout(self):
        '''set wrapper to `OrderedDict`'''
        return self.wrap(OrderedDict)

    def ostufout(self):
        '''set wrapper to `orderedstuf`'''
        return self.wrap(orderedstuf)

    def stufout(self):
        '''set wrapper to `stuf`'''
        return self.wrap(stuf)

    def reup(self):
        '''put inflow in inflow as one inflow thing'''
        with self._flow2(keep=False):
            return self._one(list(self._iterable))

    def setout(self):
        '''set wrapper to `set`'''
        return self.wrap(set)

    def tupleout(self):
        '''set wrapper to `tuple`'''
        return self.wrap(tuple)

    def unescapeout(self, format='html'):
        '''
        unescape inflow stings
        '''
        return self.wrap(getattr(self, 'un' + format))

    def unicodeout(self, encoding='utf-8', errors='strict'):
        '''
        decode each inflow thing as unicode string (regardless of type)

        @param encoding: encoding for things (default: 'utf-8')
        @param errors: error handling (default: 'strict')
        '''
        return self.wrapper(lambda x: tounicode(x, encoding, errors))

    def wrap(self, wrapper):
        '''
        wrapper for outflow

        @param wrapper: an iterator class
        '''
        self._wrapper = wrapper
        return self
