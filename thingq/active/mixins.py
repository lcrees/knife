# -*- coding: utf-8 -*-
'''active thingq mixins'''

from copy import copy
from itertools import repeat
from collections import deque
from contextlib import contextmanager

from stuf.utils import clsname

from thingq.mixins import ThingsMixin, ResultsMixin


class BaseMixin(ThingsMixin):

    '''base active things'''

    def __init__(self, *things, **kw):
        try:
            incoming = deque(things[0]) if len(things) == 1 else deque(things)
        except TypeError:
            incoming = deque()
            incoming.extend(things)
        super(BaseMixin, self).__init__(incoming, deque())
        # set iterator
        self._iterator = self._iterexcept
        # work things
        self._work = deque()
        # utility things
        self._util = deque()

    ###########################################################################
    ## mode things ############################################################
    ###########################################################################

    def ro(self):
        '''switch to read-only mode'''
        with self.ctx3(outq=self._UTILVAR, savepoint=False):
            self._xtend(self._iterable)
        with self.ctx1(hard=True, workq=self._UTILVAR, savepoint=False):
            self.current_mode = self._RO
            return self

    ###########################################################################
    ## context things #######################################################
    ###########################################################################

    @contextmanager
    def ctx2(self, **kw):
        '''swap for two-armed context'''
        self.swap(
            outq=kw.get(self._OUTCFG, self._INVAR), context=self.ctx2(), **kw
        )
        getr_ = lambda x: getattr(self, x)
        outq = getr_(self._OUTQ)
        utilq = getr_(self._UTILQ)
        workq = getr_(self._WORKQ)
        # clear all work things
        workq.clear()
        # extend work things with outgoing things
        workq.extend(outq)
        # swap iterator
        self._iterator = self._breakcount
        yield
        # clear outgoing things if so configured
        if self._clearout:
            outq.clear()
        # extend outgoing things with utility things
        outq.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global context
        self.reswap()

    @contextmanager
    def ctx3(self, **kw):
        '''swap for three-armed context'''
        self.swap(
            utilq=kw.get(self._WORKCFG, self._WORKVAR), context=self.ctx3, **kw
        )
        getr_ = lambda x: getattr(self, x)
        outq = getr_(self._OUTQ)
        utilq = getr_(self._UTILQ)
        workq = getr_(self._WORKQ)
        # clear work things
        workq.clear()
        # extend work things with incoming things
        workq.extend(getr_(self._INQ))
        # swap iterators
        self._iterator = self._breakcount
        yield
        # clear outgoing things if so configured
        if self._clearout:
            outq.clear()
        # extend outgoing things with utility things
        outq.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global context
        self.reswap()

    @contextmanager
    def ctx4(self, **kw):
        '''swap for four-armed context'''
        self.swap(context=self.ctx4, **kw)
        getr_ = lambda x: getattr(self, x)
        outq = getr_(self._OUTQ)
        utilq = getr_(self._UTILQ)
        workq = getr_(self._WORKQ)
        # clear work things
        workq.clear()
        # extend work things with incoming things
        workq.extend(getr_(self._INQ))
        # swap iterators
        self._iterator = self._iterexcept
        yield
        # clear outgoing things if so configured
        if self._clearout:
            outq.clear()
        # extend outgoing things with utility things
        outq.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global context
        self.reswap()

    @contextmanager
    def autoctx(self, **kw):
        '''swap for auto-synchronizing context'''
        self.swap(context=self.autoctx, **kw)
        getr_ = lambda x: getattr(self, x)
        inq, workq = getr_(self._INQ), getr_(self._WORKQ)
        utilq,  outq = getr_(self._UTILQ), getr_(self._OUTQ)
        # clear work things
        workq.clear()
        # extend work things with incoming things
        workq.extend(inq)
        # swap iterators
        self._iterator = self._iterexcept
        yield
        # clear outgoing things if so configured
        if self._clearout:
            outq.clear()
        outq.extend(utilq)
        # clear incoming things
        inq.clear()
        inq.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global context
        self.reswap()

    ###########################################################################
    ## savepoint for things ###################################################
    ###########################################################################

    def _savepoint(self):
        '''take savepoint of incoming things'''
        self._savepoints.append(copy(getattr(self, self._INQ)))
        return self

    ###########################################################################
    ## iterate things #########################################################
    ###########################################################################

    @property
    def _iterable(self):
        '''iterable'''
        return self._iterator(self._WORKQ)

    def _breakcount(self, attr='_UTILQ'):
        '''
        breakcount iterator

        @param attr: things to iterate over
        '''
        dq = getattr(self, attr)
        length, call = len(dq), dq.popleft
        for i in repeat(None, length):  # @UnusedVariable
            yield call()

    def _iterexcept(self, attr='_UTILQ'):
        '''
        call a function repeatedly until an exception is raised

        Converts a call-until-exception interface to an iterator interface.
        Like `iter(call, sentinel)` but uses an exception instead of a sentinel
        to end the loop.

        Raymond Hettinger, Python Cookbook recipe # 577155
        '''
        call = getattr(self, attr).popleft
        try:
            while 1:
                yield call()
        except IndexError:
            pass

    ###########################################################################
    ## extend things ##########################################################
    ###########################################################################

    def _xtend(self, things):
        '''extend utility things with `things` wrapped'''
        getattr(self, self._UTILQ).extend(things)
        return self

    def _xtendleft(self, things):
        '''extend left side of utility things with `things`'''
        getattr(self, self._UTILQ).extendleft(things)
        return self

    def _iter(self, things):
        '''extend work things with `things` wrapped in iterator'''
        getattr(self, self._UTILQ).extend(iter(things))
        return self

    ###########################################################################
    ## append things ##########################################################
    ###########################################################################

    def _append(self, things):
        '''append `things` to utility things'''
        getattr(self, self._UTILQ).append(things)
        return self

    def _appendleft(self, things):
        '''append `things` to left side of utility things'''
        getattr(self, self._UTILQ).appendleft(things)
        return self

    ###########################################################################
    ## know things ############################################################
    ###########################################################################

    def __repr__(self):
        getr_, list_ = lambda x: getattr(self, x), list
        return self._repr(
            self.__module__,
            clsname(self),
            self.current_mode.upper(),
            self._INQ,
            list_(getr_(self._INQ)),
            self._WORKQ,
            list_(getr_(self._WORKQ)),
            self._UTILQ,
            list_(getr_(self._UTILQ)),
            self._OUTQ,
            list_(getr_(self._OUTQ)),
            id(self),
        )

    def __len__(self):
        '''number of incoming things'''
        return len(self.incoming)
    
    count = __len__

    def countout(self):
        '''number of outgoing things'''
        return len(self.outgoing)

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearu(self):
        '''clear utility things'''
        self._util.clear()
        return self

    def _clearw(self):
        '''clear work things'''
        self._work.clear()
        return self

    def clearin(self):
        '''clear incoming things'''
        self.incoming.clear()
        return self

    def clearout(self):
        '''clear outgoing things'''
        self.outgoing.clear()
        return self


class AutoMixin(BaseMixin):

    '''auto-balancing queue mixin'''

    _DEFAULT_CONTEXT = 'autoctx'


class ManMixin(BaseMixin):

    '''manually balanced queue mixin'''

    _DEFAULT_CONTEXT = 'ctx4'


class EndMixin(ResultsMixin):

    '''result things mixin'''
    
    def __iter__(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self._iterexcept(self._OUTQ)
    
    results = __iter__

    def end(self):
        '''return outgoing things then clear wrap everything'''
        # return to default context
        self.unswap()
        wrap, outgoing = self._wrapper, self.outgoing
        wrap = self.outgoing.pop() if len(outgoing) == 1 else wrap(outgoing)
        # clear every last thing
        self.clear()._clearsp()
        return wrap

    def snapshot(self):
        '''snapshot of current outgoing things'''
        wrap = copy(self.outgoing)
        return wrap.pop() if len(wrap) == 1 else self._wrapper(wrap)

    def out(self):
        '''return outgoing things and clear outgoing things'''
        # return to default context
        self.unswap()
        wrap, outgoing = self._wrapper, self.outgoing
        wrap = outgoing.pop() if len(outgoing) == 1 else wrap(outgoing)
        # clear outgoing things
        self.clearout()
        return wrap


class AutoResultMixin(AutoMixin, EndMixin):

    '''auto-balancing manipulation things (with results extractor) mixin'''


class ManResultMixin(ManMixin, EndMixin):

    '''manually balanced things (with results extractor) mixin'''
