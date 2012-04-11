# -*- coding: utf-8 -*-
'''base chainsaw mixins'''

from operator import truth
from threading import local
from collections import deque

from stuf.utils import OrderedDict
from stuf.core import stuf, frozenstuf, orderedstuf

from chainsaw._compat import tounicode, tobytes

SLOTS = [
     '_IN', '_in', '_WORK', '_work', '_HOLD', '_hold', '_OUT', '_ss',
     '_out', '_buildup',  '_mode', '_CHAINCFG',  '_chain', '_truth',
     '_context', '_call', '_alt', '_wrapper', '_args', '_kw', '_original',
     '_baseline',
]


class ChainsawMixin(local):

    '''base chainsaw mixin'''

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    # chainsaw all incoming things as one thing
    _ONE = _DEFAULT_MODE = 'TREAT AS ONE'
    # chainsaw each incoming thing as one of many individual things
    _MANY = 'TREAT AS MANY'

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
        the ins to their final extraction from the out.
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

    @classmethod
    def as_auto(cls):
        '''Context where ins is automatically rebalanced out.'''
        cls._DEFAULT_CHAIN = cls._AUTO
        return cls

    @classmethod
    def as_manual(cls):
        '''Context where ins must be manually rebalanced with out.'''
        cls._DEFAULT_CHAIN = cls._MANUAL
        return cls

    def shift_in(self):
        '''Manually copy outgoing things to ins.'''
        with self._auto(
            chainin=self._OUTVAR, chainout=self._INVAR, snap=False,
        ):
            return self._xtend(self._iterable)

    def shift_out(self):
        '''Manually copy incoming things to out.'''
        with self._auto(snap=False):
            return self._xtend(self._iterable)

    @property
    def balanced(self):
        '''Determine if ins and out are in balance'''
        return self.count_out() == self.__len__()

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

    def clear(self):
        '''Clear out everything.'''
        self._truth = None
        return self.untap().unwrap().clear_out().clear_in()._clearw()._clearh()


class OutchainMixin(local):

    '''knifing output mixin'''

    def which(self, call=None, alt=None):
        '''
        Choose current callable based on results of condition mode.

        @param call: external callable to use if condition is `True`
        @param alt: external callable to use if condition is `False`
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
        '''Return outgoing things and clear out.'''
        self._unchain()
        value = self.preview()
        # clear out
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
        wrapper for out

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
