# -*- coding: utf-8 -*-
'''base chainsaw mixins'''

from threading import local
from collections import deque

from stuf.utils import OrderedDict
from stuf.core import stuf, frozenstuf, orderedstuf

from chainsaw._compat import tounicode, tobytes


class ChainsawMixin(local):

    '''base chainsaw mixin'''

    ###########################################################################
    ## things in process ######################################################
    ###########################################################################

    def as_one(self):
        '''
        Switch to performing operations on incoming things as one whole
        individual thing.
        '''
        self._mode = self._ONE
        return self

    def as_many(self):
        '''
        Switch to performing operations on each incoming thing as just one
        individual thing in a series of many individual things.
        '''
        self._mode = self._MANY
        return self

    ###########################################################################
    ## things in context ######################################################
    ###########################################################################

    def as_edit(self):
        '''
        Switch to editing context where operations can be performed on incoming
        things from initial placement to final extraction.
        '''
        self._context = self._EDIT
        self._truth = None
        return self.clear().undo(baseline=True)._unchain()

    def as_truth(self):
        '''
        Switch to evaluation context where the results of operations on
        incoming things determine which of two potential paths to execute.
        After exting the evaluation context, incoming things automatically
        revert to a prior baseline snapshot of incoming things so further
        operations can be performed on the unmodified version.
        '''
        self._context = self._TRUTH
        return self.snapshot(baseline=True)._as_chain(hard=True, snap=False)

    def as_view(self):
        '''
        Switch to query context where incoming things can be extracted and
        transformed so that the results of chainsawing them can be queried.
        Upon exit from query context by invoking `results` or `end`, all
        incoming things automatically revert to a prior baseline snapshot of
        incoming things so that further operations can be performed on the
        unmodified version.
        '''
        self._context = self._QUERY
        self._truth = None
        return self.snapshot(baseline=True)._as_chain()

    ###########################################################################
    ## things in chain ########################################################
    ###########################################################################

    @classmethod
    def as_auto(cls):
        '''
        Context where incoming things are automatically rebalanced with
        outgoing things.
        '''
        cls._DEFAULT_CHAIN = cls._AUTO
        return cls

    @classmethod
    def as_manual(cls):
        '''
        Context where incoming must be manually rebalanced with outgoing
        things.
        '''
        cls._DEFAULT_CHAIN = cls._MANUAL
        return cls

    def shift_in(self):
        '''Manually copy outgoing things to incoming things.'''
        with self._auto(
            chainin=self._OUTVAR, chainout=self._INVAR, snap=False,
        ):
            return self._xtend(self._iterable)

    def shift_out(self):
        '''Manually copy incoming things to outgoing things.'''
        with self._auto(snap=False):
            return self._xtend(self._iterable)

    @property
    def balanced(self):
        '''Determine if ins and out are in balance'''
        return self.count_out() == self.__len__()

    ###########################################################################
    ## things called ##########################################################
    ###########################################################################

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
        Assign current callable and, optionally, an alternative callable. If
        `factory` flag is set, use the `call` argument as a factory for
        building the current callable.

        @param call: primary callable to assign
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
        Place `things` after any current incoming things.

        @param things: wannabe incoming things
        '''
        with self._man1():
            return self._xtend(things)

    def extendfront(self, things):
        '''
        Place `things` after any current incoming thing.

        @param thing: one wannabe incoming thing
        '''
        with self._man1():
            return self._xtendfront(things)

    def append(self, thing):
        '''
        Place `things` before any current incoming things.

        @param thing: wannabe incoming things
        '''
        with self._man1():
            return self._append(thing)

    def appendfront(self, thing):
        '''
        Place `thing` before any current incoming things.

        @param thing: one wannabe incoming thing
        '''
        with self._man1():
            return self._appendfront(thing)

    ###########################################################################
    ## knowing things #########################################################
    ###########################################################################

    def __bool__(self):
        '''
        Return results built up while in truth context or return the length of
        incoming things.
        '''
        return (self._truth if self._truth is not None else self.__len__())

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
        Choose current callable based on results of condition mode

        @param call: external callable to use if condition is `True`
        @param alt: external callable to use if condition if `False`
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
        '''Return outgoing things and clear out every last thing.'''
        self._unchain()
        value = self._output()
        # clear every last thing
        self.clear()._clearsp()
        return value

    def results(self):
        '''Return outgoing things and clear outgoing things.'''
        self._unchain()
        value = self._output()
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
        Iterable wrapper for outgoing things.

        @param wrapper: an iterable wrapper
        '''
        self._wrapper = wrapper
        return self

    ###########################################################################
    ## string wrapping things #################################################
    ###########################################################################

    def as_ascii(self, errors='strict'):
        '''
        Set wrapper to encode each thing in a series of things as string/byte
        type encoded as `ascii` (regardless of type)

        @param errors: error handling (default: 'strict')
        '''
        return self.wrap(lambda x: tobytes(x, 'ascii', errors))

    def as_bytes(self, encoding='utf-8', errors='strict'):
        '''
        encode each incoming thing as byte string (regardless of type)

        @param encoding: encoding for stringish things (default: 'utf-8')
        @param errors: error handling for encoding stringish things
            (default: 'strict')
        '''
        return self.wrap(lambda x: tobytes(x, encoding, errors))

    def as_unicode(self, encoding='utf-8', errors='strict'):
        '''
        Set wrapper to decode each thing in a series of things as `unicode`
        type (regardless of type).

        @param encoding: encoding for stringish things (default: 'utf-8')
        @param errors: error handling for decoding stringish things
            (default: 'strict')
        '''
        return self.wrap(lambda x: tounicode(x, encoding, errors))

    ###########################################################################
    ## sequence wrapping things ###############################################
    ###########################################################################

    def as_list(self):
        '''Set wrapper to `list` type.'''
        return self.wrap(list)

    unwrap = as_list

    def as_deque(self):
        '''Set wrapper to `deque` type.'''
        return self.wrap(deque)

    def as_tuple(self):
        '''Set wrapper to `tuple` type.'''
        return self.wrap(tuple)

    ###########################################################################
    ## map wrapping things ####################################################
    ###########################################################################

    def as_dict(self):
        '''Set wrapper to `dict` type.'''
        return self.wrap(dict)

    def as_ordereddict(self):
        '''Set wrapper to `OrderedDict` type.'''
        return self.wrap(OrderedDict)

    ###########################################################################
    ## stuf wrapping things ###################################################
    ###########################################################################

    def as_frozenstuf(self):
        '''Set wrapper to `frozenstuf` type.'''
        return self.wrap(frozenstuf)

    def as_orderedstuf(self):
        '''Set iterable wrapper to `orderedstuf` type.'''
        return self.wrap(orderedstuf)

    def as_stuf(self):
        '''Set iterable wrapper to `stuf` type.'''
        return self.wrap(stuf)

    ###########################################################################
    ## set wrapping things ####################################################
    ###########################################################################

    def as_frozenset(self):
        '''Set iterable wrapper to `frozenset` type.'''
        return self.wrap(frozenset)

    def as_set(self):
        '''Set iterable wrapper to `set` type.'''
        return self.wrap(set)
